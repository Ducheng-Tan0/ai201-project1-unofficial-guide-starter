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
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |

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

**What the system returned:**

**Root cause (tied to a specific pipeline stage):**

**What you would change to fix it:**

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**

**One way your implementation diverged from the spec, and why:**

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

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*

**Instance 2**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*
