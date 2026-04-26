# 💰 Finance Assistance Agent
### A Tool-Based Multi-Agent AI App — Built with Google ADK & Gemini 2.5 Flash

---

> *"What if your AI assistant didn't just answer questions — but actually went out, searched the internet, and came back with real financial data tailored to you?"*
> That's exactly what this project does.

---

## 🌱 The Idea Behind This Project

Most people struggle with three money questions:

- *"Where is my money going?"*
- *"How do I start saving?"*
- *"What should I invest in?"*

Traditional chatbots give you **generic text answers from memory.** This project is different — it uses **AI agents that think, decide, and take real actions** to answer those questions with actual live data.

This is not just a chatbot. This is an **agentic AI application.**

---

## 🤖 What Is a Tool-Based Agentic App?

Let's break it down simply:

| Word | What It Means |
|---|---|
| **AI** | Understands your questions in plain English |
| **Agentic** | Doesn't just answer — it *thinks*, *decides*, and *acts* |
| **Tool-based** | Has real tools it can pick up and use (like a live search engine) |

Think of it like the difference between:

- ❌ Asking a friend *"what's Apple's stock price?"* — they guess from memory
- ✅ Asking an assistant who **actually opens Google**, searches it live, and tells you the real number

This app does the second one. Every single time.

---

## 🧠 The Two Agents — How They Work as a Team

This project has **two specialized AI agents** that collaborate:

```
You ask a question
        │
        ▼
┌─────────────────────────────────┐
│   Finance Assistant Agent 🧑‍💼   │  ← you always talk to this one first
│   "Your Financial Life Coach"   │
└────────────────┬────────────────┘
                 │
     ┌───────────┴────────────┐
     ▼                        ▼
Simple finance           Investment / market
question?                question?
     │                        │
Answers you              ┌────▼───────────────────┐
directly ✅              │  Investment Plan        │
                         │  Agent 📈              │
                         │  "The Market Analyst"  │
                         └────────────┬───────────┘
                                      │
                             Searches the web 🔍
                             Gets live data 📊
                             Builds your plan ✅
```

### 🧑‍💼 Agent 1 — Finance Assistant Agent
Your **first point of contact.** It understands your financial situation by collecting your income, expenses, savings, and goals. Then it gives you friendly, personalized, and actionable advice — like a financial coach who actually listens.

### 📈 Agent 2 — Investment Plan Agent
The **specialist.** When the conversation turns to investing or markets, Agent 1 automatically hands off to this one. It doesn't guess — it uses Google Search to fetch live stock prices, financial news, and market data, then builds you a real investment plan.

---

## 🛠️ The Tools — What Makes This "Agentic"

Here are the **real tools** the agents can pick up and use on their own:

```
📋 get_user_personal_finance_details()  →  fetches your financial profile
🔍 google_search                        →  live web search for market data
🤝 agent handoff (to investment agent)  →  delegates complex tasks to specialist
```

The AI **decides on its own** which tool to use, when to use it, and what to do with the result. You just ask your question — the agents figure out the rest.

---

## ❓ Why Can't We Mix Built-In and Custom Tools in the Same Agent?

This is one of the most important design decisions in this project — and a question every ADK developer runs into.

**Google ADK has two types of tools:**

- **Built-in tools** → provided by Google (e.g. `google_search`). They run on Google's own infrastructure with special backend permissions.
- **Custom tools** → Python functions you write yourself (e.g. `get_user_personal_finance_details()`). They run locally in your environment.

**The problem:** ADK does **not** allow mixing built-in and custom tools in the same agent. They operate in different execution environments — built-in tools need Google's backend; custom tools run locally. Combining them causes conflicts and breaks the agent.

**How we solved it — split the responsibility:**

```
Finance Assistant Agent   →  ONLY custom tools   (personal financial data)
Investment Plan Agent     →  ONLY built-in tools  (google_search for live market data)
```

Each agent stays clean, conflict-free, and laser-focused on its job. This is also just **better software design** — specialists outperform generalists.

---

## 📊 Why No Large Dataset? Why Do We Only Fetch What We Need?

This is a deliberate and modern architectural choice — not a limitation.

### The Old Way
Train a model on **massive datasets** — gigabytes of stock prices, market history, company reports — and hope the answers are still accurate when someone uses it weeks later.

**Problem:** Financial data goes stale *instantly.* Yesterday's dataset is already outdated.

### Our Way — Fetch Live, Fetch Smart
Don't store financial data at all. **Fetch it live, on demand,** only when the user asks for it.

```
User: "What's Tesla's stock price right now?"
        ↓
Agent uses google_search at this exact moment
        ↓
Gets today's actual real-time price from the web
        ↓
Returns a fresh, accurate answer ✅
```

**Why this is better:**

- ✅ Always up-to-date — no stale data, ever
- ✅ No massive storage or dataset maintenance costs
- ✅ Scales to any financial question without pre-training on it
- ✅ Answers reflect what's happening *right now* in the market

This follows the **RAG (Retrieval Augmented Generation)** philosophy — retrieve exactly what you need, exactly when you need it, rather than memorizing everything upfront.

---

## 🔑 How API Keys Work — And How We Handled It

### The Hotel Key Card Analogy

Imagine walking into a hotel. You don't just walk into any room — you show your **key card** at the front desk, and only then do you get access.

An **API key is exactly that key card.**

When this app talks to Google's Gemini model, Google's servers ask:
- *"Who is making this request?"*
- *"Do they have permission to use this service?"*
- *"Are they within their usage limits?"*

The API key answers all three questions instantly and silently.

### How We Implemented It Safely

**Step 1 — Store the key in a `.env` file (never in code):**
```env
GOOGLE_API_KEY=AIzaSy_your_actual_key_here
```

**Step 2 — Read it securely in Python:**
```python
from dotenv import load_dotenv
import os

load_dotenv()                              # reads the .env file
api_key = os.getenv("GOOGLE_API_KEY")    # fetches the key safely
```

**Step 3 — Google ADK picks it up automatically** from the environment. You don't even need to pass it manually to the agent.

### Why Not Just Paste the Key in the Code?

```python
# ❌ NEVER DO THIS
api_key = "AIzaSy_yourkey_abc123"
# If you push this to GitHub — bots scan repos 24/7
# Your key gets stolen within minutes, charges rack up, key gets disabled
```

```python
# ✅ ALWAYS DO THIS
api_key = os.getenv("GOOGLE_API_KEY")
# The key lives in .env, which is listed in .gitignore
# It never touches GitHub — it stays on your machine only
```

The `.env` + `.gitignore` combination is the industry-standard pattern for keeping secrets safe.

---

## ✨ Impressive Code Highlights

### 1. Passing an Agent as a Tool — The Multi-Agent Handoff
```python
# finance_assistant_agent/agent.py
root_agent = Agent(
    name="finance_assistant_agent",
    model="gemini-2.5-flash",
    instruction="You are a friendly finance coach...",
    tools=[
        get_user_personal_finance_details,  # custom Python function
        investment_plan_agent,              # another Agent — used as a tool!
    ],
)
```
> 💡 The investment agent is passed *as a tool* to the main agent. When Agent 1 decides the question needs market research, it calls Agent 2 the same way it would call a function — automatically, no manual routing needed.

---

### 2. Custom Tool — The Agent Fetches Your Financial Profile
```python
# finance_assistant_agent/agent.py
def get_user_personal_finance_details() -> dict:
    """Fetches the user's personal financial details."""
    return {
        "monthly_income": 5000,
        "monthly_expenses": 3200,
        "savings": 8000,
        "financial_goals": ["buy a house", "retire at 50"],
    }
```
> 💡 This is a plain Python function — but the AI *decides on its own* when to call it. You don't instruct it to "call this function now." The agent reasons: *"I need this person's financial details before I advise them"* — and calls it autonomously.

---

### 3. Google Search Tool — The Agent Browses the Internet
```python
# investment_plan_agent/agent.py
from google.adk.tools import google_search

investment_agent = Agent(
    name="investment_plan_agent",
    model="gemini-2.5-flash",
    instruction="""Search for real-time stock prices, market news,
    and company data. Provide investment advice with specific numbers.""",
    tools=[google_search],   # one line = internet access
)
```
> 💡 One line gives the agent the ability to search the entire internet. It decides *what* to search, reads the results, synthesizes the information, and delivers a data-backed financial plan — fully autonomously.

---

## 🗂️ Project Structure

```
Finance_assistance_agent/
│
├── .env                              # 🔐 API key (never commit this!)
├── .gitignore                        # Protects secrets from GitHub
├── requirements.txt                  # Python dependencies
│
├── finance_assistant_agent/
│   ├── __init__.py                   # Makes it a Python package
│   └── agent.py                     # Main agent — advice & routing
│
└── investment_plan_agent/
    ├── __init__.py                   # Makes it a Python package
    └── agent.py                     # Specialist — live market research
```

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/your-username/Finance_assistance_agent.git
cd Finance_assistance_agent
```

### 2. Create and activate virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate          # Linux / Mac / GitHub Codespace
# .venv\Scripts\activate           # Windows only
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up your API key
Create a `.env` file in the root folder:
```env
GOOGLE_API_KEY=your_google_api_key_here
```
> Get your free API key from [Google AI Studio](https://aistudio.google.com/app/apikey)

### 5. Run the app
```bash
adk web
```
Open the browser link shown in the terminal and start chatting! ✅

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Agent Framework | Google ADK (Agent Development Kit) |
| AI Model | Gemini 2.5 Flash |
| Web Search | Google Search Tool (built into ADK) |
| Environment Variables | python-dotenv |
| Runtime | Python 3.10+ |

---

## ⚠️ Known Limitations

- User financial data is currently **hardcoded** for demo purposes — not connected to a real bank or database yet
- No persistent memory between sessions — each conversation starts fresh
- Proof-of-concept stage — not production-ready

---

## 🔮 Future Enhancements

- [ ] Dynamic user data via Open Banking APIs or interactive forms
- [ ] Database (PostgreSQL / Firebase) for saving profiles and history
- [ ] Budget tracking, expense categorization, and spending alerts
- [ ] Goal progress monitoring with visual dashboards
- [ ] Persistent conversation memory across sessions
- [ ] Docker + Cloud Run deployment for production
- [ ] Expanded tool set — portfolio tracking, tax calculators, currency converters

---

## 🔐 Security Checklist

Your `.gitignore` must always include:

```gitignore
.env
.venv/
__pycache__/
*.pyc
```

**Never** paste API keys directly in code. **Never** commit your `.env` file.

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

*Built with 💙 using Google ADK — exploring the frontier of agentic AI, one tool at a time.*
