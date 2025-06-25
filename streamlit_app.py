import streamlit as st
from agent_host import AgentHost

st.set_page_config(page_title="Scientific‑Paper Scout", layout="wide")
st.title("🔬 Scientific‑Paper Scout")

agent = AgentHost()

# Sidebar: Show current LLM provider/model
st.sidebar.header("LLM Configuration")
st.sidebar.write(f"**Provider:** {agent.llm_provider}")
st.sidebar.write(f"**Model:** {agent.llm_model}")

# Main UI
st.markdown("""
Type a command below:
- `search <topic>` to find recent papers
- `summarize <pdf_url>` to summarize a paper
""")

if 'history' not in st.session_state:
    st.session_state['history'] = []

user_input = st.text_input("Your message", key="user_input")
submit = st.button("Send")

if submit and user_input.strip():
    st.session_state['history'].append(("You", user_input))
    with st.spinner("Thinking..."):
        response_stream = agent.handle_user_message(user_input)
        response_lines = []
        for line in response_stream:
            response_lines.append(line)
        st.session_state['history'].append(("Assistant", "\n".join(response_lines)))
    st.experimental_rerun()

# Display chat history
for sender, message in st.session_state['history']:
    if sender == "You":
        st.markdown(f"**You:** {message}")
    else:
        st.markdown(f"<div style='background:#f0f2f6;padding:10px;border-radius:8px'><b>Assistant:</b><br>{message}</div>", unsafe_allow_html=True) 