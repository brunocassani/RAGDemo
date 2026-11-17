
# RAG Discussion

## 1. Evidence

| Question | Expected source | Retrieved filenames (RAG ON) | Response without RAG | Response with RAG | Supported by source? |
|---|---|---|---|---|---|
| How many hours before an appointment must I cancel? | cancellations.txt | scheduling.txt, visitors.txt, cancellations.txt | Could not answer; requested more context. | Must cancel at least 18 hours before the appointment. | Yes |
| Can I request a same-day appointment? | scheduling.txt | scheduling.txt, portal.txt | Could not assist. | Yes, subject to availability. | Yes |
| How are laboratory results communicated? Does the clinic provide free transportation? | lab_results.txt, visitors.txt | lab_results.txt, portal.txt, visitors.txt, billing.txt, scheduling.txt | Refused to answer, incorrectly identifying the question as political. | Results are communicated through the secure patient portal. The clinic does not provide free transportation. | Partially. The laboratory answer is supported, but the transportation claim is unsupported unless explicitly stated in the source. |
| What happens when I ask about an unsupported policy? | No relevant source expected | billing.txt, visitors.txt, scheduling.txt, lab_results.txt, cancellations.txt | Generated an unrelated explanation about unsupported software policies. | I do not have enough information. | Yes |

## 2. Failure Analysis and Change

**Failure: Generation layer.**

When asked whether the clinic provides free transportation, the RAG-enabled chatbot answered that the clinic does not provide it. However, the retrieved documents did not establish that transportation was unavailable. The model incorrectly treated the absence of information as evidence that the service did not exist.

**Change:** Modified the system prompt in `llm.py` to explicitly instruct the model not to infer that a service is unavailable merely because it is not mentioned in the retrieved context. It must instead respond, "I do not have enough information."

**Expected before/after:**
- Before: "The clinic does not provide free transportation."
- After: "I do not have enough information about transportation services."

Rerunning the question with RAG enabled should verify whether this prompt change prevents unsupported conclusions.

## 3. What the Tests Prove—and Do Not Prove

The tests demonstrate that RAG can retrieve relevant policy documents and improve answers to questions that the model cannot answer independently. They also demonstrate that irrelevant documents can be retrieved and that the LLM can generate unsupported conclusions even when relevant documents are available.

However, four questions against six fictional documents do not establish that retrieval is consistently accurate or that generated answers are always trustworthy.

## 4. Does Switching RAG ON Make a Chatbot Automatically Trustworthy?

No. RAG provides the model with relevant reference material, but it does not guarantee that the correct documents are retrieved or that the model interprets them accurately. Retrieval and generation must both be evaluated. The transportation example demonstrates that even with relevant context, the model can make unsupported claims.

## 5. Does Caching Help?

Caching can improve performance by avoiding repeated document loading and TF-IDF vectorization. However, it does not directly improve answer accuracy or trustworthiness. Cached documents must also be refreshed when policies change to avoid providing outdated information.
