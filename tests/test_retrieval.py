from rag import load_documents, retrieve, build_context

def test_load_documents():
    assert len(load_documents()) == 6

def test_cancellation_policy_retrieved():
    hits = retrieve("How many hours before an appointment must I cancel?", k=2)
    assert "cancellations.txt" in [name for name, _, _ in hits]

def test_context_includes_source():
    assert "[Source: cancellations.txt]" in build_context([("cancellations.txt", "18 hours", 0.9)])

def test_empty_corpus():
    assert retrieve("question", documents=[]) == []
