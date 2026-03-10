from langchain_core.tools import tool
from rag.rag_service import RagSummarizeService
from utils.config_handler import agent_conf
from utils.path_tool import get_abs_path
from utils.logger_handler import logger
import os





rag = RagSummarizeService()


external_data = {}


@tool(description = "Search for reference materials from the vector repository")
def rag_summarize(query: str)-> str:
    return rag.rag_summarize(query)


@tool(description="Get the weather for the specified city, returned as a message string")
def get_weather(city: str):
    return f"The weather in {city} is sunny, temperature 26°C, humidity 50%, light south wind, AQI 21, very low precipitation probability in the last six hours"


@tool(description="Get the user's city")
def get_user_location() -> str:
    return "Seattle"


@tool(description="Get the user's ID, as a pure string")
def get_user_id() -> str:
    return "1001"


@tool(description="Get the current month, returned as a pure string")
def get_current_month() -> str:
    return "Sep"



def generate_external_data():
    if not external_data:
        external_data_path = get_abs_path(agent_conf["external_data_path"])

        if not os.path.exists(external_data_path):
            raise FileNotFoundError(f"External data file {external_data_path} does not exist")

        with open(external_data_path, "r", encoding="utf-8") as f:
            for line in f.readlines()[1:]:
                arr: list[str] = line.strip().split(",")

                user_id: str = arr[0].replace('"', "")
                feature: str = arr[1].replace('"', "")
                efficiency: str = arr[2].replace('"', "")
                consumables: str = arr[3].replace('"', "")
                comparison: str = arr[4].replace('"', "")
                time: str = arr[5].replace('"', "")

                if user_id not in external_data:
                    external_data[user_id] = {}

                external_data[user_id][time] = {
                    "Feature": feature,
                    "Efficiency": efficiency,
                    "Consumables": consumables,
                    "Comparison": comparison,
                }


@tool(description="Retrieve the usage records of the specified user in the specified month from the external system, returned as a pure string, return empty string if not found")
def fetch_external_data(user_id: str, month: str) -> str:
    generate_external_data()

    try:
        return external_data[user_id][month]
    except KeyError:
        logger.warning(f"[fetch_external_data] Failed to retrieve usage record data for user: {user_id} in {month}")
        return ""
    


@tool(description="No parameters, no return value. When called, triggers middleware to automatically inject context information for the report generation scenario, providing context information for subsequent prompt switching")
def fill_context_for_report():
    return "fill_context_for_report has been called"
    
