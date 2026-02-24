import streamlit as st
from groq import Groq
from novelty_agent import compute_novelty
from config import GROQ_API_KEY  # Securely load API key

# ==============================
# Initialize GROQ client
# ==============================
client = Groq(api_key=GROQ_API_KEY)

# ==============================
# PAGE CONFIG
# ==============================
st.set_page_config(
    page_title="Scholaris",
    layout="wide",
    page_icon="📚"
)

st.title("📚 Scholaris - Multi-Agent Research Intelligence System")
st.markdown(
    "AI Assistant for Literature Mining, Gap Detection, "
    "Methodology Design, IEEE Drafting & Grant Proposal Generation"
)

# ==============================
# SIDEBAR
# ==============================
st.sidebar.title("🧠 Research Agents")

agent = st.sidebar.selectbox(
    "Select Agent",
    [
        "Literature Mining",
        "Trend Analysis",
        "Research Gap Identification",
        "Methodology Design",
        "IEEE Draft Generation",
        "Grant Proposal Generation"
    ]
)

temperature = st.sidebar.slider("Creativity Level", 0.0, 1.0, 0.4)

# ==============================
# INPUT AREA
# ==============================
topic = st.text_area(
    "Enter Research Topic",
    height=150,
    placeholder="Example: Federated Learning for Healthcare Data Privacy"
)

# ==============================
# PROMPT BUILDER
# ==============================
def build_prompt(agent, topic):
    if agent == "Literature Mining":
        return f"""
Analyze the research literature on: {topic}

Provide:
- Core themes
- Key authors
- Datasets
- Limitations
"""
    elif agent == "Trend Analysis":
        return f"""
Analyze emerging trends in: {topic}

Include:
- 5-year evolution
- Future directions
"""
    elif agent == "Research Gap Identification":
        return f"""
Identify research gaps in: {topic}

Provide:
- Underexplored areas
- Open challenges
- Innovation opportunities
"""
    elif agent == "Methodology Design":
        return f"""
Design experimental methodology for: {topic}

Include:
- Dataset
- Model architecture
- Metrics
- Experimental setup
"""
    elif agent == "IEEE Draft Generation":
        return f"""
Generate IEEE-style paper draft on: {topic}

Include:
- Abstract
- Introduction
- Methodology
- Results
- Conclusion
"""
    elif agent == "Grant Proposal Generation":
        return f"""
Generate funding-ready grant proposal on: {topic}

Include:
- Executive Summary
- Objectives
- Methodology
- Impact
- Budget justification
"""

# ==============================
# GENERATE BUTTON
# ==============================
if st.button("🚀 Generate Research Intelligence"):

    if topic.strip() == "":
        st.warning("Please enter a research topic.")
    else:
        with st.spinner("Scholarix analyzing research ecosystem..."):

            prompt = build_prompt(agent, topic)

            try:
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {"role": "system", "content": "You are an advanced AI research director."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=temperature,
                )

                output = response.choices[0].message.content

                st.success("Analysis Complete")
                st.markdown(output)

                # ==============================
                # NOVELTY SCORE SECTION
                # ==============================
                novelty_score = compute_novelty(topic)

                st.markdown("---")
                st.subheader("🔬 Novelty Score Analysis")

                st.metric(
                    label="Research Novelty Score",
                    value=f"{novelty_score}/100"
                )

                if novelty_score > 75:
                    st.success("High novelty potential 🚀")
                elif novelty_score > 50:
                    st.info("Moderate novelty potential ⚡")
                else:
                    st.warning("Low novelty – consider refining idea ⚠")

            except Exception as e:
                st.error(f"Error: {str(e)}")
