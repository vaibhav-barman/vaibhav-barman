<div align="center">

<a href="https://vaibhav-barman.github.io">
  <img src="./assets/hero.svg" width="100%" alt="Vaibhav Barman. AI Engineer, agentic systems. A rotating 3D network globe over a perspective grid."/>
</a>

<p>
  <a href="https://vaibhav-barman.github.io"><img src="https://img.shields.io/badge/PORTFOLIO-vaibhav--barman.github.io-22d3ee?style=for-the-badge&labelColor=0b1022" alt="Portfolio"/></a>
  <a href="https://www.linkedin.com/in/vaibhavbarman/"><img src="https://img.shields.io/badge/LINKEDIN-vaibhavbarman-a78bfa?style=for-the-badge&labelColor=0b1022" alt="LinkedIn"/></a>
  <a href="mailto:vaibhavbarman2609@gmail.com"><img src="https://img.shields.io/badge/EMAIL-say_hello-f472b6?style=for-the-badge&labelColor=0b1022" alt="Email"/></a>
  <a href="https://vaibhav-barman.github.io/resume.html"><img src="https://img.shields.io/badge/STATUS-open_to_remote_roles-34d399?style=for-the-badge&labelColor=0b1022" alt="Status: open to remote roles"/></a>
</p>

</div>

<img src="./assets/h-whoami.svg" width="100%" alt="01 · whoami"/>

I'm an AI engineer who builds **LLM applications, RAG pipelines and multi-agent systems** in Python, often on local models.

The idea I keep coming back to: **a model shouldn't grade its own homework.** My agents draft, then deterministic checks (exit codes, linters, rule sets, retrieval metrics) decide whether the draft ships or loops back for repair.

```python
@dataclass(frozen=True)
class Vaibhav:
    role      = "AI Engineer"
    builds    = ("agentic systems", "RAG pipelines", "MCP servers", "local-LLM apps")
    orchestr  = ("LangGraph", "LangChain", "FastMCP")
    serves    = ("FastAPI", "PostgreSQL", "Docker", "AWS")
    principle = "deterministic checks over model opinion"
    studying  = "B.Sc. Computer Science @ BITS Pilani"
    status    = "open to remote AI engineering roles"
```

<img src="./assets/h-loop.svg" width="100%" alt="02 · how I build"/>

<img src="./assets/agent-loop.svg" width="100%" alt="Isometric 3D diagram of an agent loop: task, plan, act, observe, critic, ship. Rejected drafts loop from the critic back to the plan step."/>

The same loop shows up across my projects: the **critic loop** in GitCommit AI, the **execute-and-repair loop** in LocalForge-AI, and the **strategy memory** in the payment recovery agent.

<img src="./assets/h-builds.svg" width="100%" alt="03 · featured builds"/>

<table>
  <tr>
    <td width="50%" valign="top">
      <a href="https://github.com/vaibhav-barman/gitcommit-ai"><img src="./assets/poly-commit.svg" width="92" align="left" alt=""/></a>
      <h3><a href="https://github.com/vaibhav-barman/gitcommit-ai">GitCommit AI</a></h3>
      <sub><b>AGENTIC · CLI · <code>git ai-commit</code></b></sub>
      <br clear="left"/>
      <p>Learns how <i>your</i> repository writes commits (convention, style, history), drafts a message in that voice, then a deterministic critic plus an LLM faithfulness check send it back until it passes. Never stages files, and refuses to commit if the staging area changed while it was thinking.</p>
      <p><sub><code>diff + history → analyst → retrieval → generator ⇄ critic → you confirm → commit</code></sub></p>
      <code>LangGraph</code> <code>Python</code> <code>6 LLM providers</code> <code>Ollama</code> <code>eval harness</code> <code>mypy strict</code>
    </td>
    <td width="50%" valign="top">
      <a href="https://github.com/vaibhav-barman/localforge-ai"><img src="./assets/poly-forge.svg" width="92" align="left" alt=""/></a>
      <h3><a href="https://github.com/vaibhav-barman/localforge-ai">LocalForge-AI</a></h3>
      <sub><b>MULTI-AGENT · 100% OFFLINE</b></sub>
      <br clear="left"/>
      <p>A local multi-agent software team: a Product Manager agent writes the spec, a Software Engineer agent writes the code, a sandbox runs and lints it, and a QA agent routes real failures back for repair. Three open-weight models through Ollama, zero network calls at runtime.</p>
      <p><sub><code>task → product manager → engineer ⇄ run + lint → QA analyzer → package</code></sub></p>
      <code>LangGraph</code> <code>Ollama</code> <code>Python</code> <code>pytest</code> <code>local LLMs</code>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <a href="https://github.com/vaibhav-barman/agentic-rag"><img src="./assets/poly-glossa.svg" width="92" align="left" alt=""/></a>
      <h3><a href="https://github.com/vaibhav-barman/agentic-rag">Glossa</a></h3>
      <sub><b>AGENTIC RAG · NO FRAMEWORK</b></sub>
      <br clear="left"/>
      <p>Ask questions about your own documents and read each answer next to the passages it came from. Built from raw parts: hybrid keyword + vector search with reranking, incremental ingestion, and an agent that can also query the library with SQL, hand a whole document to a sub-agent, or fall back to the web. Every tool call is shown as a step.</p>
      <p><sub><code>upload → chunk + embed → hybrid search + rerank → agent tools → cited answer</code></sub></p>
      <code>FastAPI</code> <code>Postgres + pgvector</code> <code>Gemini</code> <code>Row-Level Security</code> <code>SSE</code>
    </td>
    <td width="50%" valign="top">
      <a href="https://github.com/vaibhav-barman/recovery-agent"><img src="./assets/poly-recovery.svg" width="92" align="left" alt=""/></a>
      <h3><a href="https://github.com/vaibhav-barman/recovery-agent">Recovery</a></h3>
      <sub><b>AI AGENT · RAZORPAY AI BUILDATHON</b></sub>
      <br clear="left"/>
      <p>A payment recovery agent. It classifies why a payment failed, picks a strategy (retry, delayed retry, UPI nudge, email nudge, escalate), simulates the outcome, and feeds its own past performance into the next decision, so its strategy visibly evolves.</p>
      <p><sub><code>failed payment → history + stats → LLM diagnosis → strategy → simulate → record ⟲ learn</code></sub></p>
      <code>FastAPI</code> <code>SQLite</code> <code>Groq</code> <code>Llama 3.3 70B</code> <code>structured JSON</code>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <a href="https://github.com/vaibhav-barman/gnews-mcp-server"><img src="./assets/poly-mcp.svg" width="92" align="left" alt=""/></a>
      <h3><a href="https://github.com/vaibhav-barman/gnews-mcp-server">GNews MCP Server</a></h3>
      <sub><b>MCP · AI TOOLING</b></sub>
      <br clear="left"/>
      <p>A Model Context Protocol server that gives any MCP client live news: <code>search_news</code> with language, country, date and sort filters, and <code>get_top_headlines</code>. Runs over stdio, launched by the client.</p>
      <p><sub><code>MCP client ⇄ stdio ⇄ FastMCP tools → GNews API</code></sub></p>
      <code>MCP</code> <code>FastMCP</code> <code>Python</code> <code>uv</code>
    </td>
    <td width="50%" valign="top">
      <a href="https://github.com/vaibhav-barman/odyssey-rag"><img src="./assets/poly-odyssey.svg" width="92" align="left" alt=""/></a>
      <h3><a href="https://github.com/vaibhav-barman/odyssey-rag">Odyssey RAG</a></h3>
      <sub><b>RAG · RETRIEVAL EVALUATION</b></sub>
      <br clear="left"/>
      <p>Question answering over Homer's <i>The Odyssey</i>, grounded in retrieved passages. 850 chunks, 768-dimension Gemini embeddings, cosine top-5 retrieval, and a labelled question set to score retrieval with Recall@K and MRR.</p>
      <p><sub><code>source text → chunk → embed → cosine top-5 → grounded answer</code></sub></p>
      <code>RAG</code> <code>Gemini</code> <code>embeddings</code> <code>Recall@K</code> <code>MRR</code>
    </td>
  </tr>
</table>

<img src="./assets/h-lab.svg" width="100%" alt="04 · lab notebook"/>

| Experiment | What it explores |
| :-- | :-- |
| [**ApplyIQ**](https://github.com/vaibhav-barman/apply-iq) | Resume vs. job description analysis: ATS fit, missing skills, recruiter risks. Gemini, FastAPI, PostgreSQL, Alembic. |
| [**PromptRoute**](https://github.com/vaibhav-barman/promptroute) | "Backend-as-a-prompt": a travel planner where a local Ollama model returns structured JSON instead of a server and database. |
| [**YouTube Video Summarizer**](https://github.com/vaibhav-barman/youtube-video-summarizer) | Whisper transcription plus a local LLM summary. Nothing leaves your machine. |
| [**ollama**](https://github.com/vaibhav-barman/ollama) | Local RAG lab: PDF RAG with ChromaDB and multi-query retrieval, a voice-enabled variant, function calling. |
| [**react-agent-from-scratch**](https://github.com/vaibhav-barman/react-agent-from-scratch) | The ReAct reason-act-observe loop written by hand on the Groq API, no framework. |
| [**learn-langgraph**](https://github.com/vaibhav-barman/learn-langgraph) | Notebook trail through LangGraph: workflows, prompt chaining, chatbots, persistence, tools. |
| [**coursenotes-ai**](https://github.com/vaibhav-barman/coursenotes-ai) | Turns course transcripts into structured study notes. |
| [**gemini-website-summarizer**](https://github.com/vaibhav-barman/gemini-website-summarizer) | Extracts a page's readable content and summarizes it to Markdown with Gemini. |
| [**Spendly**](https://github.com/vaibhav-barman/spendly) | Expense tracker built end to end as an agentic coding workflow with Claude Code. |

<img src="./assets/h-stack.svg" width="100%" alt="05 · stack"/>

**Agents & LLM orchestration**

![LangGraph](https://img.shields.io/badge/LangGraph-0f172a?style=for-the-badge&logo=langgraph&logoColor=22d3ee)
![LangChain](https://img.shields.io/badge/LangChain-0f172a?style=for-the-badge&logo=langchain&logoColor=22d3ee)
![MCP](https://img.shields.io/badge/MCP-0f172a?style=for-the-badge&logo=modelcontextprotocol&logoColor=22d3ee)
![FastMCP](https://img.shields.io/badge/FastMCP-0f172a?style=for-the-badge)
![RAG](https://img.shields.io/badge/RAG-0f172a?style=for-the-badge)
![Ollama](https://img.shields.io/badge/Ollama_·_local_LLMs-0f172a?style=for-the-badge&logo=ollama&logoColor=22d3ee)
![Claude Code](https://img.shields.io/badge/Claude_Code-0f172a?style=for-the-badge&logo=claude&logoColor=22d3ee)

**Model providers**

![Anthropic](https://img.shields.io/badge/Anthropic-0f172a?style=for-the-badge&logo=anthropic&logoColor=a78bfa)
![OpenAI](https://img.shields.io/badge/OpenAI-0f172a?style=for-the-badge)
![Gemini](https://img.shields.io/badge/Gemini-0f172a?style=for-the-badge&logo=googlegemini&logoColor=a78bfa)
![Groq](https://img.shields.io/badge/Groq-0f172a?style=for-the-badge)
![NVIDIA](https://img.shields.io/badge/NVIDIA-0f172a?style=for-the-badge&logo=nvidia&logoColor=a78bfa)

**Backend & data**

![Python](https://img.shields.io/badge/Python-0f172a?style=for-the-badge&logo=python&logoColor=f472b6)
![FastAPI](https://img.shields.io/badge/FastAPI-0f172a?style=for-the-badge&logo=fastapi&logoColor=f472b6)
![Pydantic](https://img.shields.io/badge/Pydantic-0f172a?style=for-the-badge&logo=pydantic&logoColor=f472b6)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-0f172a?style=for-the-badge&logo=sqlalchemy&logoColor=f472b6)
![Alembic](https://img.shields.io/badge/Alembic-0f172a?style=for-the-badge)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-0f172a?style=for-the-badge&logo=postgresql&logoColor=f472b6)
![MySQL](https://img.shields.io/badge/MySQL-0f172a?style=for-the-badge&logo=mysql&logoColor=f472b6)
![SQLite](https://img.shields.io/badge/SQLite-0f172a?style=for-the-badge&logo=sqlite&logoColor=f472b6)
![ChromaDB](https://img.shields.io/badge/ChromaDB-0f172a?style=for-the-badge)
![Redis](https://img.shields.io/badge/Redis-0f172a?style=for-the-badge&logo=redis&logoColor=f472b6)

**Cloud & DevOps**

![AWS](https://img.shields.io/badge/AWS_·_S3_·_EC2_·_Lambda-0f172a?style=for-the-badge)
![Boto3](https://img.shields.io/badge/Boto3-0f172a?style=for-the-badge)
![Docker](https://img.shields.io/badge/Docker-0f172a?style=for-the-badge&logo=docker&logoColor=34d399)
![Nginx](https://img.shields.io/badge/Nginx-0f172a?style=for-the-badge&logo=nginx&logoColor=34d399)
![Ubuntu](https://img.shields.io/badge/Ubuntu-0f172a?style=for-the-badge&logo=ubuntu&logoColor=34d399)
![Git](https://img.shields.io/badge/Git_·_GitHub-0f172a?style=for-the-badge&logo=git&logoColor=34d399)

<sub>Production habits I build with: async APIs, authN / authZ, pagination, rate limiting (SlowAPI), migrations, typed code, tests.</sub>

<img src="./assets/h-telemetry.svg" width="100%" alt="06 · telemetry"/>

<div align="center">

<img src="./profile-3d-contrib/profile-neon.svg" width="100%" alt="My GitHub contributions rendered as a 3D isometric skyline"/>

<img src="./profile-3d-contrib/snake-neon.svg" width="100%" alt="A snake eating my contribution graph"/>

</div>

<img src="./assets/h-creds.svg" width="100%" alt="07 · training data"/>

<table>
  <tr><td><b>Education</b></td><td>B.Sc. Computer Science, BITS Pilani</td></tr>
  <tr><td><b>Experience</b></td><td>AI/ML Intern, Elevate Labs</td></tr>
  <tr><td><b>Certifications</b></td><td>AI Engineer Bootcamp 2026 · Complete MCP Developer Guide · Mastering Ollama · Docker &amp; Kubernetes Fundamentals (Scaler Academy)</td></tr>
</table>

<img src="./assets/h-connect.svg" width="100%" alt="08 · open a channel"/>

<div align="center">

**Hiring for an AI engineering role, or building something agentic? I'd like to hear about it.**

<p>
  <a href="https://vaibhav-barman.github.io"><img src="https://img.shields.io/badge/Portfolio-0f172a?style=for-the-badge&logo=githubpages&logoColor=22d3ee" alt="Portfolio"/></a>
  <a href="https://vaibhav-barman.github.io/resume.html"><img src="https://img.shields.io/badge/Resume-0f172a?style=for-the-badge&logo=readdotcv&logoColor=22d3ee" alt="Resume"/></a>
  <a href="https://www.linkedin.com/in/vaibhavbarman/"><img src="https://img.shields.io/badge/LinkedIn-0f172a?style=for-the-badge" alt="LinkedIn"/></a>
  <a href="mailto:vaibhavbarman2609@gmail.com"><img src="https://img.shields.io/badge/Email-0f172a?style=for-the-badge&logo=gmail&logoColor=22d3ee" alt="Email"/></a>
  <img src="https://komarev.com/ghpvc/?username=vaibhav-barman&style=for-the-badge&color=0f172a&label=VISITORS" alt="Profile views"/>
</p>

<img src="./assets/footer.svg" width="100%" alt="End of transmission"/>

</div>
