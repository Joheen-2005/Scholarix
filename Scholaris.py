import streamlit as st
from groq import Groq
from novelty_agent import compute_novelty
from config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)

st.set_page_config(page_title="Scholaris", layout="wide", page_icon="📚")

# ══════════════════════════════════════════════════════════════
#  CSS  —  Deep Navy · Neumorphic Dark · Electric Blue Accents
# ══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Instrument+Serif:ital@0;1&family=JetBrains+Mono:wght@300;400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; }

:root {
  --s0:  #060c18;
  --s1:  #0b1220;
  --s2:  #101a2e;
  --s3:  #162038;
  --s4:  #1c2840;
  --s5:  #22304c;

  --blue:        #4f8ef7;
  --blue-bright: #7ab2ff;
  --blue-dim:    #2a5fc4;
  --blue-glow:   rgba(79,142,247,0.22);
  --blue-tint:   rgba(79,142,247,0.09);

  --teal:    #2dd4b4;
  --violet:  #8b6ef5;
  --amber:   #f5a623;
  --rose:    #f56565;
  --green:   #38d9a9;

  --t1: #f0f6ff;
  --t2: #c8d8f0;
  --t3: #8fa0c4;
  --t4: #5a6e96;

  --b1: rgba(79,142,247,0.20);
  --b2: rgba(255,255,255,0.06);

  --neu-out: 6px 6px 18px rgba(0,0,0,0.60), -4px -4px 14px rgba(24,36,60,0.55);
  --neu-in:  inset 4px 4px 12px rgba(0,0,0,0.55), inset -3px -3px 10px rgba(24,36,60,0.50);
  --neu-sm:  3px 3px 10px rgba(0,0,0,0.50), -2px -2px 8px rgba(24,36,60,0.45);
}

html, body, .stApp {
  background: var(--s1) !important;
  color: var(--t2) !important;
  font-family: 'Plus Jakarta Sans', sans-serif !important;
}

/* Force all text visible */
.stApp, .stApp * { color: var(--t2); }
p, div, li, td, th, label { color: var(--t2) !important; }
h1,h2,h3,h4,h5,h6 { color: var(--t1) !important; font-family:'Plus Jakarta Sans',sans-serif !important; font-weight:700 !important; }
strong, b { color: var(--t1) !important; font-weight:700 !important; }
em, i     { color: var(--t3) !important; }
a         { color: var(--blue-bright) !important; }
code {
  font-family: 'JetBrains Mono', monospace !important;
  color: var(--teal) !important;
  background: rgba(45,212,180,0.09) !important;
  padding: 0.15em 0.45em; border-radius:5px; font-size:0.87em !important;
}

/* ── ANIMATED BACKGROUND ── */
.stApp::before {
  content:''; position:fixed; inset:0; z-index:0; pointer-events:none;
  background:
    radial-gradient(ellipse 58% 48% at 12% 18%,  rgba(79,142,247,0.13) 0%, transparent 60%),
    radial-gradient(ellipse 42% 40% at 88% 14%,  rgba(107,163,255,0.09) 0%, transparent 55%),
    radial-gradient(ellipse 48% 52% at 52% 90%,  rgba(45,212,180,0.07) 0%, transparent 60%),
    radial-gradient(ellipse 32% 32% at 78% 62%,  rgba(139,110,245,0.07) 0%, transparent 50%);
  animation: bgPulse 11s ease-in-out infinite alternate;
}
@keyframes bgPulse {
  0%   { opacity:.75; transform:scale(1.00); }
  50%  { opacity:.95; transform:scale(1.015); }
  100% { opacity:.80; transform:scale(1.03);  }
}
.stApp::after {
  content:''; position:fixed; inset:0; z-index:0; pointer-events:none;
  background: repeating-linear-gradient(
    0deg, transparent, transparent 3px,
    rgba(79,142,247,0.012) 3px, rgba(79,142,247,0.012) 4px
  );
  animation: scanSlide 22s linear infinite;
}
@keyframes scanSlide { 0%{background-position:0 0;} 100%{background-position:0 100%;} }

/* ── HEADER ── */
.sch-header {
  text-align:center;
  padding: 3.5rem 2rem 2.6rem;
  position:relative; z-index:5;
}
.sch-eyebrow {
  font-family:'JetBrains Mono',monospace;
  font-size:0.63rem; letter-spacing:0.35em; text-transform:uppercase;
  color: var(--blue-bright) !important;
  margin-bottom:1rem; opacity:0.88;
  animation: fadeUp 0.6s ease both;
}

/* ─── WORDMARK ROW: logo + "Scholaris" side by side ─── */
.sch-wordmark-row {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 1.3rem;
  animation: fadeUp 0.6s ease 0.08s both;
}
.sch-logo-icon {
  width:  clamp(80px, 8.5vw, 104px);
  height: clamp(80px, 8.5vw, 104px);
  flex-shrink: 0;
  filter:
    drop-shadow(0 0 20px rgba(79,142,247,0.70))
    drop-shadow(0 0 8px  rgba(45,212,180,0.40))
    drop-shadow(0 5px 14px rgba(0,0,0,0.60));
  animation: iconFloat 6s ease-in-out infinite alternate,
             fadeUp 0.6s ease 0.08s both;
}
@keyframes iconFloat {
  0%   { transform:translateY(0px)  scale(1.00); filter:drop-shadow(0 0 20px rgba(79,142,247,0.70)) drop-shadow(0 0 8px rgba(45,212,180,0.40)) drop-shadow(0 5px 14px rgba(0,0,0,0.60)); }
  50%  { transform:translateY(-8px) scale(1.025); filter:drop-shadow(0 0 32px rgba(79,142,247,0.90)) drop-shadow(0 0 14px rgba(45,212,180,0.60)) drop-shadow(0 8px 18px rgba(0,0,0,0.50)); }
  100% { transform:translateY(-3px) scale(1.01); filter:drop-shadow(0 0 22px rgba(79,142,247,0.75)) drop-shadow(0 0 9px rgba(45,212,180,0.45)) drop-shadow(0 5px 14px rgba(0,0,0,0.55)); }
}

/* SCHOLARIS WORDMARK */
.sch-wordmark {
  font-size: clamp(3.2rem, 6.5vw, 5.2rem) !important;
  font-weight: 400 !important;
  letter-spacing: -0.01em !important;
  line-height: 1.0 !important;
  white-space: nowrap !important;
  display: inline-block !important;
  background: none !important;
}
.sch-wordmark .wl {
  font-family: 'Instrument Serif', serif !important;
  font-size: clamp(3.2rem, 6.5vw, 5.2rem) !important;
  font-weight: 400 !important;
  color: #f0f6ff !important;
  -webkit-text-fill-color: #f0f6ff !important;
  opacity: 1 !important;
  display: inline !important;
  background: none !important;
}
.sch-wordmark .wl-r {
  font-family: 'Instrument Serif', serif !important;
  font-size: clamp(3.2rem, 6.5vw, 5.2rem) !important;
  font-weight: 400 !important;
  color: #6ba3ff !important;
  -webkit-text-fill-color: #6ba3ff !important;
  opacity: 1 !important;
  display: inline !important;
  background: none !important;
  text-shadow: 0 0 24px rgba(107,163,255,0.90), 0 0 10px rgba(107,163,255,0.60) !important;
}


.sch-tagline {
  font-size:0.95rem; font-weight:400;
  color: var(--t3) !important;
  margin-top:0.95rem; line-height:1.72;
  max-width:580px; margin-left:auto; margin-right:auto;
  animation: fadeUp 0.6s ease 0.2s both;
}
.sch-badge {
  display:inline-flex; align-items:center; gap:0.45rem;
  margin-top:1.5rem; padding:0.3rem 1rem; border-radius:99px;
  background:var(--blue-tint); border:1px solid var(--b1);
  font-family:'JetBrains Mono',monospace;
  font-size:0.6rem; letter-spacing:0.2em; text-transform:uppercase;
  color: var(--teal) !important;
  animation: fadeUp 0.6s ease 0.32s both;
}
.sch-badge-dot {
  width:6px; height:6px; border-radius:50%;
  background:var(--teal);
  box-shadow:0 0 8px rgba(45,212,180,0.70);
  animation: breathe 2.5s ease-in-out infinite;
}
@keyframes breathe { 0%,100%{opacity:1;} 50%{opacity:0.28;} }
@keyframes fadeUp  { from{opacity:0;transform:translateY(13px);} to{opacity:1;transform:translateY(0);} }

.sch-divider {
  border:none; height:1px;
  background:linear-gradient(90deg, transparent, rgba(79,142,247,0.40), rgba(139,110,245,0.25), transparent);
  margin: 0.5rem auto 2.5rem; max-width:800px;
  animation: divPulse 4s ease-in-out infinite alternate;
}
@keyframes divPulse { 0%{opacity:0.40;} 100%{opacity:0.88;} }

/* ── SIDEBAR ── */
section[data-testid="stSidebar"] {
  background:var(--s2) !important;
  border-right:1px solid var(--b1) !important;
  box-shadow:5px 0 28px rgba(0,0,0,0.45) !important;
}
section[data-testid="stSidebar"] *,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] div,
section[data-testid="stSidebar"] label { color:var(--t2) !important; font-family:'Plus Jakarta Sans',sans-serif !important; }
section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] [data-testid="stWidgetLabel"],
section[data-testid="stSidebar"] .stSlider label {
  font-family:'JetBrains Mono',monospace !important;
  font-size:0.62rem !important; letter-spacing:0.22em !important;
  text-transform:uppercase !important; color:var(--t3) !important;
}
.sb-brand {
  display:flex; align-items:center; gap:0.6rem;
  padding:0.9rem 1.2rem;
  background:var(--s3); border:1px solid var(--b1);
  border-radius:14px; box-shadow:var(--neu-sm);
  margin-bottom:1.6rem;
  font-family:'Plus Jakarta Sans',sans-serif;
  font-size:1rem; font-weight:700; color:var(--t1) !important;
}
.sb-agent-card {
  background:var(--s3); border:1px solid var(--b1);
  border-radius:14px; box-shadow:var(--neu-in);
  padding:1.2rem 1.3rem; margin-top:0.8rem;
}
.sb-agent-icon  { font-size:1.6rem; margin-bottom:0.5rem; }
.sb-agent-name  {
  font-family:'JetBrains Mono',monospace; font-size:0.62rem;
  letter-spacing:0.2em; text-transform:uppercase;
  color:var(--blue-bright) !important; margin-bottom:0.4rem; font-weight:500;
}
.sb-agent-desc  { font-size:0.86rem; font-weight:400; color:var(--t3) !important; line-height:1.6; }

/* ── SELECT BOX ── */
.stSelectbox > div > div {
  background:var(--s3) !important; border:1px solid var(--b1) !important;
  border-radius:14px !important; color:var(--t1) !important;
  font-family:'Plus Jakarta Sans',sans-serif !important;
  font-size:0.95rem !important; font-weight:500 !important;
  box-shadow:var(--neu-sm) !important; transition:border-color 0.2s,box-shadow 0.2s;
}
.stSelectbox > div > div:hover {
  border-color:var(--blue) !important;
  box-shadow:var(--neu-sm), 0 0 0 3px var(--blue-glow) !important;
}
[data-baseweb="popover"] {
  background:var(--s3) !important; border:1px solid var(--b1) !important;
  border-radius:14px !important; box-shadow:0 12px 40px rgba(0,0,0,0.65) !important;
}
[data-baseweb="menu"] li, [data-baseweb="menu"] li * {
  color:var(--t2) !important; font-family:'Plus Jakarta Sans',sans-serif !important; font-size:0.92rem !important;
}
[data-baseweb="menu"] li:hover,[data-baseweb="menu"] li[aria-selected="true"] {
  background:var(--s4) !important; color:var(--t1) !important;
}

/* ── TEXT AREA ── */
.stTextArea label,
.stTextArea [data-testid="stWidgetLabel"],
.stTextArea [data-testid="stWidgetLabel"] * {
  font-family:'JetBrains Mono',monospace !important;
  font-size:0.63rem !important; letter-spacing:0.25em !important;
  text-transform:uppercase !important; color:var(--t3) !important;
}
.stTextArea textarea {
  background:var(--s2) !important; border:1px solid var(--b2) !important;
  border-radius:14px !important; color:var(--t1) !important;
  font-family:'Plus Jakarta Sans',sans-serif !important;
  font-size:0.97rem !important; font-weight:400 !important; line-height:1.75 !important;
  box-shadow:var(--neu-in) !important; padding:1.1rem 1.3rem !important;
  transition:border-color 0.2s,box-shadow 0.2s; caret-color:var(--blue-bright); resize:none;
}
.stTextArea textarea::placeholder { color:var(--t4) !important; font-style:italic; }
.stTextArea textarea:focus {
  outline:none !important; border-color:var(--blue) !important;
  box-shadow:var(--neu-in), 0 0 0 3px var(--blue-glow) !important;
}

/* ── BUTTONS ── */
.stButton > button {
  width:100% !important; padding:0.85rem 1.6rem !important;
  background:linear-gradient(135deg, var(--blue-dim) 0%, var(--blue) 100%) !important;
  border:1px solid rgba(122,178,255,0.42) !important;
  border-radius:14px !important; color:#ffffff !important;
  font-family:'Plus Jakarta Sans',sans-serif !important;
  font-size:0.9rem !important; font-weight:700 !important; letter-spacing:0.03em !important;
  box-shadow:0 4px 20px rgba(79,142,247,0.32), var(--neu-sm) !important;
  transition:all 0.22s ease !important; position:relative; overflow:hidden;
}
.stButton > button::before {
  content:''; position:absolute; inset:0; border-radius:14px;
  background:linear-gradient(180deg,rgba(255,255,255,0.10) 0%,transparent 100%);
  pointer-events:none;
}
.stButton > button:hover {
  transform:translateY(-2px) !important;
  box-shadow:0 8px 28px rgba(79,142,247,0.48), var(--neu-sm) !important;
  border-color:var(--blue-bright) !important; color:#ffffff !important;
}
.stButton > button:active { transform:translateY(0) !important; box-shadow:var(--neu-in) !important; }

/* second button — teal */
div[data-testid="column"]:nth-child(4) .stButton > button {
  background:linear-gradient(135deg,#1a8a74 0%, var(--teal) 100%) !important;
  border-color:rgba(45,212,180,0.42) !important;
  box-shadow:0 4px 20px rgba(45,212,180,0.28), var(--neu-sm) !important;
}
div[data-testid="column"]:nth-child(4) .stButton > button:hover {
  box-shadow:0 8px 28px rgba(45,212,180,0.42), var(--neu-sm) !important;
}

/* ── OUTPUT CARD ── */
.out-card {
  background:var(--s2); border:1px solid var(--b1); border-radius:20px;
  box-shadow:var(--neu-out); padding:2.2rem 2.6rem; margin-top:1.8rem;
  position:relative; overflow:hidden; z-index:2;
  animation: cardUp 0.5s cubic-bezier(0.16,1,0.3,1) both;
}
.out-card::before {
  content:''; position:absolute; top:0; left:0; right:0; height:2px;
  background:linear-gradient(90deg, var(--blue-dim), var(--blue-bright), var(--teal));
  background-size:200% 100%; animation:scanBar 3s linear infinite;
}
@keyframes scanBar { 0%{background-position:0% 0;} 100%{background-position:200% 0;} }
@keyframes cardUp  { from{opacity:0;transform:translateY(16px);} to{opacity:1;transform:translateY(0);} }

.out-tag {
  display:inline-flex; align-items:center; gap:0.38rem;
  font-family:'JetBrains Mono',monospace; font-size:0.6rem;
  letter-spacing:0.22em; text-transform:uppercase;
  color:var(--blue-bright) !important; background:var(--blue-tint);
  border:1px solid var(--b1); padding:0.22rem 0.75rem;
  border-radius:99px; margin-bottom:1.4rem; font-weight:500;
}
.out-card h1,.out-card h2,.out-card h3,
.out-card h4,.out-card h5,.out-card h6 {
  font-family:'Plus Jakarta Sans',sans-serif !important;
  color:var(--t1) !important; font-weight:700 !important;
  margin:1.2rem 0 0.5rem; line-height:1.3;
}
.out-card h1 { font-size:1.5rem !important; }
.out-card h2 { font-size:1.22rem !important; }
.out-card h3 { font-size:1.04rem !important; }
.out-card p,.out-card li {
  font-family:'Plus Jakarta Sans',sans-serif !important;
  font-size:0.95rem !important; font-weight:400 !important;
  line-height:1.80 !important; color:var(--t2) !important; margin-bottom:0.5rem;
}
.out-card strong,.out-card b { color:var(--t1) !important; font-weight:700 !important; }
.out-card em,.out-card i     { color:var(--t3) !important; }
.out-card code {
  font-family:'JetBrains Mono',monospace !important; font-size:0.85rem !important;
  background:rgba(45,212,180,0.09) !important; color:var(--teal) !important;
  padding:0.15em 0.5em; border-radius:5px; border:1px solid rgba(45,212,180,0.15);
}
.out-card hr { border:none; height:1px; background:linear-gradient(90deg,transparent,var(--b1),transparent); margin:1.4rem 0; }
.out-card .stMarkdown *           { color:var(--t2) !important; }
.out-card .stMarkdown strong,
.out-card .stMarkdown b           { color:var(--t1) !important; }
.out-card .stMarkdown h1,
.out-card .stMarkdown h2,
.out-card .stMarkdown h3          { color:var(--t1) !important; }
.out-card .stMarkdown code        { color:var(--teal) !important; }
.stMarkdown p  { color:var(--t2) !important; font-weight:400 !important; }
.stMarkdown li { color:var(--t2) !important; font-weight:400 !important; }
.stMarkdown h1,.stMarkdown h2,.stMarkdown h3 { color:var(--t1) !important; font-weight:700 !important; }
.stMarkdown strong,.stMarkdown b  { color:var(--t1) !important; font-weight:700 !important; }
.stMarkdown em,.stMarkdown i      { color:var(--t3) !important; }
.stMarkdown code                  { color:var(--teal) !important; }

/* ── NOVELTY CARD ── */
.nov-card {
  background:var(--s2); border:1px solid var(--b1); border-radius:20px;
  box-shadow:var(--neu-out); padding:2rem 2.5rem; margin-top:1.8rem;
  position:relative; overflow:hidden; z-index:2;
  animation:cardUp 0.5s cubic-bezier(0.16,1,0.3,1) 0.1s both;
}
.nov-card::before {
  content:''; position:absolute; top:0; left:0; right:0; height:2px;
  background:var(--bar-grad,linear-gradient(90deg,var(--blue),var(--teal)));
  opacity:0.9;
}
.nov-label {
  font-family:'JetBrains Mono',monospace; font-size:0.62rem;
  letter-spacing:0.25em; text-transform:uppercase; color:var(--t4) !important; margin-bottom:0.65rem;
}
.nov-num {
  font-family:'Instrument Serif',serif; font-size:5rem; font-weight:400;
  line-height:1; color:var(--t1) !important; letter-spacing:-0.03em;
}
.nov-denom { font-size:1.4rem; font-weight:300; color:var(--t4) !important; margin-left:0.1rem; }
.nov-track {
  height:4px; background:var(--s0); border-radius:99px;
  box-shadow:var(--neu-in); margin:1.2rem 0 0.8rem; overflow:hidden;
}
.nov-fill {
  height:100%; border-radius:99px; position:relative;
  animation:fillOut 1.3s cubic-bezier(0.16,1,0.3,1) both;
}
.nov-fill::after {
  content:''; position:absolute; top:0; left:0; right:0; height:50%;
  background:rgba(255,255,255,0.20); border-radius:99px;
}
@keyframes fillOut { from{width:0%;} }
.nov-verdict { font-size:0.88rem; font-weight:600; }

/* ── ALERTS ── */
div[data-testid="stAlert"] {
  background:var(--s3) !important; border:1px solid var(--b2) !important;
  border-radius:14px !important; box-shadow:var(--neu-sm) !important;
  font-family:'Plus Jakarta Sans',sans-serif !important;
  font-size:0.92rem !important; font-weight:500 !important;
}
div[data-testid="stAlert"] * { color:var(--t2) !important; }
.stSuccess { border-left:3px solid var(--green) !important; }
.stInfo    { border-left:3px solid var(--blue)  !important; }
.stWarning { border-left:3px solid var(--amber) !important; }
.stError   { border-left:3px solid var(--rose)  !important; }

/* ── METRIC ── */
[data-testid="stMetric"] {
  background:var(--s3) !important; border:1px solid var(--b1) !important;
  border-radius:16px !important; box-shadow:var(--neu-sm) !important; padding:1.2rem 1.6rem !important;
}
[data-testid="stMetricLabel"] {
  font-family:'JetBrains Mono',monospace !important; font-size:0.62rem !important;
  letter-spacing:0.22em !important; text-transform:uppercase !important; color:var(--t4) !important;
}
[data-testid="stMetricValue"] {
  font-family:'Instrument Serif',serif !important; color:var(--t1) !important; font-size:1.9rem !important;
}

/* ── SLIDER ── */
.stSlider [data-baseweb="slider"] > div:first-child {
  background:var(--s0) !important; box-shadow:var(--neu-in) !important;
  height:4px !important; border-radius:99px !important;
}
.stSlider [data-baseweb="slider"] div[role="slider"] {
  background:linear-gradient(135deg,var(--s4),var(--s3)) !important;
  box-shadow:var(--neu-out), 0 0 0 2px var(--blue-dim) !important;
  border:none !important; width:18px !important; height:18px !important;
}

/* ── SPINNER / SCROLLBAR ── */
.stSpinner > div > div { border-top-color:var(--blue) !important; }
::-webkit-scrollbar { width:5px; }
::-webkit-scrollbar-track { background:var(--s0); }
::-webkit-scrollbar-thumb { background:rgba(79,142,247,0.30); border-radius:4px; }
::-webkit-scrollbar-thumb:hover { background:rgba(79,142,247,0.55); }

/* ── FIX STREAMLIT WRAPPERS ── */
.stApp [data-testid="stVerticalBlock"],
.stApp [data-testid="stHorizontalBlock"],
.stApp .block-container,
.stApp .main { background:transparent !important; }
section[data-testid="stSidebar"] > div { background:var(--s2) !important; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  FLOATING PARTICLES
# ══════════════════════════════════════════════════════════════
import random
_ph = '<div style="position:fixed;inset:0;pointer-events:none;z-index:1;overflow:hidden;">'
for _ in range(18):
    l   = random.randint(2,98)
    dur = random.uniform(10,22)
    dly = random.uniform(0,16)
    sz  = random.choice([1,1,2,2,3])
    col = random.choice(["#4f8ef7","#2dd4b4","#8b6ef5","#7ab2ff"])
    op  = random.uniform(0.3,0.65)
    _ph += (f'<div style="position:absolute;border-radius:50%;left:{l}%;'
            f'width:{sz}px;height:{sz}px;background:{col};opacity:0;'
            f'animation:floatP {dur:.1f}s {dly:.1f}s linear infinite;"></div>')
_ph += '</div>'
_ph += """<style>
@keyframes floatP {
  0%   { transform:translateY(100vh) scale(0); opacity:0; }
  8%   { opacity:0.55; }
  92%  { opacity:0.25; }
  100% { transform:translateY(-8vh) scale(1.4); opacity:0; }
}
</style>"""
st.markdown(_ph, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  LOGO SVG — Scholar Cap + AI Neural Orb fused
# ══════════════════════════════════════════════════════════════
LOGO_SVG = """
<svg class="sch-logo-icon" viewBox="0 0 120 120" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <radialGradient id="oBG" cx="40%" cy="38%" r="62%">
      <stop offset="0%"   stop-color="#1c3870"/>
      <stop offset="50%"  stop-color="#0d1e4a"/>
      <stop offset="100%" stop-color="#050d22"/>
    </radialGradient>
    <radialGradient id="oLG" cx="38%" cy="32%" r="55%">
      <stop offset="0%"   stop-color="#7ab0ff" stop-opacity="0.50"/>
      <stop offset="60%"  stop-color="#4f8ef7" stop-opacity="0.15"/>
      <stop offset="100%" stop-color="#2a5fc4" stop-opacity="0.00"/>
    </radialGradient>
    <linearGradient id="rG" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%"   stop-color="#4f8ef7" stop-opacity="0.95"/>
      <stop offset="35%"  stop-color="#2dd4b4" stop-opacity="0.75"/>
      <stop offset="70%"  stop-color="#8b6ef5" stop-opacity="0.65"/>
      <stop offset="100%" stop-color="#4f8ef7" stop-opacity="0.90"/>
    </linearGradient>
    <linearGradient id="cFG" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%"   stop-color="#e8f1ff"/>
      <stop offset="40%"  stop-color="#bdd0f8"/>
      <stop offset="100%" stop-color="#90aee0"/>
    </linearGradient>
    <linearGradient id="cLG" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%"   stop-color="#6888c8"/>
      <stop offset="100%" stop-color="#334e98"/>
    </linearGradient>
    <linearGradient id="cRG" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%"   stop-color="#4a68b0"/>
      <stop offset="100%" stop-color="#1e3270"/>
    </linearGradient>
    <linearGradient id="bG" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%"   stop-color="#1a2e68"/>
      <stop offset="50%"  stop-color="#2a4a90"/>
      <stop offset="100%" stop-color="#162460"/>
    </linearGradient>
    <linearGradient id="tG" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%"   stop-color="#2dd4b4"/>
      <stop offset="100%" stop-color="#0a6050"/>
    </linearGradient>
    <linearGradient id="trG" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%"   stop-color="#4f8ef7" stop-opacity="0.0"/>
      <stop offset="50%"  stop-color="#6ba3ff" stop-opacity="0.65"/>
      <stop offset="100%" stop-color="#4f8ef7" stop-opacity="0.0"/>
    </linearGradient>
    <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="2.5" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="cGlow" x="-80%" y="-80%" width="260%" height="260%">
      <feGaussianBlur stdDeviation="5" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="dShadow">
      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#000918" flood-opacity="0.65"/>
    </filter>
    <filter id="cShadow">
      <feDropShadow dx="1" dy="3" stdDeviation="4" flood-color="#000918" flood-opacity="0.55"/>
    </filter>
    <clipPath id="bClip"><circle cx="60" cy="72" r="38"/></clipPath>
  </defs>

  <!-- Outer halo -->
  <circle cx="60" cy="72" r="47" fill="none" stroke="rgba(79,142,247,0.10)" stroke-width="6"/>
  <!-- Main orbital ring -->
  <circle cx="60" cy="72" r="42" fill="none" stroke="url(#rG)" stroke-width="1.2" opacity="0.80"/>
  <!-- Ring tick marks -->
  <g stroke="rgba(107,163,255,0.55)" stroke-width="1.5" stroke-linecap="round">
    <line x1="60"  y1="28"  x2="60"  y2="32"/>
    <line x1="89"  y1="37"  x2="87"  y2="40"/>
    <line x1="102" y1="72"  x2="98"  y2="72"/>
    <line x1="89"  y1="107" x2="87"  y2="104"/>
    <line x1="60"  y1="116" x2="60"  y2="112"/>
    <line x1="31"  y1="107" x2="33"  y2="104"/>
    <line x1="18"  y1="72"  x2="22"  y2="72"/>
    <line x1="31"  y1="37"  x2="33"  y2="40"/>
  </g>
  <!-- Dashed inner orbit -->
  <circle cx="60" cy="72" r="42" fill="none" stroke="rgba(45,212,180,0.14)"
    stroke-width="7" stroke-dasharray="4 18" stroke-linecap="round"/>

  <!-- AI Brain Orb -->
  <circle cx="60" cy="72" r="38" fill="url(#oBG)" filter="url(#dShadow)"/>
  <circle cx="60" cy="72" r="38" fill="url(#oLG)"/>
  <path d="M 28 57 A 38 38 0 0 1 92 57"
    stroke="rgba(255,255,255,0.09)" stroke-width="2" fill="none" stroke-linecap="round"/>

  <!-- Circuit traces -->
  <g clip-path="url(#bClip)" fill="none">
    <line x1="22" y1="64" x2="98" y2="64" stroke="url(#trG)" stroke-width="0.6"/>
    <line x1="22" y1="72" x2="98" y2="72" stroke="url(#trG)" stroke-width="0.6"/>
    <line x1="22" y1="80" x2="98" y2="80" stroke="url(#trG)" stroke-width="0.6"/>
    <line x1="42" y1="34" x2="42" y2="110" stroke="url(#trG)" stroke-width="0.6"/>
    <line x1="60" y1="34" x2="60" y2="110" stroke="url(#trG)" stroke-width="0.6"/>
    <line x1="78" y1="34" x2="78" y2="110" stroke="url(#trG)" stroke-width="0.6"/>
    <rect x="39.5" y="61.5" width="5" height="5" rx="1.2" fill="#4f8ef7" opacity="0.50"/>
    <rect x="75.5" y="61.5" width="5" height="5" rx="1.2" fill="#2dd4b4" opacity="0.50"/>
    <rect x="57.5" y="77.5" width="5" height="5" rx="1.2" fill="#8b6ef5" opacity="0.50"/>
    <rect x="39.5" y="77.5" width="5" height="5" rx="1.2" fill="#4f8ef7" opacity="0.35"/>
    <rect x="75.5" y="77.5" width="5" height="5" rx="1.2" fill="#2dd4b4" opacity="0.35"/>
  </g>

  <!-- Neural synapses -->
  <g clip-path="url(#bClip)" opacity="0.45" stroke="#6ba3ff" stroke-width="0.9" fill="none">
    <line x1="60" y1="50" x2="80" y2="62"/>
    <line x1="80" y1="62" x2="76" y2="83"/>
    <line x1="76" y1="83" x2="44" y2="83"/>
    <line x1="44" y1="83" x2="40" y2="62"/>
    <line x1="40" y1="62" x2="60" y2="50"/>
    <line x1="60" y1="50" x2="60" y2="72" stroke="#a8c8ff" stroke-width="0.65"/>
    <line x1="80" y1="62" x2="60" y2="72" stroke="#a8c8ff" stroke-width="0.65"/>
    <line x1="76" y1="83" x2="60" y2="72" stroke="#a8c8ff" stroke-width="0.65"/>
    <line x1="44" y1="83" x2="60" y2="72" stroke="#a8c8ff" stroke-width="0.65"/>
    <line x1="40" y1="62" x2="60" y2="72" stroke="#a8c8ff" stroke-width="0.65"/>
  </g>
  <!-- Neural nodes -->
  <g filter="url(#glow)" clip-path="url(#bClip)">
    <circle cx="60" cy="50" r="4.0" fill="#6ba3ff"/>
    <circle cx="80" cy="62" r="3.5" fill="#4f8ef7"/>
    <circle cx="76" cy="83" r="3.5" fill="#2dd4b4"/>
    <circle cx="44" cy="83" r="3.5" fill="#8b6ef5"/>
    <circle cx="40" cy="62" r="3.5" fill="#4f8ef7"/>
  </g>
  <g clip-path="url(#bClip)">
    <circle cx="60" cy="50" r="1.5" fill="#e8f4ff" opacity="0.95"/>
    <circle cx="80" cy="62" r="1.2" fill="#e8f4ff" opacity="0.85"/>
    <circle cx="76" cy="83" r="1.2" fill="#ddfdf5" opacity="0.85"/>
    <circle cx="44" cy="83" r="1.2" fill="#e8e0ff" opacity="0.85"/>
    <circle cx="40" cy="62" r="1.2" fill="#e8f4ff" opacity="0.85"/>
  </g>
  <!-- AI core nucleus -->
  <circle cx="60" cy="72" r="9"   fill="#3060c0" filter="url(#cGlow)" opacity="0.40"/>
  <circle cx="60" cy="72" r="6.5" fill="#2a52b8" opacity="0.92"/>
  <circle cx="60" cy="72" r="3.8" fill="#c0d8ff"/>
  <circle cx="58.5" cy="70.5" r="1.2" fill="white" opacity="0.75"/>

  <!-- Head band joining cap to orb -->
  <path d="M 46 42 Q 46 50 46 52 L 74 52 Q 74 50 74 42 Z" fill="url(#bG)" opacity="0.72"/>
  <ellipse cx="60" cy="42" rx="14" ry="4.5" fill="#1e3270" opacity="0.75"/>
  <ellipse cx="60" cy="52" rx="14" ry="4.0" fill="#2a4a90" opacity="0.55"/>

  <!-- Cap shadow beneath board -->
  <ellipse cx="60" cy="45" rx="26" ry="6.5" fill="rgba(0,0,0,0.35)" filter="url(#dShadow)"/>

  <!-- Mortarboard — 3-panel isometric -->
  <polygon points="60,20  34,31  34,35  60,24" fill="url(#cLG)" opacity="0.88"/>
  <polygon points="60,20  86,31  86,35  60,24" fill="url(#cRG)" opacity="0.80"/>
  <polygon points="60,10  86,23  60,36  34,23" fill="url(#cFG)" filter="url(#cShadow)" opacity="0.96"/>
  <polygon points="60,10  86,23  60,36  34,23" fill="none" stroke="rgba(220,235,255,0.35)" stroke-width="0.9"/>
  <line x1="60" y1="10" x2="34" y2="23" stroke="rgba(255,255,255,0.18)" stroke-width="1.2" stroke-linecap="round"/>

  <!-- Cap center seal -->
  <circle cx="60" cy="23" r="4.5" fill="#2a52b8" filter="url(#glow)" opacity="0.95"/>
  <circle cx="60" cy="23" r="2.5" fill="#c8dcff" opacity="0.98"/>
  <circle cx="59" cy="22" r="0.9" fill="white" opacity="0.80"/>

  <!-- Tassel cord -->
  <path d="M 82 24 C 96 28, 96 44, 88 52 C 84 58, 86 64, 86 70"
    stroke="url(#tG)" stroke-width="2.2" fill="none" stroke-linecap="round"/>
  <!-- Tassel knot -->
  <circle cx="86" cy="70" r="4.0" fill="#2dd4b4" filter="url(#glow)" opacity="0.95"/>
  <circle cx="86" cy="70" r="2.0" fill="#d8faf2" opacity="0.95"/>
  <circle cx="85.2" cy="69.2" r="0.7" fill="white" opacity="0.80"/>
  <!-- Tassel strands -->
  <g stroke-linecap="round">
    <line x1="82.5" y1="74" x2="79"  y2="84" stroke="#2dd4b4" stroke-width="1.3" opacity="0.88"/>
    <line x1="84.5" y1="74" x2="83"  y2="85" stroke="#20c0a0" stroke-width="1.3" opacity="0.85"/>
    <line x1="86"   y1="74" x2="87"  y2="85" stroke="#2dd4b4" stroke-width="1.3" opacity="0.82"/>
    <line x1="87.5" y1="74" x2="91"  y2="84" stroke="#16a888" stroke-width="1.2" opacity="0.75"/>
    <line x1="89"   y1="73" x2="94"  y2="82" stroke="#0e8870" stroke-width="1.0" opacity="0.65"/>
  </g>
  <!-- Strand tips -->
  <g filter="url(#glow)" opacity="0.80">
    <circle cx="79"  cy="84" r="1.4" fill="#2dd4b4"/>
    <circle cx="83"  cy="85" r="1.4" fill="#20c0a0"/>
    <circle cx="87"  cy="85" r="1.4" fill="#2dd4b4"/>
    <circle cx="91"  cy="84" r="1.2" fill="#16a888"/>
    <circle cx="94"  cy="82" r="1.0" fill="#0e8870"/>
  </g>
</svg>
"""

# ══════════════════════════════════════════════════════════════
#  HEADER
# ══════════════════════════════════════════════════════════════
# Build wordmark cleanly — pure string concat, no f-string issues
_wm = (
    '<div class="sch-wordmark">'
    '<span class="wl">S</span>'
    '<span class="wl">c</span>'
    '<span class="wl">h</span>'
    '<span class="wl">o</span>'
    '<span class="wl">l</span>'
    '<span class="wl">a</span>'
    '<span class="wl wl-r">r</span>'
    '<span class="wl">i</span>'
    '<span class="wl">s</span>'
    '</div>'
)
_header = (
    '<div class="sch-header">'
    '<div class="sch-eyebrow">Multi-Agent Research Intelligence &nbsp;&middot;&nbsp; v2.0</div>'
    '<div class="sch-wordmark-row">'
    + LOGO_SVG +
    _wm +
    '</div>'
    '<div class="sch-tagline">'
    'Literature Mining &nbsp;&middot;&nbsp; Gap Detection &nbsp;&middot;&nbsp; Methodology Design<br>'
    'Trend Analysis &nbsp;&middot;&nbsp; IEEE Drafting &nbsp;&middot;&nbsp; Grant Proposal Generation &nbsp;&amp;&nbsp; Citation Generation'
    '</div>'
    '<div><span class="sch-badge"><span class="sch-badge-dot"></span>&nbsp;System Online</span></div>'
    '</div>'
    '<hr class="sch-divider" />'
)
st.markdown(_header, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  SIDEBAR MINI LOGO (same SVG, scaled down inline)
# ══════════════════════════════════════════════════════════════
SIDEBAR_LOGO = """<svg width="30" height="30" viewBox="0 0 120 120" fill="none" xmlns="http://www.w3.org/2000/svg" style="flex-shrink:0;filter:drop-shadow(0 0 7px rgba(79,142,247,0.70));"><defs><radialGradient id="s_oBG" cx="40%" cy="38%" r="62%"><stop offset="0%" stop-color="#1c3870"/><stop offset="50%" stop-color="#0d1e4a"/><stop offset="100%" stop-color="#050d22"/></radialGradient><radialGradient id="s_oLG" cx="38%" cy="32%" r="55%"><stop offset="0%" stop-color="#7ab0ff" stop-opacity="0.50"/><stop offset="100%" stop-color="#2a5fc4" stop-opacity="0.00"/></radialGradient><linearGradient id="s_rG" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#4f8ef7" stop-opacity="0.95"/><stop offset="50%" stop-color="#2dd4b4" stop-opacity="0.75"/><stop offset="100%" stop-color="#4f8ef7" stop-opacity="0.90"/></linearGradient><linearGradient id="s_cFG" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#e8f1ff"/><stop offset="100%" stop-color="#90aee0"/></linearGradient><linearGradient id="s_cLG" x1="0%" y1="0%" x2="0%" y2="100%"><stop offset="0%" stop-color="#6888c8"/><stop offset="100%" stop-color="#334e98"/></linearGradient><linearGradient id="s_cRG" x1="0%" y1="0%" x2="0%" y2="100%"><stop offset="0%" stop-color="#4a68b0"/><stop offset="100%" stop-color="#1e3270"/></linearGradient><linearGradient id="s_tG" x1="0%" y1="0%" x2="0%" y2="100%"><stop offset="0%" stop-color="#2dd4b4"/><stop offset="100%" stop-color="#0a6050"/></linearGradient><filter id="s_glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="2.5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter><filter id="s_cG" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter><clipPath id="s_bClip"><circle cx="60" cy="72" r="38"/></clipPath></defs><circle cx="60" cy="72" r="42" fill="none" stroke="url(#s_rG)" stroke-width="1.2" opacity="0.80"/><circle cx="60" cy="72" r="38" fill="url(#s_oBG)"/><circle cx="60" cy="72" r="38" fill="url(#s_oLG)"/><g clip-path="url(#s_bClip)" opacity="0.40" stroke="#6ba3ff" stroke-width="0.85" fill="none"><line x1="60" y1="50" x2="80" y2="62"/><line x1="80" y1="62" x2="76" y2="83"/><line x1="76" y1="83" x2="44" y2="83"/><line x1="44" y1="83" x2="40" y2="62"/><line x1="40" y1="62" x2="60" y2="50"/><line x1="60" y1="50" x2="60" y2="72" stroke="#a8c8ff" stroke-width="0.6"/><line x1="80" y1="62" x2="60" y2="72" stroke="#a8c8ff" stroke-width="0.6"/><line x1="76" y1="83" x2="60" y2="72" stroke="#a8c8ff" stroke-width="0.6"/><line x1="44" y1="83" x2="60" y2="72" stroke="#a8c8ff" stroke-width="0.6"/><line x1="40" y1="62" x2="60" y2="72" stroke="#a8c8ff" stroke-width="0.6"/></g><g filter="url(#s_glow)" clip-path="url(#s_bClip)"><circle cx="60" cy="50" r="3.8" fill="#6ba3ff"/><circle cx="80" cy="62" r="3.3" fill="#4f8ef7"/><circle cx="76" cy="83" r="3.3" fill="#2dd4b4"/><circle cx="44" cy="83" r="3.3" fill="#8b6ef5"/><circle cx="40" cy="62" r="3.3" fill="#4f8ef7"/></g><circle cx="60" cy="72" r="9" fill="#3060c0" filter="url(#s_cG)" opacity="0.40"/><circle cx="60" cy="72" r="6.5" fill="#2a52b8" opacity="0.92"/><circle cx="60" cy="72" r="3.8" fill="#c0d8ff"/><polygon points="60,20 34,31 34,35 60,24" fill="url(#s_cLG)" opacity="0.88"/><polygon points="60,20 86,31 86,35 60,24" fill="url(#s_cRG)" opacity="0.80"/><polygon points="60,10 86,23 60,36 34,23" fill="url(#s_cFG)" opacity="0.96"/><circle cx="60" cy="23" r="4.5" fill="#2a52b8" filter="url(#s_glow)" opacity="0.95"/><circle cx="60" cy="23" r="2.5" fill="#c8dcff" opacity="0.98"/><path d="M 82 24 C 96 28, 96 44, 88 52 C 84 58, 86 64, 86 70" stroke="url(#s_tG)" stroke-width="2.2" fill="none" stroke-linecap="round"/><circle cx="86" cy="70" r="4.0" fill="#2dd4b4" filter="url(#s_glow)" opacity="0.95"/><circle cx="86" cy="70" r="2.0" fill="#d8faf2" opacity="0.95"/><g stroke-linecap="round"><line x1="82.5" y1="74" x2="79" y2="84" stroke="#2dd4b4" stroke-width="1.3" opacity="0.88"/><line x1="84.5" y1="74" x2="83" y2="85" stroke="#20c0a0" stroke-width="1.3" opacity="0.85"/><line x1="86" y1="74" x2="87" y2="85" stroke="#2dd4b4" stroke-width="1.3" opacity="0.82"/></g></svg>"""

st.sidebar.markdown(f"""
<div class="sb-brand">
  {SIDEBAR_LOGO}
  &nbsp;Scholaris
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  SIDEBAR CONTROLS
# ══════════════════════════════════════════════════════════════
agent = st.sidebar.selectbox(
    "Active Agent",
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

agent_meta = {
    "Literature Mining":           ("🔍", "Scans core themes, key authors, datasets & limitations."),
    "Trend Analysis":              ("📈", "Maps 5-year evolution and emerging future directions."),
    "Research Gap Identification": ("🕳️", "Surfaces underexplored areas and innovation openings."),
    "Methodology Design":          ("⚙️",  "Designs architecture, metrics & experimental setup."),
    "IEEE Draft Generation":       ("📄", "Generates full IEEE-structured paper draft."),
    "Grant Proposal Generation":   ("💰", "Crafts funding-ready proposals with budget justification."),
    "Citation Generator":          ("✅", "Generates accurate citations in APA, MLA & IEEE formats."),
}
icon, desc = agent_meta.get(agent, ("🤖", ""))
st.sidebar.markdown(f"""
<div class="sb-agent-card">
  <div class="sb-agent-icon">{icon}</div>
  <div class="sb-agent-name">{agent}</div>
  <div class="sb-agent-desc">{desc}</div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  INPUT
# ══════════════════════════════════════════════════════════════
topic = st.text_area(
    "Research Topic",
    height=150,
    placeholder="e.g.  Federated Learning for Healthcare Data Privacy in Low-Resource Settings"
)
st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  PROMPT BUILDER
# ══════════════════════════════════════════════════════════════
def build_prompt(agent, topic):
    if agent == "Literature Mining":
        return f"Analyze the research literature on: {topic}\n\nProvide:\n- Core themes\n- Key authors\n- Datasets\n- Limitations"
    elif agent == "Trend Analysis":
        return f"Analyze emerging trends in: {topic}\n\nInclude:\n- 5-year evolution\n- Future directions"
    elif agent == "Research Gap Identification":
        return f"Identify research gaps in: {topic}\n\nProvide:\n- Underexplored areas\n- Open challenges\n- Innovation opportunities"
    elif agent == "Methodology Design":
        return f"Design experimental methodology for: {topic}\n\nInclude:\n- Dataset\n- Model architecture\n- Metrics\n- Experimental setup"
    elif agent == "IEEE Draft Generation":
        return f"Generate IEEE-style paper draft on: {topic}\n\nInclude:\n- Abstract\n- Introduction\n- Methodology\n- Results\n- Conclusion"
    elif agent == "Grant Proposal Generation":
        return f"Generate funding-ready grant proposal on: {topic}\n\nInclude:\n- Executive Summary\n- Objectives\n- Methodology\n- Impact\n- Budget justification"
    elif agent == "Citation Generator":
        return f"""You are an expert academic citation specialist. Generate DISTINCT and CORRECTLY FORMATTED citations for the research topic: {topic}

Generate exactly 5 realistic, relevant academic references. Use plausible author names, journal names, and years.

Then format ALL 5 references in each of the 3 styles below.

## APA (7th Edition)
Author, A. A., & Author, B. B. (Year). Title in sentence case. *Journal*, Volume(Issue), Page–Page. https://doi.org/xxxxx
List all 5 in APA format.

## MLA (9th Edition)
Author Last, First. "Title in Title Case." *Journal*, vol. X, no. Y, Year, pp. Z–Z. DOI.
List all 5 in MLA format.

## IEEE
[#] A. Author, "Title," *Journal Abbrev.*, vol. X, no. Y, pp. Z–Z, Mon. Year, doi: 10.xxxx.
List all 5 in IEEE format.

IMPORTANT: Same 5 papers in all 3 formats, formatted differently per each style's rules."""

# ══════════════════════════════════════════════════════════════
#  SESSION STATE
# ══════════════════════════════════════════════════════════════
if "output"       not in st.session_state: st.session_state.output       = None
if "last_topic"   not in st.session_state: st.session_state.last_topic   = None
if "show_novelty" not in st.session_state: st.session_state.show_novelty = False

# ══════════════════════════════════════════════════════════════
#  BUTTONS
# ══════════════════════════════════════════════════════════════
col1, col2, gap, col3, col4 = st.columns([0.6, 2.2, 0.5, 2.2, 0.6])
with col2:
    clicked = st.button("🚀  Generate Research Intelligence")
with col3:
    novelty_clicked = st.button("🔬  Analyse Novelty Score")

if novelty_clicked:
    if not topic.strip():
        st.warning("Please enter a research topic first.")
    else:
        st.session_state.last_topic   = topic
        st.session_state.show_novelty = True

if clicked:
    if not topic.strip():
        st.warning("Please enter a research topic first.")
    else:
        with st.spinner("Analysing research ecosystem…"):
            try:
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {"role": "system", "content": "You are an advanced AI research director."},
                        {"role": "user",   "content": build_prompt(agent, topic)}
                    ],
                    temperature=temperature,
                )
                st.session_state.output     = response.choices[0].message.content
                st.session_state.last_topic = topic
            except Exception as e:
                st.error(f"API Error: {str(e)}")

# ══════════════════════════════════════════════════════════════
#  OUTPUT
# ══════════════════════════════════════════════════════════════
if st.session_state.output:
    st.success("Analysis complete ✓")
    st.markdown(f'<div class="out-card"><div class="out-tag">✦ {agent} &nbsp;·&nbsp; Output</div>', unsafe_allow_html=True)
    st.markdown(st.session_state.output)
    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  NOVELTY SCORE
# ══════════════════════════════════════════════════════════════
if st.session_state.show_novelty:
    novelty_score = compute_novelty(st.session_state.last_topic)
    st.markdown("<br>", unsafe_allow_html=True)
    st.metric(label="Research Novelty Score", value=f"{novelty_score} / 100")

    if novelty_score > 75:
        bar_grad = "linear-gradient(90deg,#1a8a74,#2dd4b4)"
        verdict  = "✦ High novelty — strong research foundation"
        v_col    = "#2dd4b4"
        st.success("High novelty potential ✦")
    elif novelty_score > 50:
        bar_grad = "linear-gradient(90deg,#b87830,#f5a623)"
        verdict  = "◈ Moderate novelty — refine the angle"
        v_col    = "#f5a623"
        st.info("Moderate novelty ◈")
    else:
        bar_grad = "linear-gradient(90deg,#a02040,#f56565)"
        verdict  = "⚠  Low novelty — consider a sharper focus"
        v_col    = "#f56565"
        st.warning("Low novelty ⚠")

    st.markdown(f"""
    <div class="nov-card" style="--bar-grad:{bar_grad};">
      <div class="nov-label">🔬 Novelty Score Analysis</div>
      <div>
        <span class="nov-num">{novelty_score}</span>
        <span class="nov-denom"> / 100</span>
      </div>
      <div class="nov-track">
        <div class="nov-fill" style="width:{novelty_score}%;background:{bar_grad};"></div>
      </div>
      <div class="nov-verdict" style="color:{v_col};">{verdict}</div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  FOOTER
# ══════════════════════════════════════════════════════════════
st.markdown("""
<hr class="sch-divider" style="margin-top:4rem;margin-bottom:0;" />
<div style="text-align:center;padding:1.5rem 0 1rem;
            font-family:'JetBrains Mono',monospace;
            font-size:0.57rem;letter-spacing:0.35em;text-transform:uppercase;
            color:var(--t4,#5a6e96);">
  Scholaris &nbsp;·&nbsp; Multi-Agent Research Engine &nbsp;·&nbsp;
</div>
""", unsafe_allow_html=True)


