from langchain_core.output_parsers import StrOutputParser
from rag.vector_store import VectorStoreService
from utils.prompt_loader import load_rag_prompts
from langchain_core.prompts import PromptTemplate
from model.factory import chat_model
from typing import List
import asyncio


class RagSummarizeService():
    def __init__(self):
        self.vector_store = VectorStoreService()
        self.retriever = self.vector_store.get_retriever()
        self.prompt_text = load_rag_prompts()
        self.prompt_template = PromptTemplate.from_template(self.prompt_text)
        self.model = chat_model
        self.chain = self._init_chain()


    def _init_chain(self):
        chain = self.prompt_template | self.model | StrOutputParser()
        return chain
    
    def retriever_docs(self, query : str):
        return self.retriever.invoke(query)
    
    async def aretriever_docs(self, query: str):
        """Async version of retriever docs."""
        return await self.retriever.ainvoke(query)

    def rag_summarize(self, query : str):
        context_docs = self.retriever_docs(query)
        context = ""
        counter = 0
        for doc in context_docs:
            counter +=1 
            context += f"[Reference {counter}]: {doc.page_content} | Metadata: {doc.metadata} \n"


        return self.chain.invoke(
            {
                "input" : query,
                "context" : context,
            }
        )

    async def arag_summarize(self, query: str):
        """Async RAG summarize using async retriever and model chain."""
        context_docs = await self.aretriever_docs(query)
        # Build context string (CPU-bound, small); keep synchronous for simplicity
        parts: List[str] = []
        for idx, doc in enumerate(context_docs, start=1):
            parts.append(f"[Reference {idx}]: {doc.page_content} | Metadata: {doc.metadata} \n")
        context = "".join(parts)

        return await self.chain.ainvoke({
            "input": query,
            "context": context,
        })
            
if __name__ == "__main__" :
    rag = RagSummarizeService()
    res = rag.rag_summarize("How does the robot work")

    print(res)