# 🧪 Modular Detection-and-Mitigation Framework for Long-form Table QA

**Official repository for the paper:**  
**_Improving Factual Accuracy and Completeness in Long-form Table QA: A Modular Detection-and-Mitigation Pipeline_**

This repository provides a modular, reproducible framework for evaluating and mitigating **faithfulness** and **completeness** in **Long-form Table Question Answering (LFTQA)**. It includes two complementary detection methods—**MT-RAIG** (claim-level detection of unfaithful content) and **G-Eval** (LLM-based evaluation of both faithfulness and completeness)—alongside novel mitigation and automated evaluation techniques tailored for LFTQA.

---

## 📁 Directory Structure

```
official_repo/
│
├── README.md
├── requirements.txt
├── .env                       # OpenAI API key (required)
│
├── data/
│   ├── outputs/               # Preprocessed model outputs (pipeline-ready)
│   ├── input_files/           # Raw LFTQA-Eval input files (no action needed)
│   └── ...                    # Preprocessing scripts
│
├── evaluation/                # Scripts for analysis and preparing human evaluation
│   ├── analyze_faithfulness_completeness_changes.py
│   ├── analyze_fives_and_nonfives_geval.py
│   ├── analyze_fives_and_nonfives_mtraig.py
│   ├── compute_factual_claim_percentages.py
│   ├── count_label_frequencies.py
│   └── create_mitigation_eval_file.py
│
├── mtraig/                    # MT-RAIG pipeline (faithfulness-focused)
│   ├── detection.py
│   ├── mitigation.py
│   ├── automated_eval.py
│   ├── faithfulness_scores/
│   ├── mitigation_outputs/
│   ├── automated_eval_checkpoints/
│   └── helpers/
│
├── g_eval/                    # G-Eval pipeline (faithfulness + completeness)
│   ├── detection.py
│   ├── mitigation.py
│   ├── automated_eval.py
│   ├── faithfulness_scores/
│   ├── completeness_scores/
│   ├── mitigation_outputs/
│   ├── automated_eval_checkpoints/
│   └── helpers/
│
├── human_mitigation_eval/    # Output files (JSON/CSV) for human annotation
└── results/                   # Aggregated results, plots (optional)
```

---

## ⚙️ Setup Instructions

1. **Clone the repository** and navigate to the root folder.

2. **Install dependencies** (preferably in a virtual environment):
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your OpenAI API key** (required):
   Create a `.env` file with:
   ```env
   OPENAI_API_KEY=sk-...
   ```

---

## 📦 Dataset & Inputs

- The pipeline is based on the **LFTQA-Eval** benchmark (~1500 examples each from **FeTaQA** and **QT-SUMM**) containing:
  - Tables, questions, and references
  - Model-generated outputs
  - Human-annotated **faithfulness** and **completeness** scores

- **Raw files** are already available in `data/input_files/`.  
  No action needed from the user.

- **Preprocessed files** (e.g., model outputs with human scores) are available in `data/outputs/` and ready to be used in the pipeline.

---

## 🧠 Detection & Mitigation Methods

| Component   | Scope             | Evaluation Dimensions        |
|-------------|-------------------|-------------------------------|
| **MT-RAIG** | Claim-level        | Faithfulness only             |
| **G-Eval**  | LLM-based          | Faithfulness & Completeness   |

---

## ✅ Checkpoints

The full pipeline has already been executed for the following models:
- `gpt-4o`
- `gpt-4o-mini`

Intermediate outputs and evaluation results are checkpointed in their designated folders:
- `faithfulness_scores/`, `completeness_scores/`
- `mitigation_outputs/`
- `automated_eval_checkpoints/`

You can resume or inspect any stage of the pipeline from these saved outputs.

---

## 🛠️ Evaluation Scripts

Run all scripts from the project root as Python modules:

```bash
# GEVAL vs Human: Fives and Non-Fives
python -m evaluation.analyze_fives_and_nonfives_geval --model_name gpt-4o-mini

# MTRAIG vs Human: Fives and Non-Fives
python -m evaluation.analyze_fives_and_nonfives_mtraig --model_name gpt-4o

# Compute % of Factual Claims Retained
python -m evaluation.compute_factual_claim_percentages --model gpt-4o-mini --dataset fetaqa

# Evaluate improvements post-mitigation
python -m evaluation.analyze_faithfulness_completeness_changes --model gpt-4o --dataset qtsumm

# Prepare data for human annotation
python -m evaluation.create_mitigation_eval_file --model_name gpt-4o-mini --dataset qtsumm --num_points 50
```

---

## 🚀 End-to-End Workflow

1. **Inputs are ready:**
   - `data/input_files/`: Raw LFTQA data
   - `data/outputs/`: Preprocessed and scored model outputs

2. **Run detection:**
   ```bash
   python -m mtraig.detection ...
   python -m g_eval.detection ...
   ```

3. **Run mitigation:**
   ```bash
   python -m mtraig.mitigation ...
   python -m g_eval.mitigation ...
   ```

4. **Run automated evaluation:**
   ```bash
   python -m mtraig.automated_eval ...
   python -m g_eval.automated_eval ...
   ```

5. **Analyze results:**  
   Use scripts in `evaluation/` for quantitative insights and human annotation preparation.

---

## 🔄 Model Compatibility

- ✅ **Out-of-the-box support** for OpenAI models (e.g., GPT-4, GPT-4o, GPT-3.5)
- ⚠️ **Other LLMs require minor SDK changes** (e.g., API wrappers, formatting)

---

## 📌 Notes

- All paths are relative to the `official_repo/` root.
- Checkpointing is implemented to support long-running experiments.
- Script arguments and configurations are documented inline for ease of use.

---

## 📬 Questions?

For questions, issues, or contributions, feel free to open a GitHub issue or contact the maintainers.

---
