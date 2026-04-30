import os

import requests
import streamlit as st


DEFAULT_API_URL = "https://ai-backend-api-3jn5.onrender.com"
API_URL = os.getenv("API_URL", DEFAULT_API_URL).rstrip("/")


st.set_page_config(
    page_title="AI Backend Portfolio",
    page_icon="AI",
    layout="wide",
)


def post_json(path: str, payload: dict) -> tuple[dict | None, str | None]:
    try:
        response = requests.post(f"{API_URL}{path}", json=payload, timeout=120)
    except requests.RequestException as exc:
        return None, f"API request failed: {exc}"

    if response.status_code >= 400:
        return None, response.text

    return response.json(), None


st.title("AI Backend Portfolio")
st.caption("FastAPI service for ML prediction and RAG chatbot")

with st.sidebar:
    st.header("API")
    st.write(API_URL)
    st.link_button("Open API docs", f"{API_URL}/docs")

predict_tab, chat_tab = st.tabs(["Prediction ML", "Chatbot RAG"])

with predict_tab:
    st.subheader("Sales Prediction")

    left, right = st.columns(2)

    with left:
        purchase_month = st.number_input("Purchase month", min_value=1, max_value=12, value=5)
        purchase_dayofweek = st.number_input("Purchase day of week", min_value=0, max_value=6, value=2)
        customer_state = st.text_input("Customer state", value="SP")
        customer_city = st.text_input("Customer city", value="sao paulo")
        payment_installments = st.number_input("Payment installments", min_value=1, value=3)

    with right:
        items_count = st.number_input("Items count", min_value=1, value=2)
        freight_value = st.number_input("Freight value", min_value=0.0, value=21.5)
        review_score = st.number_input("Review score", min_value=1.0, max_value=5.0, value=4.0)
        delivery_delay_days = st.number_input("Delivery delay days", value=0)

    predict_payload = {
        "purchase_month": int(purchase_month),
        "purchase_dayofweek": int(purchase_dayofweek),
        "customer_state": customer_state,
        "customer_city": customer_city,
        "payment_installments": int(payment_installments),
        "items_count": int(items_count),
        "freight_value": float(freight_value),
        "review_score": float(review_score),
        "delivery_delay_days": int(delivery_delay_days),
    }

    if st.button("Run prediction", type="primary"):
        data, error = post_json("/predict/", predict_payload)

        if error:
            st.error(error)
        else:
            st.metric("Predicted value", f"{data['prediction']:.2f}")
            st.json(data)

with chat_tab:
    st.subheader("E-commerce Assistant")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])
            if message.get("route"):
                st.caption(f"Route: {message['route']}")

    question = st.chat_input("Ask a support or catalog question")

    if question:
        st.session_state.chat_history.append({"role": "user", "content": question})

        with st.chat_message("user"):
            st.write(question)

        payload = {
            "question": question,
            "history": st.session_state.chat_history,
        }

        with st.spinner("Calling the AI backend..."):
            data, error = post_json("/chat/", payload)

        with st.chat_message("assistant"):
            if error:
                st.error(error)
            else:
                st.write(data["answer"])
                st.caption(f"Route: {data['route']}")

                if data.get("sources"):
                    st.caption("Sources: " + ", ".join(data["sources"]))

                st.session_state.chat_history.append(
                    {
                        "role": "assistant",
                        "content": data["answer"],
                        "route": data["route"],
                    }
                )

    if st.button("Clear conversation"):
        st.session_state.chat_history = []
        st.rerun()
