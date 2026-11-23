<div align="center">

<a href="https://vaibhav-barman.github.io/vaibhav-barman/">
  <img src="./assets/hero.svg" width="100%" alt="Vaibhav Barman. AI engineer building agentic systems. A liquid-chrome sphere with agents orbiting it."/>
</a>

<p>
  <a href="https://vaibhav-barman.github.io/vaibhav-barman/"><img src="https://img.shields.io/badge/ENTER-3D_PROFILE-ffffff?style=for-the-badge&labelColor=000000&color=111111&logo=threedotjs&logoColor=white" alt="ENTER"/></a>
  <a href="https://vaibhav-barman.github.io"><img src="https://img.shields.io/badge/PORTFOLIO-vaibhav--barman.github.io-ffffff?style=for-the-badge&labelColor=000000&color=111111" alt="PORTFOLIO"/></a>
  <a href="https://www.linkedin.com/in/vaibhavbarman/"><img src="https://img.shields.io/badge/LINKEDIN-vaibhavbarman-ffffff?style=for-the-badge&labelColor=000000&color=111111" alt="LINKEDIN"/></a>
  <a href="https://vaibhav-barman.github.io/resume.html"><img src="https://img.shields.io/badge/STATUS-open_to_remote_roles-ffffff?style=for-the-badge&labelColor=000000&color=111111" alt="STATUS"/></a>
</p>

</div>

<img src="./assets/h-whoami.svg" width="100%" alt="01 whoami"/>

I build **LLM agents, RAG pipelines and MCP servers** in Python, on local models and frontier APIs alike.

One rule runs through all of it: **a model shouldn't grade its own homework.** My agents draft, then something checkable (a relevance score, a grounding check, an exit code, a rule set) decides whether the draft ships or goes back for another pass, with a hard limit on retries.

```python
class Vaibhav:
    role      = "AI Engineer"
    builds    = ["agentic systems", "self-correcting RAG", "MCP servers", "local-LLM apps"]
    graphs    = ["LangGraph", "LangChain", "FastMCP"]
    serves    = ["FastAPI", "PostgreSQL", "Docker", "AWS"]
    principle = "checks over model opinion"
    studying  = "B.Sc. Computer Science @ BITS Pilani"
    status    = "open to remote AI engineering roles"
```

<img src="./assets/h-flagship.svg" width="100%" alt="02 flagship builds"/>

<a href="https://github.com/vaibhav-barman/blog-wriring-agent"><img src="./assets/fx-blog.svg" width="100%" alt="Blog Writing Agent. A LangGraph pipeline: router decides if research is needed, optional Tavily research, an orchestrator plans 4 to 6 sections, parallel workers write them via Send, a reducer orders, cites and saves Markdown."/></a>

<a href="https://github.com/vaibhav-barman/self-rag"><img src="./assets/fx-selfrag.svg" width="100%" alt="Self-RAG. Decides whether to retrieve, grades chunk relevance, checks the answer is supported and useful, revises unsupported answers and rewrites the query when the answer is not useful. Groq, Ollama embeddings, Chroma."/></a>

<a href="https://github.com/vaibhav-barman/corrective-rag"><img src="./assets/fx-crag.svg" width="100%" alt="Corrective RAG. Scores each retrieved chunk, routes CORRECT to refinement, AMBIGUOUS to books plus web, INCORRECT to a rewritten Tavily search, then generates a cited answer. Gemini, Ollama embeddings, Pinecone."/></a>

<sub>The panels animate the real graphs: each white packet is one run taking a different route through the nodes.</sub>

<img src="./assets/h-loop.svg" width="100%" alt="03 how I build"/>

<img src="./assets/agent-loop.svg" width="100%" alt="Agent loop: task, plan, act, observe, critic, ship. Rejected drafts go from critic back to plan."/>

It's the same loop each time: **ISSUP / ISUSE reflection** in Self-RAG, the **retrieval evaluator** in Corrective RAG, the **critic loop** in GitCommit AI, the **execute-and-repair loop** in LocalForge-AI.

<img src="./assets/h-builds.svg" width="100%" alt="04 more builds"/>

<table>
  <tr>
    <td width="50%" valign="top">
      <a href="https://github.com/vaibhav-barman/gitcommit-ai"><img src="./assets/poly-commit.svg" width="84" align="left" alt=""/></a>
      <h3><a href="https://github.com/vaibhav-barman/gitcommit-ai">GitCommit AI</a></h3>
      <sub><b>AGENTIC · CLI · <code>git ai-commit</code></b></sub>
      <br clear="left"/>
      <p>Learns how <i>your</i> repository writes commits, drafts a message in that voice, then a deterministic critic plus an LLM faithfulness check send it back until it passes. Never stages files, and refuses to commit if the staging area changed mid-run.</p>
      <code>LangGraph</code> <code>Python</code> <code>6 LLM providers</code> <code>Ollama</code> <code>eval harness</code>
    </td>
    <td width="50%" valign="top">
      <a href="https://github.com/vaibhav-barman/localforge-ai"><img src="./assets/poly-forge.svg" width="84" align="left" alt=""/></a>
      <h3><a href="https://github.com/vaibhav-barman/localforge-ai">LocalForge-AI</a></h3>
      <sub><b>MULTI-AGENT · 100% OFFLINE</b></sub>
      <br clear="left"/>
      <p>A local software team: a PM agent writes the spec, an engineer agent writes the code, a sandbox runs and lints it, and a QA agent routes real failures back for repair. Three open-weight models through Ollama, no network calls at runtime.</p>
      <code>LangGraph</code> <code>Ollama</code> <code>Python</code> <code>pytest</code>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <a href="https://github.com/vaibhav-barman/agentic-rag"><img src="./assets/poly-glossa.svg" width="84" align="left" alt=""/></a>
      <h3><a href="https://github.com/vaibhav-barman/agentic-rag">Glossa</a></h3>
      <sub><b>AGENTIC RAG · NO FRAMEWORK</b></sub>
      <br clear="left"/>
      <p>Answers next to the passages they came from. Hybrid keyword + vector search with reranking, incremental ingestion, and an agent that can also query the library with SQL, hand a document to a sub-agent or fall back to the web.</p>
      <code>FastAPI</code> <code>Postgres + pgvector</code> <code>Gemini</code> <code>RLS</code> <code>SSE</code>
    </td>
    <td width="50%" valign="top">
      <a href="https://github.com/vaibhav-barman/recovery-agent"><img src="./assets/poly-recovery.svg" width="84" align="left" alt=""/></a>
      <h3><a href="https://github.com/vaibhav-barman/recovery-agent">Recovery</a></h3>
      <sub><b>AI AGENT · RAZORPAY AI BUILDATHON</b></sub>
      <br clear="left"/>
      <p>A payment recovery agent. It classifies why a payment failed, picks a strategy, simulates the outcome, and feeds its own past performance into the next decision, so its strategy visibly evolves.</p>
      <code>FastAPI</code> <code>SQLite</code> <code>Groq</code> <code>Llama 3.3 70B</code>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <a href="https://github.com/vaibhav-barman/gnews-mcp-server"><img src="./assets/poly-mcp.svg" width="84" align="left" alt=""/></a>
      <h3><a href="https://github.com/vaibhav-barman/gnews-mcp-server">GNews MCP Server</a></h3>
      <sub><b>MCP · AI TOOLING</b></sub>
      <br clear="left"/>
      <p>A Model Context Protocol server that gives any MCP client live news: <code>search_news</code> with language, country, date and sort filters, and <code>get_top_headlines</code>. Runs over stdio.</p>
      <code>MCP</code> <code>FastMCP</code> <code>Python</code> <code>uv</code>
    </td>
    <td width="50%" valign="top">
      <a href="https://github.com/vaibhav-barman/odyssey-rag"><img src="./assets/poly-odyssey.svg" width="84" align="left" alt=""/></a>
      <h3><a href="https://github.com/vaibhav-barman/odyssey-rag">Odyssey RAG</a></h3>
      <sub><b>RAG · RETRIEVAL EVALUATION</b></sub>
      <br clear="left"/>
      <p>Question answering over Homer's <i>The Odyssey</i>. 850 chunks, 768-dimension Gemini embeddings, cosine top-5 retrieval, and a labelled question set that scores retrieval with Recall@K and MRR.</p>
      <code>RAG</code> <code>Gemini</code> <code>Recall@K</code> <code>MRR</code>
    </td>
  </tr>
</table>

<img src="./assets/h-lab.svg" width="100%" alt="05 lab notebook"/>

| Experiment | What it explores |
| :-- | :-- |
| [**ApplyIQ**](https://github.com/vaibhav-barman/apply-iq) | Resume vs. job description: ATS fit, missing skills, recruiter risks. Gemini, FastAPI, PostgreSQL, Alembic. |
| [**PromptRoute**](https://github.com/vaibhav-barman/promptroute) | "Backend-as-a-prompt": a travel planner where a local Ollama model returns structured JSON in place of a server and database. |
| [**YouTube Video Summarizer**](https://github.com/vaibhav-barman/youtube-video-summarizer) | Whisper transcription plus a local LLM summary. Nothing leaves your machine. |
| [**ollama**](https://github.com/vaibhav-barman/ollama) | Local RAG lab: PDF RAG with ChromaDB and multi-query retrieval, a voice variant, function calling. |
| [**react-agent-from-scratch**](https://github.com/vaibhav-barman/react-agent-from-scratch) | The ReAct reason-act-observe loop written by hand on the Groq API, no framework. |
| [**learn-langgraph**](https://github.com/vaibhav-barman/learn-langgraph) | Notebook trail through LangGraph: workflows, prompt chaining, chatbots, persistence, tools. |
| [**coursenotes-ai**](https://github.com/vaibhav-barman/coursenotes-ai) | Turns course transcripts into structured study notes. |
| [**gemini-website-summarizer**](https://github.com/vaibhav-barman/gemini-website-summarizer) | Extracts a page's readable content and summarizes it to Markdown with Gemini. |
| [**Spendly**](https://github.com/vaibhav-barman/spendly) | Expense tracker built end to end as an agentic coding workflow with Claude Code. |

<img src="./assets/h-stack.svg" width="100%" alt="06 stack"/>

<sub><b>AGENTS &amp; LLM ORCHESTRATION</b></sub><br/>
![LangGraph](https://img.shields.io/badge/LangGraph-0a0a0a?style=for-the-badge&logo=langgraph&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-0a0a0a?style=for-the-badge&logo=langchain&logoColor=white)
![MCP](https://img.shields.io/badge/MCP-0a0a0a?style=for-the-badge&logo=modelcontextprotocol&logoColor=white)
![FastMCP](https://img.shields.io/badge/FastMCP-0a0a0a?style=for-the-badge)
![RAG](https://img.shields.io/badge/RAG-0a0a0a?style=for-the-badge)
![Ollama · local LLMs](https://img.shields.io/badge/Ollama_·_local_LLMs-0a0a0a?style=for-the-badge&logo=ollama&logoColor=white)
![Claude Code](https://img.shields.io/badge/Claude_Code-0a0a0a?style=for-the-badge&logo=claude&logoColor=white)

<sub><b>MODEL PROVIDERS</b></sub><br/>
![Anthropic](https://img.shields.io/badge/Anthropic-0a0a0a?style=for-the-badge&logo=anthropic&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-0a0a0a?style=for-the-badge)
![Gemini](https://img.shields.io/badge/Gemini-0a0a0a?style=for-the-badge&logo=googlegemini&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-0a0a0a?style=for-the-badge)
![NVIDIA](https://img.shields.io/badge/NVIDIA-0a0a0a?style=for-the-badge&logo=nvidia&logoColor=white)

<sub><b>RETRIEVAL</b></sub><br/>
![ChromaDB](https://img.shields.io/badge/ChromaDB-0a0a0a?style=for-the-badge)
![Pinecone](https://img.shields.io/badge/Pinecone-0a0a0a?style=for-the-badge)
![pgvector](https://img.shields.io/badge/pgvector-0a0a0a?style=for-the-badge)
![Tavily](https://img.shields.io/badge/Tavily-0a0a0a?style=for-the-badge)
![Neo4j](https://img.shields.io/badge/Neo4j-0a0a0a?style=for-the-badge&logo=neo4j&logoColor=white)

<sub><b>BACKEND &amp; DATA</b></sub><br/>
![Python](https://img.shields.io/badge/Python-0a0a0a?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0a0a0a?style=for-the-badge&logo=fastapi&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-0a0a0a?style=for-the-badge&logo=pydantic&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-0a0a0a?style=for-the-badge&logo=sqlalchemy&logoColor=white)
![Alembic](https://img.shields.io/badge/Alembic-0a0a0a?style=for-the-badge)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-0a0a0a?style=for-the-badge&logo=postgresql&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-0a0a0a?style=for-the-badge&logo=mysql&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-0a0a0a?style=for-the-badge&logo=sqlite&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-0a0a0a?style=for-the-badge&logo=redis&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-0a0a0a?style=for-the-badge&logo=streamlit&logoColor=white)

<sub><b>CLOUD &amp; DEVOPS</b></sub><br/>
![AWS · S3 · EC2 · Lambda](https://img.shields.io/badge/AWS_·_S3_·_EC2_·_Lambda-0a0a0a?style=for-the-badge)
![Boto3](https://img.shields.io/badge/Boto3-0a0a0a?style=for-the-badge)
![Docker](https://img.shields.io/badge/Docker-0a0a0a?style=for-the-badge&logo=docker&logoColor=white)
![Nginx](https://img.shields.io/badge/Nginx-0a0a0a?style=for-the-badge&logo=nginx&logoColor=white)
![Ubuntu](https://img.shields.io/badge/Ubuntu-0a0a0a?style=for-the-badge&logo=ubuntu&logoColor=white)
![Git · GitHub](https://img.shields.io/badge/Git_·_GitHub-0a0a0a?style=for-the-badge&logo=git&logoColor=white)
![uv](https://img.shields.io/badge/uv-0a0a0a?style=for-the-badge&logo=uv&logoColor=white)

<sub>Habits I build with: async APIs, authN / authZ, pagination, rate limiting (SlowAPI), migrations, structured output, bounded retries, typed code, tests.</sub>

<img src="./assets/h-telemetry.svg" width="100%" alt="07 telemetry"/>

<div align="center">

<img src="./profile-3d-contrib/profile-neon.svg" width="100%" alt="My GitHub contributions rendered as a 3D isometric skyline"/>

<img src="./profile-3d-contrib/snake-neon.svg" width="100%" alt="A snake eating my contribution graph"/>

</div>

<img src="./assets/h-creds.svg" width="100%" alt="08 training data"/>

<table>
  <tr><td><sub><b>EDUCATION</b></sub></td><td>B.Sc. Computer Science, BITS Pilani</td></tr>
  <tr><td><sub><b>EXPERIENCE</b></sub></td><td>AI/ML Intern, Elevate Labs</td></tr>
  <tr><td><sub><b>CERTIFICATIONS</b></sub></td><td>AI Engineer Bootcamp 2026 · Complete MCP Developer Guide · Mastering Ollama · Docker &amp; Kubernetes Fundamentals (Scaler Academy)</td></tr>
</table>

<img src="./assets/h-connect.svg" width="100%" alt="09 open a channel"/>

<div align="center">

**Hiring for an AI engineering role, or building something agentic? I'd like to hear about it.**

<p>
  <a href="https://vaibhav-barman.github.io/vaibhav-barman/"><img src="https://img.shields.io/badge/3D-PROFILE-ffffff?style=for-the-badge&labelColor=000000&color=111111&logo=threedotjs&logoColor=white" alt="3D"/></a>
  <a href="https://vaibhav-barman.github.io/resume.html"><img src="https://img.shields.io/badge/RESUME-PDF-ffffff?style=for-the-badge&labelColor=000000&color=111111&logo=readdotcv&logoColor=white" alt="RESUME"/></a>
  <a href="mailto:vaibhavbarman2609@gmail.com"><img src="https://img.shields.io/badge/EMAIL-say_hello-ffffff?style=for-the-badge&labelColor=000000&color=111111&logo=gmail&logoColor=white" alt="EMAIL"/></a>
  <img src="https://komarev.com/ghpvc/?username=vaibhav-barman&style=for-the-badge&color=111111&label=VISITORS" alt="Profile views"/>
</p>

<img src="./assets/footer.svg" width="100%" alt="End of transmission"/>

</div>
