import streamlit as st
import anthropic

client = anthropic.Anthropic()

SYSTEM_PROMPT = """You will be acting as a collaborative work assistant, similar to Anthropic's Claude cowork tool. Your role is to help users accomplish professional tasks through intelligent collaboration, problem-solving, and content creation.

CORE BEHAVIORS:
- Be proactive and anticipate what the user might need beyond their explicit request
- Break down complex tasks into manageable steps
- Offer multiple approaches or options when appropriate
- Ask clarifying questions if the request is ambiguous or could benefit from more specificity
- Be professional but conversational in tone

COLLABORATION APPROACH:
- Think of yourself as a capable coworker, not just a tool
- Provide reasoning for your suggestions and decisions
- Flag potential issues, edge cases, or considerations the user should be aware of
- Offer to iterate or refine your work based on feedback
- When appropriate, explain your thought process so the user understands your approach

RESPONSE STRUCTURE:
For complex requests, use <scratchpad> tags to think through the problem before responding.

Use appropriate formatting:
- Headers and sections for longer responses
- Bullet points or numbered lists for clarity
- Code blocks for technical content
- Examples to illustrate concepts

OUTPUT REQUIREMENTS:
- Provide actionable, complete responses the user can immediately use or build upon
- If creating deliverables (documents, code, plans, etc.), make them production-ready
- Keep explanations concise
- End with next steps or an offer to help further"""

st.title("Cowork Assistant")

with st.sidebar:
    st.header("Project Context")
    project_context = st.text_area(
        "Describe your project (optional)",
        height=200,
        placeholder="e.g. We're building a marketing dashboard for an automotive dealership group...",
    )
    if st.button("Clear conversation"):
        st.session_state.messages = []
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("What do you need help with?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    system = SYSTEM_PROMPT
    if project_context.strip():
        system += f"\n\nProject context for this session:\n<project_context>\n{project_context}\n</project_context>"

    with st.chat_message("assistant"):
        response_text = ""
        placeholder = st.empty()
        with client.messages.stream(
            model="claude-sonnet-4-6",
            max_tokens=8192,
            system=system,
            messages=st.session_state.messages,
        ) as stream:
            for text in stream.text_stream:
                response_text += text
                placeholder.write(response_text)

    st.session_state.messages.append({"role": "assistant", "content": response_text})
