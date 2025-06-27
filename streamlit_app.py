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
    st.rerun()

# Display chat history
for sender, message in st.session_state['history']:
    if sender == "You":
        st.markdown(f"**You:** {message}")
    else:
        # Check if this is a search result (multiple papers, separated by ---)
        if message.strip().startswith("Title:") and '---' in message:
            papers = message.split('---')
            for paper in papers:
                lines = [l.strip() for l in paper.strip().split('\n') if l.strip()]
                if not lines:
                    continue
                title = authors = summary = link = None
                for line in lines:
                    if line.startswith("Title:"):
                        title = line.replace("Title:", "").strip()
                    elif line.startswith("Authors:"):
                        authors = line.replace("Authors:", "").strip()
                    elif line.startswith("Summary:"):
                        summary = line.replace("Summary:", "").strip()
                    elif line.startswith("Link:"):
                        link = line.replace("Link:", "").strip()
                if title or authors or summary or link:
                    with st.container():
                        st.markdown(
                            f"""
                            <div style='background:#fff;border:1px solid #e0e0e0;padding:16px;margin-bottom:12px;border-radius:10px;'>
                                <div style='font-size:1.1em;font-weight:bold;margin-bottom:4px'>{title if title else ''}</div>
                                <div style='color:#555;margin-bottom:4px'><b>Authors:</b> {authors if authors else ''}</div>
                                <div style='margin-bottom:8px'>{summary if summary else ''}</div>
                                {f'<a href="{link}" target="_blank">Read on arXiv</a>' if link else ''}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
        else:
            st.markdown(f"<div style='background:#f0f2f6;padding:10px;border-radius:8px'><b>Assistant:</b><br>{message}</div>", unsafe_allow_html=True) 