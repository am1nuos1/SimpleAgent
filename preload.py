import sys
import os
from rag.vector_store import VectorStoreService
from utils.logger_handler import logger
from utils.config_handler import chroma_conf
from utils.path_tool import get_abs_path


def main() -> int:
    data_dir = get_abs_path(chroma_conf.get("data_path", "data"))
    persist_dir = get_abs_path(os.path.join("rag", chroma_conf.get("persist_directory", "chorma_db")))

    logger.info(f"[Preload] Data directory: {data_dir}")
    logger.info(f"[Preload] Chroma persist dir: {persist_dir}")

    if not os.path.exists(data_dir):
        logger.warning(f"[Preload] Data directory does not exist: {data_dir}")

    try:
        vs = VectorStoreService()
        vs.load_document()
        logger.info("[Preload] Completed. If this was the first run, restart the app if needed.")
        return 0
    except Exception as e:
        logger.error(f"[Preload] Failed: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
