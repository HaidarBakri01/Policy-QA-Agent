"""
Enterprise Policy QA Agent Backend Logic
ChromaDB + OpenAI integration (without FastAPI or Streamlit) using RAG engine

"""

import os
import openai
import google.generativeai as genai
from dotenv import load_dotenv
import chromadb
from chromadb.utils import embedding_functions

# -----------------------------
# Load environment
# -----------------------------
load_dotenv()

#OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
#if not OPENAI_API_KEY:
#    raise RuntimeError("OPENAI_API_KEY not found")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# -----------------------------
# ChromaDB setup
# -----------------------------
embedding_fn = embedding_functions.OpenAIEmbeddingFunction(
    api_key=OPENAI_API_KEY,
    model_name="text-embedding-3-small"
)

client = chromadb.Client(
    chromadb.config.Settings(persist_directory="./chroma_store")
)

collection = client.get_or_create_collection(
    name="policy_docs",
    embedding_function=embedding_fn
)

MAX_DISTANCE_THRESHOLD = 0.35

# -----------------------------
# Prompts
# -----------------------------
SYSTEM_PROMPT = "You are an enterprise policy assistant that answers questions using internal policy documents."
USER_PROMPT_TEMPLATE = "Question: {question}\nContext: {context}"

# -----------------------------
# Helper functions
# -----------------------------

#Retreive chunks
def retrieve_chunks(question: str, country: str | None = None, top_k: int = 5):
    """
    Retrieve relevant chunks from ChromaDB.
    """
    where_filter = {"country": country} if country else None

    #Retrieval logic
    results = collection.query(
                query_texts=[question],
                n_results=top_k, 
                where=where_filter
          )
    
    chunks = []
    if not results["documents"]:
        return chunks
    for i in range(len(results["documents"][0])):
        chunks.append({
            "text": results["documents"][0][i],
            "metadata": results["metadatas"][0][i],
            "distance": results["distances"][0][i]
        })
    return chunks

def passes_evidence_threshold(chunks):
    """
    Determine if evidence is strong enough to answer.
    """
    if not chunks:
        return False
    return chunks[0]["distance"] <= MAX_DISTANCE_THRESHOLD

#answer chunck
def answer_question(question: str, country: str | None = None):
    """
    Returns:
    {
        "answer": str,
        "citations": list[str],
        "confidence": float
    }
    """
    chunks = retrieve_chunks(question, country, top_k=6)

    #Hallucination refusal logic
    if not passes_evidence_threshold(chunks):
        return {
            "answer": "INSUFFICIENT EVIDENCE",
            "citations": [],
            "confidence": 0.0
        }

    #Prompt
    context = "\n---\n".join(
        f"[{c['metadata']['doc_name']} | page {c['metadata']['page']} | {c['metadata']['section']}]\n{c['text']}"
        for c in chunks
    )

    user_prompt = USER_PROMPT_TEMPLATE.format(
        question=question,
        context=context
    )

    #LLM call
    completion = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.0,
        max_tokens=400
    )

    answer_text = completion.choices[0].message.content.strip()
    citations = [
        f"{c['metadata']['doc_name']} | page {c['metadata']['page']} | {c['metadata']['section']}"
        for c in chunks
    ]

    confidence = round(1.0 - chunks[0]["distance"], 2)
    # Return format --> streamlit read
    return {
        "answer": answer_text,
        "citations": citations,
        "confidence": confidence
    }

# -----------------------------
# Example usage
# -----------------------------
if __name__ == "__main__":
    question = "Can I work remotely from another country for 3 months?"
    result = answer_question(question, country="GLOBAL")
    print("Answer:", result["answer"])
    print("Citations:", result["citations"])
    print("Confidence:", result["confidence"])
