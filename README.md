
# Create a Lanchain Agent with MCP tools 
A Langchainagent has been created in Agents/MCPAgent.ipynb file 

Through your AI agent, integrated with MCP tools, you can: 

- Control you file System
- Get real-time weather 
- Get current news 


### How to run 

uv run MCPAgent.py .py (for .py file)

run all cells in jupyter notebook (for .ipynb file)


# Repo and Dependencies Installations commands 

- Instal [nodeJS](https://nodejs.org/en/download) 
- Issue: uv add langchain-mcp-adapters

#Checking for Node and npx (in the terminal): 
node -v 
npx -v

Resource Links:
- [Complete youtube playlist](https://www.youtube.com/playlist?list=PLfpB0rPkNb_8)
- [MCP:](https://modelcontextprotocol.io/docs/2026-07-28/getting-started/intro)
- [Official MCP Registry:](https://registry.modelcontextprotocol.io/)
- [MCP github:](https://github.com/modelcontextprotocol)
- [RAG](https://docs.langchain.com/oss/python/deepagents/rag)
- [Langgraph workflows](https://docs.langchain.com/oss/python/langgraph/workflows-agents)
- [arxivLoader](https://reference.langchain.com/python/langchain-community/document_loaders/arxiv/ArxivLoader)
- [arxivAPI](https://info.arxiv.org/help/api/basics.html)
- [Langgraph memory](https://docs.langchain.com/oss/python/langgraph/add-memory#manage-checkpoints)
- [Langgraph docs](https://docs.langchain.com/oss/python/langgraph/overview)
- [Langchain's Pre-build Middlware](https://docs.langchain.com/oss/python/langchain/middleware/built-in)
- [Langchain's middleware](https://docs.langchain.com/oss/python/langchain/middleware/overview)
- [Langgraph's short-term memory](https://docs.langchain.com/oss/python/langchain/short-term-memory) 
- [Langchain Agent](https://docs.langchain.com/oss/python/langchain/agents)
- [DuckDuckGoSearch](https://reference.langchain.com/python/langchain-community/tools/ddg_search/tool/DuckDuckGoSearchRun)
- [Youdotcom API Key](https://you.com/platform/api-keys) 
- [OpenWeatherMap](https://openweathermap.org/)
- [UV github repo](https://github.com/astral-sh/uv)
- [langchain docs]()
- [Groq API Key](https://console.groq.com/keys)
- [OpenAI API Key](https://platform.openai.com/api-keys)

## Install uv On macOS and Linux.
curl -LsSf https://astral.sh/uv/install.sh | sh

## Install uv On Windows.
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# for a fresh repo
### create a project directory and issue the following commands in the project directory:

uv init

uv venv  

source .venv/bin/activate (#activate .venv)

### then install all the dependecies

uv add *packagename*

Examples: 

uv add langchain

uv add langchain-openai 

uv add langchain-groq 

uv add ipykernel

uv add python-dotenv

#### or if you have listed all the required packages in the requirements.txt, issue: 

uv add -r requirements.txt


# Installations for a cloned repo

git clone https://github.com/NawazAli20/LLMsIntro

if you have .toml and/or .lock file just issue

uv sync 
