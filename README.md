# Project VITAL — LLM + RAG Testing Tutorial (Student Starter)

**CSCI3364 — Software Testing, Quality and Security | Boston College**  

In this tutorial you will build a local LLM chatbot, extend it with retrieval-augmented generation (RAG), and design tests that distinguish retrieval failures from generation failures.

## Before class

1. Install [Ollama](https://ollama.com/download).
2. Run `ollama pull qwen2.5:1.5b` (approximately 1 GB).
3. Check that `ollama run qwen2.5:1.5b` answers a question; type `/bye` to exit.
4. Install Python 3.10 or later.

## Run the baseline chatbot

```bash
git clone https://github.com/CSCI3364-Fall2026/VITAL-RAG-Starter.git
cd VITAL-RAG-Starter
python3 -m venv .venv
source .venv/bin/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

The baseline chatbot works without RAG. If Ollama is unavailable, check that its service is running and the model is downloaded.

## Lab schedule

| Activity |
| --- | --- |
| LLMs, hallucinations, RAG and test oracles |
| Run chatbot and establish baseline responses |
| Load policy documents and implement TF-IDF retrieval |
| Add source context to model calls and a RAG toggle |
| Design and run automated tests; compare answers |
| Interpret results and report conclusions |

## Tasks (write the code yourself)

1. **Baseline**: Ask three policy questions before implementing RAG. Record the answers.
2. **TODO 1 — load documents** in `rag.py`. Return sorted `(filename, text)` tuples for `.txt` files.
3. **TODO 2 — retrieve** in `rag.py`. Use `TfidfVectorizer` and cosine similarity to rank documents. Return at most `k` `(filename, text, score)` tuples. Exclude zero-score results and break ties by filename.
4. **TODO 3 — format context** in `rag.py`. Prefix each selected document with `[Source: filename]`.
5. **TODO 4 — integrate RAG** in `app.py`. Add a sidebar **Enable RAG** toggle and send context to `ask_llm(question, context)` when enabled. Display retrieved filenames to the user.
6. **Test and improve**: run `pytest -q`, add at least one test, investigate a failure, make one improvement, and rerun.

The included `tests/test_retrieval.py` intentionally **fails initially** because the retrieval functions are incomplete. Passing those tests is a milestone, not a guarantee that generated answers are correct.

## Suggested questions

- How many hours before an appointment must I cancel?
- Can I request a same-day appointment?
- How are laboratory results communicated?
- Does the clinic provide free transportation? (The documents do not answer this.)
- What happens when I ask about an unsupported policy?

## Evidence to submit

For at least four questions, record: (a) question, (b) expected source, (c) retrieved filenames, (d) response without RAG, (e) response with RAG, and (f) whether the response is **supported by the source**. Explain one failure, your change, and the outcome of rerunning the test. Distinguish failures in retrieval from failures in generation.

**Security and privacy:** The six clinic policy files are fictional educational materials. Never enter real patient information or protected health information. Treat retrieved documents as untrusted data.

[Project VITAL course repository](https://github.com/CSCI3364-Fall2026/Project_VITAL)
