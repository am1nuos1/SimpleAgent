from langchain_chroma import Chroma
from utils.config_handler import chroma_conf
from utils.path_tool import get_abs_path
from model.factory import embedding_model
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
from utils.file_handler import txt_loader, pdf_loader, listdir_with_allowed_type, get_file_md5_hex
from utils.logger_handler import logger


class VectorStoreService:
    def __init__(self):
        self.vector_store = Chroma(
            collection_name=chroma_conf["collection_name"],
            embedding_function=embedding_model,
            persist_directory=get_abs_path(os.path.join("rag", chroma_conf["persist_directory"]))
        )

        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size = chroma_conf["chunk_size"],
            chunk_overlap = chroma_conf["chunk_overlap"],
            separators= chroma_conf["separators"],
            length_function = len,
        )


    def get_retriever(self):
        return self.vector_store.as_retriever(search_kwargs = {"k" : chroma_conf["k"]})
    

    def load_document(self):

        def check_md5_hex(md5_for_check : str):
            file_path = get_abs_path(chroma_conf["md5_hex_store"])
            if not os.path.exists(file_path):
                open(file_path, 'w', encoding= "utf-8").close()
                return False

            with open(file_path, 'r', encoding= "utf-8") as f:
                for line in f.readlines():
                    line = line.strip()
                    if line == md5_for_check:
                        return True
                return False
            
        def save_md5_hex(md5_for_check: str):
            file_path = get_abs_path(chroma_conf["md5_hex_store"])
            # Append to preserve history of processed files
            with open(file_path, "a", encoding="utf-8") as f:
                f.write(md5_for_check + "\n")

        def get_file_documets(read_path: str):
            if read_path.endswith("txt"):
                return txt_loader(read_path)
            
            if read_path.endswith("pdf"):
                return pdf_loader(read_path)

        allowed_files_path : list[str] = listdir_with_allowed_type(
            chroma_conf["data_path"], 
            tuple(chroma_conf["allow_knowledge_file_type"]),
        )

        for path in allowed_files_path:
            md5_hex = get_file_md5_hex(path)

            if check_md5_hex(md5_hex):
                logger.info(f"[VectorStore] Skipping already indexed file: {path}")
                continue
            try:
                documents = get_file_documets(path)
                if not documents:
                    logger.warning(f"[VectorStore] No readable content found: {path}")
                    continue

                split_document = self.spliter.split_documents(documents=documents)

                if not split_document:
                    logger.warning(f"[VectorStore] No content after splitting: {path}")
                    continue
                
                self.vector_store.add_documents(split_document)

                save_md5_hex(md5_hex)

                logger.info(f"[VectorStore] Loaded successfully: {path} (chunks={len(split_document)})")
            
            except Exception as e:
                logger.error(f"[VectorStore] Load failed for {path}: {str(e)}", exc_info=True)

                continue


if __name__ == "__main__":
    vs = VectorStoreService()
    vs.load_document()
    ret = vs.get_retriever()
    res = ret.invoke("lost")

    for r in res:
        print(r.page_content)
        print(20*"=")

