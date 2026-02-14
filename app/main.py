import streamlit as st
from faq import ingest_faq_path, faq_chain
from sql import sql_chain
from pathlib import Path
from router import router

st.set_page_config(
    page_title="E-Commerce AI Assistant",
    page_icon="🛍️",
    layout="wide"
)

st.markdown("""
    <style>
        .main-title {
            font-size: 32px;
            font-weight: 700;
            color: #2E86C1;
        }
        .subtitle {
            font-size: 16px;
            color: #555;
        }
        .footer {
            text-align: center;
            font-size: 13px;
            color: grey;
            margin-top: 50px;
        }
    </style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3081/3081559.png", width=100)
    st.markdown("## 🛒 E-Commerce Bot")
    st.markdown("""
    This AI assistant can:
    - Answer FAQ queries
    - Fetch product data via SQL
    - Route intelligently using semantic routing
    """)
    st.divider()
    st.markdown("**Built with:**")
    st.markdown("- Streamlit")
    st.markdown("- LLM Router")
    st.markdown("- SQL + RAG")

st.markdown('<p class="main-title">🛍️ E-Commerce AI Assistant</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Ask about products, FAQs, or database queries</p>', unsafe_allow_html=True)
st.divider()

faqs_path = Path(__file__).parent / "resources/faq_data.csv"
ingest_faq_path(faqs_path)

def ask(query):
    try:
        route = router(query).name

        if route == "faq":
            return faq_chain(query)

        elif route == "sql":
            return sql_chain(query)

        else:
            return f"⚠ Route '{route}' not implemented yet."

    except Exception as e:
        return f"❌ Error: {str(e)}"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

query = st.chat_input("Type your question here...")

if query:
    # Display User Message
    with st.chat_message("user"):
        st.markdown(query)

    st.session_state.messages.append({
        "role": "user",
        "content": query
    })

    # Assistant Response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = ask(query)
            st.markdown(response)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })
st.markdown("""
    <div class="footer">
        © 2026 E-Commerce AI Assistant | Built using Streamlit & LLM Routing
    </div>
""", unsafe_allow_html=True)
