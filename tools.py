from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import Tool
from langchain_core.tools import ToolException
from datetime import datetime

def save_to_txt(data: str, filename: str = "research_output.txt"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_text = f"-- Research Output --\nTimestamp: {timestamp}\n\n{data}\n"
    with open(filename, "a", encoding="utf-8") as f:
        f.write(formatted_text)
    return f"Data successfully saved to {filename}"

save_tool = Tool(
    name="save_text_to_file",
    func=save_to_txt,
    description="Save structured research data to a text file",
)

search = DuckDuckGoSearchRun()
search_tool = Tool(
    name="Search",
    func=search.run,
    description="Search the web for information",
)

# Better Wikipedia tool wrapper
api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=1000)

def safe_wiki_search(query):
    try:
        return api_wrapper.run(query)
    except Exception as e:
        raise ToolException(f"Wiki tool failed: {str(e)}")

wiki_tools = Tool(
    name="Wikipedia",
    func=safe_wiki_search,
    description="Look up general knowledge using Wikipedia"
)