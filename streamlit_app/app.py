import streamlit as st
import requests
import uuid
import base64
import time
from pathlib import Path

# --- Configuration ---
BACKEND_URL = "http://localhost:8000/api/chat"
st.set_page_config(
    page_title="Enterprise AI Agent", 
    page_icon="🤖",
    layout="centered"
)

# --- Helper: Load Image as Base64 ---
def get_image_base64(path):
    try:
        with open(path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        return encoded_string
    except FileNotFoundError:
        return None

# Load Logo
logo_path = Path("streamlit_app/logo.png")
logo_base64 = get_image_base64(logo_path)

# --- Custom CSS for Premium Look ---
st.markdown(f"""
    <style>
    /* Global Styles */
    .stApp {{
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        font-family: 'Inter', sans-serif;
    }}
    
    /* Header Container */
    .header-container {{
        text-align: center;
        padding: 40px 0 20px 0;
        margin-bottom: 30px;
    }}
    
    /* Central Icon (Custom Image) */
    .agent-icon {{
        width: 140px;
        height: 140px;
        margin-bottom: 15px;
        border-radius: 50%; /* Make it circular */
        object-fit: cover;
        box-shadow: 0 0 20px rgba(66, 133, 244, 0.5); /* Glow effect */
        animation: pulse 3s infinite;
        border: 2px solid rgba(255,255,255,0.5);
    }}
    
    @keyframes pulse {{
        0% {{ transform: scale(1); box-shadow: 0 0 15px rgba(66, 133, 244, 0.4); }}
        50% {{ transform: scale(1.02); box-shadow: 0 0 25px rgba(66, 133, 244, 0.7); }}
        100% {{ transform: scale(1); box-shadow: 0 0 15px rgba(66, 133, 244, 0.4); }}
    }}

    /* Status Badge */
    .status-badge {{
        background-color: #e6f4ea;
        color: #1e8e3e;
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 20px;
        border: 1px solid rgba(30, 142, 62, 0.1);
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }}
    
    .status-dot {{
        width: 8px;
        height: 8px;
        background-color: #1e8e3e;
        border-radius: 50%;
        display: inline-block;
        box-shadow: 0 0 5px rgba(30, 142, 62, 0.4);
    }}
    
    /* Typography */
    .main-title {{
        font-size: 3.5rem;
        font-weight: 800;
        color: #0f172a;
        margin: 0;
        letter-spacing: -1.5px;
        line-height: 1.1;
    }}
    
    .sub-title {{
        font-size: 1.15rem;
        color: #64748b;
        font-weight: 500;
        margin-top: 10px;
        letter-spacing: 0.5px;
    }}
    
    /* Chat Bubbles CSS */
    .user-msg-container {{
        display: flex;
        justify-content: flex-end;
        margin-bottom: 20px;
    }}
    
    .user-msg {{
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        color: white;
        padding: 14px 22px;
        border-radius: 20px 20px 4px 20px;
        max-width: 75%;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.15);
        font-size: 16px;
        line-height: 1.5;
    }}
    
    .agent-msg-container {{
        display: flex;
        justify-content: flex-start;
        margin-bottom: 20px;
    }}
    
    .agent-msg-content {{
        max-width: 85%;
    }}
    
    .agent-msg {{
        background-color: #ffffff;
        color: #1e293b;
        padding: 16px 24px;
        border-radius: 20px 20px 20px 4px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04), 0 0 0 1px rgba(0,0,0,0.02);
        font-size: 16px;
        line-height: 1.6;
        margin-bottom: 10px;
    }}
    
    /* Telemetry Pills */
    .telemetry-row {{
        display: flex;
        gap: 8px;
        padding-left: 5px;
        opacity: 0.9;
    }}
    
    .pill {{
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 4px 10px;
        font-size: 11px;
        color: #64748b;
        font-weight: 500;
        display: flex;
        align-items: center;
        gap: 4px;
        transition: all 0.2s ease;
    }}
    
    .pill:hover {{
        background: #f1f5f9;
        border-color: #cbd5e1;
    }}
    
    /* Hide specific Streamlit elements to clean UI */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    
    </style>
""", unsafe_allow_html=True)

# --- Session State ---
if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Header UI ---
icon_html = f'<img src="data:image/png;base64,{logo_base64}" class="agent-icon">' if logo_base64 else '<div style="font-size: 80px;">🤖</div>'

st.markdown(f"""
    <div class="header-container">
        {icon_html}
        <div style="margin-top: -15px;">
             <span class="status-badge">
                <span class="status-dot"></span> Agent Active
             </span>
        </div>
        <h1 class="main-title">Enterprise<br>AI Agent</h1>
        <p class="sub-title">Reasoning • Tools • Memory</p>
    </div>
""", unsafe_allow_html=True)

# --- Chat Interface Rendering ---
# We use a container to render the chat history
chat_container = st.container()

with chat_container:
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"""
                <div class="user-msg-container">
                    <div class="user-msg">{msg['content']}</div>
                </div>
            """, unsafe_allow_html=True)
        else:
            # Metadata formatting
            meta = msg.get("metadata", {})
            tools = meta.get("tools_used", []) 
            tools_str = ", ".join(tools) if tools else "None"
            mem_active = "Active" if meta.get("memory_retrieved") else "Idle"
            time_taken = meta.get("time_taken", "0.5s") # We'll need to capture this
            
            # Icons
            tool_icon = "🛠" if tools else "⚡"
            
            st.markdown(f"""
                <div class="agent-msg-container">
                    <div class="agent-msg-content">
                        <div class="agent-msg">{msg['content']}</div>
                        <div class="telemetry-row">
                            <span class="pill">🧠 Memory: {mem_active}</span>
                            <span class="pill">📈 Tools: {tools_str}</span>
                            <span class="pill">⏱ Time: {time_taken}</span>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

# --- Input Area ---
if prompt := st.chat_input("Ask me anything..."):
    # 1. Update User State
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Force rerun to show user message immediately
    st.rerun()

# --- Logic to handle new message (triggered by rerun) ---
# Check if last message is user, if so, trigger backend
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    start_time = time.time()
    last_user_msg = st.session_state.messages[-1]["content"]
    
    # We need to render the spinner manually since we aren't inside the chat_message block
    with st.spinner("Thinking..."):
        try:
            payload = {
                "user_id": st.session_state.user_id,
                "message": last_user_msg
            }
            response = requests.post(BACKEND_URL, json=payload)
            response.raise_for_status()
            
            data = response.json()
            answer = data["response"]
            metadata = data.get("metadata", {})
            
            # Calculate time
            elapsed = time.time() - start_time
            metadata["time_taken"] = f"{elapsed:.1f}s"
            
            st.session_state.messages.append({
                "role": "assistant",
                "content": answer,
                "metadata": metadata
            })
            st.rerun()
            
        except Exception as e:
            st.error(f"Error: {e}")
