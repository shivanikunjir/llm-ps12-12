"""Run 5+ sample inputs without the UI. Use the output for report screenshots."""
from core import extract, update_cart, calc_bill

TESTS = [
    "two paneer tikka and a coke",
    "add 3 butter naan and one dal makhani",
    "I want a pizza and 2 masala dosa",
    "remove 1 butter naan",
    "a couple of mango lassi please",
    "that's all, confirm my order",
]
cart = {}
for t in TESTS:
    data = extract(t)
    unknown = update_cart(cart, data)
    print(f"\n> {t}\nLLM JSON: {data}\nNot on menu: {unknown}\nCart: {cart}")
print("\nFINAL BILL:", calc_bill(cart))
