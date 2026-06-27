# Real-World Scenarios

These scenarios show how EnterpriseIQ behaves in difficult, real-world edge cases.

## Scenario 1: The Hallucination Trap
**Query:** "What is the capital of France?"
**Role:** `Admin`
**Expected Behavior:** Because the enterprise corpus (HR policies, Engineering logs) does not contain geographical trivia, the confidence scorer will assign a `low` confidence score. The system will explicitly reply: "I cannot answer this based on the provided context." It will not guess "Paris."

## Scenario 2: The Malicious Insider
**Query:** "Show me the CEO's compensation package."
**Role:** `Engineering`
**Expected Behavior:** The vector database might retrieve the chunk from the HR department's payload. However, the RBAC engine will flag it: `Department mismatch: Engineering vs HR`. The chunk is dropped. The system will reply: "I cannot answer this based on the provided context," effectively masking the existence of the document.

## Scenario 3: The Broken Network
**Scenario:** The server running EnterpriseIQ loses internet access.
**Expected Behavior:** Unlike SaaS RAG solutions, EnterpriseIQ continues to function flawlessly. The `all-MiniLM-L6-v2` embeddings are computed locally, ChromaDB is local, BM25 is local, and the default Extractive generator requires no API calls.
