# 🧠 AI-Powered Product Strategy Assistant

A **Multi-Agent AI System** that helps Product Managers analyze business data, generate strategic insights, and produce executive-ready reports — all through an interactive chat-based interface.

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
- **Downloadable PDF Report** — Professionally formatted executive report
- **Individual Section Exports** — Download each agent's analysis as TXT
- **Regenerate Any Section** — Re-run individual agents without restarting
- **No API Key Required** — Pre-configured gateway included

---

## 📊 Expected Outputs

- Customer Insights Report
- Market Research Summary
- Competitor Analysis Report
- SWOT Analysis (with SO/WO/ST/WT strategies)
- Feature Prioritization (RICE + MoSCoW + Kano)
- Strategic Action Plan & Product Roadmap
- Executive Summary (board-level)
- Downloadable PDF Report

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
2. Upload one or more data files (CSV, PDF, DOCX, TXT, JSON, XLSX) in the sidebar
3. Click **Run Analysis**
4. Explore results across 4 tabs:
   - **Overview** — Dashboard with key metrics
   - **Analysis Results** — All 7 agent outputs
   - **AI Chat** — Ask questions about your data
   - **Executive Report** — Download full PDF

---

## 📁 Project Structure

```
product-strategy-assistant/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── render.yaml                     # Render deployment config
├── agents/
│   ├── base_agent.py               # OpenAI-compatible gateway wrapper
│   ├── orchestrator.py             # Pipeline coordinator
│   ├── customer_feedback_agent.py  # Agent 1
│   ├── market_research_agent.py    # Agent 2
│   ├── competitor_analysis_agent.py# Agent 3
│   ├── swot_analysis_agent.py      # Agent 4
│   ├── feature_prioritization_agent.py # Agent 5
│   ├── strategy_recommendation_agent.py # Agent 6
│   └── executive_report_agent.py   # Agent 7
└── utils/
    ├── document_processor.py       # Multi-format file parser
    └── pdf_generator.py            # ReportLab PDF generator
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **UI** | Streamlit |
| **AI Model** | GPT-4o-mini (via custom gateway) |
| **PDF Generation** | ReportLab |
| **Data Processing** | Pandas, PyPDF2, python-docx |
| **Deployment** | Render |

---

## 🌐 Live Demo

> Deployed on Render — [product-strategy-assistant.onrender.com](https://product-strategy-assistant.onrender.com)

---

## 📋 Sample Data

The repository includes `Sample Sales Data.csv` — a 120-row product sales dataset covering:
- 10 products across 5 categories (Electronics, Wearables, Accessories, Audio)
- 5 regions (North, South, East, West, Central)
- Revenue, cost, profit, marketing spend, customer ratings, and reviews

Use it to test the full analysis pipeline immediately after setup.

---

## 🔄 Agent Communication Flow

```
Upload Data
     │
     ▼
┌─────────────────────┐
│  Document Processor  │  ← Extracts text from all file types
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│ Customer Feedback   │  ← Analyzes sentiment, pain points
└─────────┬───────────┘
          │ shares context
          ▼
┌─────────────────────┐
│  Market Research    │  ← Revenue trends, opportunities
└─────────┬───────────┘
          │ shares context
          ▼
┌─────────────────────┐
│ Competitor Analysis │  ← Competitive landscape
└─────────┬───────────┘
          │ shares context
          ▼
┌─────────────────────┐
│   SWOT Analysis     │  ← Synthesizes all 3 prior outputs
└─────────┬───────────┘
          │ shares context
          ▼
┌─────────────────────┐
│ Feature Priority    │  ← RICE, MoSCoW, Kano
└─────────┬───────────┘
          │ shares context
          ▼
┌─────────────────────┐
│ Strategy & Roadmap  │  ← OKRs, quarterly plan
└─────────┬───────────┘
          │ shares context
          ▼
┌─────────────────────┐
│  Executive Report   │  ← Board-ready summary + PDF
└─────────────────────┘
```

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

*Built for the AI-Powered Product Strategy Assistant Assessment*
