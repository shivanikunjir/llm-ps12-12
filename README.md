# Restaurant Ordering Bot

**Problem:** Taking food orders by phone is error-prone. This chatbot shows a menu, understands natural-language orders, and confirms the bill.

**How it works:** `menu.csv` -> menu injected into the system prompt -> LLM (Llama 3.3 via Groq) returns JSON (items + quantity) -> Python validates and calculates the bill (+5% GST).

## Run
```
pip install -r requirements.txt
cp .env.example .env     # then paste your free key from console.groq.com
streamlit run app.py
```
Test without UI: `python test_cases.py`

## Screenshots
(add 1-2 here)
