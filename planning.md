# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->
Mathematics professor and course reviews of mathematics department at New York University. This knowledge is valuable because official university sources only list course descriptions — the real information about exam style, grading, and what actually helps students succeed lives in student reviews 
and forum posts that are scattered and hard to search. Also the reddit text files are expremely helpful to truly understand the process and outcome of being a math major in nyu. 
---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

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

**Chunk size:** 500 characters

**Overlap:** 100 characters

**Reasoning:**
After running analyze_docs.py on my 10 documents, my corpus 
contains 37,528 total characters across 10 files, with an 
average of 3,752 characters and 632 words per file. 

At 500 characters with 100 character overlap, the pipeline 
produces approximately 93 chunks total — well within the 
50-2000 healthy range. Each file produces roughly 7-8 chunks, 
which is enough granularity to isolate individual professor 
opinions or specific Reddit comments without splitting 
mid-thought.

I chose 500 over 300 characters because my Reddit thread 
documents build arguments across multiple sentences — a 
300-character chunk would frequently cut mid-argument and 
lose the context needed to answer questions about NYU math 
difficulty or professor teaching style.

The 100-character overlap ensures sentences near chunk 
boundaries appear in both adjacent chunks, so on average there would 
be less key opinions that are lost at some split point.
---

## Retrieval Approach


<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->



**Embedding model:**
all-MiniLM-L6-v2. 
This will run locally with no API key to produce a 384 dimensional vector chosen for zero cost and no rate limits during the development process. 

**Top-k:**

Estimate about K=5 will suffice since retreiving too few chunks for comparison can risk missing relevant information 
when a question from the input can be span of multiple vectors/different aspects. For example, a question about professor difficulty and 
office hours might need multiple chunks from different reviews. Also retrieving too much chunks will add too much irrelavant noise. 
The embedding model maps text to vectors in 384-dimensional space where semantic similarity corresponds to geometric 
proximity (measured by cosine similarity). Phrases like "strict grader" and "marks harshly" produce vectors that 
are close together in that space because the model learned during training that they appear in similar contexts. This 
means queries about "difficult grading" will retrieve chunks containing "harsh marking" even with zero word 
overlap — critical for student review text which uses 
highly varied informal language.



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

## Evaluation Plan



| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | What are Professor Michael Shelley's class assessment process of the course | Mainly grades test and midterms and around 4 homework assignments that is graded, so student will be assessed by a few things only |
| 2 | What do students say about Pang's exams and grading curve? | 
Students say exams are straightforward, practice exams are harder 
than actual exams, and there is a generous curve at end of semester |
| 3 | What are the difficulties of being a math major at NYU? | 
Extremely rigorous, proof heavy, surrounded by top students, 
need 3.6-3.7 GPA to stand out |

| 4 | What is it like being a math major at NYU Courant? | 
Sets you apart from other NYU students, STEM is uncommon at NYU, 
creative environment, heavy workload |

| 5 | Should I choose NYU for mathematics compared to other schools? | 
Courant is highly respected, strong for pure math and research, 
free MS program mentioned, 30-40% go to PhD |

---

## Anticipated Challenges


1. Review sparsity for some professors: Professors like Michael Shelley have very few reviews on Rate My Professors (In this case 13 review, small compared to others in the sources). This means the system may not have enough 
   information to answer detailed questions about those professors, 
   and may either retrieve loosely related chunks or fail to answer 
   entirely. This is a retrieval coverage problem caused by thin 
   data, not a pipeline failure.

2. Chunk boundary splitting key facts: Reddit threads often build 
   an argument across multiple sentences — for example, a student 
   might say "NYU math is proof-heavy. This means you need real 
   analysis before sophomore year. Most students who struggle do 
   so because they skip the prerequisites." If this gets split 
   across chunks, the retrieved chunk might only contain one 
   sentence without the context that makes it meaningful. The 
   100-character overlap reduces but does not fully eliminate this risk.
---

## Architecture

```
Raw .txt files in documents/ folder
(10 files: RMP professor reviews + Reddit threads)
         │
         ▼
┌─────────────────────────────┐
│   INGESTION — ingest.py     │
│   - os.listdir() to load    │
│     all .txt files          │
│   - Clean whitespace,       │
│     blank lines, artifacts  │
│   - Output: list of dicts   │
│     {text, source filename} │
└─────────────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│   CHUNKING — ingest.py      │
│   - Chunk size: 500 chars   │
│   - Overlap: 100 chars      │
│   - Step size: 400 chars    │
│   - Output: ~93 chunks      │
│     each with source        │
│     filename as metadata    │
└─────────────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│   EMBEDDING — embed.py      │
│   - sentence-transformers   │
│   - Model: all-MiniLM-L6-v2 │
│   - Each chunk → 384-dim    │
│     vector in R³⁸⁴          │
└─────────────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│   VECTOR STORE — embed.py   │
│   - ChromaDB (local)        │
│   - Stores: vectors +       │
│     chunk text + metadata   │
│     (source filename,       │
│      chunk index)           │
└─────────────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│   RETRIEVAL — query.py      │
│   - User query → embed      │
│     with same model         │
│   - Cosine similarity       │
│     search in ChromaDB      │
│   - Returns top K=5 chunks  │
│     + source filenames      │
└─────────────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│   GENERATION — query.py     │
│   - Groq API                │
│   - Model: llama-3.3-70b    │
│   - Retrieved chunks fed    │
│     as context only         │
│   - Prompt enforces         │
│     grounding — no outside  │
│     knowledge allowed       │
│   - Answer includes source  │
│     filename citation       │
└─────────────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│   INTERFACE — app.py        │
│   - Gradio web UI           │
│   - Input: text question    │
│   - Output: answer +        │
│     source file citations   │
│   - Runs at localhost:7860  │
└─────────────────────────────┘
```
---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**
