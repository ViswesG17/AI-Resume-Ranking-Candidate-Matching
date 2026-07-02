# Redrob Hackathon — Submission Metadata Template
# Copy this file to your repo root as `submission_metadata.yaml` and fill it in.
# The fields here should match what you submit via the portal at upload time.
# Stage 3 review uses this file to verify your portal metadata.

# ============================================================================
# Team identity
# ============================================================================
team_name: "Hacksmith-6"  # Used in leaderboard and announcements

primary_contact:
  name: "GOLLA VISWES SRI SAI RAJU"
  email: "viswesg51@gmail.com"   # Used for all organizer communication
  phone: "+91-XXXXXXXXXX"        # Please replace with your actual mobile number

team_members:
  - name: "GOLLA VISWES SRI SAI RAJU"
    email: "viswesg51@gmail.com"
    role: "Team Lead & Data Engineer"
  - name: "Pavani Mynam"
    email: "mynampavani2854@gmail.com"
    role: "ML Engineer"
  - name: "Rangu Sukanya"
    email: "sukanya.rangu105@gmail.com"
    role: "Backend Developer"

# ============================================================================
# Code and reproducibility
# ============================================================================
github_repo: "https://github.com/YOUR_USERNAME/YOUR_REPO" # Please update with your link
# Required. Must be reachable. Private repos OK if you can grant organizer
# access at Stage 3 (the email to add will be communicated then).

sandbox_link: "http://localhost:8501" # Update this to your deployed URL if you push it online
# Required. A working hosted environment where the ranker can be run on a small
# candidate sample. See Section 10.5 of submission_spec.md for acceptable
# platforms (HuggingFace Spaces, Streamlit Cloud, Replit, Colab, Docker, Binder).

reproduce_command: "streamlit run app.py --server.maxUploadSize=100000"
# The single command that produces submission.csv from candidates.jsonl.
# Should run end-to-end within 5 minutes on CPU with 16GB RAM and no network.

# ============================================================================
# Compute environment
# ============================================================================
compute:
  platform: "Local Windows PC"                  # Or: "AWS EC2 c5.4xlarge", "Local Linux box", etc.
  cpu_cores: 8                                  # Number of CPU cores used
  ram_gb: 16                                    # Available RAM in GB
  python_version: "3.12.0"                      # Updated to match your Windows Store Python 3.12 path
  os: "Windows 11"                              # Your active desktop OS
  uses_gpu_for_inference: false                 # Must be false — see compute constraints
  has_network_during_ranking: false             # Must be false — no API calls during ranking (Fully offline TF-IDF Matrix version)
  pre_computation_required: false               # true if you pre-compute embeddings or train models offline
  pre_computation_time_minutes: 0               # Approximate, if applicable

# ============================================================================
# AI tools declaration
# ============================================================================
# Transparency only — declared use is NOT penalized. Be honest. Stage 5 interview
# may verify these declarations against your code; declarations that contradict
# your code or your interview are flagged.
ai_tools_used:
  - "Gemini"        # Used for structural pipeline debugging and optimization layout iterations

ai_usage_summary: |
  Used Gemini for code review, structuring data format outputs to match template fields, 
  and migrating away from network-dependent models to an optimized offline matrix-matching workflow.
  No candidate data was shared with external cloud LLMs during the local execution pass.

# ============================================================================
# Approach summary (optional but recommended)
# ============================================================================
methodology_summary: |
  High-speed local text processing ranker utilizing an offline TF-IDF vector vocabulary matrix configuration.
  Matches candidate resume blocks against job descriptions completely offline to sidestep network rate limits,
  API tokens, or folder permissions blocks. Dynamically parses formatting identifiers into a compact 
  string reasoning schema, allocating unique high-resolution float match scores between 0.0000 and 1.0000.
  Optimized footprint ensures 100k profile outputs finish execution smoothly in seconds well under a 5MB storage limit.

# ============================================================================
# Declarations
# ============================================================================
declarations:
  read_submission_spec: true        # I have read submission_spec.md in full
  code_is_original_work: true       # My code is my team's original work (using AI as a tool is fine)
  no_collusion: true                # I have not coordinated my submission with other teams
  honeypot_check_done: true         # Set true if you explicitly checked for honeypots in your ranking
  reproduction_tested: true         # I have tested that my reproduce_command runs end-to-end
