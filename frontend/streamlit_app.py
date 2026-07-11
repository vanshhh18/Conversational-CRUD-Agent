# """
# HobbyFi Vendor Copilot — Streamlit Chat Widget
# Powered by Groq + LangGraph

# A modern, minimalist floating chatbot interface. Clicking the
# floating icon in the bottom-right corner toggles a chat panel
# with rounded bubbles, soft shadows, and smooth animations.
# """

# import streamlit as st
# import requests

# # --------------------------------------------------------------------------
# # Page config
# # --------------------------------------------------------------------------
# st.set_page_config(
#     page_title="HobbyFi Copilot",
#     page_icon="🏸",
#     layout="wide",
# )

# BACKEND_URL = "http://127.0.0.1:8000/chat"
# THREAD_ID = "vendor_1"


# # --------------------------------------------------------------------------
# # Session state
# # --------------------------------------------------------------------------
# def init_state():
#     if "messages" not in st.session_state:
#         st.session_state.messages = []
#     if "chat_open" not in st.session_state:
#         st.session_state.chat_open = False
#     if "is_loading" not in st.session_state:
#         st.session_state.is_loading = False


# def toggle_chat():
#     st.session_state.chat_open = not st.session_state.chat_open


# # --------------------------------------------------------------------------
# # Styling
# # --------------------------------------------------------------------------
# def inject_css():
#     st.markdown(
#         """
#         <style>
#         /* ---------- General cleanup ---------- */
#         #MainMenu, footer {visibility: hidden;}

#         /* ---------- Floating toggle button ---------- */
#         div[data-testid="stButton"] button[kind="secondary"]#chat_toggle_btn,
#         .floating-toggle button {
#             position: fixed;
#             bottom: 28px;
#             right: 28px;
#             width: 60px;
#             height: 60px;
#             border-radius: 50%;
#             background: linear-gradient(135deg, #6C5CE7, #8E7CFF);
#             color: white;
#             font-size: 26px;
#             border: none;
#             box-shadow: 0 8px 24px rgba(108, 92, 231, 0.45);
#             z-index: 9999;
#             transition: transform 0.2s ease, box-shadow 0.2s ease;
#             cursor: pointer;
#         }
#         .floating-toggle button:hover {
#             transform: scale(1.08);
#             box-shadow: 0 10px 28px rgba(108, 92, 231, 0.6);
#         }

#         /* ---------- Chat panel container ---------- */
#         .chat-panel {
#             position: fixed;
#             bottom: 100px;
#             right: 28px;
#             width: 380px;
#             max-height: 560px;
#             background: #ffffff;
#             border-radius: 18px;
#             box-shadow: 0 12px 40px rgba(0, 0, 0, 0.18);
#             z-index: 9998;
#             display: flex;
#             flex-direction: column;
#             overflow: hidden;
#             animation: slideUp 0.25s ease-out;
#             border: 1px solid rgba(0,0,0,0.06);
#         }

#         @keyframes slideUp {
#             from { opacity: 0; transform: translateY(16px); }
#             to   { opacity: 1; transform: translateY(0); }
#         }

#         .chat-header {
#             background: linear-gradient(135deg, #6C5CE7, #8E7CFF);
#             color: white;
#             padding: 16px 18px;
#             font-weight: 600;
#             font-size: 16px;
#             display: flex;
#             align-items: center;
#             gap: 8px;
#         }

#         .chat-subtitle {
#             font-size: 12px;
#             font-weight: 400;
#             opacity: 0.85;
#         }

#         .chat-body {
#             padding: 14px 16px;
#             overflow-y: auto;
#             flex: 1;
#             background: #F7F7FB;
#         }

#         /* ---------- Bubbles ---------- */
#         .bubble-row {
#             display: flex;
#             margin-bottom: 10px;
#         }
#         .bubble-row.user { justify-content: flex-end; }
#         .bubble-row.assistant { justify-content: flex-start; }

#         .bubble {
#             max-width: 80%;
#             padding: 10px 14px;
#             border-radius: 16px;
#             font-size: 14px;
#             line-height: 1.45;
#             word-wrap: break-word;
#         }
#         .bubble.user {
#             background: #6C5CE7;
#             color: white;
#             border-bottom-right-radius: 4px;
#         }
#         .bubble.assistant {
#             background: white;
#             color: #2D2D2D;
#             border: 1px solid #ECECF3;
#             border-bottom-left-radius: 4px;
#         }

#         .typing-dots span {
#             display: inline-block;
#             width: 6px;
#             height: 6px;
#             margin-right: 3px;
#             background: #A8A0E8;
#             border-radius: 50%;
#             animation: blink 1.2s infinite ease-in-out;
#         }
#         .typing-dots span:nth-child(2) { animation-delay: 0.2s; }
#         .typing-dots span:nth-child(3) { animation-delay: 0.4s; }
#         @keyframes blink {
#             0%, 80%, 100% { opacity: 0.2; }
#             40% { opacity: 1; }
#         }

#         /* ---------- Empty state ---------- */
#         .empty-state {
#             text-align: center;
#             color: #9A9AAE;
#             font-size: 13px;
#             margin-top: 40px;
#         }

#         /* ---------- Input row tucked under panel ---------- */
#         .chat-input-wrapper {
#             position: fixed;
#             bottom: 100px;
#             right: 28px;
#             width: 380px;
#             z-index: 9998;
#         }
#         </style>
#         """,
#         unsafe_allow_html=True,
#     )


# # --------------------------------------------------------------------------
# # Backend call
# # --------------------------------------------------------------------------
# def get_bot_response(user_message: str) -> str:
#     try:
#         response = requests.post(
#             BACKEND_URL,
#             json={"message": user_message, "thread_id": THREAD_ID},
#             timeout=30,
#         )
#         response.raise_for_status()
#         return response.json().get("response", "Sorry, I didn't get a response.")
#     except requests.exceptions.RequestException as e:
#         return f"⚠️ Couldn't reach the assistant service ({e})."


# # --------------------------------------------------------------------------
# # UI pieces
# # --------------------------------------------------------------------------
# def render_toggle_button():
#     st.markdown('<div class="floating-toggle">', unsafe_allow_html=True)
#     icon = "✕" if st.session_state.chat_open else "🏸"
#     st.button(icon, key="chat_toggle_btn", on_click=toggle_chat)
#     st.markdown("</div>", unsafe_allow_html=True)


# def render_messages_html() -> str:
#     if not st.session_state.messages:
#         return '<div class="empty-state">👋 Ask me anything about your vendor account.</div>'

#     rows = []
#     for msg in st.session_state.messages:
#         role = msg["role"]
#         content = msg["content"].replace("<", "&lt;").replace(">", "&gt;")
#         rows.append(
#             f'<div class="bubble-row {role}"><div class="bubble {role}">{content}</div></div>'
#         )

#     if st.session_state.is_loading:
#         rows.append(
#             '<div class="bubble-row assistant"><div class="bubble assistant">'
#             '<span class="typing-dots"><span></span><span></span><span></span></span>'
#             "</div></div>"
#         )

#     return "".join(rows)


# def render_chat_panel():
#     st.markdown('<div class="chat-panel">', unsafe_allow_html=True)

#     st.markdown(
#         """
#         <div class="chat-header">
#             🏸 HobbyFi Vendor Copilot
#             <span class="chat-subtitle">&nbsp;· Powered by Groq + LangGraph</span>
#         </div>
#         """,
#         unsafe_allow_html=True,
#     )

#     st.markdown(
#         f'<div class="chat-body">{render_messages_html()}</div>',
#         unsafe_allow_html=True,
#     )

#     st.markdown("</div>", unsafe_allow_html=True)

#     # Input lives just below the panel, same width, still floating
#     st.markdown('<div class="chat-input-wrapper">', unsafe_allow_html=True)
#     prompt = st.chat_input("Ask anything...", key="floating_chat_input")
#     st.markdown("</div>", unsafe_allow_html=True)

#     return prompt


# def handle_new_message(prompt: str):
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     st.session_state.is_loading = True
#     st.rerun()


# def process_pending_response():
#     """After a rerun triggered by a new user message, fetch the bot reply."""
#     if st.session_state.is_loading and st.session_state.messages:
#         last_user_msg = st.session_state.messages[-1]
#         if last_user_msg["role"] == "user":
#             answer = get_bot_response(last_user_msg["content"])
#             st.session_state.messages.append({"role": "assistant", "content": answer})
#         st.session_state.is_loading = False
#         st.rerun()


# # --------------------------------------------------------------------------
# # Main app
# # --------------------------------------------------------------------------
# def main():
#     init_state()
#     inject_css()

#     st.title("🏸 HobbyFi Vendor Copilot")
#     st.caption("Powered by Groq + LangGraph")
#     st.write(
#         "Use the floating chat icon in the bottom-right corner to open the assistant."
#     )

#     render_toggle_button()

#     if st.session_state.chat_open:
#         prompt = render_chat_panel()
#         if prompt:
#             handle_new_message(prompt)

#     process_pending_response()


# if __name__ == "__main__":
#     main()




import streamlit as st
import requests

# --------------------------------------------------------------------------
# Page config
# --------------------------------------------------------------------------
st.set_page_config(
    page_title="HobbyFi Copilot",
    page_icon="🏸",
    layout="wide",
)

BACKEND_URL = "http://127.0.0.1:8000/chat"
THREAD_ID = "vendor_1"


# --------------------------------------------------------------------------
# Session state
# --------------------------------------------------------------------------
def init_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "chat_open" not in st.session_state:
        st.session_state.chat_open = False
    if "is_loading" not in st.session_state:
        st.session_state.is_loading = False


def toggle_chat():
    st.session_state.chat_open = not st.session_state.chat_open


# --------------------------------------------------------------------------
# Styling
# --------------------------------------------------------------------------
def inject_css():
    st.markdown(
        """
        <style>
        #MainMenu, footer {visibility: hidden;}

        /* ================= Floating toggle button ================= */
        .st-key-chat_toggle_container {
            position: fixed;
            bottom: 28px;
            right: 28px;
            z-index: 9999;
            width: 60px;
        }
        .st-key-chat_toggle_container button {
            width: 60px;
            height: 60px;
            border-radius: 50% !important;
            background: linear-gradient(135deg, #6C5CE7, #8E7CFF) !important;
            color: white !important;
            border: none !important;
            box-shadow: 0 8px 24px rgba(108, 92, 231, 0.45);
            transition: transform 0.15s ease, box-shadow 0.15s ease;
        }
        .st-key-chat_toggle_container button:hover {
            transform: scale(1.08);
            box-shadow: 0 10px 28px rgba(108, 92, 231, 0.6);
        }
        .st-key-chat_toggle_container button p {
            font-size: 22px !important;
            margin: 0 !important;
        }

        /* ================= Floating chat panel ================= */
        .st-key-chat_panel_container {
            position: fixed;
            bottom: 104px;
            right: 28px;
            width: 380px;
            max-height: 620px;
            background: #ffffff;
            border-radius: 18px;
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.20);
            z-index: 9998;
            overflow: hidden;
            border: 1px solid rgba(0,0,0,0.06);
            animation: slideUp 0.22s ease-out;
            display: flex;
            flex-direction: column;
        }

        @keyframes slideUp {
            from { opacity: 0; transform: translateY(16px); }
            to   { opacity: 1; transform: translateY(0); }
        }

        .chat-header {
            background: linear-gradient(135deg, #6C5CE7, #8E7CFF);
            color: white;
            padding: 16px 18px;
            font-weight: 600;
            font-size: 16px;
        }
        .chat-subtitle {
            font-size: 12px;
            font-weight: 400;
            opacity: 0.85;
            display: block;
            margin-top: 2px;
        }

        .chat-body {
            padding: 14px 16px;
            overflow-y: auto;
            max-height: 380px;
            background: #F7F7FB;
        }

        /* ---- Bubbles ---- */
        .bubble-row { display: flex; margin-bottom: 10px; }
        .bubble-row.user { justify-content: flex-end; }
        .bubble-row.assistant { justify-content: flex-start; }

        .bubble {
            max-width: 80%;
            padding: 10px 14px;
            border-radius: 16px;
            font-size: 14px;
            line-height: 1.45;
            word-wrap: break-word;
        }
        .bubble.user {
            background: #6C5CE7;
            color: white;
            border-bottom-right-radius: 4px;
        }
        .bubble.assistant {
            background: white;
            color: #2D2D2D;
            border: 1px solid #ECECF3;
            border-bottom-left-radius: 4px;
        }

        .typing-dots span {
            display: inline-block;
            width: 6px;
            height: 6px;
            margin-right: 3px;
            background: #A8A0E8;
            border-radius: 50%;
            animation: blink 1.2s infinite ease-in-out;
        }
        .typing-dots span:nth-child(2) { animation-delay: 0.2s; }
        .typing-dots span:nth-child(3) { animation-delay: 0.4s; }
        @keyframes blink {
            0%, 80%, 100% { opacity: 0.2; }
            40% { opacity: 1; }
        }

        .empty-state {
            text-align: center;
            color: #9A9AAE;
            font-size: 13px;
            margin-top: 30px;
        }

        /* Chat input rendered inside the panel container */
        .st-key-chat_panel_container div[data-testid="stChatInput"] {
            padding: 8px 12px 12px 12px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# --------------------------------------------------------------------------
# Backend call
# --------------------------------------------------------------------------
def get_bot_response(user_message: str) -> str:
    try:
        response = requests.post(
            BACKEND_URL,
            json={"message": user_message, "thread_id": THREAD_ID},
            timeout=30,
        )
        response.raise_for_status()
        return response.json().get("response", "Sorry, I didn't get a response.")
    except requests.exceptions.RequestException as e:
        return f"⚠️ Couldn't reach the assistant service ({e})."


# --------------------------------------------------------------------------
# UI pieces
# --------------------------------------------------------------------------
def render_toggle_button():
    with st.container(key="chat_toggle_container"):
        icon = "✕" if st.session_state.chat_open else "🏸"
        st.button(icon, key="chat_toggle_btn", on_click=toggle_chat)


def render_messages_html() -> str:
    if not st.session_state.messages:
        return '<div class="empty-state">👋 Ask me anything about your vendor account.</div>'

    rows = []
    for msg in st.session_state.messages:
        role = msg["role"]
        content = msg["content"].replace("<", "&lt;").replace(">", "&gt;")
        rows.append(
            f'<div class="bubble-row {role}"><div class="bubble {role}">{content}</div></div>'
        )

    if st.session_state.is_loading:
        rows.append(
            '<div class="bubble-row assistant"><div class="bubble assistant">'
            '<span class="typing-dots"><span></span><span></span><span></span></span>'
            "</div></div>"
        )

    return "".join(rows)


def render_chat_panel():
    with st.container(key="chat_panel_container"):
        st.markdown(
            """
            <div class="chat-header">
                🏸 HobbyFi Vendor Copilot
                <span class="chat-subtitle">Your personal assistant</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            f'<div class="chat-body">{render_messages_html()}</div>',
            unsafe_allow_html=True,
        )

        prompt = st.chat_input("Ask anything...", key="floating_chat_input")

    return prompt


def handle_new_message(prompt: str):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.is_loading = True
    st.rerun()


def process_pending_response():
    """After a rerun triggered by a new user message, fetch the bot reply."""
    if st.session_state.is_loading and st.session_state.messages:
        last_user_msg = st.session_state.messages[-1]
        if last_user_msg["role"] == "user":
            answer = get_bot_response(last_user_msg["content"])
            st.session_state.messages.append({"role": "assistant", "content": answer})
        st.session_state.is_loading = False
        st.rerun()


# --------------------------------------------------------------------------
# Main app
# --------------------------------------------------------------------------
def main():
    init_state()
    inject_css()

    st.title("🏸 HobbyFi Vendor Copilot")
    
    render_toggle_button()

    if st.session_state.chat_open:
        prompt = render_chat_panel()
        if prompt:
            handle_new_message(prompt)

    process_pending_response()


if __name__ == "__main__":
    main()