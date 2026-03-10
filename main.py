from rag.rag_service import RagSummarizeService


rag = RagSummarizeService()
res = rag.rag_summarize("机器人如何工作")

print(res)