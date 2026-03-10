from rag.vector_store import VectorStoreService


vs = VectorStoreService()
vs.load_document()
ret = vs.get_retriever()
res = ret.invoke("lost")

for r in res:
    print(r.page_content)
    print(20*"=")