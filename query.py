import os
from groq import Groq
from dotenv import load_dotenv
from ingest import run_pipeline
from embed import embed_and_store, retrieve, collection
#Loads the api kev from .env 
load_dotenv() 

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Track whether we have embedded chunks yet
# We only want to run the pipeline once per session
_pipeline_initialized = False

def initialize_pipeline():
    """
    Runs the ingestion and embedding pipeline once.
    After this, all 97 chunks are stored in ChromaDB
    and ready to be retrieved.
    """
    global _pipeline_initialized
    
    if not _pipeline_initialized:
        print("Initializing pipeline (first query only)...")
        all_chunks = run_pipeline()
        embed_and_store(all_chunks)
        _pipeline_initialized = True
        print("Pipeline ready.\n")


# ── PROMPT TEMPLATE ───────────────────────────────────────
def build_prompt(question, chunks, sources):
    """
    Builds the prompt that gets sent to the LLM.
    
    This is the most important function for grounding.
    The prompt MUST:
    1. Tell the LLM to use ONLY the provided documents
    2. Tell it to say "I don't have enough information"
       if the answer isn't in the documents
    3. Tell it to cite which source file it used
    """
    
    # Format each chunk with its source label
    context_blocks = []
    for i, (chunk, source) in enumerate(zip(chunks, sources)):
        context_blocks.append(
            f"[Document {i+1} — {source}]:\n{chunk}"
        )
    
    context = "\n\n".join(context_blocks)
    # This is a test prompt for the llm 
    prompt = f"""You are a helpful assistant that answers questions 
about NYU Mathematics professors and courses based ONLY on the 
student reviews and forum posts provided below.

STRICT RULES:
1. Answer ONLY using information from the documents provided.
2. Do NOT use any outside knowledge or make assumptions.
3. If the documents don't contain enough information to answer 
   the question, respond with exactly: 
   "I don't have enough information in my documents to answer that."
4. Always cite which document(s) your answer came from using 
   the format: (Source: filename)

DOCUMENTS:
{context}

QUESTION: {question}

ANSWER (cite your sources):"""
    
    return prompt


# ─ask function 
def ask(question):
    """
    The main function that ties everything together.
    
    Given a plain English question:
    1. Retrieves the 5 most relevant chunks from ChromaDB
    2. Builds a grounded prompt with those chunks
    3. Sends to Groq LLM
    4. Returns the answer + list of source filenames
    
    Returns a dict:
    {
        "answer": "The answer text...",
        "sources": ["prof_Liming_Pang_rmp.txt", ...]
    }
    """
    
    # Make sure pipeline has been run
    initialize_pipeline()
    
    # Step 1: Retrieve top 5 relevant chunks
    results = retrieve(question, k=5)
    
    chunks   = results["documents"][0]
    metadata = results["metadatas"][0]
    distances = results["distances"][0]
    
    # Extract unique source filenames
    sources = [meta["source"] for meta in metadata]
    unique_sources = list(dict.fromkeys(sources))
    
    # Step 2: Build the grounded prompt
    prompt = build_prompt(question, chunks, sources)
    
    # Step 3: Send to Groq LLM
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a grounded assistant. You answer "
                    "questions strictly from provided documents. "
                    "Never use outside knowledge."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.1,  # low temperature = more factual,
                          # less creative/hallucination
        max_tokens=500
    )
    
    answer = response.choices[0].message.content
    
    return {
        "answer":  answer,
        "sources": unique_sources
    }


# ── TEST GROUNDING ────────────────────────────────────────
def test_grounding():
    """
    Tests 3 queries end-to-end to verify grounding.
    Run this before building the interface.
    """
    
    test_cases = [
        {
            "question": "What do students say about Pang's exams and grading curve?",
            "should_answer": True  # documents cover this
        },
        {
            "question": "How does Professor Michael Shelley assess students?",
            "should_answer": True  # documents cover this
        },
        {
            "question": "What is the food like at NYU dining halls?",
            "should_answer": False  # documents do NOT cover this
                                    # system should decline
        }
    ]
    
    for test in test_cases:
        q = test["question"]
        print("=" * 60)
        print(f"QUESTION: {q}")
        print(f"Expected: {'Should answer' if test['should_answer'] else 'Should DECLINE'}")
        print("-" * 60)
        
        result = ask(q)
        
        print(f"ANSWER:\n{result['answer']}")
        print(f"\nSOURCES: {result['sources']}")
        print()


# Run grounding test when cal  
if __name__ == "__main__":
    test_grounding()