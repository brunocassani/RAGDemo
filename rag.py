"""Inspectable TF-IDF retrieval over fictional clinic policies."""
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

DOCS = Path(__file__).parent / "knowledge_base"

def load_documents(directory=DOCS):
    return [(p.name, p.read_text(encoding="utf-8")) for p in sorted(Path(directory).glob("*.txt"))]

def retrieve(question: str, k: int = 2, documents=None):
    docs = load_documents() if documents is None else documents
    if not docs or k <= 0:
        return []
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    vectors = vectorizer.fit_transform([text for _, text in docs] + [question])
    scores = cosine_similarity(vectors[-1], vectors[:-1]).ravel()
    ranked = sorted(range(len(docs)), key=lambda i: (-scores[i], docs[i][0]))
    return [(docs[i][0], docs[i][1], float(scores[i])) for i in ranked[:k] if scores[i] > 0]

def build_context(results):
    return "\n\n".join(f"[Source: {name}]\n{text}" for name, text, _ in results)

def answer_with_rag(question: str, k: int = 2):
    from llm import ask_llm
    results = retrieve(question, k)
    return ask_llm(question, build_context(results)), [name for name, _, _ in results]