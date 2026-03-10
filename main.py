from rag.rag_service import RagSummarizeService


rag = RagSummarizeService()
res = rag.rag_summarize("How does the robot work")

print(res)