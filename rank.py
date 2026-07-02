import argparse
import json
import pandas as pd
from docx import Document
from pypdf import PdfReader

from candidate_ranking import rank_candidates


def read_jd(path):
    """
    Read Job Description from txt, docx or pdf.
    """

    if path.endswith(".txt"):

        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    elif path.endswith(".docx"):

        document = Document(path)

        return "\n".join(
            p.text
            for p in document.paragraphs
        )

    elif path.endswith(".pdf"):

        reader = PdfReader(path)

        text = ""

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        return text

    else:

        raise ValueError(
            "Unsupported JD format. Use txt, docx or pdf."
        )


def read_candidates(path):
    """
    Read JSONL candidate file.
    """

    candidates = []

    with open(path, "r", encoding="utf-8") as f:

        for line in f:

            candidates.append(
                json.loads(line)
            )

    return candidates


def main():

    parser = argparse.ArgumentParser(
        description="AI Resume Ranking & Candidate Matching"
    )

    parser.add_argument(
        "--candidates",
        required=True,
        help="Path to candidates.jsonl"
    )

    parser.add_argument(
        "--jd",
        required=True,
        help="Path to Job Description (.txt/.docx/.pdf)"
    )

    parser.add_argument(
        "--out",
        default="submission.csv",
        help="Output CSV"
    )

    args = parser.parse_args()

    print("Reading Job Description...")

    jd_text = read_jd(args.jd)

    print("Reading Candidates...")

    candidates = read_candidates(args.candidates)

    print(f"Loaded {len(candidates)} candidates.")

    print("Ranking candidates...")

    submission = rank_candidates(
        jd_text,
        candidates
    )

    submission.to_csv(
        args.out,
        index=False
    )

    print(f"\nSubmission saved to {args.out}")


if __name__ == "__main__":
    main()