# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->
Mathematics professor and course reviews of mathematics department at New York University. This knowledge is valuable because official university sources only list course descriptions — the real information about exam style, grading, and what actually helps students succeed lives in student reviews 
and forum posts that are scattered and hard to search.
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

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:**

**Overlap:**

**Reasoning:**

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**

**Top-k:**

**Production tradeoff reflection:**

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | | |
| 2 | | |
| 3 | | |
| 4 | | |
| 5 | | |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1.

2.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

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
