# %%
import json
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
candidates = []

file_path = r"C:\Users\mynam\Downloads\[PUB] India_runs_data_and_ai_challenge\[PUB] India_runs_data_and_ai_challenge\India_runs_data_and_ai_challenge\candidates.jsonl"

with open(file_path, "r", encoding="utf-8") as f:
    for line in f:
        candidates.append(json.loads(line))

print("Total Candidates:", len(candidates))
print(candidates[0]["candidate_id"])

# %%
def build_candidate_text(candidate):

    profile = candidate["profile"]

    summary = profile.get("summary", "")

    titles = " ".join(
        job["title"]
        for job in candidate["career_history"]
    )

    career = " ".join(
        job["description"]
        for job in candidate["career_history"]
    )

    return f"""
    Career Titles:
    {titles}

    Summary:
    {summary}

    Career History:
    {career}
    """

# %%
RELEVANT_TERMS = [
    "retrieval",
    "ranking",
    "recommendation",
    "search",
    "matching",
    "relevance",
    "vector",
    "embedding",
    "milvus",
    "faiss",
    "pinecone",
    "qdrant",
    "elasticsearch",
    "opensearch",
    "bm25",
    "ndcg",
    "mrr",
    "map"
]

# %%
def retrieval_score(text):

    text = text.lower()

    score = 0

    for term in RELEVANT_TERMS:

        if term in text:
            score += 1

    return score

# %%
def experience_score(candidate):

    exp = candidate["profile"]["years_of_experience"]

    if 5 <= exp <= 9:
        return 1.0

    elif 4 <= exp <= 10:
        return 0.8

    return 0.3

# %%
def recruitability_score(candidate):

    s = candidate["redrob_signals"]

    score = 0

    # Availability
    if s["open_to_work_flag"]:
        score += 0.20

    # Recruiter responsiveness
    score += s["recruiter_response_rate"] * 0.15

    # Interview attendance
    score += s["interview_completion_rate"] * 0.15

    # Recruiter interest
    score += min(
        s["saved_by_recruiters_30d"]/20,
        1
    ) * 0.10

    # Active candidate
    score += min(
        s["profile_views_received_30d"]/100,
        1
    ) * 0.05

    score += min(
        s["search_appearance_30d"]/500,
        1
    ) * 0.05

    # GitHub signal
    if s["github_activity_score"] > 0:
        score += (
            s["github_activity_score"]/100
        ) * 0.10

    # Fast response
    if s["avg_response_time_hours"] < 48:
        score += 0.05

    # Short notice period
    if s["notice_period_days"] <= 30:
        score += 0.05

    # Verification trust
    if s["verified_email"]:
        score += 0.05

    if s["verified_phone"]:
        score += 0.05

    return min(score, 1.0)

# %%


# %%
from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)



# %%
HIGH_VALUE_TITLES = [
    "AI Engineer",
    "Machine Learning Engineer",
    "ML Engineer",
    "Search Engineer",
    "Recommendation Systems Engineer",
    "NLP Engineer",
    "Applied ML Engineer",
    "Senior AI Engineer",
    "Data Scientist"
]

LOW_VALUE_TITLES = [
    "HR Manager",
    "Marketing Manager",
    "Sales Executive",
    "Accountant",
    "Civil Engineer",
    "Mechanical Engineer",
    "Customer Support"
]



def title_score(title):

    if title in HIGH_VALUE_TITLES:
        return 1.0

    elif title in LOW_VALUE_TITLES:
        return 0.0

    return 0.3


JD_TITLES = [
    "AI Engineer",
    "Machine Learning Engineer",
    "ML Engineer",
    "Search Engineer",
    "Recommendation Systems Engineer",
    "NLP Engineer",
    "Applied ML Engineer",
    "Senior AI Engineer",
    "Senior NLP Engineer",
    "Lead AI Engineer",
    "Senior Machine Learning Engineer"
]

def jd_bonus(candidate):

    title = candidate["profile"]["current_title"]

    if title in JD_TITLES:
        return 0.2

    return 0.0

CAREER_TERMS = [
    "retrieval",
    "ranking",
    "recommendation",
    "search",
    "matching",
    "relevance",
    "embeddings",
    "vector",
    "semantic search",
    "candidate matching",
    "recommendation engine",
    "elasticsearch",
    "faiss",
    "milvus",
    "pinecone",
    "qdrant",
    "bm25",
    "ndcg",
    "mrr",
    "ab testing"
]

# %%
def career_score(candidate):

    text = ""

    for job in candidate["career_history"]:
        text += " " + job["description"].lower()

    score = 0

    for term in CAREER_TERMS:
        if term in text:
            score += 1

    return score / len(CAREER_TERMS)



def combined_score(candidate,
                   semantic_score,
                   retrieval_score,
                   recruitability_score):

    title = candidate["profile"]["current_title"]

    tscore = title_score(title)

    exp = experience_score(candidate)

    career = career_score(candidate)

    score = (

        0.30 * semantic_score +

        0.25 * career +

        0.15 * retrieval_score +

        0.15 * tscore +

        0.10 * recruitability_score +

        0.05 * exp

    )

    return score


# %%




def generate_reasoning(candidate):

    profile = candidate["profile"]
    signals = candidate["redrob_signals"]

    title = profile.get("current_title", "")
    years = round(profile.get("years_of_experience", 0))

    skills = [s["name"] for s in candidate.get("skills", [])]

    career_text = " ".join(
        job.get("description", "")
        for job in candidate.get("career_history", [])
    ).lower()

    reasons = []

    # -------------------------------------------------
    # Basic profile
    # -------------------------------------------------

    reasons.append(f"{title} with {years} years of experience")

    # -------------------------------------------------
    # AI / ML skills
    # -------------------------------------------------

    ai_keywords = [
        "Machine Learning",
        "Deep Learning",
        "NLP",
        "Fine-tuning LLMs",
        "Computer Vision",
        "Image Classification",
        "Speech Recognition",
        "Recommendation Systems",
        "Search",
        "PyTorch",
        "TensorFlow",
        "Scikit-learn"
    ]

    infra_keywords = [
        "Spark",
        "Kafka",
        "Airflow",
        "Databricks",
        "AWS",
        "Azure",
        "GCP",
        "Docker",
        "Kubernetes",
        "Apache Beam",
        "MLflow"
    ]

    ai_found = [k for k in ai_keywords if k in skills]
    infra_found = [k for k in infra_keywords if k in skills]

    if ai_found:
        reasons.append(
            f"strong background in {', '.join(ai_found[:2])}"
        )

    elif infra_found:
        reasons.append(
            f"experience with {', '.join(infra_found[:2])}"
        )

    # -------------------------------------------------
    # Career history
    # -------------------------------------------------

    career_map = {
        "rag": "experience building RAG systems",
        "retrieval": "retrieval system development",
        "vector": "vector search expertise",
        "embedding": "embedding pipelines",
        "recommendation": "recommendation systems",
        "search": "search infrastructure",
        "nlp": "NLP applications",
        "llm": "LLM applications",
        "transformer": "transformer models",
        "spark": "large-scale Spark pipelines",
        "airflow": "workflow orchestration",
        "kafka": "real-time streaming systems",
        "mlflow": "ML lifecycle management",
        "docker": "containerized deployments",
        "kubernetes": "cloud-native deployment"
    }

    career_reason = None

    for keyword, sentence in career_map.items():

        if keyword in career_text:

            career_reason = sentence

            break

    if career_reason:

        reasons.append(career_reason)

    # -------------------------------------------------
    # Behavioural signals
    # -------------------------------------------------

    if signals.get("open_to_work_flag"):

        reasons.append("actively open to work")

    if signals.get("github_activity_score", -1) >= 70:

        reasons.append("strong GitHub activity")

    if signals.get("recruiter_response_rate", 0) >= 0.70:

        reasons.append("high recruiter response rate")

    if signals.get("interview_completion_rate", 0) >= 0.80:

        reasons.append("excellent interview completion history")

    # -------------------------------------------------
    # Caveats
    # -------------------------------------------------

    caveats = []

    if signals.get("notice_period_days", 0) > 90:

        caveats.append(
            f"{signals['notice_period_days']}-day notice period"
        )

    if not signals.get("open_to_work_flag"):

        caveats.append(
            "currently not marked open to work"
        )

    if (
        signals.get("avg_response_time_hours", 0) > 120
        and signals.get("recruiter_response_rate", 0) < 0.40
    ):

        caveats.append(
            "slow recruiter response"
        )

    # -------------------------------------------------
    # Final sentence
    # -------------------------------------------------

    summary = "; ".join(reasons[:5])

    if caveats:

        summary += "; caveat: " + ", ".join(caveats)

    return summary + "."

# %%
def rank_candidates(jd_text, candidates, top_k=100):
    candidates = candidates[:1000]
    """
    Rank candidates for a given Job Description.

    Parameters
    ----------
    jd_text : str
        Job description text.

    candidates : list
        List of candidate dictionaries.

    top_k : int
        Number of top candidates to return.

    Returns
    -------
    pandas.DataFrame
        Submission dataframe.
    """

    # --------------------------------------------
    # Candidate Texts
    # --------------------------------------------

    candidate_texts = [
        build_candidate_text(c)
        for c in candidates
    ]

    # --------------------------------------------
    # Candidate Embeddings
    # --------------------------------------------

    candidate_embeddings = model.encode(
        candidate_texts,
        batch_size=32,
        show_progress_bar=True,
        convert_to_numpy=True
    )

    # --------------------------------------------
    # JD Embedding
    # --------------------------------------------

    jd_embedding = model.encode(
        jd_text,
        convert_to_numpy=True
    )

    # --------------------------------------------
    # Semantic Similarity
    # --------------------------------------------

    similarities = cosine_similarity(
        [jd_embedding],
        candidate_embeddings
    )[0]

    # --------------------------------------------
    # Score Every Candidate
    # --------------------------------------------

    results = []

    for idx, candidate in enumerate(candidates):

        semantic = similarities[idx]

        retrieval = (
            retrieval_score(
                build_candidate_text(candidate)
            )
            / len(RELEVANT_TERMS)
        )

        recruit = recruitability_score(candidate)

        score = combined_score(
            candidate,
            semantic,
            retrieval,
            recruit
        )

        score += jd_bonus(candidate)

        results.append({

            "candidate_id":
                candidate["candidate_id"],

            "title":
                candidate["profile"]["current_title"],

            "semantic_score":
                semantic,

            "retrieval_score":
                retrieval,

            "recruitability":
                recruit,

            "final_score":
                round(score * 100, 2)

        })

    # --------------------------------------------
    # Convert to DataFrame
    # --------------------------------------------

    df = pd.DataFrame(results)

    ranked_candidates = (
        df.sort_values(
            by="final_score",
            ascending=False
        )
        .reset_index(drop=True)
    )

    # --------------------------------------------
    # Top Candidates
    # --------------------------------------------

    final_top100 = ranked_candidates.head(top_k).copy()

    final_top100["rank"] = range(
        1,
        len(final_top100) + 1
    )

    # --------------------------------------------
    # Candidate Lookup
    # --------------------------------------------

    candidate_lookup = {

        c["candidate_id"]: c

        for c in candidates

    }

    # --------------------------------------------
    # Generate Reasoning
    # --------------------------------------------

    final_top100["reasoning"] = [

        generate_reasoning(
            candidate_lookup[cid]
        )

        for cid in final_top100["candidate_id"]

    ]

    # --------------------------------------------
    # Final Submission
    # --------------------------------------------

    submission = final_top100[
        [
            "candidate_id",
            "rank",
            "final_score",
            "reasoning"
        ]
    ].copy()

    submission.rename(
        columns={
            "final_score": "score"
        },
        inplace=True
    )

   

    return submission

if __name__ == "__main__":

    jd_text = """
    Senior AI Engineer.

    Must have experience building production retrieval,
    ranking, recommendation and matching systems.

    Experience with embeddings, vector databases,
    semantic search, FAISS, Milvus, Elasticsearch,
    hybrid search, evaluation metrics such as NDCG,
    MRR and MAP.

    Strong Python.
    Production ML.
    Product company experience preferred.
    Open to shipping systems quickly.
    Not looking for pure researchers.
    """

    submission = rank_candidates(
        jd_text,
        candidates
    )

    print(submission.head())


