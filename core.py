"""Core logic: menu, prompt, LLM extraction, cart, bill. No UI code here."""
import os, csv, json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
MODEL = os.getenv("LLM_MODEL", "llama-3.3-70b-versatile")
GST_RATE = 0.05


def load_menu(path="menu.csv"):
    with open(path, newline="", encoding="utf-8") as f:
        return {r["item"]: int(r["price"]) for r in csv.DictReader(f)}


MENU = load_menu()

SYSTEM_PROMPT = f"""You are an order-taking assistant for an Indian restaurant.
MENU (item: price in INR):
{json.dumps(MENU, ensure_ascii=False)}

Read the customer's message and reply with ONLY a JSON object:
{{"action": "add" | "remove" | "confirm" | "clear" | "chat",
 "items": [{{"item": "<exact menu name>", "qty": <positive integer>}}],
 "unknown": ["<requested things NOT on the menu>"],
 "reply": "<one short friendly sentence>"}}

Rules:
- "item" must match a menu name exactly. Fix spelling and spoken forms
  ("a couple" = 2, "an" = 1, "paneer tikka" -> "Paneer Tikka").
- Anything not on the menu goes in "unknown", never in "items".
- "confirm" = customer is done / wants to place the order.
- "clear" = cancel the whole order. "chat" = greeting or menu question (items = []).
- "remove" = customer wants to take items off the order.
- Output no text outside the JSON."""


def extract(user_text: str) -> dict:
    """Ask the LLM to turn free text into structured JSON."""
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    resp = client.chat.completions.create(
        model=MODEL,
        temperature=0,  # 0 = most predictable output
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_text},
        ],
    )
    return json.loads(resp.choices[0].message.content)


def update_cart(cart: dict, data: dict) -> list:
    """Apply LLM result to cart. Python validates everything. Returns unknown items."""
    action = data.get("action", "chat")
    unknown = list(data.get("unknown", []))
    if action == "clear":
        cart.clear()
    for it in data.get("items", []):
        name, qty = it.get("item"), it.get("qty", 1)
        if name not in MENU:          # guard against LLM mistakes
            unknown.append(str(name))
            continue
        try:
            qty = max(1, int(qty))
        except (TypeError, ValueError):
            qty = 1
        if action == "add":
            cart[name] = cart.get(name, 0) + qty
        elif action == "remove" and name in cart:
            cart[name] -= qty
            if cart[name] <= 0:
                del cart[name]
    return unknown


def calc_bill(cart: dict) -> dict:
    """Python does the maths (LLMs can get arithmetic wrong)."""
    lines = [(n, q, MENU[n], MENU[n] * q) for n, q in cart.items()]
    subtotal = sum(l[3] for l in lines)
    gst = round(subtotal * GST_RATE, 2)
    return {"lines": lines, "subtotal": subtotal, "gst": gst, "total": round(subtotal + gst, 2)}
