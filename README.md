# AI-Researcher-Agent

## Overview

AI-Researcher-Agent is an autonomous research assistant designed to streamline academic literature discovery, extraction, synthesis, and reporting. It automates the process of gathering scholarly papers, extracting insights, synthesizing literature, and generating structured reports or experiment ideas, significantly accelerating the research workflow for scientists, engineers, and students.

Key benefits:
- Automated literature search and triage (papers, patents, blogs)
- PDF parsing, citation extraction, and multi-level summarization
- Knowledge base construction (vector store, graph, markdown notes)
- Structured report and data artifact generation
- Modular, extensible architecture (add tools, swap LLMs, support new APIs)

---

## Key Features

| Area               | Description                                                                  |
|--------------------|------------------------------------------------------------------------------|
| Autonomous Loop    | Iterative task planning, execution, and reflection cycle                      |
| Web/Paper Retrieval| Integrates with arXiv, Semantic Scholar, PubMed, CrossRef APIs                |
| Document Parsing   | PDF to text, section segmentation, citation extraction                        |
| Summarization      | Hierarchical, query-focused, multi-document summarization                     |
| Knowledge Base     | Vector store (FAISS/Chroma), markdown notes, simple graph storage             |
| Report Generation  | Structured markdown/JSON outputs, comparative tables, synthesis               |
| Configurability    | Pluggable model providers, rate limiting, caching, file system organization   |
| Tooling            | Browsing, code/data extraction, CLI and HTTP interfaces                       |
| Persistence        | Outputs stored locally as markdown, JSON, and vector cache                    |

---

## Architecture

```
+---------------------------+
| Entry Point (CLI / API)   |
+-------------+-------------+
              |
              v
+---------------------------+
| Orchestrator / Agent Core |
+-------------+-------------+
              |
   +----------+-----------+
   |                      |
   v                      v
Task Planner        Tool Executor
   |                      |
   v                      v
Memory / KB <----> Retrieval Layer <----> External Sources
   |
   v
Report / Artifact Generator
```

### Main Modules

| Module         | Path                     | Purpose                                   |
|----------------|--------------------------|-------------------------------------------|
| Orchestrator   | `ai_researcher/agent.py` | Task loop, planning, reflection           |
| Tools          | `ai_researcher/tools/`   | Web, PDF, search, parsing                 |
| Models         | `ai_researcher/models/`  | LLM abstraction (OpenAI, Claude, local)   |
| Memory         | `ai_researcher/memory/`  | Vector store, cache                       |
| Parsers        | `ai_researcher/parsers/` | PDF/HTML/metadata extraction              |
| Summarizers    | `ai_researcher/summarization/` | Multi-pass summarization           |
| Reporters      | `ai_researcher/reporting/`| Markdown/JSON exporters                  |
| Config         | `ai_researcher/config/`  | Environment and runtime configuration     |
| Interfaces     | `scripts/`, CLI          | CLI/HTTP adapters                         |
| Utilities      | `ai_researcher/utils/`   | Logging, rate limiting, retries           |

---

## Technology Stack

- **Language:** Python 3.11+
- **Frameworks:** Typer (CLI), LangChain, FastAPI (if HTTP interface used)
- **Models:** OpenAI GPT-4o, Claude, local Llama/other LLMs
- **Embeddings:** OpenAI text-embedding-3-large, Sentence-Transformers
- **Storage:**
  - Vector: FAISS, Chroma, Milvus, LanceDB
  - Cache: SQLite, Redis, or local JSON
  - Artifacts: Markdown (`/notes`), JSON (`/outputs`)
- **PDF Handling:** pymupdf, pdfminer.six, unstructured
- **Search APIs:** SerpAPI, arXiv API, Semantic Scholar API

---

## Installation

### Prerequisites

- Python 3.11+
- [Poetry](https://python-poetry.org/) or pip for dependency management

### Clone

```bash
git clone https://github.com/Shezan57/AI-Researcher-Agent.git
cd AI-Researcher-Agent
```

### Environment Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# OR
poetry install
```

### Configuration

- Copy `.env.example` to `.env` and fill in required API keys (OpenAI, arXiv, etc.)
- Adjust settings in `ai_researcher/config/` as needed

---

## Quick Start

```bash
python ai_researcher/agent.py --topic "Your Research Topic"
```

Or use CLI entry point if provided.

---

## Workflow Stages

1. **Topic Initialization:** Normalize and expand research queries.
2. **Retrieval:** Search external sources (papers, blogs, etc.) using relevance and recency.
3. **Parsing & Chunking:** Segment PDFs, extract sections, chunk to fit token limits.
4. **Embedding & Indexing:** Convert text to vectors for semantic search and deduplication.
5. **Summarization:** Multi-pass summarization (chunk, document, cross-doc).
6. **Knowledge Graph:** (Optional) Extract concepts, methods, datasets, and relationships.
7. **Report Generation:** Create structured outputs (executive summary, tables, references).

---

## Configuration Reference

| Setting            | Description                 | Default         |
|--------------------|----------------------------|-----------------|
| `max_sources`      | Max docs to retrieve        | 25              |
| `retrieval_depth`  | Expansion depth             | 2               |
| `chunk_tokens`     | Token size per chunk        | 1024            |
| `overlap_tokens`   | Token overlap per chunk     | 100             |
| `llm_model`        | Main LLM for reasoning      | openai/gpt-4o   |
| `embedding_model`  | Embedding provider          | openai/text-embedding-3-large |
| `rate_limit_per_min`| API throttling             | 60              |
| `cache_enabled`    | Use cached retrieval        | true            |
| `graph_enabled`    | Build concept graph         | false           |

---

## File / Directory Layout

```
.
├─ ai_researcher/
│  ├─ __init__.py
│  ├─ agent.py
│  ├─ planner.py
│  ├─ tools/
│  │  ├─ web_search.py
│  │  ├─ pdf_loader.py
│  │  └─ ...
│  ├─ retrieval/
│  ├─ summarization/
│  ├─ memory/
│  ├─ reporting/
│  └─ config/
├─ scripts/
├─ tests/
├─ data/
│  ├─ cache/
│  └─ vectors/
├─ outputs/
├─ requirements.txt / pyproject.toml
├─ .env.example
└─ README.md
```

---

## Logging & Monitoring

- Uses built-in Python logging
- Levels: DEBUG, INFO, WARN, ERROR
- Example log output:
  ```
  [INFO] Retrieval seeded: 5 queries
  [INFO] Downloaded 18 / 25 papers
  [DEBUG] Chunked: paper_012 (42 chunks)
  [INFO] Summarization pass 2 complete (9 docs)
  ```

---

## Error Handling

| Scenario         | Strategy                                 |
|------------------|------------------------------------------|
| Rate limit       | Exponential backoff                      |
| Missing PDF      | Skip and log warning                     |
| Parse failure    | Retain metadata, mark content unavailable|
| LLM timeout      | Retry up to 3 times                      |
| Incomplete sources| Fallback to next-best search provider   |

---

## Performance Considerations

- Supports parallel/async retrieval and summarization.
- Multi-layer caching (raw HTML, parsed text, embeddings, summaries).
- Token cost is optimized via hierarchical summarization and chunk reuse.
- Deduplication via fuzzy title matching.

---

## Security & Privacy

- API keys/secrets loaded only from environment variables.
- Option for local-only mode (no external LLM calls).
- Potential for PII scrubbing (if implemented).
- Network call restrictions can be enforced (sandboxing).

---

## Testing

| Test Type     | Location            | Notes                      |
|---------------|---------------------|----------------------------|
| Unit          | `tests/unit`        | Mock external APIs         |
| Integration   | `tests/integration` | Live retrieval (tagged)    |
| Regression    | `tests/regression`  | Snapshot outputs           |
| Performance   | `tests/perf`        | Token & time profiling     |

Run all tests:

```bash
pytest -q
```

Generate coverage report:

```bash
pytest --cov=ai_researcher --cov-report=term-missing
```

---

## Extending the System

### Add a New Retrieval Source
- Implement interface `BaseRetriever`
- Register in `retrieval_registry`
- Add config toggle
- Write tests

### Add a Tool
- Create class in `tools/`
- Define `run()` method
- Register in tool manifest

### Swap LLM Provider
- Implement adapter for `LLMClient` protocol
- Register in model factory

---

## Output Formats

| Format           | Description                      |
|------------------|----------------------------------|
| Markdown Report  | Human-readable synthesis         |
| JSON Structured  | Machine-consumable metadata      |
| GraphML/CSV      | Concept relationships, metrics   |

Sample JSON Output:
```json
{
  "topic": "LLM Prompt Engineering",
  "generated_at": "2025-09-12T00:00:00Z",
  "documents": [
    {"id": "arxiv:1234.5678", "title": "Prompt Engineering for LLMs", "year": 2024, "summary": "Overview of prompt engineering strategies.", "citations": 123}
  ],
  "themes": [
    {"name": "Few-shot Learning", "supporting_docs": ["arxiv:1234.5678"], "insights": ["Better performance with in-context examples"]}
  ],
  "open_questions": ["How to automate prompt optimization?"]
}
```

---

## Roadmap

- [ ] Multi-agent decomposition
- [ ] Local-only mode
- [ ] UI dashboard
- [ ] Citation graph visualization
- [ ] Evaluation harness (ROUGE/factual consistency)
- [ ] Plugin architecture for new domains

---

## FAQ

**Q:** Does it store API keys in code?  
**A:** No, all secrets are loaded from environment variables.

**Q:** Can it run fully offline?  
**A:** Yes, in local-only mode (with local models and no external API calls).

**Q:** How are duplicates avoided?  
**A:** Fuzzy title/content matching and deduplication heuristics.

---

## Troubleshooting

| Issue            | Possible Cause           | Fix                                  |
|------------------|-------------------------|--------------------------------------|
| Empty summaries  | Invalid LLM key         | Check/reconfigure environment        |
| Few papers found | Narrow search query     | Use broader/expanded topic           |
| High token cost  | Large chunk size        | Tune chunk/overlap settings          |
| Slow retrieval   | Serial requests         | Enable parallel mode                 |

---

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feat/new-feature`
3. Run tests and linters before PR: `pytest && ruff check .`
4. Open a PR with a clear description and reasoning

Coding Style:
- Type hints required
- Docstrings for public functions
- Avoid hard-coded model names

---

## License

MIT License. See [LICENSE](LICENSE) for details.

---

## Acknowledgments

- OpenAI, LangChain, pymupdf, FAISS, Chroma, Semantic Scholar, arXiv, and other open-source projects/APIs.

---

*For more details, see the source code and [GitHub repository](https://github.com/Shezan57/AI-Researcher-Agent).*
