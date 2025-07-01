import os
from openai import OpenAI
from typing import List
from mtraig.helpers.prompts import CLAIM_DECOMPOSITION_PROMPT, CLAIM_VERIFICATION_PROMPT
from mtraig.helpers.schemas import ClaimDecompositionResult, ClaimVerificationResult
from dotenv import load_dotenv

load_dotenv()


def decompose_claims(schema: str, insight: str, temperature: float = 0.0, model: str = "gpt-4o-mini") -> List[str]:
    api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)
    user_content = CLAIM_DECOMPOSITION_PROMPT.format(schema=schema, insight=insight)
    messages = [
        {"role": "system", "content": "You are a helpful assistant that breaks down insights into verifiable atomic-level claims, and returns a function call to 'decompose_claims'."},
        {"role": "user", "content": user_content}
    ]
    function_definition = {
        "name": "decompose_claims",
        "description": "Decomposes the given insight into atomic-level claims based on a provided table schema. Returns a JSON object with a single key 'claims' mapping to a list of strings.",
        "parameters": ClaimDecompositionResult.model_json_schema()
    }
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        functions=[function_definition],
        temperature=temperature,
        function_call={"name": "decompose_claims"},
    )
    function_call = response.choices[0].message.function_call
    arguments_json = function_call.arguments
    result = ClaimDecompositionResult.model_validate_json(arguments_json)
    return result.claims

def verify_claims(table: str, claims: List[str], temperature: float = 0.0, model: str = "gpt-4o-mini") -> List[bool]:
    api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)
    verifications: List[bool] = []
    function_definition2 = {
        "name": "verify_claim",
        "description": "Given a table and a claim, returns {\"faithfulness\": 0 or 1} where 1 means the claim is faithful to the table data, 0 otherwise.",
        "parameters": ClaimVerificationResult.model_json_schema()
    }
    for claim in claims:
        prompt = CLAIM_VERIFICATION_PROMPT.format(table=table, claim=claim)
        messages = [
            {"role": "system", "content": "You are a helpful assistant that verifies claims against table data. Return your response by calling the function 'verify_claim' with a JSON object that has exactly one key 'faithfulness' (0 or 1)."},
            {"role": "user", "content": prompt}
        ]
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            functions=[function_definition2],
            function_call={"name": "verify_claim"},
            temperature=temperature,
        )
        func_call = response.choices[0].message.function_call
        arguments_json = func_call.arguments
        result = ClaimVerificationResult.model_validate_json(arguments_json)
        verifications.append(result.faithfulness == 1)
    return verifications 