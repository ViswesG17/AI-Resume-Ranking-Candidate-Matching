# 🚀 AI Resume Ranking & Candidate Matching Platform

An AI-powered candidate ranking system that matches candidates against a Job Description using semantic similarity, behavioral signals, retrieval scoring, and AI-generated reasoning.

## Features

- Semantic candidate matching using Sentence Transformers
- Retrieval-based keyword matching
- Behavioral signal scoring
- Career history analysis
- AI-generated reasoning for every ranked candidate
- Outputs submission in the required CSV format

---

# Project Structure

```
AI-Candidate-Ranker/
│
├── app.py
├── rank.py
├── candidate_ranking.py
├── requirements.txt
├── README.md
├── submission_metadata.yaml
│
├── data/
│   ├── sample_candidates.jsonl
│   └── sample_job_description.docx
│
└── assets/
```

---

# Installation

Clone the repository

```bash
git clone <YOUR_GITHUB_REPO_URL>
```

Move into the project directory

```bash
cd AI-Candidate-Ranker
```

Create a virtual environment (Recommended)

Windows

```bash
python -m venv venv
venv\Scripts\activate
```

Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

Install all dependencies

```bash
pip install -r requirements.txt
```

---

# Generate Submission CSV

Place the following files inside the **data/** directory.

```
data/
    candidates.jsonl
    job_description.docx
```

Run

```bash
python rank.py --candidates data/candidates.jsonl --jd data/job_description.docx --out submission.csv
```

The generated file

```
submission.csv
```

will be saved in the project root.

---

# Running the Streamlit Application

Launch the web interface

```bash
streamlit run app.py
```

Then open

```
http://localhost:8501
```

Upload

- Job Description (.docx / .pdf / .txt)
- Candidate Database (.jsonl / .zip)

The application will rank candidates and allow downloading the generated submission CSV.

---

# Ranking Pipeline

```
Job Description
        │
        ▼
Sentence Transformer Embedding
        │
        ▼
Semantic Similarity
        │
        ▼
Retrieval Scoring
        │
        ▼
Behavioral Signal Scoring
        │
        ▼
Career History Analysis
        │
        ▼
Weighted Candidate Ranking
        │
        ▼
AI Reason Generation
        │
        ▼
submission.csv
```

---

# Technologies Used

- Python
- Streamlit
- Sentence Transformers
- Scikit-learn
- Pandas
- NumPy
- PyTorch

---

# Output Format

The generated CSV contains

- candidate_id
- rank
- score
- reasoning

exactly as required by the challenge.

---

# Notes

- Supports Job Descriptions in `.docx`, `.pdf`, and `.txt` formats.
- Supports candidate databases in `.jsonl` and compressed `.zip` formats.
- Ranking logic is implemented in `candidate_ranking.py`.
- `rank.py` is the reproducible command-line entry point.
- `app.py` provides the interactive Streamlit interface.