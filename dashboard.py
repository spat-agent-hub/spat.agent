import streamlit as st
from api.utils import is_active_subscriber

st.set_page_config(page_title="Spat Agent | 100k Club", layout="centered")

st.title("🔋 Spat Agent: Subscription Portal")
st.markdown("### Cost of Access: 100,000 $SPAT / Month")

user_addr = st.text_input("Enter your Privy/Smart Wallet Address")

if user_addr:
    is_active = is_active_subscriber(user_addr)
    if is_active:
        st.success("✅ **Access Granted.** Your $SPAT subscription is active.")
    else:
        st.error("❌ **Access Denied.** 100k $SPAT subscription required.")
        st.info("Top up your wallet and call 'subscribe' on our Base contract.")

st.divider()
st.link_button("View Token on BaseScan", "https://basescan.org/token/0x7f18bdbe376b3b0648ad75da2fcc52f8c107bcdf")
