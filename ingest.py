import os 
import random 


def load_documents(folder = "documents/"): 
    """
    Reads every .txt file in the documents/ folder.
    Returns a list of dicts
    """
    documents = [] 
    for filename in sorted(os.listdir(folder)): 
        if filename.endswith(".txt"): 
            filepath = os.path.join(folder, filename)

            with open(filepath, "r", encoding = "utf-8") as f: 
                text = f.read()
            documents.append({"source": filename, "text": text})
            print(f"loaded: {filename} ({len(text)} chars)")
    print(f"\nTotal documents loaded: {len(documents)}\n")
    return documents        


#Cleaning 

def clean_text(text):
    """
    Cleans a single document's text.
    Removes: extra blank lines, leading/trailing whitespace,
             excessive spaces between words.
    """
 
    lines = text.splitlines()

    cleaned_lines = []
    for line in lines:
        stripped = line.strip()

        if len(stripped) < 3:
            continue

        cleaned_lines.append(stripped)

    cleaned = " ".join(cleaned_lines)


    while "  " in cleaned:
        cleaned = cleaned.replace("  ", " ")

    return cleaned.strip()


# Chunk 
def chunk_text(text, source, chunk_size=500, overlap=100):
    """
    Splits a cleaned text into overlapping chunks.

    chunk_size = 500: each chunk is 500 characters long
    overlap    = 100: consecutive chunks share 100 characters
    step       = 400: each new chunk starts 400 chars after
                      the previous one (500 - 100 = 400)
    """
    chunks = []
    step = chunk_size - overlap  # = 400
    start = 0
    chunk_index = 0

    while start < len(text):
        end = start + chunk_size

 
        chunk = text[start:end].strip()

        # Only keep chunks that have real content
        if len(chunk) > 50:
            chunks.append({
                "text": chunk,
                "source": source,
                "chunk_index": chunk_index
            })
            chunk_index += 1

   
        start += step

    return chunks



def run_pipeline():

    # LOAD
    documents = load_documents()

    # CLEAN + CHUNK 
    all_chunks = []

    for doc in documents:
        cleaned = clean_text(doc["text"])
        chunks = chunk_text(cleaned, doc["source"])
        all_chunks.extend(chunks)

        print(f"{doc['source']}: {len(chunks)} chunks")

 
    print(f"\nTotal chunks across all documents: {len(all_chunks)}")
    print(f"Expected: ~93 chunks\n")

 
    print("=" * 60)
    print("SAMPLE CHUNKS — read each one carefully")
    print("=" * 60)

    sample = random.sample(all_chunks, min(20, len(all_chunks)))

    for i, chunk in enumerate(sample):
        print(f"\n--- Chunk {i+1} ---")
        print(f"Source    : {chunk['source']}")
        print(f"Index     : {chunk['chunk_index']}")
        print(f"Length    : {len(chunk['text'])} chars")
        print(f"Content   :\n{chunk['text']}")
        print("-" * 40)

    return all_chunks



if __name__ == "__main__":
    all_chunks = run_pipeline()