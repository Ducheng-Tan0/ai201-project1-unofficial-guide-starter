import os


"""  This small script was used to calculate the correct amount of chunks to use. """
def analyze_documents(folder="documents/"):
    print("=" * 50)
    print("DOCUMENT ANALYSIS")
    print("=" * 50)
    
    total_chars = 0
    total_words = 0
    file_count = 0
    
    for filename in sorted(os.listdir(folder)):
        if filename.endswith(".txt"):
            filepath = os.path.join(folder, filename)
            
            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()
            
            char_count = len(text)
            word_count = len(text.split())
            line_count = len(text.splitlines())
            
            # Estimate how many 500-char chunks this makes
            # With 100 overlap, effective step size is 400 per chunk
            # so we divide by 400 to account for overlap
            estimated_chunks = max(1, char_count // 400)
            
            print(f"\nFile: {filename}")
            print(f"  Characters : {char_count}")
            print(f"  Words      : {word_count}")
            print(f"  Lines      : {line_count}")
            print(f"  Est. chunks: ~{estimated_chunks} chunks")

            # These three lines are now INSIDE the if block
            total_chars += char_count
            total_words += word_count
            file_count += 1

    print("\n" + "=" * 50)
    print("OVERALL SUMMARY")
    print("=" * 50)
    print(f"Total files     : {file_count}")
    print(f"Total characters: {total_chars}")
    print(f"Total words     : {total_words}")
    print(f"Avg chars/file  : {total_chars // max(file_count, 1)}")
    print(f"Avg words/file  : {total_words // max(file_count, 1)}")
    print(f"\nEstimated total chunks at 500 chars (no overlap)  : ~{total_chars // 500}")
    print(f"Estimated total chunks at 500 chars (100 overlap) : ~{total_chars // 400}")
    print(f"Estimated total chunks at 300 chars (no overlap)  : ~{total_chars // 300}")
    print(f"Estimated total chunks at 300 chars (50 overlap)  : ~{total_chars // 250}")

analyze_documents()
