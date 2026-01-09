import streamlit as st
import google.generativeai as genai

# 1. Setup Streamlit Page
st.set_page_config(page_title="Gemini Chatbot", layout="centered")
st.title("🤖 Simple Gemini Chatbot")

# 2. Sidebar for API Key
with st.sidebar:
    st.title("Settings")
    api_key = st.text_input("AIzaSyBm9_QJLHP8S9i-q_3XLIwelheoIVDnJQE", type="password")
    st.info("Get a key at [Google AI Studio](https://aistudio.google.com/)")

# 3. Configure Gemini API
if api_key:
    genai.configure(api_key=api_key)
    # UPDATED: Use gemini-2.5-flash (Gemini 1.5 is retired)
    # Use 'gemini-3-flash-preview' if you want the very latest features
    model = genai.GenerativeModel("gemini-2.5-flash")
else:
    st.warning("Please enter your API Key in the sidebar to begin.")
    st.stop()

# 4. Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. Display Chat Messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. Chat Input Logic
if prompt := st.chat_input("How can I help you today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Use streaming for better experience
            response = model.generate_content(prompt, stream=True)
            full_response = st.write_stream(chunk.text for chunk in response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error(f"Error: {e}")