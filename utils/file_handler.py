import os
import hashlib
from logger_handler import logger
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader, TextLoader

def get_file_hex5_hex(filepath: str):
    if not os.path.exists(filepath):
        logger.error(f"[MD5hex]{filepath} do not exists")
        return
    if not os.path.isfile(filepath):
        logger.error(f"[MD5hex]{filepath} is not a file")
        return
    md5_obj = hashlib.md5()
    chunk_size = 4096
    try:
        with open(filepath, "rb") as f:
            while chunk := f.read(chunk_size):
                md5_obj.update(chunk)
            md5_hex = md5_obj.hexdigest()
            return md5_hex
    except Exception as e:
        logger.error(f"failed when calculating {filepath}, error: {str(e)}")
        return None
        

def listdir_with_allowed_type(folderpath : str, allowed_types: tuple[str]):
    files = []

    if not allowed_types:
        return files
    if not os.path.isdir(folderpath):
        logger.error(f"{folderpath} is not a folder")
        return allowed_types

    for f in os.listdir(folderpath):
        if f.endswith(allowed_types):
            files.append(f)
    
    return tuple(files)


def pdf_loader(filepath: str, password : None) -> list[Document]:
    return PyPDFLoader(filepath, password).load()


def txt_loader(filepath: str) -> list[Document]:
    return TextLoader(filepath).load()