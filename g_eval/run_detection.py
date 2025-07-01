"""
Script to run the G-Eval detection pipeline for a specified dataset, model, and mode.
"""

import argparse
from official_repo.g_eval.detection import evaluate

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run G-Eval detection pipeline.")
    parser.add_argument('--dataset', type=str, default='fetaqa', help="Dataset name (fetaqa or qtsumm)")
    parser.add_argument('--model', type=str, default='gpt-4o-mini', help="Model name (e.g., gpt-4o-mini)")
    parser.add_argument('--mode', type=str, default='faithfulness', choices=['faithfulness', 'completeness'], help="Evaluation mode")
    args = parser.parse_args()

    print(f"Running detection for dataset={args.dataset}, model={args.model}, mode={args.mode}")
    evaluate(args.dataset, model_name=args.model, mode=args.mode) 