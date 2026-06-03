# krkn-doc-sync-poc

An experimental proof-of-concept demonstrating an automated, LLM-powered documentation synchronization bot for the **krkn-chaos** ecosystem. This project specifically addresses the challenge of **documentation drift** by leveraging a multi-agent validation workflow to ensure generated Hugo/Docsy documentation aligns 100% with upstream repository changes before opening a Pull Request.

## 🚀 The Core Problem & Solution

In fast-moving, multi-repository environments like `krkn-chaos`, manual documentation updates often fall behind code changes (e.g., config updates, flag changes, or new scenarios). 

While deploying LLMs to parse code diffs and write documentation tables is efficient, probabilistic models are prone to hallucinating fields or misinterpreting default values. This repository proves that a **Generator-Validator Agent Loop** can catch and correct these drift errors autonomously before human review.

### Architecture Workflow


```
[Upstream Git Diff / Schema Change]
                        │
                        ▼
              ┌───────────────────┐
              │  Generator Agent  │◄─────────────────┐
              └─────────┬─────────┘                  │
                        │                            │
                (Drafts MD Table)             (Feedback Loop
                        │                      if Flagged)
                        ▼                            │
              ┌───────────────────┐                  │
              │  Validator Agent  ├──────────────────┘
              └─────────┬─────────┘
                        │
            (Checks against Raw Diff)
                        │
                    (PASSED)
                        ▼
         [Zero-Drift Draft PR Created]

```

1. **Generator Agent:** Reads the upstream git diff context and generates Hugo-compatible Markdown tables following strict formatting guidelines.
2. **Validator Agent (The Guardrail):** Cross-references the generated Markdown against the raw source code schema. If it catches discrepancies (wrong defaults, mismatched types, or hallucinations), it provides critical feedback and routes it back to the Generator.

---

## 🛠️ Prerequisites

To run this PoC locally, you will need:

* **Python 3.8+**
* **Ollama** installed and running on your local machine.
* A lightweight local LLM downloaded via Ollama (optimized for ~3B models like `llama3.2` or `phi3`).

---

## 📦 Installation

1. Clone this repository:
```bash
   git clone [https://github.com/YOUR_GITHUB_USERNAME/krkn-doc-sync-poc.git](https://github.com/YOUR_GITHUB_USERNAME/krkn-doc-sync-poc.git)
   cd krkn-doc-sync-poc
```

2. Install the required dependencies:

```bash
   pip install langchain-core langchain-ollama
```

3. Pull your local model of choice (e.g., Llama 3.2 3B):

```bash
   ollama run llama3.2
```

---

## 💻 Running the PoC

Ensure the model name in `doc_sync_agent.py` matches your downloaded Ollama model, then execute the script:

```bash
python doc_sync_agent.py
```

### Expected Output Behavior

During execution, you should see the multi-agent validation loop actively self-correcting:

* **Iteration 1:** The Generator compiles the raw diff context but may introduce formatting nuances or minor data-type discrepancies. The Validator reviews it line-by-line, identifies the specific drift points, and flags the errors.
* **Iteration 2:** The Generator reviews the Validator's critique, updates the markdown table to align precisely with the raw git diff parameters, and receives a `PASSED` verification status.
