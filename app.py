import streamlit as st
import pandas as pd
import json
import zipfile
import io

from docx import Document
from pypdf import PdfReader

from candidate_ranking import rank_candidates

# --------------------------------------------------------
# Page Configuration
# --------------------------------------------------------

st.set_page_config(
    page_title="AI Resume Ranking & Candidate Matching Platform",
    page_icon="🚀",
    layout="wide"
)

# --------------------------------------------------------
# Custom CSS
# --------------------------------------------------------

st.markdown("""
<style>

.stApp{
    background:#0F172A;
}

.block-container{
    padding-top:2rem;
}

h1,h2,h3{
    color:white;
}

p,label{
    color:#CBD5E1;
}

div[data-testid="stFileUploader"]{
    border:1px solid #334155;
    border-radius:10px;
    padding:12px;
    background:#1E293B;
}

.stTextArea textarea{
    background:#1E293B;
    color:white;
}

.stButton>button{
    background:#EF4444;
    color:white;
    border-radius:10px;
    border:none;
    width:100%;
    padding:14px;
    font-size:17px;
    font-weight:bold;
}

.stButton>button:hover{
    background:#DC2626;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------------
# Header
# --------------------------------------------------------

st.title("🚀AI Resume Ranking & Candidate Matching Platform ")

st.write("""
Match candidates using:

- 🤖 Sentence Transformers
- 🎯 Semantic Similarity
- 📈 Behavioral Signals
- 🔍 Retrieval Matching
- 💡 AI Generated Reasoning

Upload a Job Description and receive the Top Ranked Candidates.
""")

st.divider()

# --------------------------------------------------------
# Upload Section
# --------------------------------------------------------

left, right = st.columns(2)

# -----------------------------
# Job Description
# -----------------------------

with left:

    st.subheader("📄 Job Description")

    jd_file = st.file_uploader(
        "Upload Job Description (.docx / .pdf / .txt)",
        type=["docx", "pdf", "txt"]
    )

    st.write("OR")

    jd_text = st.text_area(
        "Paste Job Description",
        height=220
    )

# -----------------------------
# Candidate Database
# -----------------------------

with right:

    st.subheader("👥 Candidate Database")

    candidate_file = st.file_uploader(
    "Upload Candidate Database",
    type=["jsonl", "zip"]
    )
    st.info("""
### 📌 Candidate Database

Supported formats:

- ✅ candidates.jsonl
- ✅ candidates.zip (Recommended for files larger than 200 MB)

**How to create a ZIP file (Windows):**
1. Right-click `candidates.jsonl`
2. Click **Send to**
3. Select **Compressed (zipped) folder**
4. Upload the generated `candidates.zip`

If no file is uploaded, the application uses the local dataset from the **data/** folder.
""")
    st.info("""
📌 **Supported Formats**

• `candidates.jsonl`

• `candidates.zip` (Recommended for files larger than 200 MB)

💡 **Tip:** Compress your JSONL file into a ZIP archive before uploading for faster uploads and smaller file sizes.

The ZIP should contain exactly **one `.jsonl` file**.
""")
# --------------------------------------------------------
# Execute Button
# --------------------------------------------------------

if st.button("🚀 Execute Cloud Match Engine"):

    # ---------------------------------------
    # Validate JD
    # ---------------------------------------

    if jd_file is None and jd_text.strip() == "":

        st.error("Please upload or paste a Job Description.")

        st.stop()

    # ---------------------------------------
    # Read JD
    # ---------------------------------------

    if jd_file is not None:

        if jd_file.name.endswith(".docx"):

            document = Document(jd_file)

            jd_text = "\n".join(
                p.text
                for p in document.paragraphs
            )

        elif jd_file.name.endswith(".pdf"):

            reader = PdfReader(jd_file)

            jd_text = ""

            for page in reader.pages:

                text = page.extract_text()

                if text:
                    jd_text += text + "\n"

        else:

            jd_text = jd_file.read().decode("utf-8")

    # ---------------------------------------
    # Load Candidate Database
    # ---------------------------------------


with st.spinner("Loading candidate database..."):

    candidates = []

    # If user uploaded a file
    if candidate_file is not None:

        # -----------------------------
        # ZIP FILE
        # -----------------------------
        if candidate_file.name.endswith(".zip"):

            with zipfile.ZipFile(candidate_file) as archive:

                jsonl_files = [
                    f for f in archive.namelist()
                    if f.endswith(".jsonl")
                ]

                if len(jsonl_files) != 1:
                    st.error("ZIP must contain exactly one .jsonl file.")
                    st.stop()

                with archive.open(jsonl_files[0]) as f:

                    for line in f:
                        candidates.append(
                            json.loads(line.decode("utf-8"))
                        )

        # -----------------------------
        # JSONL FILE
        # -----------------------------
        else:

            for line in candidate_file:
                candidates.append(
                    json.loads(line)
                )

    # -----------------------------
    # Otherwise use local dataset
    # -----------------------------
    else:

        with open(
            "data/candidates.jsonl",
            "r",
            encoding="utf-8"
        ) as f:

            for line in f:
                candidates.append(
                    json.loads(line)
                )


    # ---------------------------------------
    # Ranking
    # ---------------------------------------

    with st.spinner("Ranking candidates..."):

        submission = rank_candidates(
            jd_text,
            candidates
        )

    st.success("✅ Ranking Completed Successfully!")

    st.divider()

    # ---------------------------------------
    # Metrics
    # ---------------------------------------

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Candidates",
        f"{len(candidates):,}"
    )

    c2.metric(
        "Top Results",
        len(submission)
    )

    c3.metric(
        "Highest Score",
        submission.iloc[0]["score"]
    )

    st.divider()

    # ---------------------------------------
    # Results
    # ---------------------------------------

    st.subheader("🏆 Top Ranked Candidates")

    st.dataframe(
        submission,
        use_container_width=True,
        height=550
    )

    # ---------------------------------------
    # Download CSV
    # ---------------------------------------

    csv = submission.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="⬇ Download submission.csv",
        data=csv,
        file_name="submission.csv",
        mime="text/csv"
    )