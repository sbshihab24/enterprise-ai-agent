import streamlit as st
import requests
import uuid

# --- Configuration ---
BACKEND_URL = "http://localhost:8000/api/chat"
st.set_page_config(page_title="Enterprise AI Agent", page_icon="🤖")

# --- Session State Management ---
if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- UI Layout ---
st.title("🤖 Enterprise AI Agent")
st.markdown("A production-style agent with **Memory**, **Tools**, and **Reasoning**.")

# Display Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "metadata" in msg and msg["metadata"]:
            with st.expander("🛠️ Metadata (Tools & Memory)"):
                st.json(msg["metadata"])

# Input Area
if prompt := st.chat_input("How can I help you?"):
    # 1. Display User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Call Backend API
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                payload = {
                    "user_id": st.session_state.user_id,
                    "message": prompt
                }
                response = requests.post(BACKEND_URL, json=payload)
                response.raise_for_status()
                
                data = response.json()
                answer = data["response"]
                metadata = data.get("metadata", {})

                # 3. Display Assistant Response
                st.markdown(answer)
                if metadata:
                    with st.expander("🛠️ Metadata (Tools & Memory)"):
                        st.json(metadata)

                # 4. Update History
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": answer,
                    "metadata": metadata
                })

            except requests.exceptions.ConnectionError:
                st.error("❌ Could not connect to the backend. Is it running? (http://localhost:8000)")
            except Exception as e:
                st.error(f"❌ An error occurred: {e}")
