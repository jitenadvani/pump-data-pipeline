import streamlit as st
import pandas as pd
import re, time, requests
from datetime import datetime
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

st.set_page_config(
    page_title="VibroConvert",
    page_icon="📳",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ═══════════════════════════════════════════════════════════════════
# CSS  —  Bold & Colorful, Futuristic SaaS
# ═══════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&family=Fira+Code:wght@400;500&display=swap');

/* ── TOKENS ─────────────────────────────────────────────────── */
:root {
  --bg:       #0b0e17;
  --surface:  #111827;
  --s2:       #1a2236;
  --s3:       #202c42;
  --border:   #1f2d47;
  --b2:       #2a3d5e;

  --lime:     #a3e635;
  --lime-d:   rgba(163,230,53,.10);
  --lime-g:   rgba(163,230,53,.20);
  --sky:      #38bdf8;
  --sky-d:    rgba(56,189,248,.10);
  --sky-g:    rgba(56,189,248,.20);
  --rose:     #fb7185;
  --rose-d:   rgba(251,113,133,.10);
  --amber:    #fbbf24;
  --amber-d:  rgba(251,191,36,.10);
  --purple:   #c084fc;
  --purple-d: rgba(192,132,252,.10);
  --green:    #34d399;
  --green-d:  rgba(52,211,153,.10);
  --green-g:  rgba(52,211,153,.20);

  --t1: #f1f5ff;
  --t2: #8ea3c3;
  --t3: #3d5270;

  --syne:    'Syne', sans-serif;
  --jakarta: 'Plus Jakarta Sans', sans-serif;
  --fira:    'Fira Code', monospace;
}

/* ── RESET / BASE ──────────────────────────────────────────── */
html, body, [class*="css"] { font-family: var(--jakarta); }
.stApp {
  background: var(--bg);
  background-image:
    radial-gradient(ellipse 70% 35% at 0% 0%,   rgba(163,230,53,.04)  0%, transparent 55%),
    radial-gradient(ellipse 50% 30% at 100% 100%,rgba(56,189,248,.04)  0%, transparent 55%),
    radial-gradient(ellipse 40% 25% at 60%  50%, rgba(192,132,252,.03) 0%, transparent 50%);
}
.block-container { padding: 0 2rem 4rem; max-width: 1440px; }
#MainMenu, footer, header { visibility: hidden; }
* { box-sizing: border-box; }
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: var(--surface); }
::-webkit-scrollbar-thumb { background: var(--b2); border-radius: 2px; }
::-webkit-scrollbar-thumb:hover { background: var(--lime); }

/* ── SIDEBAR ───────────────────────────────────────────────── */
[data-testid="stSidebar"] {
  background: var(--surface) !important;
  border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] .block-container { padding: 1rem; }
[data-testid="stSidebar"] label {
  color: var(--t2) !important;
  font-family: var(--jakarta) !important;
  font-size: 0.78rem !important;
}
[data-testid="stSidebar"] .stTextInput > div > div > input {
  background: var(--s2) !important;
  border: 1px solid var(--b2) !important;
  color: var(--t1) !important;
  border-radius: 8px !important;
  font-family: var(--fira) !important;
  font-size: 0.8rem !important;
}
[data-testid="stSidebar"] .stTextInput > div > div > input:focus {
  border-color: var(--lime) !important;
  box-shadow: 0 0 0 3px var(--lime-d) !important;
}

/* ── TOP BAR ───────────────────────────────────────────────── */
.topbar {
  position: sticky;
  top: 0;
  z-index: 100;
  background: rgba(11,14,23,.92);
  backdrop-filter: blur(16px);
  border-bottom: 1px solid var(--border);
  padding: 0.75rem 2rem;
  margin: 0 -2rem 0;
  display: flex;
  align-items: center;
  gap: 1rem;
}
.topbar-brand {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  flex-shrink: 0;
}
.brand-mark {
  width: 34px; height: 34px;
  background: linear-gradient(135deg, var(--lime), #65a30d);
  border-radius: 9px;
  display: flex; align-items: center; justify-content: center;
  font-size: 1rem;
  box-shadow: 0 0 18px var(--lime-g);
  flex-shrink: 0;
}
.brand-name {
  font-family: var(--syne);
  font-size: 1.25rem;
  font-weight: 800;
  color: var(--t1);
  letter-spacing: -.03em;
  line-height: 1;
}
.brand-ver {
  font-family: var(--fira);
  font-size: 0.52rem;
  color: var(--t3);
  letter-spacing: .12em;
  text-transform: uppercase;
}
.topbar-controls {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  flex: 1;
}
.topbar-right {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-shrink: 0;
}
.status-badge {
  font-family: var(--fira);
  font-size: 0.58rem;
  letter-spacing: .1em;
  text-transform: uppercase;
  padding: 0.25rem 0.7rem;
  border-radius: 100px;
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
}
.status-badge.idle   { background: var(--s3); border: 1px solid var(--border); color: var(--t3); }
.status-badge.active { background: var(--amber-d); border: 1px solid rgba(251,191,36,.25); color: var(--amber); }
.status-badge.done   { background: var(--green-d); border: 1px solid rgba(52,211,153,.25); color: var(--green); }
.sbdot { width:5px;height:5px;border-radius:50%;background:currentColor;animation:pulse 2s ease-in-out infinite; }
@keyframes pulse { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:.3;transform:scale(.6)} }

/* ── SECTION HEADING ───────────────────────────────────────── */
.sh {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  margin: 2rem 0 1rem;
}
.sh-num {
  width: 24px; height: 24px;
  background: linear-gradient(135deg, var(--lime), #65a30d);
  border-radius: 6px;
  font-family: var(--syne);
  font-size: 0.7rem;
  font-weight: 800;
  color: #0b0e17;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}
.sh-label {
  font-family: var(--syne);
  font-size: 1rem;
  font-weight: 700;
  color: var(--t1);
  letter-spacing: -.01em;
}
.sh-line { flex: 1; height: 1px; background: var(--border); }
.sh-count {
  font-family: var(--fira);
  font-size: 0.62rem;
  color: var(--t3);
  background: var(--s2);
  border: 1px solid var(--border);
  padding: .18rem .55rem;
  border-radius: 100px;
}

/* ── SESSION TAB NAV ───────────────────────────────────────── */
.tab-nav {
  display: flex;
  gap: 0.35rem;
  flex-wrap: wrap;
  margin-bottom: 1rem;
  padding: 0.4rem;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 12px;
}
.tab-btn {
  padding: 0.45rem 1rem;
  border-radius: 8px;
  font-family: var(--jakarta);
  font-size: 0.82rem;
  font-weight: 500;
  cursor: pointer;
  border: none;
  transition: all .18s;
  white-space: nowrap;
}
.tab-btn.inactive {
  background: transparent;
  color: var(--t2);
}
.tab-btn.inactive:hover {
  background: var(--s2);
  color: var(--t1);
}
.tab-btn.active-0  { background: linear-gradient(135deg,#164e35,var(--lime)); color:#0b1a06; font-weight:700; box-shadow:0 2px 10px var(--lime-g); }
.tab-btn.active-1  { background: linear-gradient(135deg,#0c3256,var(--sky));  color:#041020; font-weight:700; box-shadow:0 2px 10px var(--sky-g); }
.tab-btn.active-2  { background: linear-gradient(135deg,#4a1045,var(--purple)); color:#1a0620; font-weight:700; }
.tab-btn.active-3  { background: linear-gradient(135deg,#7c1d2a,var(--rose));   color:#200508; font-weight:700; }
.tab-btn.active-4  { background: linear-gradient(135deg,#78350f,var(--amber));  color:#200900; font-weight:700; }
.tab-btn.merge-tab { background: linear-gradient(135deg,#064e3b,var(--green)); color:#011a12; font-weight:700; box-shadow:0 2px 10px var(--green-g); }
.tab-btn.merge-tab.inactive { background:var(--s2); color:var(--t3); }

/* ── SESSION PANEL ─────────────────────────────────────────── */
.sess-panel {
  border-radius: 14px;
  overflow: hidden;
  border: 1px solid var(--border);
}
.sess-hero {
  padding: 1.2rem 1.4rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
}
.sess-title {
  font-family: var(--syne);
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--t1);
  flex: 1;
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.sess-body { padding: 0 1.4rem 1.4rem; }

/* Hero accent colors per tab */
.hero-0 { background: linear-gradient(135deg, #0d2010 0%, #112918 100%); border-bottom:1px solid rgba(163,230,53,.15); }
.hero-1 { background: linear-gradient(135deg, #071625 0%, #0b1e30 100%); border-bottom:1px solid rgba(56,189,248,.15); }
.hero-2 { background: linear-gradient(135deg, #180d26 0%, #200f30 100%); border-bottom:1px solid rgba(192,132,252,.15); }
.hero-3 { background: linear-gradient(135deg, #200a12 0%, #280d16 100%); border-bottom:1px solid rgba(251,113,133,.15); }
.hero-4 { background: linear-gradient(135deg, #1c1003 0%, #231405 100%); border-bottom:1px solid rgba(251,191,36,.15); }

/* accent dots */
.accent-0 { background:var(--lime); }
.accent-1 { background:var(--sky); }
.accent-2 { background:var(--purple); }
.accent-3 { background:var(--rose); }
.accent-4 { background:var(--amber); }

/* ── BADGE ─────────────────────────────────────────────────── */
.badge {
  font-family: var(--fira);
  font-size: 0.58rem;
  letter-spacing: .08em;
  text-transform: uppercase;
  padding: .2rem .55rem;
  border-radius: 4px;
}
.badge-api    { background:var(--purple-d); color:var(--purple); border:1px solid rgba(192,132,252,.2); }
.badge-upload { background:var(--sky-d);    color:var(--sky);    border:1px solid rgba(56,189,248,.2); }
.badge-ok     { background:var(--green-d);  color:var(--green);  border:1px solid rgba(52,211,153,.2); }

/* ── META GRID ─────────────────────────────────────────────── */
.meta-row {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 0.5rem;
  margin: 0.8rem 0;
}
.meta-cell {
  background: var(--s2);
  border: 1px solid var(--border);
  border-radius: 9px;
  padding: .55rem .75rem;
}
.meta-k { font-family:var(--fira); font-size:.54rem; letter-spacing:.1em; text-transform:uppercase; color:var(--t3); margin-bottom:.15rem; }
.meta-v { font-family:var(--fira); font-size:.82rem; color:var(--t1); font-weight:500; }
.meta-v.hi0 { color:var(--lime); }
.meta-v.hi1 { color:var(--sky); }
.meta-v.hi2 { color:var(--purple); }
.meta-v.hi3 { color:var(--rose); }
.meta-v.hi4 { color:var(--amber); }

/* ── TXT PREVIEW ───────────────────────────────────────────── */
.pre {
  background: #060810;
  border: 1px solid var(--b2);
  border-radius: 9px;
  padding: .85rem 1rem;
  font-family: var(--fira);
  font-size: .7rem;
  color: #3a6655;
  max-height: 150px;
  overflow-y: auto;
  line-height: 1.65;
  white-space: pre;
  margin-bottom: .9rem;
}
.pre::-webkit-scrollbar { width: 3px; }
.pre::-webkit-scrollbar-thumb { background: var(--b2); border-radius: 2px; }

/* ── RESULT STATS ──────────────────────────────────────────── */
.stat-strip {
  display: flex;
  gap: .5rem;
  flex-wrap: wrap;
  margin: .7rem 0;
}
.stat-block {
  flex: 1;
  min-width: 80px;
  background: var(--s2);
  border: 1px solid var(--border);
  border-radius: 9px;
  padding: .6rem .8rem;
  text-align: center;
}
.stat-v { font-family:var(--syne); font-size:1.3rem; font-weight:800; line-height:1; }
.stat-k { font-family:var(--fira); font-size:.55rem; letter-spacing:.1em; text-transform:uppercase; color:var(--t3); margin-top:.15rem; }

/* ── DIVIDER ────────────────────────────────────────────────── */
.divline { height:1px; background:linear-gradient(90deg,transparent,var(--b2),transparent); margin:1rem 0; }

/* ── DOWNLOAD ROW ──────────────────────────────────────────── */
.dl-label {
  font-family: var(--fira);
  font-size: .6rem;
  letter-spacing: .08em;
  text-transform: uppercase;
  margin-bottom: .35rem;
}

/* ── MERGE ZONE ─────────────────────────────────────────────── */
.merge-hero {
  background: linear-gradient(135deg, #04160e 0%, #071f16 100%);
  border-bottom: 1px solid rgba(52,211,153,.2);
  padding: 1.2rem 1.4rem;
}
.merge-title {
  font-family: var(--syne);
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--t1);
  margin-bottom: .15rem;
}
.merge-sub {
  font-family: var(--jakarta);
  font-size: .8rem;
  color: var(--t2);
}
.merge-table {
  width: 100%;
  border-collapse: collapse;
  font-family: var(--fira);
  font-size: .75rem;
  margin: .8rem 0;
}
.merge-table th {
  color: var(--t3);
  font-size: .6rem;
  letter-spacing: .1em;
  text-transform: uppercase;
  padding: .4rem .7rem;
  border-bottom: 1px solid var(--border);
  text-align: left;
}
.merge-table td {
  color: var(--t2);
  padding: .45rem .7rem;
  border-bottom: 1px solid var(--border);
}
.merge-table td:first-child { color: var(--t1); }
.merge-table tr:last-child td { border-bottom: none; }

/* ── ALERTS ─────────────────────────────────────────────────── */
.ax { border-radius:8px; padding:.65rem 1rem; font-family:var(--jakarta); font-size:.82rem; margin:.4rem 0; }
.ax.ok   { background:var(--green-d);  border:1px solid rgba(52,211,153,.25);  color:var(--green); }
.ax.err  { background:var(--rose-d);   border:1px solid rgba(251,113,133,.25); color:var(--rose); }
.ax.warn { background:var(--amber-d);  border:1px solid rgba(251,191,36,.25);  color:var(--amber); }
.ax.info { background:var(--sky-d);    border:1px solid rgba(56,189,248,.25);  color:var(--sky); }

/* ── STREAMLIT WIDGET OVERRIDES ─────────────────────────────── */
/* Primary button */
.stButton > button {
  background: linear-gradient(135deg,#1a4d14,var(--lime)) !important;
  color: #0a1a06 !important;
  font-family: var(--syne) !important;
  font-weight: 700 !important;
  font-size: .82rem !important;
  border: none !important;
  border-radius: 8px !important;
  padding: .55rem 1.2rem !important;
  letter-spacing: .02em !important;
  transition: all .18s !important;
  box-shadow: 0 3px 12px var(--lime-g) !important;
}
.stButton > button:hover {
  filter: brightness(1.12) !important;
  box-shadow: 0 5px 18px var(--lime-g) !important;
  transform: translateY(-1px) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* Sky button */
.btn-sky > button {
  background: linear-gradient(135deg,#0c3050,var(--sky)) !important;
  color: #040f1e !important;
  box-shadow: 0 3px 12px var(--sky-g) !important;
}
.btn-sky > button:hover { box-shadow: 0 5px 18px var(--sky-g) !important; }

/* Ghost */
.btn-ghost > button {
  background: transparent !important;
  color: var(--t2) !important;
  border: 1px solid var(--b2) !important;
  box-shadow: none !important;
}
.btn-ghost > button:hover {
  border-color: var(--lime) !important;
  color: var(--lime) !important;
  background: var(--lime-d) !important;
  box-shadow: none !important;
}

/* Danger */
.btn-danger > button {
  background: transparent !important;
  color: var(--rose) !important;
  border: 1px solid rgba(251,113,133,.25) !important;
  box-shadow: none !important;
  font-size: .78rem !important;
  padding: .45rem .9rem !important;
}
.btn-danger > button:hover {
  background: var(--rose-d) !important;
  border-color: var(--rose) !important;
  box-shadow: none !important;
}

/* Green download */
.stDownloadButton > button {
  background: var(--s2) !important;
  color: var(--lime) !important;
  border: 1px solid rgba(163,230,53,.25) !important;
  border-radius: 8px !important;
  font-family: var(--jakarta) !important;
  font-weight: 600 !important;
  font-size: .8rem !important;
  padding: .55rem 1rem !important;
  width: 100% !important;
  box-shadow: none !important;
  transition: all .18s !important;
}
.stDownloadButton > button:hover {
  background: var(--lime-d) !important;
  border-color: var(--lime) !important;
  box-shadow: 0 3px 12px var(--lime-g) !important;
  transform: translateY(-1px) !important;
}
/* Sky download */
.dl-sky .stDownloadButton > button {
  color: var(--sky) !important;
  border-color: rgba(56,189,248,.25) !important;
}
.dl-sky .stDownloadButton > button:hover {
  background: var(--sky-d) !important;
  border-color: var(--sky) !important;
  box-shadow: 0 3px 12px var(--sky-g) !important;
}
/* Emerald download (merge) */
.dl-green .stDownloadButton > button {
  color: var(--green) !important;
  border-color: rgba(52,211,153,.25) !important;
  background: var(--s3) !important;
  font-size: .85rem !important;
  padding: .65rem 1rem !important;
}
.dl-green .stDownloadButton > button:hover {
  background: var(--green-d) !important;
  border-color: var(--green) !important;
  box-shadow: 0 3px 12px var(--green-g) !important;
}

/* Slider */
.stSlider > div > div > div > div { background: var(--lime) !important; }
.stSlider > div > div > div { background: var(--b2) !important; height: 3px !important; }

/* Metrics */
[data-testid="metric-container"] {
  background: var(--s2) !important; border: 1px solid var(--border) !important;
  border-radius: 9px !important; padding: .7rem .9rem !important;
}
[data-testid="metric-container"] label { color:var(--t3) !important; font-family:var(--fira) !important; font-size:.58rem !important; letter-spacing:.1em !important; }
[data-testid="metric-container"] [data-testid="stMetricValue"] { color:var(--t1) !important; font-family:var(--fira) !important; font-size:1.1rem !important; }

/* Selectbox */
.stSelectbox > div > div { background:var(--s2) !important; border:1px solid var(--b2) !important; border-radius:8px !important; color:var(--t1) !important; font-family:var(--fira) !important; font-size:.8rem !important; }
.stSelectbox label { color:var(--t2) !important; font-family:var(--fira) !important; font-size:.62rem !important; letter-spacing:.08em !important; text-transform:uppercase !important; }
.stSelectbox > div > div:focus-within { border-color:var(--lime) !important; box-shadow:0 0 0 2px var(--lime-d) !important; }

/* Radio */
.stRadio > div { flex-direction:row !important; gap:.4rem !important; flex-wrap:wrap; }
.stRadio > div > label { background:var(--s2) !important; border:1px solid var(--b2) !important; border-radius:7px !important; padding:.45rem .9rem !important; color:var(--t2) !important; font-family:var(--jakarta) !important; font-size:.8rem !important; font-weight:500 !important; cursor:pointer !important; transition:all .15s !important; }
.stRadio > div > label:hover { border-color:var(--lime) !important; color:var(--t1) !important; background:var(--lime-d) !important; }

/* Expander */
.streamlit-expanderHeader { background:var(--s2) !important; border:1px solid var(--border) !important; border-radius:8px !important; color:var(--t2) !important; font-family:var(--jakarta) !important; font-size:.82rem !important; }
.streamlit-expanderContent { background:var(--s2) !important; border:1px solid var(--border) !important; border-top:none !important; border-radius:0 0 8px 8px !important; padding:.8rem !important; }

/* Dataframe */
.stDataFrame { border-radius: 10px; overflow: hidden; }

/* File uploader */
[data-testid="stFileUploader"] {
  background: var(--s2) !important;
  border: 1px dashed var(--b2) !important;
  border-radius: 10px !important;
  padding: .5rem !important;
}
[data-testid="stFileUploader"]:hover { border-color: var(--sky) !important; }
[data-testid="stFileUploader"] label { color: var(--t2) !important; font-family: var(--jakarta) !important; font-size: .82rem !important; }

/* Caption */
.stCaption { color:var(--t3) !important; font-family:var(--fira) !important; font-size:.67rem !important; }

/* Checkbox */
.stCheckbox label { color:var(--t2) !important; font-family:var(--jakarta) !important; font-size:.84rem !important; }

hr { border:none; height:1px; background:linear-gradient(90deg,transparent,var(--b2),transparent); margin:1.2rem 0; }

.footer { text-align:center; padding:2.5rem 0 1rem; font-family:var(--fira); font-size:.55rem; letter-spacing:.15em; text-transform:uppercase; color:var(--t3); }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════
# SESSION STATE
# ═══════════════════════════════════════════════════════════════════
DEFAULTS = {
    "sessions":        [],
    "active_tab":      0,     # 0..N-1 = session idx, N = merge tab
    "fetch_msg":       None,
    "fetch_msg_type":  None,
    "last_upload_sig": None,
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ═══════════════════════════════════════════════════════════════════
# CONFIG
# ═══════════════════════════════════════════════════════════════════
API_BASE  = "https://pumpdata.duckdns.org/api"
LABEL_MAP = {
    "None":                  None,
    "Normal_Mode (0)":       0,
    "Seal Failure (1)":      1,
    "Bearing (2)":           2,
    "Shaft Misalignment (3)":3,
    "Unbalance_impeller (4)":4,
    "Cavitation (5)":        5,
}
TAB_COLORS   = ["lime","sky","purple","rose","amber"]
TAB_HEX      = {"lime":  "#a3e635","sky":   "#38bdf8","purple":"#c084fc",
                "rose":  "#fb7185","amber": "#fbbf24","green":  "#34d399"}

# ═══════════════════════════════════════════════════════════════════
# CORE FUNCTIONS
# ═══════════════════════════════════════════════════════════════════
def normalize_time(t):
    return datetime.strptime(t.strip(), "%m/%d/%Y %I:%M:%S %p").strftime("%d/%m/%Y %H:%M:%S")

def parse_vibration(txt):
    rows=[]; lines=[l.strip() for l in txt.splitlines() if l.strip()]; i=0
    tre=re.compile(r"\d+/\d+/\d+\s+\d+:\d+:\d+\s+(AM|PM)")
    pnr=re.compile(r"Peak\s+(\d+)\s+Parameter-\d+\s+([-\d.]+)\s+Parameter-\d+\s+([-\d.]+)")
    por=re.compile(r"Peak\s+(\d+)\s+Freq\s+([-\d.]+)\s+Mag\s+([-\d.]+)")
    def tf(tok,j):
        try: return float(tok[j])
        except: return None
    while i<len(lines):
        if tre.match(lines[i]):
            row={"Time":normalize_time(lines[i])}; i+=1
            for ax in ["X","Y","Z"]:
                while i<len(lines) and f"{ax} Axis" not in lines[i]: i+=1
                i+=1; peaks={}
                while i<len(lines) and not lines[i].endswith("Axis:") and not tre.match(lines[i]):
                    line=lines[i]; tok=line.split()
                    if tok and re.match(r"^Parameter-(\d+)$",tok[0]):
                        pn=int(tok[0].split("-")[1]); val=tf(tok,1)
                        if   pn==1: row[f"Parameter-1_{ax}"]=val
                        elif pn==2: row[f"Parameter-2_{ax}"]=val
                        elif pn==3: row[f"Parameter-3_{ax}"]=val
                        i+=1; continue
                    if   line.startswith("RMS"):     row[f"Parameter-1_{ax}"]=tf(tok,1)
                    elif line.startswith("PP"):       row[f"Parameter-2_{ax}"]=tf(tok,1)
                    elif line.startswith("Kurtosis"): row[f"Parameter-3_{ax}"]=tf(tok,1)
                    else:
                        m=pnr.match(line) or por.match(line)
                        if m: peaks[int(m.group(1))]=(float(m.group(2)),float(m.group(3)))
                    i+=1
                for p in range(1,9):
                    fp=2+p*2; mp=2+p*2+1
                    row[f"Parameter-{fp}_{ax}"]=peaks.get(p,(None,None))[0]
                    row[f"Parameter-{mp}_{ax}"]=peaks.get(p,(None,None))[1]
            rows.append(row)
        else: i+=1
    return pd.DataFrame(rows)

def reorder57(df):
    cols=["Time"]
    for n in range(1,4):
        for ax in ["X","Y","Z"]: cols.append(f"Parameter-{n}_{ax}")
    for p in range(1,9):
        fp=2+p*2; mp=2+p*2+1
        for ax in ["X","Y","Z"]: cols.append(f"Parameter-{fp}_{ax}")
        for ax in ["X","Y","Z"]: cols.append(f"Parameter-{mp}_{ax}")
    for c in cols:
        if c not in df.columns: df[c]=pd.NA
    return df[cols]

def to19(df):
    rows=[]; hl="Label" in df.columns
    for _,row in df.iterrows():
        for ax in ["X","Y","Z"]:
            nr={"Time":row.get("Time",pd.NA)}
            for n in range(1,4): nr[f"Parameter-{n}"]=row.get(f"Parameter-{n}_{ax}",pd.NA)
            for p in range(1,9):
                fp=2+p*2; mp=2+p*2+1
                nr[f"Parameter-{fp}"]=row.get(f"Parameter-{fp}_{ax}",pd.NA)
                nr[f"Parameter-{mp}"]=row.get(f"Parameter-{mp}_{ax}",pd.NA)
            if hl: nr["Label"]=row["Label"]
            rows.append(nr)
    c19=["Time"]+[f"Parameter-{n}" for n in range(1,20)]
    d=pd.DataFrame(rows)
    if hl: c19.append("Label")
    return d[c19]

def do_convert(idx):
    sess=st.session_state.sessions[idx]; t0=time.time()
    try: df_raw=parse_vibration(sess["txt"])
    except Exception as e: return False,str(e)
    if df_raw.empty: return False,"No records found."
    df57=reorder57(df_raw.copy())
    lv=sess.get("label")
    if lv is not None: df57["Label"]=lv
    df19=to19(df57)
    st.session_state.sessions[idx].update({
        "df57":df57,"df19":df19,"converted":True,
        "conv_time":round(time.time()-t0,2)
    })
    # Reset filtered slice when re-converting
    st.session_state.sessions[idx]["df57_filtered"]=None
    st.session_state.sessions[idx]["df19_filtered"]=None
    return True,None

def extract_meta(content, payload=None):
    tre=re.compile(r"(\d+/\d+/\d+)\s+(\d+:\d+:\d+)\s+(AM|PM)")
    ts=tre.findall(content)
    t_s=f"{ts[0][0]} {ts[0][1]} {ts[0][2]}"   if ts else "—"
    t_e=f"{ts[-1][0]} {ts[-1][1]} {ts[-1][2]}" if ts else "—"
    rec=content.count("#Vibration Value")
    sz=round(len(content)/1024,1)
    # Sample rate
    sr="—"
    if payload:
        sr=payload.get("sampling_rate") or payload.get("sample_rate") or payload.get("interval") or "—"
    if sr=="—" and len(ts)>=2:
        try:
            fmt="%m/%d/%Y %I:%M:%S %p"
            t1=datetime.strptime(f"{ts[0][0]} {ts[0][1]} {ts[0][2]}",fmt)
            t2=datetime.strptime(f"{ts[1][0]} {ts[1][1]} {ts[1][2]}",fmt)
            d=int((t2-t1).total_seconds())
            if d>0: sr=f"{d}s"
        except: pass
    # Duration
    dur="—"
    if payload:
        raw_dur=(payload.get("duration") or payload.get("duration_hours")
                 or payload.get("hours") or payload.get("duration_min") or "—")
        if raw_dur!="—":
            try:
                dv=float(str(raw_dur))
                dur=f"{dv:.0f}h" if dv==int(dv) else f"{dv}h"
            except: dur=str(raw_dur)
    if dur=="—" and len(ts)>=2:
        try:
            fmt="%m/%d/%Y %I:%M:%S %p"
            t1=datetime.strptime(f"{ts[0][0]} {ts[0][1]} {ts[0][2]}",fmt)
            te=datetime.strptime(f"{ts[-1][0]} {ts[-1][1]} {ts[-1][2]}",fmt)
            secs=int((te-t1).total_seconds())
            if secs>0:
                h=secs//3600; m=(secs%3600)//60
                dur=f"{h}h {m}m" if h else f"{m}m"
        except: pass
    # Device name
    dn="—"
    if payload:
        for k in ["device_name","deviceName","device_id","deviceId","name","sensor_name","sensorName","id","sensor_id","device","unit"]:
            val=payload.get(k)
            if val and str(val).strip().lower() not in ("","none","null","unknown","-"):
                dn=str(val).strip(); break
    return {"device_name":dn,"sampling_rate":sr,"duration":dur,"records":rec,
            "t_start":t_s,"t_end":t_e,"size_kb":sz,"fetched_at":datetime.now().strftime("%H:%M:%S")}

def hl_txt(raw):
    lines=[]
    for line in raw.splitlines():
        ls=line.strip()
        if re.match(r"\d+/\d+/\d+\s+\d+:\d+:\d+",ls):
            lines.append(f'<span style="color:#38bdf8;font-weight:500;">{line}</span>')
        elif "Axis:" in ls:
            lines.append(f'<span style="color:#a3e635;">{line}</span>')
        elif ls.startswith("Peak"):
            lines.append(f'<span style="color:#c084fc;">{line}</span>')
        elif ls.startswith("#"):
            lines.append(f'<span style="color:#2a3d5e;">{line}</span>')
        else:
            lines.append(f'<span style="color:#2e5544;">{line}</span>')
    return "<br>".join(lines)

def make_plot(df, cols, title, color):
    palettes = {
        "lime":   ["#a3e635","#65a30d","#365314"],
        "sky":    ["#38bdf8","#0284c7","#075985"],
        "purple": ["#c084fc","#9333ea","#581c87"],
        "rose":   ["#fb7185","#e11d48","#9f1239"],
        "amber":  ["#fbbf24","#d97706","#92400e"],
        "green":  ["#34d399","#059669","#064e3b"],
    }
    cl = palettes.get(color, palettes["lime"])
    fig, ax = plt.subplots(figsize=(4.8, 2.6), facecolor="#111827")
    ax.set_facecolor("#0b0e17")
    for i, c in enumerate(cols):
        if c in df.columns:
            lbl = c.split("_")[-1] if "_" in c else c
            ax.plot(df[c].values, label=lbl, linewidth=1.5, alpha=0.9, color=cl[i % len(cl)])
    ax.set_title(title, fontsize=9, color="#8ea3c3", pad=8, fontfamily="monospace")
    ax.legend(fontsize=6, framealpha=0, labelcolor="#8ea3c3", loc="best")
    ax.grid(True, alpha=0.08, linestyle="--", linewidth=0.4, color="#1f2d47")
    for sp in ax.spines.values(): sp.set_color("#1f2d47")
    ax.tick_params(labelsize=6, colors="#3d5270")
    ax.set_xlabel("Sample", fontsize=7, color="#3d5270")
    fig.tight_layout(pad=0.8)
    return fig

# ═══════════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown('<div style="font-family:var(--syne);font-size:.9rem;font-weight:700;color:var(--t1);padding:.3rem 0 1rem;border-bottom:1px solid var(--border);margin-bottom:1rem;">⚙ Settings</div>', unsafe_allow_html=True)
    file_prefix = st.text_input("Output file prefix", placeholder="e.g. pump_run_01", key="fp")
    st.markdown("---")
    st.markdown('<div class="btn-danger">', unsafe_allow_html=True)
    if st.button("🗑  Clear All Sessions", use_container_width=True, key="clr_all"):
        st.session_state.sessions=[]
        st.session_state.active_tab=0
        st.session_state.last_upload_sig=None
        st.session_state.fetch_msg=None
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    if st.session_state.sessions:
        st.markdown("---")
        st.markdown('<div style="font-family:var(--fira);font-size:.58rem;letter-spacing:.15em;text-transform:uppercase;color:var(--t3);margin-bottom:.5rem;">Sessions</div>', unsafe_allow_html=True)
        for i,sess in enumerate(st.session_state.sessions):
            col=TAB_COLORS[i % len(TAB_COLORS)]
            dot_color=TAB_HEX[col]
            st.markdown(f'<div style="display:flex;align-items:center;gap:.5rem;padding:.3rem 0;border-bottom:1px solid var(--border);font-family:var(--fira);font-size:.7rem;"><span style="width:7px;height:7px;border-radius:50%;background:{dot_color};flex-shrink:0;"></span><span style="color:{"#34d399" if sess.get("converted") else "var(--t2)"};flex:1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{sess["name"][:26]}</span></div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════
# TOP BAR  (sticky compact)
# ═══════════════════════════════════════════════════════════════════
n_sess = len(st.session_state.sessions)
n_conv = sum(1 for s in st.session_state.sessions if s.get("converted"))
status = "done" if n_sess>0 and n_conv==n_sess else ("active" if n_sess>0 else "idle")
stat_lbl = f"{n_conv}/{n_sess} converted" if n_sess>0 else "No sessions"

st.markdown(f"""
<div class="topbar">
  <div class="topbar-brand">
    <div class="brand-mark">📳</div>
    <div>
      <div class="brand-name">VibroConvert</div>
      <div class="brand-ver">v3.1 · Vibration Pipeline</div>
    </div>
  </div>
  <div style="flex:1;"></div>
  <span class="status-badge {status}">
    <span class="sbdot"></span>{stat_lbl}
  </span>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════
# SECTION 1 — ADD DATA  (compact two-column top section)
# ═══════════════════════════════════════════════════════════════════
st.markdown("""
<div class="sh">
  <div class="sh-num">1</div>
  <div class="sh-label">Add Data</div>
  <div class="sh-line"></div>
</div>
""", unsafe_allow_html=True)

col_up, col_fetch = st.columns(2)

with col_up:
    st.markdown('<p style="font-family:var(--fira);font-size:.62rem;letter-spacing:.1em;text-transform:uppercase;color:var(--sky);margin:0 0 .4rem;">📁 Upload TXT Files</p>', unsafe_allow_html=True)
    uploaded = st.file_uploader(
        "Drop TXT files", type=["txt"],
        accept_multiple_files=True,
        key="fu", label_visibility="collapsed",
    )
    if uploaded:
        sig=str(sorted([(f.name,f.size) for f in uploaded]))
        if st.session_state.last_upload_sig != sig:
            st.session_state.last_upload_sig = sig
            added=0
            for f in uploaded:
                existing=[s["name"] for s in st.session_state.sessions]
                if f.name not in existing:
                    content=f.read().decode("utf-8",errors="replace")
                    rec=content.count("#Vibration Value")
                    sz=round(len(content)/1024,1)
                    st.session_state.sessions.append({
                        "name":f.name,"source":"upload","txt":content,
                        "label":None,"records":rec,"size_kb":sz,"meta":None,
                        "converted":False,"df57":None,"df19":None,
                        "df57_filtered":None,"df19_filtered":None,
                    })
                    added+=1
            if added:
                st.session_state.active_tab=len(st.session_state.sessions)-1
                st.rerun()

with col_fetch:
    st.markdown(f'<p style="font-family:var(--fira);font-size:.62rem;letter-spacing:.1em;text-transform:uppercase;color:var(--purple);margin:0 0 .4rem;">📡 Device API — {API_BASE}/latest</p>', unsafe_allow_html=True)
    st.markdown('<div class="btn-sky">', unsafe_allow_html=True)
    fetch_btn = st.button("📡  Fetch Latest Session", use_container_width=True, key="fetch_btn")
    st.markdown('</div>', unsafe_allow_html=True)
    if st.session_state.fetch_msg:
        css={"success":"ok","error":"err","warning":"warn"}.get(st.session_state.fetch_msg_type,"info")
        st.markdown(f'<div class="ax {css}" style="margin-top:.4rem;">{st.session_state.fetch_msg}</div>', unsafe_allow_html=True)
    if fetch_btn:
        with st.spinner("Connecting…"):
            try:
                resp=requests.get(f"{API_BASE}/latest",timeout=15)
                if resp.status_code==200:
                    payload=resp.json()
                    content=payload.get("content","").strip()
                    if content:
                        meta=extract_meta(content,payload)
                        dn=meta["device_name"]
                        sess_name=f"{dn} @ {meta['fetched_at']}" if dn!="—" else f"API @ {meta['fetched_at']}"
                        existing=[s["name"] for s in st.session_state.sessions]
                        if sess_name not in existing:
                            st.session_state.sessions.append({
                                "name":sess_name,"source":"api","txt":content,
                                "label":None,"records":meta["records"],"size_kb":meta["size_kb"],
                                "meta":meta,"converted":False,"df57":None,"df19":None,
                                "df57_filtered":None,"df19_filtered":None,
                            })
                            st.session_state.active_tab=len(st.session_state.sessions)-1
                            st.session_state.fetch_msg=f"✅ Added: <strong>{sess_name}</strong> — {meta['records']:,} records"
                            st.session_state.fetch_msg_type="success"
                        else:
                            st.session_state.fetch_msg=f"ℹ Already queued: {sess_name}"
                            st.session_state.fetch_msg_type="warning"
                    else:
                        st.session_state.fetch_msg="ℹ No data yet — run the Device Simulator."
                        st.session_state.fetch_msg_type="warning"
                else:
                    st.session_state.fetch_msg=f"⚠ HTTP {resp.status_code}"
                    st.session_state.fetch_msg_type="error"
            except requests.exceptions.ConnectionError:
                st.session_state.fetch_msg=f"🔌 Cannot reach {API_BASE}"
                st.session_state.fetch_msg_type="error"
            except requests.exceptions.Timeout:
                st.session_state.fetch_msg="⏱ Timeout — retry"
                st.session_state.fetch_msg_type="error"
            except Exception as e:
                st.session_state.fetch_msg=f"❌ {e}"
                st.session_state.fetch_msg_type="error"
        st.rerun()

# ═══════════════════════════════════════════════════════════════════
# SECTION 2 — SESSIONS IN TABS
# ═══════════════════════════════════════════════════════════════════
if not st.session_state.sessions:
    st.markdown("""
    <div style="text-align:center;padding:5rem 2rem;border:1px dashed var(--b2);border-radius:16px;margin-top:2rem;">
      <div style="font-size:2.5rem;margin-bottom:.8rem;opacity:.25;">📳</div>
      <div style="font-family:var(--syne);font-size:1rem;font-weight:700;color:var(--t2);margin-bottom:.4rem;">No sessions loaded</div>
      <div style="font-family:var(--jakarta);font-size:.82rem;color:var(--t3);max-width:380px;margin:0 auto;">
        Upload TXT files or fetch from the device API above. Each becomes its own tab — process, label, download individually, then merge.
      </div>
    </div>
    """, unsafe_allow_html=True)
else:
    # clamp active tab
    merge_tab_idx = len(st.session_state.sessions)
    if st.session_state.active_tab > merge_tab_idx:
        st.session_state.active_tab = 0

    st.markdown("""
    <div class="sh" style="margin-top:2rem;">
      <div class="sh-num">2</div>
      <div class="sh-label">Process Sessions</div>
      <div class="sh-line"></div>
    </div>
    """, unsafe_allow_html=True)

    # ── TAB NAV ──────────────────────────────────────────────────
    tab_html = '<div class="tab-nav">'
    for i, sess in enumerate(st.session_state.sessions):
        col   = TAB_COLORS[i % len(TAB_COLORS)]
        is_active = (st.session_state.active_tab == i)
        cls   = f"active-{i % len(TAB_COLORS)}" if is_active else "inactive"
        short = sess["name"][:22] + ("…" if len(sess["name"])>22 else "")
        conv_mark = " ✓" if sess.get("converted") else ""
        tab_html += f'<span class="tab-btn {cls}">{short}{conv_mark}</span>'
    # merge tab
    n_conv_tabs = sum(1 for s in st.session_state.sessions if s.get("converted"))
    merge_active = st.session_state.active_tab == merge_tab_idx
    merge_cls = "merge-tab" if (merge_active and n_conv_tabs>0) else ("merge-tab inactive" if n_conv_tabs==0 else ("merge-tab" if merge_active else "inactive"))
    tab_html += f'<span class="tab-btn {merge_cls}" style="margin-left:auto;">⬡ Merge All ({n_conv_tabs}/{len(st.session_state.sessions)})</span>'
    tab_html += '</div>'
    st.markdown(tab_html, unsafe_allow_html=True)

    # Tab select buttons (invisible — Streamlit-native)
    tab_cols = st.columns(len(st.session_state.sessions) + 1)
    for i in range(len(st.session_state.sessions)):
        with tab_cols[i]:
            short = st.session_state.sessions[i]["name"][:14]+"…" if len(st.session_state.sessions[i]["name"])>14 else st.session_state.sessions[i]["name"]
            if st.button(f"Tab {i+1}", key=f"tabnav_{i}", use_container_width=True,
                         help=f"Open: {st.session_state.sessions[i]['name']}"):
                st.session_state.active_tab = i
                st.rerun()
    with tab_cols[-1]:
        if st.button("Merge", key="tabnav_merge", use_container_width=True):
            st.session_state.active_tab = merge_tab_idx
            st.rerun()

    # ── ACTIVE SESSION PANEL ──────────────────────────────────────
    at = st.session_state.active_tab

    if at < len(st.session_state.sessions):
        sess = st.session_state.sessions[at]
        col  = TAB_COLORS[at % len(TAB_COLORS)]
        hex_col = TAB_HEX[col]
        meta = sess.get("meta")
        conv = sess.get("converted", False)
        src  = sess["source"]

        st.markdown(f"""
        <div class="sess-panel">
          <div class="sess-hero hero-{at % len(TAB_COLORS)}">
            <div style="width:10px;height:10px;border-radius:50%;background:{hex_col};flex-shrink:0;box-shadow:0 0 8px {hex_col};"></div>
            <div class="sess-title">{sess['name']}</div>
            <span class="badge badge-{'api' if src=='api' else 'upload'}">{'API' if src=='api' else 'File'}</span>
            {"<span class='badge badge-ok'>✓ Converted</span>" if conv else ""}
          </div>
          <div class="sess-body">
        """, unsafe_allow_html=True)

        # Meta
        hi_cls = f"hi{at % len(TAB_COLORS)}"
        if meta:
            st.markdown(f"""
            <div class="meta-row">
              <div class="meta-cell"><div class="meta-k">Device</div><div class="meta-v {hi_cls}">{meta.get('device_name','—')}</div></div>
              <div class="meta-cell"><div class="meta-k">Sample Rate</div><div class="meta-v">{meta.get('sampling_rate','—')}</div></div>
              <div class="meta-cell"><div class="meta-k">Duration</div><div class="meta-v">{meta.get('duration','—')}</div></div>
              <div class="meta-cell"><div class="meta-k">Records</div><div class="meta-v {hi_cls}">{meta.get('records',sess['records']):,}</div></div>
              <div class="meta-cell"><div class="meta-k">Start</div><div class="meta-v" style="font-size:.7rem;">{meta.get('t_start','—')}</div></div>
              <div class="meta-cell"><div class="meta-k">End</div><div class="meta-v" style="font-size:.7rem;">{meta.get('t_end','—')}</div></div>
              <div class="meta-cell"><div class="meta-k">Size</div><div class="meta-v">{meta.get('size_kb','—')} KB</div></div>
              <div class="meta-cell"><div class="meta-k">Fetched</div><div class="meta-v">{meta.get('fetched_at','—')}</div></div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="stat-strip">
              <div class="stat-block"><div class="stat-v" style="color:{hex_col};">{sess['records']:,}</div><div class="stat-k">Records</div></div>
              <div class="stat-block"><div class="stat-v" style="color:{hex_col};">{sess['size_kb']} KB</div><div class="stat-k">File Size</div></div>
            </div>
            """, unsafe_allow_html=True)

        # TXT Preview
        with st.expander("📄 Preview raw TXT data", expanded=False):
            raw_prev = sess["txt"][:1200] + ("\n…[truncated]" if len(sess["txt"])>1200 else "")
            st.markdown(f'<div class="pre">{hl_txt(raw_prev)}</div>', unsafe_allow_html=True)

        # Label + Convert
        st.markdown('<div class="divline"></div>', unsafe_allow_html=True)
        c_lbl, c_btn, c_rm = st.columns([3,2,1])
        with c_lbl:
            lk = f"lbl_{at}"
            cur = next((k for k,v in LABEL_MAP.items() if v==sess.get("label")), "None")
            sel = st.selectbox("Fault Label", list(LABEL_MAP.keys()),
                               index=list(LABEL_MAP.keys()).index(cur), key=lk)
            nv  = LABEL_MAP[sel]
            if nv != sess.get("label"):
                st.session_state.sessions[at]["label"]     = nv
                st.session_state.sessions[at]["converted"] = False
                st.session_state.sessions[at]["df57"]      = None
                st.session_state.sessions[at]["df19"]      = None
                st.session_state.sessions[at]["df57_filtered"] = None
                st.session_state.sessions[at]["df19_filtered"] = None
        with c_btn:
            st.markdown("&nbsp;", unsafe_allow_html=True)
            if st.button("⚡  Convert Session", key=f"conv_{at}", use_container_width=True):
                with st.spinner("Converting…"):
                    ok, err = do_convert(at)
                if ok: st.rerun()
                else: st.markdown(f'<div class="ax err">❌ {err}</div>', unsafe_allow_html=True)
        with c_rm:
            st.markdown("&nbsp;", unsafe_allow_html=True)
            st.markdown('<div class="btn-danger">', unsafe_allow_html=True)
            if st.button("🗑 Remove", key=f"rm_{at}", use_container_width=True):
                st.session_state.sessions.pop(at)
                st.session_state.active_tab = max(0, at-1)
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        # ── Results ──────────────────────────────────────────────
        if conv and sess.get("df57") is not None:
            df57_base = sess["df57"].copy()
            df19_base = sess["df19"].copy()

            st.markdown('<div class="divline"></div>', unsafe_allow_html=True)
            ct = sess.get("conv_time","—")
            st.markdown(f"""
            <div class="stat-strip">
              <div class="stat-block"><div class="stat-v" style="color:{hex_col};">{len(df57_base):,}</div><div class="stat-k">Records</div></div>
              <div class="stat-block"><div class="stat-v" style="color:{hex_col};">{len(df57_base.columns)}</div><div class="stat-k">57 Cols</div></div>
              <div class="stat-block"><div class="stat-v" style="color:{hex_col};">{len(df19_base):,}</div><div class="stat-k">19-feat rows</div></div>
              <div class="stat-block"><div class="stat-v" style="color:{hex_col};">{ct}s</div><div class="stat-k">Conv Time</div></div>
            </div>
            """, unsafe_allow_html=True)

            # Time window
            df57_base["Time_dt"] = pd.to_datetime(df57_base["Time"], format="%d/%m/%Y %H:%M:%S")
            tl  = df57_base["Time_dt"].tolist()
            tmn = df57_base["Time_dt"].min().to_pydatetime()
            tmx = df57_base["Time_dt"].max().to_pydatetime()
            nn  = len(tl)

            st.markdown(f'<p style="font-family:var(--fira);font-size:.62rem;letter-spacing:.1em;text-transform:uppercase;color:{hex_col};margin:.8rem 0 .4rem;">⏱ Time Window Selection</p>', unsafe_allow_html=True)
            tw_method = st.radio("tw_method", ["⚡ Quick Slider", "🎯 Precise Input"],
                                 horizontal=True, key=f"tw_{at}", label_visibility="collapsed")

            if tw_method == "⚡ Quick Slider":
                cs, cm = st.columns([4,1])
                with cs:
                    si,ei = st.slider("range",0,nn-1,(0,nn-1),key=f"sl_{at}",label_visibility="collapsed")
                    sdt=tl[si]; edt=tl[ei]
                    st.caption(f"{sdt.strftime('%d/%m/%Y %H:%M:%S')}  →  {edt.strftime('%d/%m/%Y %H:%M:%S')}")
                with cm:
                    st.metric("Total",nn); st.metric("Selected",ei-si+1)
            else:
                c1,c2,c3=st.columns([2,2,1])
                with c1:
                    sd=st.date_input("Start Date",tmn.date(),tmn.date(),tmx.date(),key=f"sd_{at}")
                    sv=st.time_input("Start Time",tmn.time(),key=f"sv_{at}")
                    sdt=datetime.combine(sd,sv)
                with c2:
                    ed=st.date_input("End Date",tmx.date(),tmn.date(),tmx.date(),key=f"ed_{at}")
                    ev=st.time_input("End Time",tmx.time(),key=f"ev_{at}")
                    edt=datetime.combine(ed,ev)
                with c3:
                    sn=len(df57_base[(df57_base["Time_dt"]>=sdt)&(df57_base["Time_dt"]<=edt)])
                    st.metric("Total",nn); st.metric("Selected",sn)
                if sdt>edt:
                    st.markdown('<div class="ax err">⚠ Start must be before End.</div>',unsafe_allow_html=True)
                    sdt,edt=tmn,tmx

            # Apply filter
            mask    = (df57_base["Time_dt"]>=sdt)&(df57_base["Time_dt"]<=edt)
            df57_f  = df57_base[mask].drop(columns="Time_dt").reset_index(drop=True)
            df19_f  = to19(df57_f)

            # ── IMPORTANT: store filtered slices for merge ──────
            st.session_state.sessions[at]["df57_filtered"] = df57_f
            st.session_state.sessions[at]["df19_filtered"] = df19_f

            if df57_f.empty:
                st.markdown('<div class="ax warn">⚠ Empty selection — adjust the time range.</div>', unsafe_allow_html=True)
            else:
                # Plots
                st.markdown('<div class="divline"></div>', unsafe_allow_html=True)
                p1,p2,p3=st.columns(3)
                with p1: st.pyplot(make_plot(df57_f,["Parameter-1_X","Parameter-1_Y","Parameter-1_Z"],"Param-1 · RMS",col),use_container_width=True)
                with p2: st.pyplot(make_plot(df57_f,["Parameter-2_X","Parameter-2_Y","Parameter-2_Z"],"Param-2 · PP",col),use_container_width=True)
                with p3: st.pyplot(make_plot(df57_f,["Parameter-3_X","Parameter-3_Y","Parameter-3_Z"],"Param-3 · Kurtosis",col),use_container_width=True)

                # Tables
                with st.expander("📊 57-Feature Table (filtered)", expanded=False):
                    st.dataframe(df57_f, height=240, use_container_width=True)
                with st.expander("📊 19-Feature Table (filtered)", expanded=False):
                    st.dataframe(df19_f, height=240, use_container_width=True)

                # Downloads
                st.markdown('<div class="divline"></div>', unsafe_allow_html=True)
                ts_sfx  = datetime.now().strftime("%Y%m%d_%H%M%S")
                pfx     = file_prefix.strip() if file_prefix.strip() else f"sess{at+1}"
                clean   = re.sub(r'[^\w\-.]','_',sess['name'])[:25]
                f57     = f"{pfx}_{clean}_57feat.csv"
                f19     = f"{pfx}_{clean}_19feat.csv"

                st.markdown(f'<p style="font-family:var(--fira);font-size:.6rem;letter-spacing:.1em;text-transform:uppercase;color:{hex_col};margin:0 0 .5rem;">⬇ Downloads — {len(df57_f):,} records (filtered selection)</p>', unsafe_allow_html=True)
                dc1,dc2=st.columns(2)
                with dc1:
                    st.download_button(f"⬇  57-Feature CSV  ·  {len(df57_f):,} rows",
                                       df57_f.to_csv(index=False),f57,"text/csv",
                                       key=f"dl57_{at}",use_container_width=True)
                with dc2:
                    st.markdown('<div class="dl-sky">', unsafe_allow_html=True)
                    st.download_button(f"⬇  19-Feature CSV  ·  {len(df19_f):,} rows",
                                       df19_f.to_csv(index=False),f19,"text/csv",
                                       key=f"dl19_{at}",use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('</div></div>', unsafe_allow_html=True)  # close sess-body + sess-panel

    # ── MERGE TAB ─────────────────────────────────────────────────
    elif at == merge_tab_idx:
        conv_sessions = [s for s in st.session_state.sessions if s.get("converted") and s.get("df57") is not None]

        if not conv_sessions:
            st.markdown('<div class="ax warn" style="margin-top:.5rem;">⚠ Convert at least one session first — then come back here to merge.</div>', unsafe_allow_html=True)
        else:
            # Build merged using FILTERED data (respects time window slider)
            merged57_parts = []
            merged19_parts = []
            for s in conv_sessions:
                f57 = s.get("df57_filtered")
                f19 = s.get("df19_filtered")
                if f57 is None or f57.empty:
                    f57 = s["df57"]
                    f19 = s["df19"]
                merged57_parts.append(f57)
                merged19_parts.append(f19)

            merged57 = pd.concat(merged57_parts, ignore_index=True)
            merged19 = pd.concat(merged19_parts, ignore_index=True)

            # Merge hero
            st.markdown(f"""
            <div class="sess-panel">
              <div class="merge-hero">
                <div class="merge-title">⬡ Merged Dataset</div>
                <div class="merge-sub">
                  {len(conv_sessions)} session{"s" if len(conv_sessions)>1 else ""} merged
                  &nbsp;·&nbsp; uses each session's active time-window selection
                  &nbsp;·&nbsp; {len(merged57):,} total records
                </div>
              </div>
              <div class="sess-body">
            """, unsafe_allow_html=True)

            # Summary table
            rows_html=""
            for i,s in enumerate(conv_sessions):
                col=TAB_COLORS[st.session_state.sessions.index(s) % len(TAB_COLORS)]
                hx=TAB_HEX[col]
                f57_used = s.get("df57_filtered")
                used_rec  = len(f57_used) if f57_used is not None and not f57_used.empty else len(s["df57"])
                lbl_name  = next((k for k,v in LABEL_MAP.items() if v==s.get("label")), "None")
                rows_html += f'<tr><td><span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:{hx};margin-right:.5rem;"></span>{s["name"][:40]}</td><td style="color:{hx};">{used_rec:,}</td><td style="color:{"var(--purple)" if lbl_name!="None" else "var(--t3)"};">{lbl_name}</td><td style="color:var(--t3);">{"slider-filtered" if s.get("df57_filtered") is not None and not s["df57_filtered"].empty else "full"}</td></tr>'

            st.markdown(f"""
            <table class="merge-table">
              <thead><tr><th>Session</th><th>Records Used</th><th>Label</th><th>Window</th></tr></thead>
              <tbody>{rows_html}</tbody>
            </table>
            """, unsafe_allow_html=True)

            # Stats
            st.markdown(f"""
            <div class="stat-strip">
              <div class="stat-block"><div class="stat-v" style="color:var(--green);">{len(conv_sessions)}</div><div class="stat-k">Sessions</div></div>
              <div class="stat-block"><div class="stat-v" style="color:var(--green);">{len(merged57):,}</div><div class="stat-k">Total Records</div></div>
              <div class="stat-block"><div class="stat-v" style="color:var(--green);">{len(merged57.columns)}</div><div class="stat-k">57-feat Cols</div></div>
              <div class="stat-block"><div class="stat-v" style="color:var(--green);">{len(merged19):,}</div><div class="stat-k">19-feat Rows</div></div>
            </div>
            """, unsafe_allow_html=True)

            # Plots of merged
            st.markdown('<div class="divline"></div>', unsafe_allow_html=True)
            mp1,mp2,mp3=st.columns(3)
            with mp1: st.pyplot(make_plot(merged57,["Parameter-1_X","Parameter-1_Y","Parameter-1_Z"],"Merged · Param-1 RMS","green"),use_container_width=True)
            with mp2: st.pyplot(make_plot(merged57,["Parameter-2_X","Parameter-2_Y","Parameter-2_Z"],"Merged · Param-2 PP","green"),use_container_width=True)
            with mp3: st.pyplot(make_plot(merged57,["Parameter-3_X","Parameter-3_Y","Parameter-3_Z"],"Merged · Param-3 Kurtosis","green"),use_container_width=True)

            with st.expander("📊 Merged 57-Feature Table", expanded=False):
                st.dataframe(merged57, height=260, use_container_width=True)
            with st.expander("📊 Merged 19-Feature Table", expanded=False):
                st.dataframe(merged19, height=260, use_container_width=True)

            # Downloads
            st.markdown('<div class="divline"></div>', unsafe_allow_html=True)
            ts_sfx  = datetime.now().strftime("%Y%m%d_%H%M%S")
            pfx     = file_prefix.strip() if file_prefix.strip() else f"merged_{ts_sfx}"
            mf57    = f"{pfx}_MERGED_57feat.csv"
            mf19    = f"{pfx}_MERGED_19feat.csv"

            st.markdown('<p style="font-family:var(--fira);font-size:.6rem;letter-spacing:.1em;text-transform:uppercase;color:var(--green);margin:0 0 .5rem;">⬇ Download Merged Dataset</p>', unsafe_allow_html=True)
            mc1,mc2=st.columns(2)
            with mc1:
                st.markdown('<div class="dl-green">', unsafe_allow_html=True)
                st.download_button(f"⬇  Merged 57-Feature  ·  {len(merged57):,} rows",
                                   merged57.to_csv(index=False),mf57,"text/csv",
                                   key="dlm57",use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            with mc2:
                st.markdown('<div class="dl-green">', unsafe_allow_html=True)
                st.download_button(f"⬇  Merged 19-Feature  ·  {len(merged19):,} rows",
                                   merged19.to_csv(index=False),mf19,"text/csv",
                                   key="dlm19",use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('</div></div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════════
st.markdown('<div class="footer">VibroConvert v3.1 · pump_project · Vibration Analysis Pipeline</div>', unsafe_allow_html=True)
