"""
Data loading utilities for the project.
"""

import json
from typing import List, Dict, Any
import os

INPUT_DIR = os.path.join(os.path.dirname(__file__), 'input_files')

def load_json(filename: str) -> Any:
    """
    Load a JSON file from the input_files directory.
    """
    path = os.path.join(INPUT_DIR, filename)
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_model_outputs() -> List[Dict]:
    """
    Load the main model outputs from model_outputs.json.
    """
    return load_json('model_outputs.json')

def load_human_faithfulness_scores(dataset: str) -> List[Dict]:
    """
    Load human faithfulness scores for a given dataset (fetaqa or qtsumm).
    """
    assert dataset in {'fetaqa', 'qtsumm'}
    return load_json(f'human_faithfulness_scores_{dataset}.json')

def load_human_comprehensiveness_scores(dataset: str) -> List[Dict]:
    """
    Load human comprehensiveness scores for a given dataset (fetaqa or qtsumm).
    """
    assert dataset in {'fetaqa', 'qtsumm'}
    return load_json(f'human_comprehensiveness_scores_{dataset}.json') 