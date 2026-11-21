import streamlit as st
import pandas as pd
from core import MENU, extract, update_cart, calc_bill, GST_RATE

st.set_page_config(page_title="Restaurant Ordering Bot", page_icon="🍽️")
st.title("🍽️ Restaurant Ordering Bot")

# session_state keeps data between reruns (Streamlit reruns the script on every click)
ss = st.session_state
ss.setdefault("cart", {})
ss.setdefault("chat", [("assistant", "Welcome! Tell me what you'd like, e.g. '2 paneer tikka and a coke'.")])
ss.setdefault("confirmed", False)

user_text = st.chat_input("Type your order...", disabled=ss.confirmed)
if user_text:
    ss.chat.append(("user", user_text))
    try:
        data = extract(user_text)
        unknown = update_cart(ss.cart, data)
        reply = data.get("reply", "")
        if unknown:
            reply += f" Sorry, not on our menu: {', '.join(unknown)}."
        if data.get("action") == "confirm":
            if ss.cart:
                ss.confirmed = True
                reply = "Order confirmed! Thank you 🎉"
            else:
                reply = "Your order is empty. What would you like?"
    except Exception as e:
        reply = f"Sorry, something went wrong ({e}). Please try again."
    ss.chat.append(("assistant", reply))

for role, msg in ss.chat:
    st.chat_message(role).write(msg)

# Sidebar: menu + live bill
with st.sidebar:
    st.subheader("Menu")
    st.table(pd.DataFrame({"Item": MENU.keys(), "Price (₹)": MENU.values()}).set_index("Item"))
    st.subheader("Your order")
    if ss.cart:
        b = calc_bill(ss.cart)
        st.table(pd.DataFrame(b["lines"], columns=["Item", "Qty", "Price", "Amount"]).set_index("Item"))
        st.write(f"Subtotal: ₹{b['subtotal']}")
        st.write(f"GST ({int(GST_RATE*100)}%): ₹{b['gst']}")
        st.markdown(f"**Total: ₹{b['total']}**")
        if not ss.confirmed and st.button("Confirm order"):
            ss.confirmed = True
            ss.chat.append(("assistant", "Order confirmed! Thank you 🎉"))
            st.rerun()
    else:
        st.write("Nothing yet.")
    if st.button("New order"):
        ss.cart, ss.confirmed = {}, False
        ss.chat = [("assistant", "Welcome! What would you like?")]
        st.rerun()
