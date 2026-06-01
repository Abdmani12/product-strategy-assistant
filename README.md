# 🧠 AI-Powered Product Strategy Assistant

A **Multi-Agent AI System** that helps Product Managers analyze business data, generate strategic insights, and produce executive-ready reports — all through an interactive chat-based interface.

🌐 **Live Demo:** [https://product-strategy-assistant.onrender.com](https://product-strategy-assistant.onrender.com)

---

## 🎯 Overview

Upload your product data (sales reports, customer reviews, market research, competitor info) and **7 specialized AI agents** will analyze it from every angle, collaborate with each other, and deliver actionable insights with a downloadable PDF report.

---

## 🤖 Agent Architecture

| # | Agent | Responsibility |
|---|-------|---------------|
| 1 | **Customer Feedback Agent** | Sentiment analysis, pain points, satisfaction drivers, VOC quotes |
| 2 | **Market Research Agent** | Revenue trends, regional analysis, market penetration, growth opportunities |
| 3 | **Competitor Analysis Agent** | Competitive positioning, white space, battle cards, threat assessment |
| 4 | **SWOT Analysis Agent** | Synthesizes all prior analyses into SO/WO/ST/WT strategies |
| 5 | **Feature Prioritization Agent** | RICE scoring, MoSCoW, Value/Effort matrix, Kano model, roadmap |
| 6 | **Strategy Recommendation Agent** | OKRs, quarterly roadmap, 30/90-day action plans, risk register |
| 7 | **Executive Report Agent** | Board-ready summary, KPI table, 90-day action plan |

Each agent builds on the outputs of previous agents, creating a **collaborative intelligence pipeline**.

---

## ✨ Features

- **Multi-format Data Ingestion** — Upload CSV, PDF, DOCX, TXT, JSON, XLSX files
- **7-Agent Pipeline** — Sequential analysis with shared context between agents
- **Interactive Chat** — Ask follow-up questions with full analysis context
- **Downloadable PDF Report** — Professionally formatted executive report (ReportLab)
- **Individual Section Exports** — Download each agent's analysis as TXT
- **Regenerate Any Section** — Re-run individual agents without restarting
- **No API Key Required** — Pre-configured AI gateway included
- **Custom Streamlit Theme** — Clean, professional UI with branded colors

---

## 📊 Expected Outputs

| Output | Agent |
|--------|-------|
| Customer Insights Report | Customer Feedback Agent |
| Market Research Summary | Market Research Agent |
| Competitor Analysis Report | Competitor Analysis Agent |
| SWOT Analysis (SO/WO/ST/WT) | SWOT Analysis Agent |
| Feature Prioritization (RICE + MoSCoW + Kano) | Feature Prioritization Agent |
| Strategic Action Plan & Product Roadmap | Strategy Recommendation Agent |
| Executive Summary (board-level) | Executive Report Agent |
| Downloadable PDF Report | All agents combined |

---

## 🚀 Quick Start

### Local Setup

```bash
# Clone the repository
git clone https://github.com/Abdmani12/product-strategy-assistant.git
cd product-strategy-assistant

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

Open your browser at **http://localhost:8501**

### Usage

1. Open the app in your browser
2. Upload one or more data files in the sidebar (CSV, PDF, DOCX, TXT, JSON, XLSX)
3. Click **Run Analysis**
4. Explore results across 4 tabs:
   - **Overview** — Dashboard with key metrics and agent status
   - **Analysis Results** — All 7 agent outputs (expandable, regeneratable)
   - **AI Chat** — Ask natural language questions about your data
   - **Executive Report** — Preview and download full PDF

---

## 📁 Project Structure

```
product-strategy-assistant/
├── app.py                               # Main Streamlit application (4-tab UI)
├── requirements.txt                     # Python dependencies
├── render.yaml                          # Render deployment configuration
├── .streamlit/
│   └── config.toml                      # Streamlit server & theme config
├── agents/
│   ├── base_agent.py                    # OpenAI-compatible gateway wrapper
│   ├── orchestrator.py                  # 7-agent pipeline coordinator
│   ├── customer_feedback_agent.py       # Agent 1 — VOC & sentiment
│   ├── market_research_agent.py         # Agent 2 — market intelligence
│   ├── competitor_analysis_agent.py     # Agent 3 — competitive landscape
│   ├── swot_analysis_agent.py           # Agent 4 — SWOT synthesis
│   ├── feature_prioritization_agent.py  # Agent 5 — RICE/MoSCoW/Kano
│   ├── strategy_recommendation_agent.py # Agent 6 — OKRs & roadmap
│   └── executive_report_agent.py        # Agent 7 — board-level summary
└── utils/
    ├── document_processor.py            # Multi-format file parser
    └── pdf_generator.py                 # ReportLab PDF generator
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **UI** | Streamlit 1.38+ |
| **AI Model** | GPT-4o-mini (via custom OpenAI-compatible gateway) |
| **PDF Generation** | ReportLab 4.2 |
| **Data Processing** | Pandas, PyPDF2, python-docx, openpyxl |
| **HTTP Client** | httpx (SSL-flexible for gateway) |
| **Deployment** | Render (Free tier) |
| **Version Control** | GitHub |

---

## 🔄 Agent Communication Flow

```
Upload Data
     │
     ▼
┌──────────────────────┐
│  Document Processor  │  ← Parses CSV / PDF / DOCX / TXT / JSON / XLSX
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Customer Feedback    │  ← Sentiment, pain points, VOC
└──────────┬───────────┘
           │ shares context ↓
┌──────────────────────┐
│  Market Research     │  ← Revenue trends, regional analysis
└──────────┬───────────┘
           │ shares context ↓
┌──────────────────────┐
│ Competitor Analysis  │  ← Competitive positioning, threats
└──────────┬───────────┘
           │ shares context ↓
┌──────────────────────┐
│   SWOT Analysis      │  ← Synthesizes all 3 prior outputs
└──────────┬───────────┘
           │ shares context ↓
┌──────────────────────┐
│ Feature Priority     │  ← RICE, MoSCoW, Kano, roadmap
└──────────┬───────────┘
           │ shares context ↓
┌──────────────────────┐
│ Strategy & Roadmap   │  ← OKRs, quarterly plan, risk register
└──────────┬───────────┘
           │ shares context ↓
┌──────────────────────┐
│  Executive Report    │  ← Board summary + downloadable PDF
└──────────────────────┘
```

---

## 🌐 Deployment

The app is deployed on **Render** (free tier):

| Property | Value |
|----------|-------|
| **Live URL** | https://product-strategy-assistant.onrender.com |
| **Platform** | Render Web Service |
| **Region** | Oregon (US West) |
| **Runtime** | Python 3.10 |
| **Auto-deploy** | Enabled (pushes to `main` trigger rebuild) |

> **Note:** First load after inactivity may take ~30 seconds as Render spins up the free-tier instance.

### Deploy Your Own

1. Fork this repo
2. Go to [dashboard.render.com](https://dashboard.render.com) → **New Web Service**
3. Connect your fork — Render auto-detects `render.yaml`
4. Click **Create Web Service** — done

---

## 📋 Sample Data

The repository includes `Sample Sales Data.csv` — a 120-row product sales dataset:

| Column | Description |
|--------|-------------|
| Date | Transaction date |
| Product_Name | 10 products (SmartWatch X, Laptop Air, FitBand Pro, etc.) |
| Category | Electronics, Wearables, Accessories, Audio |
| Region | North, South, East, West, Central |
| Revenue_USD / Profit_USD | Financial performance |
| Customer_Rating | 1–5 star ratings |
| Review | Customer review text |

Upload it directly to test the full 7-agent analysis pipeline.

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

*Built for the AI-Powered Product Strategy Assistant Assessment*
*Powered by Multi-Agent AI · Deployed on Render · [Live Demo](https://product-strategy-assistant.onrender.com)*
