# Gemstone Knowledge Assistant

An Agentic AI RAG Application for Gemstone Domain Knowledge Retrieval, Classification, and Analysis.

---

## Project Description

The **Gemstone Knowledge Assistant** is an agentic Retrieval-Augmented Generation (RAG) system built for gemological domain question-answering. It leverages a specialized **4-Agent Architecture** (`ClassifierAgent`, `PlannerAgent`, `RetrievalAgent`, and `SynthesizerAgent`) powered by Groq LLMs and a persistent ChromaDB vector store containing 20 curated reference documents covering Rubies, Sapphires, Moonstones, and Sri Lankan gemology.

The system intelligently classifies user intent, formulates optimal vector search queries, fetches relevant text chunks, synthesizes grounded answers with document citations, and gracefully redirects off-topic questions without hallucinating.

---

## 4-Agent Architecture Diagram

```mermaid
graph TD
    User([User / Browser]) <--> UI[Streamlit Web App: app/streamlit_app.py]
    UI <--> Orch[Agent Orchestrator: app/orchestrator.py]
    
    subgraph Specialized 4-Agent Pipeline
        Orch --> A1[Agent 1: ClassifierAgent]
        A1 -->|Intent & Category Payload| A2[Agent 2: PlannerAgent]
        A2 -->|Optimized Query & K Plan| A3[Agent 3: RetrievalAgent]
        A3 -->|Retrieved Chunks & Sources| A4[Agent 4: SynthesizerAgent]
    end
    
    subgraph RAG & Database Layer
        A3 -->|Query & Top-K| DB[(Persistent ChromaDB: ./chroma_db)]
        DB -->|Matching Chunks & Metadata| A3
    end
    
    subgraph Groq Cloud Models
        A1 -.->|Classification: gpt-oss-20b| Groq1[Groq API]
        A2 -.->|Planning: gpt-oss-20b| Groq2[Groq API]
        A4 -.->|Synthesis: gpt-oss-120b| Groq3[Groq API]
    end
```

---

## Setup Instructions

### Prerequisites
- Python 3.10+ installed
- Git installed

### Installation Steps

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Sajini2/Gemstone-Knowledge-Assistant-.git
   cd Gemstone-Knowledge-Assistant-
   ```

2. **Configure Environment Variables**:
   Copy `.env.example` to `.env` and set your Groq API Key:
   ```bash
   cp .env.example .env
   ```
   Edit `.env`:
   ```env
   GROQ_API_KEY=gsk_your_actual_groq_api_key_here
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Build the Vector Database Index**:
   ```bash
   python app/build_index.py
   ```

5. **Run Agent Test Suite**:
   ```bash
   python test_agents.py
   ```

6. **Launch the Streamlit Web Application**:
   ```bash
   python -m streamlit run app/streamlit_app.py
   ```

---

## Model Comparison Table

| Feature / Metric | Agent 1 & Agent 2: Routing & Planning (`openai/gpt-oss-20b`) | Agent 4: Answer Synthesis (`openai/gpt-oss-120b`) |
| :--- | :--- | :--- |
| **Primary Role** | Intent classification (`ruby`, `sapphire`, `moonstone`, `sri_lankan_gems`, `off_topic`), search query rewriting, and `k` planning | In-context synthesis, fact extraction, and source-grounded response generation |
| **Latency** | **Ultra-Low (~100-200 ms)** — Optimized for fast lightweight decision making | **Moderate (~500-800 ms)** — Balanced for complex multi-chunk reasoning |
| **Token Cost** | Extremely low resource footprint per request | Higher token capacity allocation for deep generation |
| **Context Window** | 8,192 tokens | 32,768 tokens (handles large retrieved context blocks) |
| **Reasoning Quality & Justification** | Ideal for deterministic JSON classification & structured parameter output without latency overhead | Superior multi-document synthesis, strict factual adherence, and minimal hallucination |

---

## 4-Agent Sequence Diagram

```mermaid
sequenceDiagram
    autonumber
    actor User
    participant App as Streamlit UI (streamlit_app.py)
    participant Orch as Orchestrator (orchestrator.py)
    participant A1 as Agent 1: ClassifierAgent
    participant A2 as Agent 2: PlannerAgent
    participant A3 as Agent 3: RetrievalAgent
    participant A4 as Agent 4: SynthesizerAgent
    participant VectorDB as ChromaDB (chroma_db)
    participant Groq as Groq LLM API

    User->>App: Submits question ("What is Ruby?")
    App->>Orch: ask(question)
    Orch->>A1: process(question)
    A1->>Groq: Classify intent (gpt-oss-20b)
    Groq-->>A1: {category, is_off_topic}
    A1-->>Orch: Payload 1
    
    Orch->>A2: process(Payload 1)
    alt is Off-Topic
        A2-->>Orch: Skip planning (retrieval_query="", k=0)
        Orch->>A3: process(Payload 2)
        A3-->>Orch: Empty chunks (sources=[])
        Orch->>A4: process(Payload 3)
        A4-->>Orch: Return Polite Redirect Response (No LLM/Vector call)
    else is Gemstone Query
        A2->>Groq: Optimize query & plan k (gpt-oss-20b)
        Groq-->>A2: {retrieval_query, k}
        A2-->>Orch: Payload 2
        Orch->>A3: process(Payload 2)
        A3->>VectorDB: retrieve(retrieval_query, k)
        VectorDB-->>A3: Top-K Document Chunks & Metadata
        A3-->>Orch: Payload 3 (chunks + sources)
        Orch->>A4: process(Payload 3)
        A4->>Groq: Synthesize answer with context (gpt-oss-120b)
        Groq-->>A4: Grounded Answer String
        A4-->>Orch: Payload 4 {answer, sources, category}
    end
    
    Orch-->>App: Final Response Dictionary
    App-->>User: Render Answer Card & Grounded Sources List
```

---

## RAG Pipeline Explanation

The RAG architecture converts 20 domain reference documents into an indexed vector knowledge base:

1. **Chunking Strategy**: Uses LangChain's `RecursiveCharacterTextSplitter` configured with `chunk_size=400` characters and `chunk_overlap=50` characters. This creates 106 distinct chunks, preserving sentence boundaries and context overlap across document splits.
2. **Embedding Model**: Employs sentence-transformers' `all-MiniLM-L6-v2` model executed locally via ChromaDB's ONNX runtime (`ONNXMiniLM_L6_V2`). Produces 384-dimensional embeddings locally with zero API cost.
3. **Vector Database**: Persists vector collections in `./chroma_db` using ChromaDB's `PersistentClient`.
4. **Retrieval Evaluation Summary**: Evaluated across 5 benchmark queries (`eval/retrieval_eval.py`), achieving 100% precision across source attribution and domain relevance:
   - **"What is Ruby?"** — Retrieves corundum composition, chromium trace elements, and Burmese/Thai origins (`ruby_geological_origin.txt`, `ruby_famous_rubies.txt`).
   - **"What is Sapphire?"** — Retrieves fancy corundum varieties, valence charge transfer, and valuation factors (`sapphire_color_varieties.txt`, `sapphire_valuation.txt`).
   - **"What is Moonstone?"** — Retrieves orthoclase-albite exsolution lamellae and adularescence physics (`moonstone_formation.txt`, `moonstone_adularescence.txt`).
   - **"What is Gem Certification?"** — Retrieves National Gem and Jewellery Authority (NGJA) laboratory testing standards (`sri_lankan_ngja_certification.txt`).
   - **"Which gems are found in Sri Lanka?"** — Retrieves Geuda sapphires, Alexandrite, Sinhalite, Spinel, and Ratnapura placer deposits (`sri_lankan_unique_species.txt`, `sri_lankan_ratnapura_region.txt`).

---

## Known Limitations

- **Domain Scope**: Specialized strictly for gemology; non-gemstone queries are politely redirected by design.
- **Local Persistence**: Vector database is stored locally in `./chroma_db`. Re-indexing is required if documents are modified.
- **API Dependency**: Final answer synthesis relies on active Groq API credentials.

---

## Live Streamlit App Demo

[Live Streamlit App Demo](https://gemstone-knowledge-assistant.streamlit.app)
