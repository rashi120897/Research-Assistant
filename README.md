# 🧠 Research Assistant

An AI-powered **Multi-Agent Research Pipeline** that automates the entire research process — from web search to final report generation — with built-in quality review.

Built with **LangChain**, **LangGraph**, and **Streamlit**.

## ✨ Features

- **Search Agent** — Finds recent, reliable sources using Tavily Search
- **Reader Agent** — Scrapes and extracts key content from top URLs
- **Writer Chain** — Drafts structured, professional research reports
- **Critic Chain** — Reviews and scores the report with actionable feedback
- **Streamlit UI** — Modern dark-themed interface with real-time progress tracking

## 🛠️ Tech Stack

- **LangChain + LangGraph** — Agent orchestration
- **OpenAI GPT-4o-mini** — LLM backbone
- **Tavily** — Web search API
- **BeautifulSoup** — Web scraping
- **Streamlit** — Interactive UI

## 🚀 Getting Started

1. **Clone the repo**
   ```bash
   git clone https://github.com/rashi120897/Research-Assistant.git
   cd Research-Assistant
   ```

2. **Create a virtual environment**
   ```bash
   uv venv && source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   uv pip install -r requirements.txt
   ```

4. **Set up environment variables** — Create a `.env` file:
   ```
   OPENAI_API_KEY=your_openai_key
   TAVILY_API_KEY=your_tavily_key
   ```

5. **Run the app**
   ```bash
   streamlit run app.py
   ```

## 📁 Project Structure

| File | Description |
|------|-------------|
| `app.py` | Streamlit UI entry point |
| `pipeline.py` | Research pipeline orchestration |
| `agents.py` | Agent and chain definitions |
| `tools.py` | Web search and scraping tools |
| `requirements.txt` | Python dependencies |
