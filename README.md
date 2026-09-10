
# Course Assistant MCP Server

Build your first custom Model Context Protocol (MCP) server with Python and FastMCP. This YouTube class shows how to expose two Python functions as MCP tools, read a local course catalog, and test the tools in MCP Inspector.

| Tool | Purpose |
| --- | --- |
| `get_course_list()` | Return the ID and title of each available course. |
| `get_course_details(course_id)` | Return the complete record for a matching course, or an error message with available IDs. |

This class covers **tools only**, using **stdio** transport. Resources and prompts will be covered in the next class.

## Project structure

```text
course-assistant-mcp/
├── README.md
├── mcpserver.py
├── data/
│   └── courses.json
├── pyproject.toml       # Created by uv init
└── uv.lock             # Created by uv add; commit this for repeatable installs
```

`data/courses.json` is supplied in this GitHub repository. Use the supplied file; there is no separate dataset download. It contains a JSON array of course objects, each with at least `course_id` and `title`. Additional fields are returned by the details tool unchanged.

## Prerequisites

- Python 3.10 or newer; the setup below uses Python 3.12.
- `uv` to manage Python and project dependencies.
- A current Node.js LTS installation, including `npm` and `npx`, to launch MCP Inspector. Download it from [Node.js](https://nodejs.org/en/download).
- Git if you want to clone the repository; GitHub's **Code → Download ZIP** also works.
- A terminal and a code editor.

No API key, paid service, or LLM client is needed to test these tools in Inspector.

## 1. Install uv

Use the command for your operating system from the [official uv installation guide](https://docs.astral.sh/uv/getting-started/installation/).

**macOS / Linux:**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows PowerShell:**

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Open a new terminal after installation, then check:

```bash
uv --version
node --version
npm --version
npx --version
```

## 2. Set up the project and install MCP

Download or clone this repository using the URL in its GitHub **Code** menu. Open a terminal in the downloaded repository folder. Run all remaining commands from that folder.

Install Python if needed:

```bash
uv python install 3.12
```

### First-time setup for the class

If the folder does not yet contain `pyproject.toml`, initialize it:

```bash
uv init --bare --python 3.12
```

Install the MCP SDK **with its CLI extra**:

```bash
uv add "mcp[cli]>=1.28,<2"
```

This installs the SDK, the `mcp` command, and their dependencies into the project's `.venv`. It also records the dependency in `pyproject.toml` and creates or updates `uv.lock`. `uv run` uses this environment automatically, so manual activation is unnecessary.

This class intentionally uses the **v1 SDK** because the sample imports `FastMCP` from `mcp.server.fastmcp`. The `<2` constraint preserves that API. See the [official v1 SDK documentation](https://github.com/modelcontextprotocol/python-sdk/tree/v1.x).

`pathlib`, `json`, and `typing` are Python standard-library modules: no installation is needed. The separate `fastmcp` package is not required for this import.

### If the repository already includes pyproject.toml and uv.lock

Use the committed dependencies instead of initializing the project again:

```bash
uv sync --locked
```


How it works

- `FastMCP` creates the server; `@mcp.tool()` exposes each decorated function as a tool.
- Type hints describe the tool inputs and outputs; docstrings describe each tool.
- `_load_courses()` reads the local JSON file using UTF-8. The two underscore-prefixed helper functions are not registered as tools.
- `_normalize_course_id()` converts IDs to uppercase and removes whitespace, so `CS111`, `cs111`, and `CS 111` match.
- `mcp.run(transport="stdio")` exchanges MCP messages through standard input and output.

## 4. Run the server locally

```bash
uv run python mcpserver.py
```

The server waits for an MCP client to send protocol messages. A quiet terminal is normal: this command does not open a browser or create an HTTP endpoint. Press **Ctrl+C** to stop it before continuing.

Avoid adding `print()` calls to standard output: stdout carries MCP messages. Use logging to stderr if you need debugging output.

## 5. Launch MCP Inspector

From the repository folder, run:

```bash
uv run mcp dev mcpserver.py
```

The MCP development command launches Inspector using `npx`. Allow the Inspector package installation if prompted, and open the local URL printed in the terminal. Keep that terminal running while testing.

Inspector launches its own server process; you do not need to leave the server from step 4 running.

You can also launch Inspector explicitly:

```bash
npx -y @modelcontextprotocol/inspector uv run python mcpserver.py
```

Use either launch command. If Inspector asks for connection settings, use:

| Setting | Value |
| --- | --- |
| Transport | `STDIO` |
| Command | `uv` |
| Arguments | `run python mcpserver.py` |

Click **Connect** if it is not already connected. If you opened Inspector outside the repository folder, use absolute paths for the project and script, or relaunch from the repository folder. See the [official Inspector documentation](https://github.com/modelcontextprotocol/inspector) for launch details.

## 6. Test the tools in Inspector

Button labels may vary slightly by Inspector version.

### List available courses

1. Open **Tools** and click **List Tools** or refresh the tool list.
2. Confirm that `get_course_list` and `get_course_details` appear.
3. Select `get_course_list`.
4. Leave the arguments empty (`{}` if using a JSON input editor).
5. Click **Run Tool**.

Expected behavior: a list containing `Course_id` and `Title` for every record in the supplied file. For example, if the file contains CS111:

```json
[
  {
    "Course_id": "CS111",
    "Title": "AI for All"
  }
]
```

This is illustrative; the actual list depends on the repository's dataset. Inspector may display the result inside MCP content or structured-output fields.

### Get course details

1. Select `get_course_details`.
2. Enter an ID returned by the list tool in the required `course_id` field.
3. Click **Run Tool**.

For example, if CS111 is in the list, the JSON arguments are:

```json
{"course_id": "CS111"}
```

Expected behavior: the entire matching JSON object, including `course_id`, `title`, and every additional field stored for that course.

Repeat with `cs111` and `CS 111`. Both should return the same record as `CS111`.

### Try an unavailable course

Enter an ID that does not occur in the dataset, for example:

```json
{"course_id": "UNKNOWN999"}
```

Expected behavior: a normal tool response containing an `Error` message and an `Available_courses` list. For a catalog containing only CS111, it would be:

```json
{
  "Error": "UNKNOWN999 is not available",
  "Available_courses": ["CS111"]
}
```

The available IDs come from the supplied file. This not-found response is a returned dictionary, not a raised MCP execution error.

## Troubleshooting

| Problem | What to check |
| --- | --- |
| `uv` or `npx` is not found | Reopen the terminal after installing uv or Node.js and check the version commands. |
| MCP command or import is missing | Run `uv add "mcp[cli]>=1.28,<2"` in the project folder, then launch with `uv run`. |
| Server appears idle when run directly | This is expected with stdio. Launch Inspector to call the tools. |
| Inspector cannot connect | Select STDIO, check the command and arguments, and launch from the repository folder. |
| A tool fails while reading course data | Confirm that `data/courses.json` exists, is valid UTF-8 JSON, and contains an array of objects with `course_id` and `title`.




# Repo and Dependencies Installations commands 
- uv add deepagents 
- Instal [nodeJS](https://nodejs.org/en/download) 
- Issue: uv add langchain-mcp-adapters
- download github-mcp-server: https://github.com/github/github-mcp-server/releases?utm_source=chatgpt.com
- [How to generate github personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)

#Checking for Node and npx (in the terminal): 
node -v 
npx -v

MongoDB Installations: https://www.mongodb.com/docs/manual/administration/install-community/?operating-system=macos&macos-installation-method=homebrew

MongoDB CRUD operations syntax: https://www.mongodb.com/docs/manual/crud/?msockid=050612d8208b6ac13bc3054421d26b1d
MogoDB MCP: 

MCP Documentations: https://www.mongodb.com/docs/mcp-server/get-started/?msockid=050612d8208b6ac13bc3054421d26b1d

Resource Links:
- [Complete youtube playlist](https://www.youtube.com/playlist?list=PLfpB0rPkNb_8)
- [DeepAgent](https://docs.langchain.com/oss/python/deepagents/quickstart)
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
