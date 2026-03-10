import os
import hashlib
from utils.logger_handler import logger
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader, TextLoader

def get_file_md5_hex(filepath: str):
    if not os.path.exists(filepath):
        logger.error(f"[FileHandler] File does not exist: {filepath}")
        return
    if not os.path.isfile(filepath):
        logger.error(f"[FileHandler] Path is not a file: {filepath}")
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
        logger.error(f"[FileHandler] Failed to compute MD5 for {filepath}: {str(e)}")
        return None
        

def listdir_with_allowed_type(folderpath : str, allowed_types: tuple[str, ...]):
    files = []

    if not allowed_types:
        return files
    if not os.path.isdir(folderpath):
        logger.error(f"[FileHandler] Not a directory or missing: {folderpath}")
        return files

    for f in os.listdir(folderpath):
        if f.endswith(allowed_types):
            files.append(os.path.join(folderpath,f))
     
    return files


def pdf_loader(filepath: str, password: str | None = None) -> list[Document]:
    """Load a PDF file. Password is optional.

    Note: "password : None" is only a type annotation and does not set a default.
    The correct way to make it optional is "password: str | None = None".
    """
    try:
        if password is None:
            loader = PyPDFLoader(filepath)
        else:
            try:
                loader = PyPDFLoader(filepath, password)
            except TypeError:
                loader = PyPDFLoader(filepath, password=password)
        return loader.load()
    except Exception as e:
        logger.error(f"[FileHandler] PDF load failed for {filepath}: {e}", exc_info=True)
        raise


def txt_loader(filepath: str) -> list[Document]:
    return TextLoader(filepath, encoding="utf-8").load()

