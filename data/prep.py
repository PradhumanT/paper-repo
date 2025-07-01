"""
Data preparation logic for the project.
"""

import os
import json
from typing import List, Dict
from .loading import load_model_outputs, load_human_faithfulness_scores, load_human_comprehensiveness_scores

def filter_empty_model_outputs(model_outputs: List[Dict]) -> List[Dict]:
    """
    Remove entries with empty or missing model_output.
    """
    return [entry for entry in model_outputs if entry.get("model_output", "").strip()]

def merge_human_scores(
    filtered_outputs: List[Dict],
    faith_scores: List[Dict],
    comp_scores: List[Dict],
    dataset: str
) -> List[Dict]:
    """
    Merge human faithfulness and comprehensiveness scores into filtered model outputs.
    """
    # Create lookup maps
    faith_map = {(entry["example_id"], entry["model"]): entry["score"] for entry in faith_scores}
    comp_map = {(entry["example_id"], entry["model"]): entry["score"] for entry in comp_scores}

    combined = []
    for entry in filtered_outputs:
        key = (entry["example_id"], entry["model"])
        entry_with_scores = entry.copy()
        if key in faith_map and key in comp_map:
            entry_with_scores["faithfulness_score"] = faith_map[key]
            entry_with_scores["completeness_score"] = comp_map[key]
            combined.append(entry_with_scores)
    return combined

def save_json(data: List[Dict], path: str):
    """
    Save a list of dicts as a JSON file.
    """
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

def serialize_table(entry: Dict, dataset: str) -> Dict:
    """
    Create a serialized_table field for an entry based on the dataset type.
    """
    metadata = entry.get('metadata', {})
    if dataset == 'fetaqa':
        return {
            'title': f"{metadata.get('table_page_title', '')} - {metadata.get('table_section_title', '')}",
            'header': metadata.get('table_array', [[]])[0],
            'rows': metadata.get('table_array', [[]])[1:]
        }
    else:  # qtsumm
        table = metadata.get('table', {})
        return {
            'title': table.get('title', ''),
            'header': table.get('header', []),
            'rows': table.get('rows', [])
        }

def run_full_data_prep_pipeline(output_dir: str = None):
    """
    Run the full data preparation pipeline for both 'fetaqa' and 'qtsumm'.
    Loads model outputs, filters, merges human scores, adds serialized_table, and saves the processed files.
    Output files are saved as 'outputs/model_outputs_with_scores_{dataset}.json' in the data folder by default.
    """
    datasets = ['fetaqa', 'qtsumm']
    model_outputs = filter_empty_model_outputs(load_model_outputs())

    # Default output_dir is the 'outputs' subfolder in the current directory
    if output_dir is None:
        output_dir = os.path.join(os.path.dirname(__file__), 'outputs')
    os.makedirs(output_dir, exist_ok=True)

    for dataset in datasets:
        faith_scores = load_human_faithfulness_scores(dataset)
        comp_scores = load_human_comprehensiveness_scores(dataset)
        combined = merge_human_scores(model_outputs, faith_scores, comp_scores, dataset)
        # Add serialized_table field
        for entry in combined:
            entry['serialized_table'] = serialize_table(entry, dataset)
        out_path = os.path.join(output_dir, f"model_outputs_with_scores_{dataset}.json")
        save_json(combined, out_path)
        print(f"Saved {len(combined)} entries to {out_path}")

if __name__ == "__main__":
    run_full_data_prep_pipeline() 