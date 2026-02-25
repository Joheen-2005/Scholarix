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

# ==============================
# INJECT CUSTOM CSS + ANIMATIONS
# ==============================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;800;900&family=Rajdhani:wght@300;400;500;600&family=Share+Tech+Mono&display=swap');

*, *::before, *::after { box-sizing: border-box; }

:root {
  --void:    #010409;
  --deep:    #060d1a;
  --surface: #0a1628;
  --glass:   rgba(10,22,44,0.72);
  --border:  rgba(0,212,255,0.18);
  --cyan:    #00d4ff;
  --teal:    #00ffcc;
  --violet:  #7b2fff;
  --gold:    #ffd166;
  --txt:     #c8d8f0;
  --txt-dim: #4a6080;
  --glow-c:  rgba(0,212,255,0.4);
}

html, body, .stApp {
  background: var(--void) !important;
  color: var(--txt) !important;
  font-family: 'Rajdhani', sans-serif !important;
}

.stApp::before {
  content: '';
  position: fixed;
  inset: 0;
  background:
    radial-gradient(ellipse 80% 50% at 20% 10%, rgba(0,212,255,0.08) 0%, transparent 60%),
    radial-gradient(ellipse 60% 40% at 80% 80%, rgba(123,47,255,0.10) 0%, transparent 60%),
    radial-gradient(ellipse 50% 60% at 50% 50%, rgba(0,255,204,0.04) 0%, transparent 70%);
  pointer-events: none;
  z-index: 0;
  animation: nebulaPulse 12s ease-in-out infinite alternate;
}
@keyframes nebulaPulse {
  0%   { opacity:0.6; transform:scale(1); }
  100% { opacity:1;   transform:scale(1.04); }
}

.stApp::after {
  content: '';
  position: fixed;
  inset: 0;
  background-image:
    linear-gradient(rgba(0,212,255,0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0,212,255,0.03) 1px, transparent 1px);
  background-size: 48px 48px;
  pointer-events: none;
  z-index: 0;
}

/* ── HEADER ── */
.scholaris-header {
  position: relative;
  text-align: center;
  padding: 3.5rem 2rem 2.5rem;
  margin-bottom: 2rem;
  overflow: hidden;
}
.scholaris-header::before {
  content: '';
  position: absolute;
  left:50%; top:50%;
  transform: translate(-50%,-50%);
  width:600px; height:200px;
  background: radial-gradient(ellipse, rgba(0,212,255,0.12) 0%, transparent 70%);
  border-radius: 50%;
  animation: headerGlow 4s ease-in-out infinite alternate;
  pointer-events: none;
}
@keyframes headerGlow {
  0%   { opacity:0.5; transform:translate(-50%,-50%) scale(0.9); }
  100% { opacity:1;   transform:translate(-50%,-50%) scale(1.1); }
}
.scholaris-logo-line {
  font-family: 'Orbitron', monospace;
  font-size: clamp(2rem,5vw,3.8rem);
  font-weight: 900;
  letter-spacing: 0.12em;
  background: linear-gradient(135deg,#00d4ff 0%,#00ffcc 40%,#7b2fff 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  background-size: 200% auto;
  animation: logoShimmer 3s linear infinite;
}
@keyframes logoShimmer {
  0%   { background-position:0% center; }
  100% { background-position:200% center; }
}
.scholaris-sub {
  font-family: 'Share Tech Mono', monospace;
  font-size: 0.78rem;
  letter-spacing: 0.25em;
  color: var(--txt-dim);
  text-transform: uppercase;
  margin-top: 0.6rem;
  animation: fadeInUp 1s ease 0.4s both;
}
.scholaris-desc {
  font-family: 'Rajdhani', sans-serif;
  font-size: 1.05rem;
  font-weight: 300;
  color: rgba(200,216,240,0.6);
  margin-top: 0.9rem;
  max-width: 700px;
  margin-left: auto;
  margin-right: auto;
  animation: fadeInUp 1s ease 0.7s both;
}
@keyframes fadeInUp {
  from { opacity:0; transform:translateY(16px); }
  to   { opacity:1; transform:translateY(0); }
}
.status-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  font-family: 'Share Tech Mono', monospace;
  font-size: 0.7rem;
  letter-spacing: 0.15em;
  color: var(--teal);
  padding: 0.25rem 0.75rem;
  border: 1px solid rgba(0,255,204,0.25);
  border-radius: 99px;
  background: rgba(0,255,204,0.05);
}
.status-dot {
  width:6px; height:6px;
  border-radius:50%;
  background: var(--teal);
  box-shadow: 0 0 6px var(--teal);
  animation: pulse 2s ease-in-out infinite;
}
@keyframes pulse { 0%,100%{opacity:1;} 50%{opacity:0.3;} }

.holo-divider {
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--cyan), var(--teal), var(--violet), transparent);
  margin: 1.2rem 0;
  background-size: 200% 100%;
  animation: dividerScan 3s linear infinite;
}
@keyframes dividerScan {
  0%   { background-position:-100% 0; }
  100% { background-position:200% 0; }
}

/* ── SIDEBAR ── */
section[data-testid="stSidebar"] {
  background: linear-gradient(180deg, var(--deep) 0%, var(--surface) 100%) !important;
  border-right: 1px solid var(--border) !important;
}
section[data-testid="stSidebar"] * {
  font-family: 'Rajdhani', sans-serif !important;
  color: var(--txt) !important;
}
section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stSlider label {
  font-family: 'Share Tech Mono', monospace !important;
  font-size: 0.75rem !important;
  letter-spacing: 0.15em !important;
  color: var(--cyan) !important;
  text-transform: uppercase;
}
.sidebar-title {
  font-family: 'Orbitron', monospace;
  font-size: 0.95rem;
  font-weight: 600;
  letter-spacing: 0.15em;
  color: var(--cyan);
  padding: 0.8rem 1.2rem;
  border: 1px solid var(--border);
  border-radius: 8px;
  background: rgba(0,212,255,0.06);
  margin-bottom: 1.4rem;
  text-align: center;
  text-transform: uppercase;
}

/* ── SELECT BOX ── */
.stSelectbox > div > div {
  background: var(--glass) !important;
  border: 1px solid var(--border) !important;
  border-radius: 10px !important;
  color: var(--txt) !important;
  font-family: 'Rajdhani', sans-serif !important;
  font-size: 1rem !important;
  backdrop-filter: blur(12px);
  transition: border-color 0.3s, box-shadow 0.3s;
}
.stSelectbox > div > div:hover,
.stSelectbox > div > div:focus-within {
  border-color: var(--cyan) !important;
  box-shadow: 0 0 16px var(--glow-c) !important;
}

/* ── TEXT AREA ── */
.stTextArea textarea {
  background: var(--glass) !important;
  border: 1px solid var(--border) !important;
  border-radius: 12px !important;
  color: var(--txt) !important;
  font-family: 'Rajdhani', sans-serif !important;
  font-size: 1.05rem !important;
  backdrop-filter: blur(12px);
  padding: 1rem 1.2rem !important;
  transition: border-color 0.3s, box-shadow 0.3s;
}
.stTextArea textarea:focus {
  border-color: var(--cyan) !important;
  box-shadow: 0 0 20px var(--glow-c) !important;
  outline: none !important;
}
.stTextArea label {
  font-family: 'Share Tech Mono', monospace !important;
  font-size: 0.78rem !important;
  letter-spacing: 0.18em !important;
  color: var(--cyan) !important;
  text-transform: uppercase;
}

/* ── BUTTON ── */
.stButton > button {
  width: 100%;
  padding: 1rem 2rem !important;
  background: linear-gradient(135deg, rgba(0,212,255,0.15), rgba(123,47,255,0.15)) !important;
  border: 1px solid var(--cyan) !important;
  border-radius: 12px !important;
  color: var(--cyan) !important;
  font-family: 'Orbitron', monospace !important;
  font-size: 0.82rem !important;
  font-weight: 600 !important;
  letter-spacing: 0.22em !important;
  text-transform: uppercase !important;
  position: relative;
  overflow: hidden;
  transition: all 0.35s ease !important;
  backdrop-filter: blur(8px);
}
.stButton > button::before {
  content: '';
  position: absolute;
  top:-50%; left:-60%;
  width:40%; height:200%;
  background: rgba(255,255,255,0.06);
  transform: skewX(-20deg);
  transition: left 0.5s ease;
}
.stButton > button:hover {
  background: linear-gradient(135deg, rgba(0,212,255,0.28), rgba(123,47,255,0.28)) !important;
  box-shadow: 0 0 28px var(--glow-c), 0 0 60px rgba(0,212,255,0.15) !important;
  transform: translateY(-2px) !important;
}
.stButton > button:hover::before { left:160%; }
.stButton > button:active { transform: translateY(0) !important; }

/* ── OUTPUT CARD ── */
.output-card {
  background: var(--glass);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 2rem 2.4rem;
  backdrop-filter: blur(16px);
  margin-top: 1.5rem;
  position: relative;
  overflow: hidden;
  animation: cardReveal 0.6s cubic-bezier(0.16,1,0.3,1) both;
}
.output-card::before {
  content: '';
  position: absolute;
  top:0; left:0; right:0;
  height: 2px;
  background: linear-gradient(90deg, var(--violet), var(--cyan), var(--teal));
  background-size: 200% 100%;
  animation: topBarScan 2.5s linear infinite;
}
@keyframes topBarScan {
  0%   { background-position:-100% 0; }
  100% { background-position:200% 0; }
}
@keyframes cardReveal {
  from { opacity:0; transform:translateY(24px) scale(0.98); }
  to   { opacity:1; transform:translateY(0) scale(1); }
}
.output-card h1,.output-card h2,.output-card h3 {
  font-family: 'Orbitron', monospace !important;
  color: var(--cyan) !important;
  letter-spacing: 0.08em;
}
.output-card p,.output-card li {
  font-family: 'Rajdhani', sans-serif !important;
  font-size: 1.02rem !important;
  line-height: 1.75 !important;
  color: var(--txt) !important;
}
.output-card code {
  font-family: 'Share Tech Mono', monospace !important;
  background: rgba(0,212,255,0.08) !important;
  color: var(--teal) !important;
  padding: 0.1em 0.4em;
  border-radius: 4px;
}

/* ── NOVELTY CARD ── */
.novelty-card {
  background: linear-gradient(135deg, rgba(0,22,44,0.85), rgba(10,0,30,0.85));
  border: 1px solid rgba(123,47,255,0.3);
  border-radius: 16px;
  padding: 1.8rem 2rem;
  margin-top: 1.5rem;
  backdrop-filter: blur(16px);
  position: relative;
  overflow: hidden;
  animation: cardReveal 0.6s cubic-bezier(0.16,1,0.3,1) 0.2s both;
}
.novelty-card::before {
  content: '';
  position: absolute;
  top:0; left:0; right:0;
  height: 2px;
  background: linear-gradient(90deg, var(--violet), var(--gold));
}
.novelty-label {
  font-family: 'Share Tech Mono', monospace;
  font-size: 0.72rem;
  letter-spacing: 0.25em;
  color: var(--txt-dim);
  text-transform: uppercase;
}
.novelty-score-display {
  font-family: 'Orbitron', monospace;
  font-size: 4rem;
  font-weight: 800;
  line-height: 1;
  margin: 0.5rem 0;
}
.novelty-bar-track {
  height: 6px;
  background: rgba(255,255,255,0.06);
  border-radius: 99px;
  overflow: hidden;
  margin: 1rem 0 0.5rem;
}
.novelty-bar-fill {
  height: 100%;
  border-radius: 99px;
  animation: barGrow 1.4s cubic-bezier(0.16,1,0.3,1) both;
}
@keyframes barGrow { from { width:0; } }

/* ── SECTION LABEL ── */
.section-label {
  font-family: 'Share Tech Mono', monospace;
  font-size: 0.72rem;
  letter-spacing: 0.3em;
  color: var(--txt-dim);
  text-transform: uppercase;
  margin-bottom: 0.6rem;
  display: flex;
  align-items: center;
  gap: 0.6rem;
}
.section-label::before {
  content: '';
  display: inline-block;
  width: 20px; height: 1px;
  background: var(--cyan);
}

/* ── SPINNER ── */
.stSpinner > div > div { border-top-color: var(--cyan) !important; }

/* ── ALERTS ── */
.stSuccess { border-radius:10px !important; border-left:3px solid var(--teal) !important; background:rgba(0,255,204,0.06) !important; }
.stInfo    { border-radius:10px !important; border-left:3px solid var(--cyan) !important; background:rgba(0,212,255,0.06) !important; }
.stWarning { border-radius:10px !important; border-left:3px solid var(--gold) !important; background:rgba(255,209,102,0.06) !important; }
.stError   { border-radius:10px !important; border-left:3px solid #ff4d6d !important; background:rgba(255,77,109,0.06) !important; }

/* ── METRIC ── */
[data-testid="stMetric"] {
  background: var(--glass) !important;
  border: 1px solid var(--border) !important;
  border-radius: 12px !important;
  padding: 1rem 1.4rem !important;
}
[data-testid="stMetricLabel"] {
  font-family: 'Share Tech Mono', monospace !important;
  font-size: 0.72rem !important;
  letter-spacing: 0.2em !important;
  color: var(--txt-dim) !important;
}
[data-testid="stMetricValue"] {
  font-family: 'Orbitron', monospace !important;
  color: var(--cyan) !important;
}

/* ── SLIDER ── */
.stSlider [data-baseweb="slider"] div[role="slider"] {
  background: var(--cyan) !important;
  border-color: var(--cyan) !important;
}

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width:6px; }
::-webkit-scrollbar-track { background: var(--deep); }
::-webkit-scrollbar-thumb { background: rgba(0,212,255,0.3); border-radius:3px; }
::-webkit-scrollbar-thumb:hover { background: var(--cyan); }

/* ── PARTICLES ── */
.particle-field {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 1;
  overflow: hidden;
}
.particle {
  position: absolute;
  border-radius: 50%;
  opacity: 0;
  animation: floatParticle linear infinite;
}
@keyframes floatParticle {
  0%   { transform:translateY(100vh) scale(0); opacity:0; }
  10%  { opacity:0.6; }
  90%  { opacity:0.3; }
  100% { transform:translateY(-10vh) scale(1.5); opacity:0; }
}
</style>
""", unsafe_allow_html=True)

# ── FLOATING PARTICLES
import random
particles_html = '<div class="particle-field">'
colors = ["#00d4ff","#00ffcc","#7b2fff","#ffd166"]
for i in range(20):
    left  = random.randint(2, 98)
    dur   = random.uniform(8, 20)
    delay = random.uniform(0, 15)
    size  = random.choice([1,1,2,2,3])
    color = random.choice(colors)
    particles_html += (
        f'<div class="particle" style="left:{left}%;width:{size}px;height:{size}px;'
        f'background:{color};animation-duration:{dur:.1f}s;animation-delay:{delay:.1f}s;"></div>'
    )
particles_html += '</div>'
st.markdown(particles_html, unsafe_allow_html=True)

# ── HEADER
st.markdown("""
<div class="scholaris-header">
  <div class="scholaris-logo-line">◈ SCHOLARIS</div>
  <div class="scholaris-sub">Multi-Agent Research Intelligence System · v2.0</div>
  <div class="scholaris-desc">
    AI Assistant for Literature Mining, Gap Detection,
    Methodology Design, IEEE Drafting &amp; Grant Proposal Generation
  </div>
  <div style="margin-top:1.2rem;">
    <span class="status-badge">
      <span class="status-dot"></span> SYSTEM ONLINE
    </span>
  </div>
</div>
<div class="holo-divider"></div>
""", unsafe_allow_html=True)

# ==============================
# SIDEBAR
# ==============================
st.sidebar.markdown('<div class="sidebar-title">🧠 Research Agents</div>', unsafe_allow_html=True)

agent = st.sidebar.selectbox(
    "Select Agent",
    [
        "Literature Mining",
        "Trend Analysis",
        "Research Gap Identification",
        "Methodology Design",
        "IEEE Draft Generation",
        "Grant Proposal Generation",
        "Citation Generator"
    ]
)

temperature = st.sidebar.slider("Creativity Level", 0.0, 1.0, 0.4)

agent_icons = {
    "Literature Mining":           ("🔍", "Scans core themes, key authors, datasets & limitations."),
    "Trend Analysis":              ("📈", "Maps 5-year evolution and emerging future directions."),
    "Research Gap Identification": ("🕳️", "Surfaces underexplored areas and innovation openings."),
    "Methodology Design":          ("⚙️", "Designs architecture, metrics & experimental setup."),
    "IEEE Draft Generation":       ("📄", "Generates full IEEE-structured paper draft."),
    "Grant Proposal Generation":   ("💰", "Crafts funding-ready proposals with budget justification."),
    "Citation Generator":          ("✅", "Generates accurate citations in APA, MLA, IEEE & Chicago styles."),
}
icon, desc = agent_icons.get(agent, ("🤖", ""))
st.sidebar.markdown(f"""
<div style="background:rgba(0,212,255,0.05);border:1px solid rgba(0,212,255,0.15);
            border-radius:12px;padding:1rem 1.2rem;margin-top:1rem;">
  <div style="font-family:'Orbitron',monospace;font-size:1.2rem;margin-bottom:0.5rem;">{icon}</div>
  <div style="font-family:'Share Tech Mono',monospace;font-size:0.7rem;color:#00d4ff;
              letter-spacing:0.15em;text-transform:uppercase;margin-bottom:0.4rem;">{agent}</div>
  <div style="font-family:'Rajdhani',sans-serif;font-size:0.9rem;
              color:rgba(200,216,240,0.6);line-height:1.5;">{desc}</div>
</div>
""", unsafe_allow_html=True)

# ==============================
# INPUT AREA
# ==============================
topic = st.text_area(
    "Enter Research Topic",
    height=150,
    placeholder="Example: Federated Learning for Healthcare Data Privacy"
)

st.markdown('<br>', unsafe_allow_html=True)

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
    elif agent == "Citation Generator":
        return f"""
Generate comprehensive citations for the research topic: {topic}

Provide citations in the following formats:
- APA (7th edition)
- MLA (9th edition)
- IEEE
- Chicago

For each format include:
- 5 highly relevant academic references with full citation details
- In-text citation examples
- Brief note on when to use each citation style
"""

# ==============================
# SESSION STATE INIT
# ==============================
if "output" not in st.session_state:
    st.session_state.output = None
if "last_topic" not in st.session_state:
    st.session_state.last_topic = None
if "show_novelty" not in st.session_state:
    st.session_state.show_novelty = False

# ==============================
# BUTTONS ROW — Generate & Novelty side by side
# ==============================
col1, col2, col3, col4, col5 = st.columns([1, 2, 0.3, 2, 1])
with col2:
    clicked = st.button("🚀 Generate Research Intelligence")
with col4:
    novelty_clicked = st.button("🔬 Analyse Novelty Score")

if novelty_clicked:
    if topic.strip() == "":
        st.warning("Please enter a research topic.")
    else:
        st.session_state.last_topic = topic
        st.session_state.show_novelty = True

if clicked:
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
                st.session_state.output    = response.choices[0].message.content
                st.session_state.last_topic = topic
            except Exception as e:
                st.error(f"Error: {str(e)}")

# ── Show output if it exists (independent of novelty)
if st.session_state.output:
    st.success("Analysis Complete")

    st.markdown(f"""
    <div class="output-card">
      <div class="section-label" style="margin-bottom:1.2rem;">{agent} · Output</div>
    """, unsafe_allow_html=True)
    st.markdown(st.session_state.output)
    st.markdown("</div>", unsafe_allow_html=True)

# ── Show novelty independently — only needs topic, not output
if st.session_state.show_novelty:
    novelty_score = compute_novelty(st.session_state.last_topic)

    st.markdown("---")

    st.metric(
        label="Research Novelty Score",
        value=f"{novelty_score}/100"
    )

    if novelty_score > 75:
        bar_color   = "linear-gradient(90deg, #00ffcc, #00d4ff)"
        verdict     = "🚀 High novelty potential"
        verdict_col = "#00ffcc"
        st.success("High novelty potential 🚀")
    elif novelty_score > 50:
        bar_color   = "linear-gradient(90deg, #ffd166, #ff9f43)"
        verdict     = "⚡ Moderate novelty potential"
        verdict_col = "#ffd166"
        st.info("Moderate novelty potential ⚡")
    else:
        bar_color   = "linear-gradient(90deg, #ff4d6d, #c9184a)"
        verdict     = "⚠ Low novelty – consider refining idea"
        verdict_col = "#ff4d6d"
        st.warning("Low novelty – consider refining idea ⚠")

    st.markdown(f"""
    <div class="novelty-card">
      <div class="novelty-label">🔬 Novelty Score Analysis</div>
      <div class="novelty-score-display" style="background:{bar_color};
           -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">
        {novelty_score}<span style="font-size:1.8rem;font-weight:400;">/100</span>
      </div>
      <div class="novelty-bar-track">
        <div class="novelty-bar-fill" style="width:{novelty_score}%;background:{bar_color};"></div>
      </div>
      <div style="font-family:'Orbitron',monospace;font-size:0.82rem;
                  letter-spacing:0.12em;color:{verdict_col};margin-top:0.8rem;">
        {verdict}
      </div>
    </div>
    """, unsafe_allow_html=True)

# ── FOOTER
st.markdown("""
<div class="holo-divider" style="margin-top:3rem;"></div>
<div style="text-align:center;padding:1.2rem 0;font-family:'Share Tech Mono',monospace;
            font-size:0.68rem;letter-spacing:0.25em;color:rgba(74,96,128,0.6);">
  SCHOLARIS · MULTI-AGENT RESEARCH INTELLIGENCE · POWERED BY GROQ × LLAMA
</div>
""", unsafe_allow_html=True)
