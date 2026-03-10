from abc import ABC, abstractmethod
import os
from langchain_core.embeddings import Embeddings
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.chat_models import ChatTongyi
from utils.config_handler import rag_conf



class BaseModelFactory(ABC):
    #return embedding modles/ basemodel
    def __init__(self):
        self.api = rag_conf["dashscope_api_key"]

    def _resolve_api_key(self) -> str | None:
        return self.api or os.getenv("DASHSCOPE_API_KEY")
    @abstractmethod
    def generator(self):
        pass


class ChatModelFactory(BaseModelFactory):
    def generator(self):
        key = self._resolve_api_key()
        model_name = rag_conf["chat_model_name"]
        if key:
            return ChatTongyi(api_key=key, model=model_name)
        return ChatTongyi(model=model_name)
    

class EmbeddingsFactory(BaseModelFactory):
    def generator(self):
        key = self._resolve_api_key()
        model_name = rag_conf["embedding_model_name"]
        if key:
            return DashScopeEmbeddings(dashscope_api_key=key, model=model_name)
        return DashScopeEmbeddings(model=model_name)


chat_model = ChatModelFactory().generator()
embedding_model = EmbeddingsFactory().generator()