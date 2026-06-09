import chromadb
from sentence_transformers import SentenceTransformer
from ingest import run_pipeline

# SETUP
# Load the embedding model
# This downloads ~80MB the first time, then caches locally
print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")
print("Model loaded.\n")

# Create a local ChromaDB client
# This stores your vectors in memory during the session
client = chromadb.Client()

# Create a collection — think of this like a table in a 
# regular database, but instead of rows it stores vectors
collection = client.create_collection(
    name="nyu_math_reviews",
    metadata={"hnsw:space": "cosine"} 
)


# 1: EMBED AND STORE 
def embed_and_store(chunks):
    """
    Takes all chunks from ingest.py and:
    1. Converts each chunk's text into a 384-dim vector
    2. Stores that vector in ChromaDB along with:
       - the original text
       - the source filename
       - the chunk index
    """
    print(f"Embedding {len(chunks)} chunks...")
    print("This may take 1-2 minutes on first run.\n")

   
    batch_size = 50
    
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i : i + batch_size]
        
        # Extract the text from each chunk in this batch
        texts = [chunk["text"] for chunk in batch]
        
        # Convert all texts to vectors at once
        # model.encode() returns a numpy array of shape
        # (batch_size, 384)
        embeddings = model.encode(texts)
        
        # Prepare data for ChromaDB
        ids        = [f"chunk_{i + j}" for j in range(len(batch))]
        documents  = texts
        metadatas  = [
            {
                "source":      chunk["source"],
                "chunk_index": chunk["chunk_index"]
            }
            for chunk in batch
        ]
        
        # Store everything in ChromaDB
        collection.add(
            ids        = ids,
            embeddings = [e.tolist() for e in embeddings],
            documents  = documents,
            metadatas  = metadatas
        )
        
        print(f"  Stored chunks {i} to {i + len(batch) - 1}")

    print(f"\nAll {len(chunks)} chunks embedded and stored.\n")


# 2. RETRIEVE 
def retrieve(query, k=5):
    """
    Takes a plain English question and finds the
    K most semantically similar chunks.
    
    Steps:
    1. Converts your query into a 384-dim vector
    2. Compares it against all stored vectors using
       cosine similarity
    3. Returns the K closest chunks with their metadata
    """
    # Embed the query using the same model
    query_embedding = model.encode(query).tolist()
    
    # Search ChromaDB for the K nearest vectors
    results = collection.query(
        query_embeddings = [query_embedding],
        n_results        = k
    )
    
    return results


# 3. TEST RETRIEVAL 
def test_retrieval():
    """
    Runs 3 of your evaluation plan questions through
    the retrieval system and prints results so you can
    judge quality before moving to generation.
    """
    
    # These are 3 of your 5 evaluation plan questions
    test_queries = [
        "What are Professor Michael Shelley's assessments like?",
         "What do students say about Pang exams and grading curve?",
        "What are the difficulties of being a math major at NYU?",
            "What is it like being a math major at NYU Courant?",
    "Should I choose NYU for mathematics compared to other schools?"
    ]
    
    for query in test_queries:
        print("=" * 60)
        print(f"QUERY: {query}")
        print("=" * 60)
        
        results = retrieve(query, k=5)
        
        # results is a dict with these keys:
        # - 'documents': list of chunk texts
        # - 'metadatas': list of metadata dicts
        # - 'distances': list of distance scores
        #   (lower = more similar, better match)
        
        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]
        
        for rank, (doc, meta, dist) in enumerate(
            zip(documents, metadatas, distances), start=1
        ):
            print(f"\n  Result #{rank}")
            print(f"  Source  : {meta['source']}")
            print(f"  Distance: {dist:.4f}  ", end="")
            
            # Give a quality signal next to the score
            if dist < 0.3:
                print("✓ STRONG MATCH")
            elif dist < 0.5:
                print("~ ACCEPTABLE")
            else:
                print("✗ WEAK — may be off-topic")
                
            print(f"  Content : {doc[:200]}...")
        
        print()

def inspect_source(source_filename):
    """
    Prints all chunks that came from a specific file.
    Useful for checking if header junk got embedded.
    """
    results = collection.get(
        where={"source": source_filename}
    )
    
    print(f"\nAll chunks from: {source_filename}")
    print("=" * 60)
    
    for i, (doc, meta) in enumerate(
        zip(results["documents"], results["metadatas"])
    ):
        print(f"\nChunk {meta['chunk_index']}:")
        print(doc[:300])
        print("-" * 40)

# MAIN 
if __name__ == "__main__":
    # This block ONLY runs when you type: python embed.py
    # It does NOT run when another file imports from embed.py
    
    print("Running ingestion pipeline...")
    all_chunks = run_pipeline()
    
    embed_and_store(all_chunks)
    
    inspect_source("prof_Liming_Pang_rmp.txt")
    
    test_retrieval()