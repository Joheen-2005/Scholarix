import streamlit as st
from groq import Groq
from novelty_agent import compute_novelty
from config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)

st.set_page_config(page_title="Scholaris", layout="wide", page_icon="📚")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Instrument+Serif:ital@0;1&family=JetBrains+Mono:wght@300;400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; }

/* ══════════════════════════════════════════
   DESIGN TOKENS  —  deep navy dark theme
══════════════════════════════════════════ */
:root {
  /* Surfaces — layered dark navy */
  --s0:  #080d18;   /* deepest background */
  --s1:  #0d1424;   /* app bg */
  --s2:  #111b30;   /* card surface */
  --s3:  #172038;   /* elevated card */
  --s4:  #1e2a45;   /* hover / active */
  --s5:  #243050;   /* border highlight */

  /* Blue accent system — electric but controlled */
  --blue:       #4f8ef7;
  --blue-bright:#6ba3ff;
  --blue-dim:   #2a5fc4;
  --blue-glow:  rgba(79,142,247,0.20);
  --blue-tint:  rgba(79,142,247,0.08);

  /* Secondary accents */
  --teal:       #2dd4b4;
  --teal-dim:   rgba(45,212,180,0.12);
  --violet:     #8b6ef5;
  --violet-dim: rgba(139,110,245,0.12);
  --amber:      #f5a623;
  --rose:       #f56565;
  --green:      #38d9a9;

  /* Text — ALL HIGH CONTRAST */
  --t1: #f0f4ff;    /* primary — almost white-blue */
  --t2: #c8d4f0;    /* secondary */
  --t3: #8fa0c4;    /* tertiary / supporting */
  --t4: #5a6e96;    /* muted labels */

  /* Borders */
  --b1: rgba(79,142,247,0.18);
  --b2: rgba(255,255,255,0.07);
  --b3: rgba(79,142,247,0.35);

  /* Neumorphic dark shadows */
  --neu-up:   6px 6px 18px rgba(0,0,0,0.55), -4px -4px 14px rgba(30,42,69,0.60);
  --neu-in:   inset 4px 4px 12px rgba(0,0,0,0.50), inset -3px -3px 10px rgba(30,42,69,0.55);
  --neu-sm:   3px 3px 10px rgba(0,0,0,0.45), -2px -2px 8px rgba(30,42,69,0.50);

  --r-xl: 20px;
  --r-lg: 16px;
  --r-md: 12px;
  --r-sm:  8px;
  --r-pill: 99px;
}

/* ══════════════════════════════════════════
   GLOBAL BASE
══════════════════════════════════════════ */
html, body, .stApp {
  background: var(--s1) !important;
  color: var(--t2) !important;
  font-family: 'Plus Jakarta Sans', sans-serif !important;
}

/* All text default high contrast */
.stApp, .stApp * { color: var(--t2); }
p, span, div, li, td, th, label { color: var(--t2) !important; }
h1, h2, h3, h4, h5, h6 {
  color: var(--t1) !important;
  font-family: 'Plus Jakarta Sans', sans-serif !important;
  font-weight: 700 !important;
}
strong, b { color: var(--t1) !important; font-weight: 700 !important; }
em, i { color: var(--t3) !important; font-style: italic; }
a { color: var(--blue-bright) !important; text-decoration: none; }
code {
  font-family: 'JetBrains Mono', monospace !important;
  color: var(--teal) !important;
  background: rgba(45,212,180,0.08) !important;
  padding: 0.15em 0.45em;
  border-radius: 5px;
  font-size: 0.87em !important;
}

/* ══════════════════════════════════════════
   ANIMATED BACKGROUND — electric blue orbs
   Subtle. Professional. Not distracting.
══════════════════════════════════════════ */
.stApp::before {
  content: '';
  position: fixed; inset: 0; z-index: 0; pointer-events: none;
  background:
    radial-gradient(ellipse 55% 45% at 12% 18%,  rgba(79,142,247,0.13) 0%, transparent 60%),
    radial-gradient(ellipse 40% 38% at 88% 12%,  rgba(107,163,255,0.09) 0%, transparent 55%),
    radial-gradient(ellipse 45% 50% at 50% 92%,  rgba(45,212,180,0.07) 0%, transparent 60%),
    radial-gradient(ellipse 30% 30% at 80% 60%,  rgba(139,110,245,0.07) 0%, transparent 50%);
  animation: bgPulse 11s ease-in-out infinite alternate;
}
@keyframes bgPulse {
  0%   { opacity: 0.75; transform: scale(1.00); }
  50%  { opacity: 0.95; transform: scale(1.015); }
  100% { opacity: 0.80; transform: scale(1.03);  }
}

/* Moving thin scan-line — very subtle */
.stApp::after {
  content: '';
  position: fixed; inset: 0; z-index: 0; pointer-events: none;
  background: repeating-linear-gradient(
    0deg,
    transparent,
    transparent 3px,
    rgba(79,142,247,0.012) 3px,
    rgba(79,142,247,0.012) 4px
  );
  animation: scanSlide 20s linear infinite;
}
@keyframes scanSlide {
  0%   { background-position: 0 0;    }
  100% { background-position: 0 100%; }
}

/* ══════════════════════════════════════════
   HEADER
══════════════════════════════════════════ */
.sch-header {
  text-align: center;
  padding: 3.5rem 2rem 2.8rem;
  position: relative;
  z-index: 5;
}
.sch-eyebrow {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.63rem;
  letter-spacing: 0.35em;
  text-transform: uppercase;
  color: var(--blue-bright) !important;
  margin-bottom: 1rem;
  opacity: 0.85;
  animation: fadeUp 0.6s ease both;
}
.sch-wordmark {
  font-family: 'Instrument Serif', serif;
  font-size: clamp(2.8rem, 6vw, 4.5rem);
  font-weight: 400;
  color: var(--t1) !important;
  letter-spacing: -0.02em;
  line-height: 1.06;
  animation: fadeUp 0.6s ease 0.08s both;
}
.sch-wordmark .hi { color: var(--blue-bright) !important; }
.sch-tagline {
  font-size: 0.95rem;
  font-weight: 400;
  color: var(--t3) !important;
  margin-top: 0.9rem;
  line-height: 1.72;
  max-width: 560px;
  margin-left: auto; margin-right: auto;
  animation: fadeUp 0.6s ease 0.18s both;
}
.sch-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.45rem;
  margin-top: 1.5rem;
  padding: 0.3rem 1rem;
  border-radius: var(--r-pill);
  background: var(--blue-tint);
  border: 1px solid var(--b1);
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.6rem;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--teal) !important;
  animation: fadeUp 0.6s ease 0.28s both;
}
.sch-badge-dot {
  width: 6px; height: 6px; border-radius: 50%;
  background: var(--teal);
  box-shadow: 0 0 8px rgba(45,212,180,0.7);
  animation: breathe 2.5s ease-in-out infinite;
}
@keyframes breathe { 0%,100%{opacity:1;box-shadow:0 0 8px rgba(45,212,180,0.7);} 50%{opacity:0.35;box-shadow:0 0 3px rgba(45,212,180,0.2);} }
@keyframes fadeUp  { from{opacity:0;transform:translateY(12px);} to{opacity:1;transform:translateY(0);} }

.sch-divider {
  border: none; height: 1px;
  background: linear-gradient(90deg, transparent, var(--b3), rgba(139,110,245,0.25), transparent);
  margin: 0 auto 2.5rem; max-width: 800px;
  animation: divPulse 4s ease-in-out infinite alternate;
}
@keyframes divPulse { 0%{opacity:0.45;} 100%{opacity:0.85;} }

/* ══════════════════════════════════════════
   SIDEBAR
══════════════════════════════════════════ */
section[data-testid="stSidebar"] {
  background: var(--s2) !important;
  border-right: 1px solid var(--b1) !important;
  box-shadow: 4px 0 30px rgba(0,0,0,0.40) !important;
}
/* Override ALL sidebar text to be clearly visible */
section[data-testid="stSidebar"] *,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] div,
section[data-testid="stSidebar"] label {
  color: var(--t2) !important;
  font-family: 'Plus Jakarta Sans', sans-serif !important;
}

/* Selectbox label in sidebar */
section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] {
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 0.65rem !important;
  letter-spacing: 0.22em !important;
  text-transform: uppercase !important;
  color: var(--t3) !important;
  font-weight: 400 !important;
  margin-bottom: 0.4rem !important;
}
section[data-testid="stSidebar"] .stSlider label,
section[data-testid="stSidebar"] .stSlider [data-testid="stWidgetLabel"] {
  color: var(--t3) !important;
}

.sb-brand {
  display: flex; align-items: center; gap: 0.6rem;
  padding: 1rem 1.2rem;
  background: var(--s3);
  border: 1px solid var(--b1);
  border-radius: var(--r-lg);
  box-shadow: var(--neu-sm);
  margin-bottom: 1.6rem;
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: 1rem;
  font-weight: 700;
  color: var(--t1) !important;
  letter-spacing: -0.01em;
}
.sb-brand .logo-dot {
  width: 28px; height: 28px; border-radius: 8px;
  background: linear-gradient(135deg, var(--blue-dim), var(--violet));
  display: flex; align-items: center; justify-content: center;
  font-size: 0.85rem;
  box-shadow: 0 0 12px rgba(79,142,247,0.35);
}

.sb-agent-card {
  background: var(--s3);
  border: 1px solid var(--b1);
  border-radius: var(--r-lg);
  box-shadow: var(--neu-in);
  padding: 1.2rem 1.3rem;
  margin-top: 0.8rem;
}
.sb-agent-icon { font-size: 1.6rem; margin-bottom: 0.55rem; }
.sb-agent-name {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.63rem;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--blue-bright) !important;
  margin-bottom: 0.4rem;
  font-weight: 500;
}
.sb-agent-desc {
  font-size: 0.86rem;
  font-weight: 400;
  color: var(--t3) !important;
  line-height: 1.6;
}

/* ══════════════════════════════════════════
   SELECT BOX — dark + visible text
══════════════════════════════════════════ */
.stSelectbox > div > div {
  background: var(--s3) !important;
  border: 1px solid var(--b1) !important;
  border-radius: var(--r-lg) !important;
  color: var(--t1) !important;
  font-family: 'Plus Jakarta Sans', sans-serif !important;
  font-size: 0.95rem !important;
  font-weight: 500 !important;
  box-shadow: var(--neu-sm) !important;
  transition: border-color 0.2s, box-shadow 0.2s;
}
.stSelectbox > div > div:hover {
  border-color: var(--blue) !important;
  box-shadow: var(--neu-sm), 0 0 0 3px var(--blue-glow) !important;
}
/* Dropdown items */
[data-baseweb="popover"] {
  background: var(--s3) !important;
  border: 1px solid var(--b1) !important;
  border-radius: var(--r-lg) !important;
  box-shadow: 0 12px 40px rgba(0,0,0,0.6) !important;
}
[data-baseweb="menu"] li,
[data-baseweb="menu"] li * {
  color: var(--t2) !important;
  font-family: 'Plus Jakarta Sans', sans-serif !important;
  font-size: 0.92rem !important;
  background: transparent !important;
}
[data-baseweb="menu"] li:hover,
[data-baseweb="menu"] li[aria-selected="true"] {
  background: var(--s4) !important;
  color: var(--t1) !important;
}

/* ══════════════════════════════════════════
   TEXT AREA — dark, visible, clean
══════════════════════════════════════════ */
.stTextArea label,
.stTextArea [data-testid="stWidgetLabel"],
.stTextArea [data-testid="stWidgetLabel"] * {
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 0.63rem !important;
  letter-spacing: 0.25em !important;
  text-transform: uppercase !important;
  color: var(--t3) !important;
  font-weight: 400 !important;
}
.stTextArea textarea {
  background: var(--s2) !important;
  border: 1px solid var(--b2) !important;
  border-radius: var(--r-lg) !important;
  color: var(--t1) !important;
  font-family: 'Plus Jakarta Sans', sans-serif !important;
  font-size: 0.97rem !important;
  font-weight: 400 !important;
  line-height: 1.75 !important;
  box-shadow: var(--neu-in) !important;
  padding: 1.1rem 1.3rem !important;
  transition: border-color 0.2s, box-shadow 0.2s;
  caret-color: var(--blue-bright);
  resize: none;
}
.stTextArea textarea::placeholder {
  color: var(--t4) !important;
  font-style: italic;
}
.stTextArea textarea:focus {
  outline: none !important;
  border-color: var(--blue) !important;
  box-shadow: var(--neu-in), 0 0 0 3px var(--blue-glow) !important;
}

/* ══════════════════════════════════════════
   BUTTONS — prominent, visible, dark
══════════════════════════════════════════ */
.stButton > button {
  width: 100% !important;
  padding: 0.82rem 1.5rem !important;
  background: linear-gradient(135deg, var(--blue-dim) 0%, var(--blue) 100%) !important;
  border: 1px solid rgba(107,163,255,0.40) !important;
  border-radius: var(--r-lg) !important;
  color: #ffffff !important;
  font-family: 'Plus Jakarta Sans', sans-serif !important;
  font-size: 0.88rem !important;
  font-weight: 700 !important;
  letter-spacing: 0.03em !important;
  text-transform: none !important;
  box-shadow: 0 4px 20px rgba(79,142,247,0.30), var(--neu-sm) !important;
  transition: all 0.22s ease !important;
  position: relative; overflow: hidden;
}
.stButton > button::before {
  content: '';
  position: absolute; inset: 0;
  background: linear-gradient(180deg, rgba(255,255,255,0.10) 0%, transparent 100%);
  border-radius: var(--r-lg);
  pointer-events: none;
}
.stButton > button:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 28px rgba(79,142,247,0.45), var(--neu-sm) !important;
  border-color: var(--blue-bright) !important;
  color: #ffffff !important;
}
.stButton > button:active {
  transform: translateY(0) !important;
  box-shadow: var(--neu-in) !important;
}

/* Second button — teal variant */
div[data-testid="column"]:nth-child(4) .stButton > button {
  background: linear-gradient(135deg, #1a8a74 0%, var(--teal) 100%) !important;
  border-color: rgba(45,212,180,0.40) !important;
  box-shadow: 0 4px 20px rgba(45,212,180,0.25), var(--neu-sm) !important;
}
div[data-testid="column"]:nth-child(4) .stButton > button:hover {
  box-shadow: 0 8px 28px rgba(45,212,180,0.38), var(--neu-sm) !important;
}

/* ══════════════════════════════════════════
   OUTPUT CARD
══════════════════════════════════════════ */
.out-card {
  background: var(--s2);
  border: 1px solid var(--b1);
  border-radius: var(--r-xl);
  box-shadow: var(--neu-up);
  padding: 2.2rem 2.6rem;
  margin-top: 1.8rem;
  position: relative; overflow: hidden; z-index: 2;
  animation: cardUp 0.5s cubic-bezier(0.16,1,0.3,1) both;
}
.out-card::before {
  content: '';
  position: absolute; top: 0; left: 0; right: 0; height: 2px;
  background: linear-gradient(90deg, var(--blue-dim), var(--blue-bright), var(--teal));
  animation: scanBar 3s linear infinite;
  background-size: 200% 100%;
}
@keyframes scanBar  { 0%{background-position:0% 0;} 100%{background-position:200% 0;} }
@keyframes cardUp   { from{opacity:0;transform:translateY(16px);} to{opacity:1;transform:translateY(0);} }

.out-tag {
  display: inline-flex; align-items: center; gap: 0.38rem;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.6rem; letter-spacing: 0.22em; text-transform: uppercase;
  color: var(--blue-bright) !important;
  background: var(--blue-tint);
  border: 1px solid var(--b1);
  padding: 0.22rem 0.75rem; border-radius: var(--r-pill);
  margin-bottom: 1.4rem; font-weight: 500;
}

/* All output text — high contrast */
.out-card h1, .out-card h2, .out-card h3,
.out-card h4, .out-card h5, .out-card h6 {
  font-family: 'Plus Jakarta Sans', sans-serif !important;
  color: var(--t1) !important; font-weight: 700 !important;
  margin: 1.2rem 0 0.5rem; line-height: 1.3;
}
.out-card h1 { font-size: 1.5rem !important; }
.out-card h2 { font-size: 1.22rem !important; }
.out-card h3 { font-size: 1.04rem !important; }
.out-card p, .out-card li {
  font-family: 'Plus Jakarta Sans', sans-serif !important;
  font-size: 0.95rem !important; font-weight: 400 !important;
  line-height: 1.80 !important; color: var(--t2) !important;
  margin-bottom: 0.5rem;
}
.out-card strong, .out-card b { color: var(--t1) !important; font-weight: 700 !important; }
.out-card em, .out-card i     { color: var(--t3) !important; }
.out-card code {
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 0.85rem !important; font-weight: 400 !important;
  background: rgba(45,212,180,0.08) !important;
  color: var(--teal) !important;
  padding: 0.15em 0.5em; border-radius: 5px;
  border: 1px solid rgba(45,212,180,0.15);
}
.out-card pre {
  background: var(--s0) !important; border-radius: var(--r-md) !important;
  border: 1px solid var(--b2) !important;
  padding: 1.1rem 1.3rem !important; overflow-x: auto;
}
.out-card hr {
  border: none; height: 1px;
  background: linear-gradient(90deg, transparent, var(--b1), transparent);
  margin: 1.4rem 0;
}
.out-card blockquote {
  border-left: 3px solid var(--blue) !important;
  margin: 0.8rem 0 !important; padding-left: 1rem !important;
  color: var(--t3) !important;
}
/* Streamlit markdown rendered inside card */
.out-card .stMarkdown * { color: var(--t2) !important; }
.out-card .stMarkdown strong, .out-card .stMarkdown b { color: var(--t1) !important; }
.out-card .stMarkdown h1,.out-card .stMarkdown h2,.out-card .stMarkdown h3 { color: var(--t1) !important; }
.out-card .stMarkdown code { color: var(--teal) !important; }

/* Global streamlit markdown */
.stMarkdown p  { color: var(--t2) !important; font-weight: 400 !important; }
.stMarkdown li { color: var(--t2) !important; font-weight: 400 !important; }
.stMarkdown h1,.stMarkdown h2,.stMarkdown h3 { color: var(--t1) !important; font-weight: 700 !important; }
.stMarkdown strong,.stMarkdown b { color: var(--t1) !important; font-weight: 700 !important; }
.stMarkdown em,.stMarkdown i { color: var(--t3) !important; }
.stMarkdown code { color: var(--teal) !important; }

/* ══════════════════════════════════════════
   NOVELTY CARD
══════════════════════════════════════════ */
.nov-card {
  background: var(--s2);
  border: 1px solid var(--b1);
  border-radius: var(--r-xl);
  box-shadow: var(--neu-up);
  padding: 2rem 2.5rem;
  margin-top: 1.8rem;
  position: relative; overflow: hidden; z-index: 2;
  animation: cardUp 0.5s cubic-bezier(0.16,1,0.3,1) 0.1s both;
}
.nov-card::before {
  content: '';
  position: absolute; top: 0; left: 0; right: 0; height: 2px;
  background: var(--bar-grad, linear-gradient(90deg, var(--blue), var(--teal)));
  opacity: 0.9;
}
.nov-label {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.62rem; letter-spacing: 0.25em; text-transform: uppercase;
  color: var(--t4) !important; margin-bottom: 0.65rem;
}
.nov-num {
  font-family: 'Instrument Serif', serif;
  font-size: 5rem; font-weight: 400; line-height: 1;
  color: var(--t1) !important; letter-spacing: -0.03em;
}
.nov-denom {
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: 1.4rem; font-weight: 300;
  color: var(--t4) !important; margin-left: 0.1rem;
}
.nov-track {
  height: 4px; background: var(--s0); border-radius: var(--r-pill);
  box-shadow: var(--neu-in); margin: 1.2rem 0 0.8rem; overflow: hidden;
}
.nov-fill {
  height: 100%; border-radius: var(--r-pill);
  animation: fillOut 1.3s cubic-bezier(0.16,1,0.3,1) both;
  position: relative;
}
.nov-fill::after {
  content: ''; position: absolute; top: 0; left: 0; right: 0; height: 50%;
  background: rgba(255,255,255,0.20); border-radius: var(--r-pill);
}
@keyframes fillOut { from{width:0%;} }
.nov-verdict {
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: 0.88rem; font-weight: 600;
}

/* ══════════════════════════════════════════
   ALERTS
══════════════════════════════════════════ */
div[data-testid="stAlert"] {
  background: var(--s3) !important;
  border: 1px solid var(--b2) !important;
  border-radius: var(--r-lg) !important;
  box-shadow: var(--neu-sm) !important;
  font-family: 'Plus Jakarta Sans', sans-serif !important;
  font-size: 0.92rem !important; font-weight: 500 !important;
  z-index: 2; position: relative;
}
div[data-testid="stAlert"] * { color: var(--t2) !important; }
.stSuccess { border-left: 3px solid var(--green) !important; }
.stInfo    { border-left: 3px solid var(--blue)  !important; }
.stWarning { border-left: 3px solid var(--amber) !important; }
.stError   { border-left: 3px solid var(--rose)  !important; }

/* ══════════════════════════════════════════
   METRIC
══════════════════════════════════════════ */
[data-testid="stMetric"] {
  background: var(--s3) !important; border: 1px solid var(--b1) !important;
  border-radius: var(--r-lg) !important; box-shadow: var(--neu-sm) !important;
  padding: 1.2rem 1.6rem !important;
}
[data-testid="stMetricLabel"] {
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 0.62rem !important; letter-spacing: 0.22em !important;
  text-transform: uppercase !important; color: var(--t4) !important;
}
[data-testid="stMetricValue"] {
  font-family: 'Instrument Serif', serif !important;
  color: var(--t1) !important; font-size: 1.9rem !important;
}

/* ══════════════════════════════════════════
   SLIDER
══════════════════════════════════════════ */
.stSlider [data-baseweb="slider"] > div:first-child {
  background: var(--s0) !important;
  box-shadow: var(--neu-in) !important;
  height: 4px !important; border-radius: var(--r-pill) !important;
}
.stSlider [data-baseweb="slider"] [data-testid="stThumbValue"] {
  color: var(--blue-bright) !important;
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 0.7rem !important;
}
.stSlider [data-baseweb="slider"] div[role="slider"] {
  background: linear-gradient(135deg, var(--s4), var(--s3)) !important;
  box-shadow: var(--neu-up), 0 0 0 2px var(--blue-dim) !important;
  border: none !important;
  width: 18px !important; height: 18px !important;
}

/* ══════════════════════════════════════════
   MISC / SPINNER / SCROLLBAR
══════════════════════════════════════════ */
.stSpinner > div > div { border-top-color: var(--blue) !important; }

::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: var(--s0); }
::-webkit-scrollbar-thumb {
  background: rgba(79,142,247,0.30);
  border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover { background: rgba(79,142,247,0.55); }

/* Fix any remaining white bleed */
.stApp [data-testid="stVerticalBlock"],
.stApp [data-testid="stHorizontalBlock"],
.stApp .block-container,
.stApp .main { background: transparent !important; }

section[data-testid="stSidebar"] > div { background: var(--s2) !important; }
</style>
""", unsafe_allow_html=True)

# ══ HEADER ══════════════════════════════════════════════
st.markdown("""
<div class="sch-header">
  <div class="sch-eyebrow">Multi-Agent Research Intelligence · v2.0</div>
  <div class="sch-wordmark">Schol<span class="hi">a</span>ris</div>
  <div class="sch-tagline">
    Literature Mining &nbsp;·&nbsp; Gap Detection &nbsp;·&nbsp; Methodology Design &nbsp;·&nbsp; Trend Analysis<br>
    IEEE Drafting &nbsp;&amp;&nbsp; Grant Proposal Generation &nbsp;&amp;&nbsp; Citation Generation
  </div>
  <div><span class="sch-badge"><span class="sch-badge-dot"></span>System Online</span></div>
</div>
<hr class="sch-divider" />
""", unsafe_allow_html=True)

# ══ SIDEBAR ═════════════════════════════════════════════
st.sidebar.markdown("""
<div class="sb-brand">
  <div class="logo-dot">◈</div>
  Scholaris
</div>
""", unsafe_allow_html=True)

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

# ══ INPUT ════════════════════════════════════════════════
topic = st.text_area(
    "Research Topic",
    height=150,
    placeholder="e.g.  Federated Learning for Healthcare Data Privacy in Low-Resource Settings"
)
st.markdown("<br>", unsafe_allow_html=True)

# ══ PROMPT BUILDER ═══════════════════════════════════════
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

Generate exactly 5 realistic, relevant academic references. Format ALL 5 references in each style:

## APA (7th Edition)
Author, A. A., & Author, B. B. (Year). Title in sentence case. Journal Name, Volume(Issue), Page–Page. https://doi.org/xxxxx
List all 5 in APA format.

## MLA (9th Edition)
Author Last, First. "Title in Title Case." Journal, vol. X, no. Y, Year, pp. Z–Z. DOI.
List all 5 in MLA format.

## IEEE
[#] A. Author, "Title," Journal Abbrev., vol. X, no. Y, pp. Z–Z, Mon. Year, doi: 10.xxxx.
List all 5 in IEEE format."""

# ══ SESSION STATE ════════════════════════════════════════
if "output"       not in st.session_state: st.session_state.output       = None
if "last_topic"   not in st.session_state: st.session_state.last_topic   = None
if "show_novelty" not in st.session_state: st.session_state.show_novelty = False

# ══ BUTTON ROW ═══════════════════════════════════════════
c1, c2, gap, c3, c4 = st.columns([0.6, 2.2, 0.5, 2.2, 0.6])
with c2:
    clicked = st.button("🚀  Generate Research Intelligence")
with c3:
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

# ══ OUTPUT ═══════════════════════════════════════════════
if st.session_state.output:
    st.success("Analysis complete ✓")
    st.markdown(f'<div class="out-card"><div class="out-tag">✦ {agent} · Output</div>', unsafe_allow_html=True)
    st.markdown(st.session_state.output)
    st.markdown("</div>", unsafe_allow_html=True)

# ══ NOVELTY ══════════════════════════════════════════════
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
        verdict  = "⚠  Low novelty — consider sharper focus"
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

# ══ FOOTER ═══════════════════════════════════════════════
st.markdown("""
<hr class="sch-divider" style="margin-top:4rem;margin-bottom:0;" />
<div style="text-align:center;padding:1.4rem 0 1rem;
            font-family:'JetBrains Mono',monospace;
            font-size:0.57rem;letter-spacing:0.35em;text-transform:uppercase;
            color:var(--t4,#5a6e96);">
  Scholaris &nbsp;·&nbsp; Multi-Agent Research Engine &nbsp;·&nbsp;
</div>
""", unsafe_allow_html=True)

