# Restaurant Ordering Bot

**Problem:** Taking food orders by phone is error-prone. This chatbot shows a menu, understands natural-language orders, and confirms the bill.

**How it works:** `menu.csv` -> menu injected into the system prompt -> LLM (Llama 3.3 via Groq) returns JSON (items + quantity) -> Python validates and calculates the bill (+5% GST).

## Run
```
pip install -r requirements.txt
cp .env.example .env    
Add LLM_MODEL=openai/gpt-oss-20b to .env
streamlit run app.py
```
Test without UI: `python test_cases.py`

## Screenshots
(add 1-2 here)
<img width="177" height="289" alt="Screenshot 2026-11-21 151536" src="https://github.com/user-attachments/assets/0e3e664d-b4a8-49a1-afbb-455a2182c7c1" />
<img width="952" height="428" alt="Screenshot 2026-11-21 152553" src="https://github.com/user-attachments/assets/c90a570e-01c2-49ea-ae9f-45c8db5abaa4" />
<img width="957" height="422" alt="Screenshot 2026-11-21 152543" src="https://github.com/user-attachments/assets/9cb18dcd-0f5a-4850-8c44-d2d059f90914" />
