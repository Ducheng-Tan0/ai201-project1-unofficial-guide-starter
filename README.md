# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

Mathematics professor and course reviews of mathematics department at New York University. This knowledge is valuable because official university sources only list course descriptions — the real information about exam style, grading, and what actually helps students succeed lives in student reviews 
and forum posts that are scattered and hard to search. Also the reddit text files are expremely helpful to truly understand the process and outcome of being a math major in nyu. 

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->
| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | Rate My Professor |  Mathematics Department at NYU - Michael Shelley  | https://www.ratemyprofessors.com/professor/1085124|
| 2 | Rate My Professor | Department at NYU  - Liming Pang | https://www.ratemyprofessors.com/professor/2291493 |
| 3 | Rate My Professor |  Department at NYU  - John Chiarelli |https://www.ratemyprofessors.com/professor/2721237|
| 4 | Rate My Professor | Department at NYU  - Julius_Damarackas | https://www.ratemyprofessors.com/professor/2742712 |
| 5 | Rate My Professor | Department at NYU  - Jose_Diaz-Alban| https://www.ratemyprofessors.com/professor/805403 |
| 6 | Reddit |r/nyu | https://www.reddit.com/r/nyu/comments/1s5zg5g/nyu_courant_pure_math_ms_advice/|
| 7 | Reddit | r/nyu  | https://www.reddit.com/r/nyu/comments/rhfnnk/is_nyu_mathematics_really_that_good/ |
| 8 | Reddit | r/ApplyingToCollege | https://www.reddit.com/r/ApplyingToCollege/comments/1lb12ce/nyu_vs_cmu_math_major/ | 
| 9 | Quora | How are Math majors at Courant Institute compared to the rest of the students at NYU?| https://www.quora.com/How-are-Math-majors-at-Courant-Institute-compared-to-the-rest-of-the-students-at-NYU |
| 10 | Reddit  | r/nyu | https://www.reddit.com/r/nyu/comments/1j3p0z2/in_my_freshman_year_of_undergrad_right_now_and_im/  |


---

## Chunking Strategy


## Chunking Strategy

**Chunk size:** 500 characters

**Overlap:** 100 characters

**Why these choices fit your documents:**

After running analyze_docs.py on my 10 documents, my corpus 
contains 38750 total characters across 10 files, with an 
average of 3875 characters and 654 words per file. 

At 500 characters with 100 character overlap, the pipeline 
produces approximately 96 chunks total which well within the 
50-2000 healthy range recommended.

I chose 500 over 300 characters because my Reddit thread 
documents build arguments across multiple sentences a 
300-character chunk would frequently cut mid-argument and 
lose the context needed to answer questions about NYU math 
difficulty or professor teaching style. I also experimented with tunning the character per chunk from 300 to 650, in result it seems that 500 is approximately is the best to use based on the distance metric. 

The 100-character overlap ensures sentences near chunk 
boundaries appear in both adjacent chunks, so on average there would be less key opinions that are lost at some split point.


**Final chunk count:**
96 chunks with 100 overlap at 500 characters 
---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**
all-MiniLM-L6-v2. 
This will run locally with no API key to produce a 384 dimensional vector chosen for zero cost and no rate limits during the development process. 


**Production tradeoff reflection:**
- Context length: all-MiniLM-L6-v2 truncates at 256 tokens.
  For longer Reddit threads, text-embedding-3-large 
  (8191 token limit) would avoid truncation.
  
- Domain accuracy: A model fine-tuned on academic review 
  language would produce more accurate similarity scores 
  for domain-specific terms like "curved exams" or 
  "proof-based coursework."
  
- Cost vs latency: all-MiniLM-L6-v2 runs locally in 
  milliseconds at no cost. OpenAI embeddings are more 
  accurate but cost per API call and add network latency.
  
- Multilingual support: Not needed here mostly (In English), except for one comment in the rmp.txt is in Chinese 
 
---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**

In the function build_promt() in query.py, I gave explicit instruction such as 
    """
    1. Tell the LLM to use ONLY the provided documents
    2. Tell it to say "I don't have enough information"
       if the answer isn't in the documents
    3. Tell it to cite which source file it used
    """
The LLM will use "I don't have enough information" as a response to any prompt 
that is not related to the domain or can not be answered with the given files 
to avoid misleading answers or answers that have no citation. 

**How source attribution is surfaced in the response:**

In the side bar of the answer textbox the sources are listed in bullets that correspond to the answer. Also for every claim made in the answer it follows up with the citation of the source as the .txt file from /documents. 

e.g. 

Your Question : 
What are the difficulties of being a math major at NYU?

Answer : 
Being a math major at NYU can be challenging. It is mentioned that the undergrad math major is "not an easy major" and that one should not expect a high GPA (3.7+) unless they are "really good" (Source: nyu_kumokiri2000_reddit.txt). Additionally, it is stated that "Math major is good but hard" and that even passing through the honors math degree can be difficult (Source: nyu_Cheacheahuntyer_reddit.txt). Furthermore, it is noted that the curriculum might be stressful for some students, especially those who do not consider themselves to be "the sharpest tool in the shed" (Source: nyu_kumokiri2000_reddit.txt).

In addition there are bench mark questions that are listed as example on the bottom of the UI that can guide the users to click on if the question is of interest to them. 
---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What are Professor Michael Shelley's class assessment process of the course | Mainly grades test and midterms and around 4 homework assignments that is graded, so student will be assessed by a few things only | Professor Michael Shelley's class assessment process includes exams that are considered doable if one goes through his lecture notes carefully, and the homework and textbook are also part of the assessment. The textbook is not very helpful, and it's recommended to rely on the professor's lecture notes. The class is described as lecture-heavy and test-heavy. The professor does give points where he can on exams. (Source: prof_Michael_Shelley_rmp.txt, Documents 1, 2, 4) | Relevant | Partially accurate | 
| 2 | What do students say about Pang's exams and grading curve? | 
Students say exams are straightforward, practice exams are harder 
than actual exams, and there is a generous curve at end of semester | According to the documents, students say that Professor Pang's exams are "very straightforward" and "most of the questions are of similar difficulty to the textbook's problems" (Source: prof_Liming_Pang_rmp.txt). Additionally, it is mentioned that "Practice exams are MUCH harder than the actual exam" (Source: prof_Liming_Pang_rmp.txt). There is no explicit mention of a grading curve for Professor Pang's course in the provided documents. | Relevant | Accurate | 
| 3 | What are the difficulties of being a math major at NYU? | 
Extremely rigorous, proof heavy, surrounded by top students, 
need 3.6-3.7 GPA to stand out | Being a math major at NYU can be challenging. It is mentioned that the undergrad math major is "not an easy major" and that one should not expect a high GPA (3.7+) unless they are "really good" (Source: nyu_kumokiri2000_reddit.txt). Additionally, it is stated that "Most people don’t get a masters" and that the math major is "good but hard" (Source: nyu_Cheacheahuntyer_reddit.txt). Furthermore, it is noted that even passing through the honors math degree is difficult (Source: nyu_Cheacheahuntyer_reddit.txt). 

It is also implied that the curriculum might be stressful, with one student expressing concern about being able to handle a "top-tier curriculum" (Source: nyu_kumokiri2000_reddit.txt). Overall, the difficulties of being a math major at NYU seem to stem from the challenging coursework and high academic standards. | Relevant |Accurate|
| 4 | What is it like being a math major at NYU Courant? | 
Sets you apart from other NYU students, STEM is uncommon at NYU, 
creative environment, heavy workload | Being a math major at NYU Courant sets you apart from other NYU students, as STEM majors are not as common as they might be at other schools. Math majors at Courant are widely regarded as a distinct subpopulation within NYU for academic rigor, research orientation, and culture. They admit students with very strong quantitative profiles and have a research-oriented approach. If you truly enjoy complex mathematics and like to be surrounded by people who are very creative and have majors that are completely different from yours, you will do well as a math major at NYU. (Source: Document 1 — Quora_MO.txt, Document 3 — Quora_MO.txt, Document 4 — Quora_MO.txt) | Relevant | Accurate |
| 5 | Should I choose NYU for mathematics compared to other schools? | 
Courant is highly respected, strong for pure math and research, 
free MS program mentioned, 30-40% go to PhD | You should consider choosing NYU for mathematics, especially if you're interested in traditional math or applied math. NYU is a strong school for math, with its Applied Math department regularly ranking top 1-2 in the country (Source: A2C_epicthrowaway0000_reddit.txt). The faculty in math at NYU is also highly regarded (Source: A2C_epicthrowaway0000_reddit.txt). However, it's worth noting that other schools, such as CMU, may have a stronger overall STEM ecosystem (Source: A2C_epicthrowaway0000_reddit.txt). Ultimately, the decision depends on your individual priorities and circumstances, such as cost and your specific interests within math (Source: A2C_epicthrowaway0000_reddit.txt). | Relevant | Accurate |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**
What are Professor Michael Shelley's class assessment process of the course

**What the system returned:**
Professor Michael Shelley's class assessment process includes exams that are "quite doable if went through his lecture notes carefully" (Source: Document 4 — prof_Michael_Shelley_rmp.txt), and the class is described as "Lecture heavy Test heavy" (Source: Document 2 — prof_Michael_Shelley_rmp.txt). The assessment also includes homework, as one review mentions that "the hw" is part of the class (Source: Document 2 — prof_Michael_Shelley_rmp.txt). Additionally, the class is "Graded by few things" (Source: Document 2 — prof_Michael_Shelley_rmp.txt).

**Root cause (tied to a specific pipeline stage):**
I rate the system to be partially accurate as it did not have the specific amount of assessements in details like 
the answer suggested. 

**What you would change to fix it:**
It could be that the question is to vague and I made need to change the question to be less subjective. 
---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**
The spec are important to look back at during implementation so the pipline will stay on track. 

**One way your implementation diverged from the spec, and why:**

From a point of view I would argue it did not diverge from the spec. 

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**
*What I gave the AI:* Tell me where to change in app.py such that when I run it the website can be popped up by itself without manually pasting in the link. [app.py pasted in LLM]
- *What it produced:*
Find this line at the very bottom of app.py:
pythondemo.launch()
Change it to:
pythondemo.launch(inbrowser=True)
That single parameter tells Gradio to automatically open your default browser to http://localhost:7860 the moment you run python app.py. No manual copying needed.
- *What I changed or overrode:*
Added inbrowser=True into the launch function in the app.py

**Instance 2**

- *What I gave the AI:* Please help construct a python script that will read in a list of documents from a folder and counts character and word counts with and without character overlap. Then in the output print the corresponding number of chunks for a given number of words allowed in a chunk. 
- *What it produced:* import os


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

- *What I changed or overrode:* Overrode a total character per chunk to be set to 500 and 300. 

