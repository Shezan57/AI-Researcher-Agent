# AI-Researcher-Agent
# AI Researcher Agent

An AI-powered research assistant that searches arXiv for scientific papers, reads and analyzes them, proposes new research directions, and writes full research papers rendered as LaTeX PDFs — all through a conversational chat interface.

---

## Features

- **arXiv search** — finds the most recently published papers on any topic via the arXiv API.
- **PDF reading** — downloads and extracts text from any PDF by URL.
- **LaTeX PDF generation** — compiles AI-written research papers to PDF using a locally installed LaTeX engine (pdflatex / xelatex).
- **Conversational workflow** — guides you from choosing a topic, through reading and comparing papers, to generating a complete new paper.
- **Persistent memory** — the custom LangGraph agent remembers the full conversation across turns within a session.
- **Streamlit UI** — a clean browser-based chat interface with real-time streaming responses and a PDF download button.

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Streamlit Frontend                    │
│                      front_end.py                        │
└──────────────────────────┬──────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────┐
│            LangGraph Agent  (ai_researcher2.py)          │
│   StateGraph  ──►  call_model  ──►  ToolNode             │
│   MemorySaver checkpointer (in-memory conversation)      │
└───────┬───────────────────────┬────────────────────────-─┘
        │                       │
┌───────▼───────┐   ┌───────────▼──────────┐   ┌──────────────────────┐
│  arxiv_tool   │   │     read_pdf.py       │   │    write_pdf.py       │
│  arxiv_search │   │  read_pdf (URL→text)  │   │  render_latex_pdf    │
│  (arXiv API)  │   │  (PyPDF2 + requests)  │   │  (pdflatex/xelatex)  │
└───────────────┘   └───────────────────────┘   └──────────────────────┘
```

### Key files

| File | Purpose |
|---|---|
| `front_end.py` | Streamlit chat UI; streams agent responses and offers PDF download |
| `ai_researcher2.py` | Custom LangGraph `StateGraph` agent with `MemorySaver` (recommended) |
| `ai_researcher.py` | Simpler LangGraph `create_react_agent` version (CLI only) |
| `arxiv_tool.py` | `arxiv_search` LangChain tool — queries the arXiv Atom API and returns paper metadata |
| `read_pdf.py` | `read_pdf` LangChain tool — fetches and extracts text from a PDF URL |
| `write_pdf.py` | `render_latex_pdf` LangChain tool — compiles a LaTeX string to a PDF file |
| `initial_prompt.py` | System prompt that defines the agent's expert researcher persona |

---

## Requirements

- Python 3.10+
- An **OpenAI API key** (GPT-4o is used by default)
- A LaTeX distribution with `pdflatex` or `xelatex` on your `PATH`
  - **Linux/macOS:** `sudo apt install texlive-latex-base` or `brew install --cask mactex`
  - **Windows:** [MiKTeX](https://miktex.org/) or [TeX Live](https://tug.org/texlive/)

---

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/Shezan57/AI-Researcher-Agent.git
   cd AI-Researcher-Agent
   ```

2. **Create and activate a virtual environment**

   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Windows: .venv\Scripts\activate
   ```

3. **Install Python dependencies**

   ```bash
   pip install langchain-openai langgraph streamlit PyPDF2 requests python-dotenv
   ```

4. **Set your OpenAI API key**

   Create a `.env` file in the project root:

   ```env
   OPENAI_API_KEY=sk-...
   ```

---

## Usage

### Streamlit web UI (recommended)

```bash
streamlit run front_end.py
```

Open the URL shown in your terminal (usually `http://localhost:8501`).  
Type a research topic in the chat box and follow the agent's prompts.  
When the agent finishes writing the paper, a **Download PDF** button will appear.

### CLI (terminal)

```bash
python ai_researcher.py
```

Type your research topic at the `User:` prompt and interact with the agent in a loop.

---

## Conversation workflow

The agent follows a structured research process guided by its system prompt:

1. **Topic discovery** — the agent asks what field or topic you want to explore.
2. **Paper search** — it queries arXiv and presents a list of recent papers with summaries.
3. **Deep read** — once you pick a paper, the agent downloads and reads it in full.
4. **Idea generation** — the agent identifies future research directions from the paper.
5. **Paper writing** — after you choose an idea, the agent writes a complete research paper with mathematical equations and references.
6. **PDF export** — the paper is compiled to a LaTeX PDF and made available for download.

---

## Project roadmap

The project is planned to evolve into a two-tier SaaS product:

| Tier | LLM provider | Features |
|---|---|---|
| **Free** | GroqCloud (open-weight model) | Basic search, summarization, limited daily quota |
| **Paid** | OpenAI GPT-5 / GPT-5.1 | Long context, multi-paper synthesis, deeper reasoning, priority limits |

---

## License

This project is licensed under the terms of the [LICENSE](LICENSE) file included in this repository.
