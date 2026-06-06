# Enterprise Policy Compliance QA Agent 🎯

An enterprise-grade, zero-hallucination Retrieval-Augmented Generation (RAG) system engineered to provide employees with fast, accurate, and consistently grounded answers to complex corporate policy questions, strictly utilizing internal documents.

## 💼 Business Value & Impact

* **Reduced Compliance Risk:** By utilizing a strict RAG architecture, the system virtually eliminates LLM hallucinations, ensuring all answers are traceable, factual, and compliant with internal rules.
* **Operational Efficiency:** Dramatically reduces the volume of repetitive queries hitting HR, legal, and compliance teams by automating first-line policy support.
* **Auditability & Trust:** Every generated response is backed by exact document references and a quantifiable confidence metric, building deep user trust.

---

## 🛠️ Technical Architecture & Innovation

The system is built on a custom modular RAG framework designed for precision, speed, and enterprise scalability.

### Core Technology Stack
* **LLM Engine:** OpenAI API (`gpt-4o-mini` for generation, `text-embedding-3-small` for semantic representation).
* **Vector Database:** ChromaDB (high-performance local vector storage for semantic indexing).
* **Frontend UI:** Streamlit (clean, interactive UI for end-users).
* **Data Processing:** PDF context parsing utilities (`pdfplumber` preparation built into `utils.py`).

### Key Implementation Innovations
* **Contextual Filtering:** Engineered to handle global enterprise complexity by applying metadata routing (e.g., `country="GLOBAL"` filtering) directly within the vector database search query to enforce region-specific compliance.
* **Overlapping Chunking Strategy:** Implemented a smart sliding window technique during document ingestion to preserve context across text segment boundaries and optimize prompt context quality.

---

## 🛡️ Trust & Reliability Framework (Hallucination Defense)

To solve the reliability issues inherent in baseline LLM deployments, this system enforces a **Dual-Layer Defense Mechanism**:

1. **Semantic Distance Thresholding:** The agent evaluates vector distance scores against a strict ceiling (e.g., `0.35`). If the closest piece of evidence in the vector store fails to pass this threshold, generation is halted.
2. **Mandatory Graceful Refusal:** When information is missing or uncertain, the engine avoids guessing and outputs a hard-coded `"INSUFFICIENT EVIDENCE"` response.
3. **Traceable Citations:** Outputs are explicitly bound to their source components (`Document Name | Page | Section`).
4. **Quantifiable Trust Metric:** Accompanies every answer with an explicit *Confidence Score* mathematically calculated as:
   $$\text{Confidence Score} = 1.0 - \text{Semantic Distance}$$

---

🚀 Setup & Local Installation
1. Clone the Repository
git clone [https://github.com/HaidarBakri01/policy-qa-agent.git](https://github.com/YOUR_USERNAME/policy-qa-agent.git)
cd policy-qa-agent

2. Configure Your Virtual Environment

# Create the environment
python -m venv venv

# Activate on Windows (Command Prompt)
venv\Scripts\activate.bat

# Activate on macOS / Linux
source venv/bin/activate

3. Install Dependencies

pip install -r requirements.

4. Set Up Environment Variables
OPENAI_API_KEY=your_actual_openai_api_key_here

5. Run the Application

# Run the user-facing app
streamlit run streamlit_app.py