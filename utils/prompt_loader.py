from utils.config_handler import prompt_conf
from utils.path_tool import get_abs_path
from utils.logger_handler import logger


def load_system_prompts():
    try:
        prompt_path = get_abs_path(prompt_conf["main_prompt_path"])
    except KeyError as e:
        logger.error(f"[load_system_prompts] no key named main_prompt_path in config/prompt_config.yaml, error: {e}")
        raise e

    try:
        return open(prompt_path, "r", encoding="utf-8").read()
    except Exception as e:
        logger.error(f"[load_system_prompts] error occurred when loading main_prompt_path in config/prompt_config.yaml, error: {e}")
        raise e


def load_rag_prompts():
    try:
        prompt_path = get_abs_path(prompt_conf["rag_summarize_prompt_path"])
    except KeyError as e:
        logger.error(f"[load_rag_prompts] no key named rag_summarize_prompt_path in config/prompt_config.yaml, error: {e}")
        raise e

    try:
        return open(prompt_path, "r", encoding="utf-8").read()
    except Exception as e:
        logger.error(f"[load_rag_prompts] error occurred when loading rag_summarize_prompt_path in config/prompt_config.yaml, error: {e}")
        raise e


def load_report_prompts():
    try:
        prompt_path = get_abs_path(prompt_conf["report_prompt_path"])
    except KeyError as e:
        logger.error(f"[load_report_prompts] no key named report_prompt_path in config/prompt_config.yaml, error: {e}")
        raise e

    try:
        return open(prompt_path, "r", encoding="utf-8").read()
    except Exception as e:
        logger.error(f"[load_report_prompts] error occurred when loading report_prompt_path in config/prompt_config.yaml, error: {e}")
        raise e
    

if __name__ == "__main__":
    print(load_report_prompts())