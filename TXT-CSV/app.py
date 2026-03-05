import streamlit as st
import pandas as pd
import re
import requests
from datetime import datetime
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Vibration Data Converter",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════════
# CSS
# ══════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap');

:root {
  /* Backgrounds */
  --page-bg   : #f0f2f5;
  --white     : #ffffff;
  --surface-1 : #f7f8fa;
  --surface-2 : #eef1f6;

  /* Borders */
  --bd-subtle : #dde3ed;
  --bd-mid    : #c8d0de;
  --bd-strong : #aab2c5;

  /* Brand */
  --navy      : #0d1b3e;
  --navy-2    : #1a2f5a;
  --blue      : #1a56db;
  --blue-h    : #1447c0;
  --blue-lt   : #eef2ff;
  --blue-md   : #c7d7fc;

  /* Teal */
  --teal      : #0694a2;
  --teal-lt   : #e0f7fa;

  /* Status */
  --green     : #047857;
  --green-lt  : #ecfdf5;
  --green-bd  : #a7f3d0;
  --amber     : #92400e;
  --amber-lt  : #fffbeb;
  --amber-bd  : #fde68a;
  --red       : #991b1b;
  --red-lt    : #fef2f2;
  --red-bd    : #fecaca;

  /* Text */
  --tx-1 : #0f172a;
  --tx-2 : #374151;
  --tx-3 : #6b7280;
  --tx-4 : #9ca3af;
  --tx-5 : #d1d5db;

  /* Typography */
  --font-body : 'IBM Plex Sans', system-ui, sans-serif;
  --font-mono : 'IBM Plex Mono', monospace;

  /* Shadows */
  --sh-1 : 0 1px 2px rgba(15,23,42,.06), 0 1px 3px rgba(15,23,42,.04);
  --sh-2 : 0 3px 8px rgba(15,23,42,.07), 0 1px 3px rgba(15,23,42,.04);
  --sh-3 : 0 6px 20px rgba(15,23,42,.09), 0 2px 6px rgba(15,23,42,.05);
}

/* ── Global ────────────────────────────────────────────────── */
html, body, [class*="css"] { font-family: var(--font-body); }
.stApp { background: var(--page-bg); }
.block-container { padding: 0 2.5rem 5rem !important; max-width: 1280px !important; }
#MainMenu, footer, header { visibility: hidden; }
* { box-sizing: border-box; }

::-webkit-scrollbar        { width: 5px; height: 5px; }
::-webkit-scrollbar-track  { background: var(--page-bg); }
::-webkit-scrollbar-thumb  { background: var(--bd-mid); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--blue); }

/* ── Sidebar ───────────────────────────────────────────────── */
[data-testid="stSidebar"] {
  background: var(--navy) !important;
  border-right: none !important;
}
[data-testid="stSidebar"] .block-container { padding: 2rem 1.4rem !important; }
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] li { color: #94a3b8 !important; font-size: .82rem !important; }
[data-testid="stSidebar"] strong { color: #e2e8f0 !important; }
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 { color: #f1f5f9 !important; }
[data-testid="stSidebar"] .stTextInput > div > div > input {
  background  : rgba(255,255,255,.06) !important;
  border      : 1px solid rgba(255,255,255,.13) !important;
  color       : #f1f5f9 !important;
  border-radius: 7px !important;
  font-family : var(--font-mono) !important;
  font-size   : .84rem !important;
  padding     : .45rem .75rem !important;
}
[data-testid="stSidebar"] .stTextInput > div > div > input:focus {
  border-color : #60a5fa !important;
  box-shadow   : 0 0 0 3px rgba(96,165,250,.15) !important;
}

/* ── Top bar ───────────────────────────────────────────────── */
.topbar {
  background   : var(--white);
  border-bottom: 1px solid var(--bd-subtle);
  margin       : 0 -2.5rem 2.5rem;
  padding      : 1.4rem 2.5rem 1.3rem;
  box-shadow   : var(--sh-1);
  display      : flex;
  align-items  : flex-end;
  justify-content: space-between;
  gap: 1rem;
}
.topbar-brand { line-height: 1; }
.topbar-title {
  font-size    : 1.65rem;
  font-weight  : 700;
  color        : var(--navy);
  letter-spacing: -.025em;
  margin       : 0;
}
.topbar-title span { color: var(--blue); }
.topbar-sub {
  font-size  : .8rem;
  color      : var(--tx-4);
  margin-top : .25rem;
  font-weight: 400;
}
.topbar-badges { display: flex; gap: .5rem; align-items: center; }

/* ── Status badge ──────────────────────────────────────────── */
.sbadge {
  display       : inline-flex;
  align-items   : center;
  gap           : .35rem;
  font-size     : .7rem;
  font-weight   : 600;
  letter-spacing: .04em;
  padding       : .3rem .75rem;
  border-radius : 100px;
}
.sbadge-blue  { background: var(--blue-lt); color: var(--blue);  border: 1px solid var(--blue-md); }
.sbadge-green { background: var(--green-lt); color: var(--green); border: 1px solid var(--green-bd); }
.sbadge-gray  { background: var(--surface-1); color: var(--tx-3); border: 1px solid var(--bd-subtle); }
.sbadge-dot   { width: 6px; height: 6px; border-radius: 50%; background: currentColor; }

/* ── Step heading ──────────────────────────────────────────── */
.step-h {
  display    : flex;
  align-items: center;
  gap        : .75rem;
  margin     : 2.2rem 0 1rem;
}
.step-num {
  width        : 28px;
  height       : 28px;
  border-radius: 7px;
  background   : var(--blue);
  color        : white;
  font-size    : .78rem;
  font-weight  : 700;
  display      : flex;
  align-items  : center;
  justify-content: center;
  flex-shrink  : 0;
}
.step-label {
  font-size    : .72rem;
  font-weight  : 700;
  letter-spacing: .1em;
  text-transform: uppercase;
  color        : var(--tx-3);
}
.step-line { flex: 1; height: 1px; background: var(--bd-subtle); }
.step-count {
  font-size    : .65rem;
  color        : var(--tx-4);
  background   : var(--white);
  border       : 1px solid var(--bd-subtle);
  padding      : .15rem .55rem;
  border-radius: 100px;
}

/* ── Panel (white card) ────────────────────────────────────── */
.panel {
  background   : var(--white);
  border       : 1px solid var(--bd-subtle);
  border-radius: 12px;
  box-shadow   : var(--sh-1);
  overflow     : hidden;
  margin-bottom: 1.5rem;
  transition   : box-shadow .2s;
}
.panel:hover { box-shadow: var(--sh-2); }

.panel-header {
  background   : var(--surface-1);
  border-bottom: 1px solid var(--bd-subtle);
  padding      : 1rem 1.5rem;
  display      : flex;
  align-items  : center;
  gap          : .85rem;
}
.panel-icon {
  width        : 38px;
  height       : 38px;
  border-radius: 9px;
  display      : flex;
  align-items  : center;
  justify-content: center;
  font-size    : 1.1rem;
  flex-shrink  : 0;
}
.panel-icon.blue { background: var(--blue-lt); }
.panel-icon.teal { background: var(--teal-lt); }

.panel-name {
  font-size  : .96rem;
  font-weight: 600;
  color      : var(--navy);
  flex       : 1;
  overflow   : hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.panel-body { padding: 1.5rem; }

/* ── Row label (inside panel) ─────────────────────────────── */
.row-lbl {
  font-size    : .67rem;
  font-weight  : 700;
  letter-spacing: .1em;
  text-transform: uppercase;
  color        : var(--tx-3);
  margin       : 1.3rem 0 .6rem;
  display      : flex;
  align-items  : center;
  gap          : .5rem;
}
.row-lbl::after { content: ''; flex: 1; height: 1px; background: var(--bd-subtle); }

/* ── Info grid ─────────────────────────────────────────────── */
.info-grid {
  display              : grid;
  grid-template-columns: repeat(auto-fill, minmax(148px, 1fr));
  gap                  : .55rem;
  margin-bottom        : 1rem;
}
.info-cell {
  background   : var(--surface-1);
  border       : 1px solid var(--bd-subtle);
  border-radius: 8px;
  padding      : .65rem .9rem;
}
.info-k {
  font-size    : .6rem;
  font-weight  : 600;
  letter-spacing: .08em;
  text-transform: uppercase;
  color        : var(--tx-4);
  margin-bottom: .18rem;
}
.info-v {
  font-family: var(--font-mono);
  font-size  : .84rem;
  font-weight: 500;
  color      : var(--tx-1);
}
.info-v.accent { color: var(--blue); }
.info-v.small  { font-size: .73rem; }

/* ── Stat strip ────────────────────────────────────────────── */
.stat-strip { display: flex; gap: .55rem; flex-wrap: wrap; margin: .5rem 0 .9rem; }
.stat-block {
  flex         : 1;
  min-width    : 80px;
  background   : var(--surface-1);
  border       : 1px solid var(--bd-subtle);
  border-radius: 8px;
  padding      : .65rem 1rem;
  text-align   : center;
}
.stat-v { font-size: 1.3rem; font-weight: 700; color: var(--navy); line-height: 1; }
.stat-k { font-size: .58rem; font-weight: 600; letter-spacing: .07em; text-transform: uppercase; color: var(--tx-4); margin-top: .12rem; }

/* ── TXT preview ───────────────────────────────────────────── */
.txt-pre {
  background   : #0d1b2e;
  border-radius: 8px;
  padding      : .9rem 1.1rem;
  font-family  : var(--font-mono);
  font-size    : .71rem;
  max-height   : 170px;
  overflow-y   : auto;
  line-height  : 1.7;
  white-space  : pre;
  border       : 1px solid #1e3050;
}
.txt-pre::-webkit-scrollbar       { width: 3px; }
.txt-pre::-webkit-scrollbar-thumb { background: #2d4a6e; border-radius: 2px; }

/* ── Alerts ────────────────────────────────────────────────── */
.ax { border-radius: 8px; padding: .8rem 1.1rem; font-size: .84rem; line-height: 1.55; margin: .6rem 0; }
.ax.info  { background: var(--blue-lt);  border: 1px solid var(--blue-md);  color: #1e3a8a; }
.ax.ok    { background: var(--green-lt); border: 1px solid var(--green-bd); color: #14532d; }
.ax.warn  { background: var(--amber-lt); border: 1px solid var(--amber-bd); color: #78350f; }
.ax.error { background: var(--red-lt);   border: 1px solid var(--red-bd);   color: #7f1d1d; }

/* ── Fetch source panels ───────────────────────────────────── */
.src-panel {
  background   : var(--white);
  border       : 1px solid var(--bd-subtle);
  border-radius: 12px;
  padding      : 1.5rem;
  box-shadow   : var(--sh-1);
  height       : 100%;
}
.src-title {
  font-size    : .72rem;
  font-weight  : 700;
  letter-spacing: .09em;
  text-transform: uppercase;
  color        : var(--tx-3);
  margin       : 0 0 .75rem;
  display      : flex;
  align-items  : center;
  gap          : .4rem;
}
.src-title-dot { width: 7px; height: 7px; border-radius: 50%; flex-shrink: 0; }

/* ── Merge section ─────────────────────────────────────────── */
.merge-section {
  background   : linear-gradient(135deg, var(--navy) 0%, var(--navy-2) 100%);
  border-radius: 14px;
  padding      : 2rem 2.2rem;
  margin-top   : 2.5rem;
  box-shadow   : var(--sh-3);
}
.merge-title { font-size: 1.3rem; font-weight: 700; color: #f1f5f9; margin: 0 0 .25rem; letter-spacing: -.02em; }
.merge-sub   { font-size: .84rem; color: #64748b; margin: 0 0 1.5rem; }
.merge-stat {
  background   : rgba(255,255,255,.07);
  border       : 1px solid rgba(255,255,255,.1);
  border-radius: 8px;
  padding      : .65rem 1rem;
  text-align   : center;
}
.merge-stat-v { font-size: 1.3rem; font-weight: 700; color: #93c5fd; line-height: 1; }
.merge-stat-k { font-size: .6rem; font-weight: 600; letter-spacing: .07em; text-transform: uppercase; color: #475569; margin-top: .12rem; }
.merge-dl-banner {
  border-radius: 10px;
  padding      : 1.1rem 1.3rem .75rem;
  text-align   : center;
  margin-bottom: .5rem;
}
.merge-dl-banner.b { background: linear-gradient(135deg,#1e3a8a,#2563eb); border: 1px solid rgba(147,197,253,.18); }
.merge-dl-banner.t { background: linear-gradient(135deg,#134e4a,#0d9488); border: 1px solid rgba(153,246,228,.18); }
.merge-dl-title { color: #f1f5f9; font-weight: 600; font-size: .95rem; margin-bottom: .18rem; }
.merge-dl-sub   { color: rgba(255,255,255,.4); font-size: .75rem; }
.merge-table { width: 100%; border-collapse: collapse; margin: .8rem 0 1.2rem; }
.merge-table th { font-size: .62rem; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; color: #475569; padding: .45rem .8rem; border-bottom: 1px solid rgba(255,255,255,.08); text-align: left; }
.merge-table td { font-size: .82rem; color: #94a3b8; padding: .45rem .8rem; border-bottom: 1px solid rgba(255,255,255,.05); font-family: var(--font-mono); }
.merge-table td:first-child { color: #e2e8f0; font-family: var(--font-body); font-weight: 500; }
.merge-table tr:last-child td { border-bottom: none; }

/* ══ STREAMLIT OVERRIDES ══════════════════════════════════════ */

/* Primary button */
.stButton > button {
  background    : var(--blue) !important;
  color         : white !important;
  font-family   : var(--font-body) !important;
  font-weight   : 600 !important;
  font-size     : .87rem !important;
  border        : none !important;
  border-radius : 8px !important;
  padding       : .6rem 1.5rem !important;
  transition    : all .18s !important;
  box-shadow    : 0 1px 4px rgba(26,86,219,.3) !important;
  letter-spacing: .01em !important;
}
.stButton > button:hover {
  background : var(--blue-h) !important;
  box-shadow : 0 4px 14px rgba(26,86,219,.4) !important;
  transform  : translateY(-1px) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

.btn-teal > button { background: var(--teal) !important; box-shadow: 0 1px 4px rgba(6,148,162,.3) !important; }
.btn-teal > button:hover { background: #0e7490 !important; box-shadow: 0 4px 14px rgba(6,148,162,.4) !important; }

.btn-ghost > button {
  background : var(--white) !important;
  color      : var(--tx-2) !important;
  border     : 1px solid var(--bd-mid) !important;
  box-shadow : var(--sh-1) !important;
}
.btn-ghost > button:hover { border-color: var(--blue) !important; color: var(--blue) !important; }

.btn-sm > button {
  background  : var(--white) !important;
  color       : var(--red) !important;
  border      : 1px solid var(--red-bd) !important;
  box-shadow  : none !important;
  font-size   : .77rem !important;
  padding     : .38rem .8rem !important;
}
.btn-sm > button:hover { background: var(--red-lt) !important; box-shadow: none !important; transform: none !important; }

/* Download buttons */
.stDownloadButton > button {
  background    : var(--blue) !important;
  color         : white !important;
  border        : none !important;
  border-radius : 8px !important;
  font-family   : var(--font-body) !important;
  font-weight   : 600 !important;
  font-size     : .87rem !important;
  padding       : .65rem 1.2rem !important;
  width         : 100% !important;
  transition    : all .18s !important;
  box-shadow    : 0 1px 4px rgba(26,86,219,.3) !important;
}
.stDownloadButton > button:hover {
  background : var(--blue-h) !important;
  box-shadow : 0 4px 14px rgba(26,86,219,.4) !important;
  transform  : translateY(-1px) !important;
}
.dl-teal .stDownloadButton > button { background: var(--teal) !important; box-shadow: 0 1px 4px rgba(6,148,162,.3) !important; }
.dl-teal .stDownloadButton > button:hover { background: #0e7490 !important; box-shadow: 0 4px 14px rgba(6,148,162,.4) !important; }
.dl-merge-b .stDownloadButton > button { background: linear-gradient(135deg,#1e3a8a,#2563eb) !important; font-size: .92rem !important; padding: .7rem 1.2rem !important; box-shadow: 0 3px 12px rgba(26,86,219,.4) !important; }
.dl-merge-t .stDownloadButton > button { background: linear-gradient(135deg,#134e4a,#0d9488) !important; font-size: .92rem !important; padding: .7rem 1.2rem !important; box-shadow: 0 3px 12px rgba(6,148,162,.4) !important; }

/* Slider */
.stSlider > div > div > div > div { background: var(--blue) !important; }
.stSlider > div > div > div { background: var(--bd-mid) !important; height: 4px !important; }

/* Metrics */
[data-testid="metric-container"] {
  background    : var(--surface-1) !important;
  border        : 1px solid var(--bd-subtle) !important;
  border-radius : 8px !important;
  padding       : .7rem .9rem !important;
}
[data-testid="metric-container"] label { color: var(--tx-4) !important; font-size: .62rem !important; font-weight: 600 !important; letter-spacing: .07em !important; text-transform: uppercase !important; }
[data-testid="metric-container"] [data-testid="stMetricValue"] { color: var(--navy) !important; font-size: 1.15rem !important; font-weight: 700 !important; }

/* Selectbox */
.stSelectbox > div > div { background: var(--white) !important; border: 1px solid var(--bd-mid) !important; border-radius: 7px !important; color: var(--tx-1) !important; font-size: .86rem !important; box-shadow: var(--sh-1) !important; }
.stSelectbox label { color: var(--tx-2) !important; font-size: .72rem !important; font-weight: 600 !important; letter-spacing: .06em !important; text-transform: uppercase !important; }
.stSelectbox > div > div:focus-within { border-color: var(--blue) !important; box-shadow: 0 0 0 3px rgba(26,86,219,.12) !important; }

/* Radio */
.stRadio > div { flex-direction: row !important; gap: .4rem !important; flex-wrap: wrap; }
.stRadio > div > label { background: var(--white) !important; border: 1px solid var(--bd-mid) !important; border-radius: 7px !important; padding: .45rem .95rem !important; color: var(--tx-2) !important; font-size: .84rem !important; font-weight: 500 !important; cursor: pointer !important; transition: all .15s !important; box-shadow: var(--sh-1) !important; }
.stRadio > div > label:hover { border-color: var(--blue) !important; color: var(--blue) !important; }
.stRadio label[data-baseweb="radio"] span { background: var(--blue) !important; }

/* Checkbox */
.stCheckbox label { color: var(--tx-2) !important; font-size: .86rem !important; font-weight: 400 !important; }

/* Dataframe */
.stDataFrame { border-radius: 8px; overflow: hidden; box-shadow: var(--sh-1); }

/* File uploader */
[data-testid="stFileUploader"] { background: var(--surface-1) !important; border: 1.5px dashed var(--bd-mid) !important; border-radius: 9px !important; transition: border-color .18s !important; }
[data-testid="stFileUploader"]:hover { border-color: var(--blue) !important; }
[data-testid="stFileUploader"] label { color: var(--tx-3) !important; font-size: .85rem !important; }

/* Caption */
.stCaption { color: var(--tx-4) !important; font-size: .71rem !important; }

/* Spinner */
.stSpinner > div { border-top-color: var(--blue) !important; }

/* Expander — we don't use Streamlit expanders, using custom panels instead */
.streamlit-expanderHeader { background: var(--white) !important; border: 1px solid var(--bd-subtle) !important; border-radius: 8px !important; color: var(--tx-2) !important; font-size: .86rem !important; box-shadow: var(--sh-1) !important; }
.streamlit-expanderContent { background: var(--white) !important; border: 1px solid var(--bd-subtle) !important; border-top: none !important; border-radius: 0 0 8px 8px !important; padding: 1rem !important; }

hr { border: none; height: 1px; background: var(--bd-subtle); margin: 1.5rem 0; }

.pg-footer { text-align: center; padding: 2.5rem 0 1rem; font-size: .75rem; color: var(--tx-4); }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
# CONSTANTS
# ══════════════════════════════════════════════════════════════════════
API_BASE  = "https://pumpdata.duckdns.org/api"

LABEL_MAP = {
    "Normal_Mode (0)":        0,
    "Seal Failure (1)":       1,
    "Bearing (2)":            2,
    "Shaft Misalignment (3)": 3,
    "Unbalance_impeller (4)": 4,
    "Cavitation (5)":         5,
}

# Sampling rate integer → human label (matches device.py rate_map)
SR_LABEL = {5:"5 sec", 10:"10 sec", 15:"15 sec", 30:"30 sec"}

# ══════════════════════════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════════════════════════
for k, v in {
    "api_sessions"   : [],   # list of {name, txt, meta}
    "fetch_msg"      : None,
    "fetch_type"     : None,
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ══════════════════════════════════════════════════════════════════════
# CORE LOGIC  (unchanged from reference)
# ══════════════════════════════════════════════════════════════════════
def normalize_time(t):
    return datetime.strptime(t.strip(), "%m/%d/%Y %I:%M:%S %p").strftime("%d/%m/%Y %H:%M:%S")

def parse_vibration(txt):
    rows=[]; lines=[l.strip() for l in txt.splitlines() if l.strip()]; i=0
    time_re = re.compile(r"\d+/\d+/\d+\s+\d+:\d+:\d+\s+(AM|PM)")
    pnr = re.compile(r"Peak\s+(\d+)\s+Parameter-\d+\s+([-\d.]+)\s+Parameter-\d+\s+([-\d.]+)")
    por = re.compile(r"Peak\s+(\d+)\s+Freq\s+([-\d.]+)\s+Mag\s+([-\d.]+)")
    def tf(tok,j):
        try: return float(tok[j])
        except: return None
    while i<len(lines):
        if time_re.match(lines[i]):
            row={"Time":normalize_time(lines[i])}; i+=1
            for axis in ["X","Y","Z"]:
                while i<len(lines) and f"{axis} Axis" not in lines[i]: i+=1
                i+=1; peaks={}
                while i<len(lines) and not lines[i].endswith("Axis:") and not time_re.match(lines[i]):
                    line=lines[i]; tok=line.split()
                    if tok and re.match(r"^Parameter-(\d+)$",tok[0]):
                        pn=int(tok[0].split("-")[1]); val=tf(tok,1)
                        if   pn==1: row[f"Parameter-1_{axis}"]=val
                        elif pn==2: row[f"Parameter-2_{axis}"]=val
                        elif pn==3: row[f"Parameter-3_{axis}"]=val
                        i+=1; continue
                    if   line.startswith("RMS"):     row[f"Parameter-1_{axis}"]=tf(tok,1)
                    elif line.startswith("PP"):       row[f"Parameter-2_{axis}"]=tf(tok,1)
                    elif line.startswith("Kurtosis"): row[f"Parameter-3_{axis}"]=tf(tok,1)
                    else:
                        m=pnr.match(line) or por.match(line)
                        if m: peaks[int(m.group(1))]=(float(m.group(2)),float(m.group(3)))
                    i+=1
                for p in range(1,9):
                    fp=2+p*2; mp=2+p*2+1
                    row[f"Parameter-{fp}_{axis}"]=peaks.get(p,(None,None))[0]
                    row[f"Parameter-{mp}_{axis}"]=peaks.get(p,(None,None))[1]
            rows.append(row)
        else: i+=1
    return pd.DataFrame(rows)

def reorder_columns_57(df):
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

def convert_to_19_features(df):
    rows_19=[]; has_label="Label" in df.columns
    for _,row in df.iterrows():
        for axis in ["X","Y","Z"]:
            nr={"Time":row.get("Time",pd.NA)}
            for n in range(1,4): nr[f"Parameter-{n}"]=row.get(f"Parameter-{n}_{axis}",pd.NA)
            for p in range(1,9):
                fp=2+p*2; mp=2+p*2+1
                nr[f"Parameter-{fp}"]=row.get(f"Parameter-{fp}_{axis}",pd.NA)
                nr[f"Parameter-{mp}"]=row.get(f"Parameter-{mp}_{axis}",pd.NA)
            if has_label: nr["Label"]=row["Label"]
            rows_19.append(nr)
    c19=["Time"]+[f"Parameter-{n}" for n in range(1,20)]
    d=pd.DataFrame(rows_19)
    if has_label: c19.append("Label")
    return d[c19]

def extract_meta(content, payload=None):
    """Extract rich device info — uses exact keys from device.py"""
    tre = re.compile(r"(\d+/\d+/\d+)\s+(\d+:\d+:\d+)\s+(AM|PM)")
    ts  = tre.findall(content)
    t_s = f"{ts[0][0]} {ts[0][1]} {ts[0][2]}"    if ts else "—"
    t_e = f"{ts[-1][0]} {ts[-1][1]} {ts[-1][2]}" if ts else "—"
    rec = content.count("#Vibration Value")
    sz  = round(len(content)/1024, 1)

    # ── Device Name  (device.py sends key "device_name") ──────────
    dn = "—"
    if payload:
        # exact key first, then fallbacks
        for key in ["device_name", "deviceName", "device_id", "deviceId",
                    "name", "sensor_name", "id", "device"]:
            v = payload.get(key)
            if v and str(v).strip().lower() not in ("", "none", "null", "unknown", "-", "n/a"):
                dn = str(v).strip()
                break

    # ── Sampling Rate  (device.py sends key "sampling_rate" as int seconds) ──
    sr = "—"
    if payload:
        raw_sr = payload.get("sampling_rate") or payload.get("sample_rate") or payload.get("interval")
        if raw_sr is not None:
            try:
                sr_int = int(raw_sr)
                sr = SR_LABEL.get(sr_int, f"{sr_int}s")
            except:
                sr = str(raw_sr)
    # fallback: auto-detect from timestamps
    if sr == "—" and len(ts) >= 2:
        try:
            fmt = "%m/%d/%Y %I:%M:%S %p"
            t1  = datetime.strptime(f"{ts[0][0]} {ts[0][1]} {ts[0][2]}", fmt)
            t2  = datetime.strptime(f"{ts[1][0]} {ts[1][1]} {ts[1][2]}", fmt)
            d   = int((t2-t1).total_seconds())
            if d > 0: sr = SR_LABEL.get(d, f"{d}s")
        except: pass

    # ── Duration  (device.py sends key "duration_val" as int hours) ──
    dur = "—"
    if payload:
        raw_dur = payload.get("duration_val") or payload.get("duration") or payload.get("duration_hours") or payload.get("hours")
        if raw_dur is not None:
            try:
                dv = int(float(str(raw_dur)))
                dur = f"{dv} hour{'s' if dv!=1 else ''}"
            except:
                dur = str(raw_dur)
    # fallback: compute from timestamps
    if dur == "—" and len(ts) >= 2:
        try:
            fmt  = "%m/%d/%Y %I:%M:%S %p"
            t1   = datetime.strptime(f"{ts[0][0]} {ts[0][1]} {ts[0][2]}", fmt)
            te   = datetime.strptime(f"{ts[-1][0]} {ts[-1][1]} {ts[-1][2]}", fmt)
            secs = int((te-t1).total_seconds())
            if secs > 0:
                h = secs//3600; m = (secs%3600)//60
                dur = f"{h}h {m}m" if h else f"{m}m"
        except: pass

    # ── Derived stats ──────────────────────────────────────────────
    # Records per hour
    rph = "—"
    if rec > 0 and sr != "—":
        try:
            sr_secs = int(str(sr).replace("s","").replace(" sec","").strip())
            rph = f"{3600//sr_secs:,}"
        except: pass

    # Total expected records
    exp_rec = "—"
    if dur != "—" and sr != "—":
        try:
            hours = int(str(dur).split()[0])
            sr_secs = int(str(sr).replace("s","").replace(" sec","").strip())
            exp_rec = f"{(hours*3600)//sr_secs:,}"
        except: pass

    return {
        "device_name"  : dn,
        "sampling_rate": sr,
        "duration"     : dur,
        "records"      : rec,
        "expected_rec" : exp_rec,
        "rec_per_hour" : rph,
        "t_start"      : t_s,
        "t_end"        : t_e,
        "size_kb"      : sz,
        "fetched_at"   : datetime.now().strftime("%H:%M:%S"),
        "fetched_date" : datetime.now().strftime("%d %b %Y"),
    }

def hl_txt(raw):
    out = []
    for line in raw.splitlines():
        ls = line.strip()
        if re.match(r"\d+/\d+/\d+\s+\d+:\d+:\d+", ls):
            out.append(f'<span style="color:#60a5fa;font-weight:500;">{line}</span>')
        elif "Axis:" in ls:
            out.append(f'<span style="color:#34d399;">{line}</span>')
        elif ls.startswith("Peak"):
            out.append(f'<span style="color:#a78bfa;">{line}</span>')
        elif ls.startswith("#"):
            out.append(f'<span style="color:#2d4a6e;">{line}</span>')
        else:
            out.append(f'<span style="color:#4b6785;">{line}</span>')
    return "<br>".join(out)

def make_chart(df, cols, title, palette):
    palettes = {
        "blue" : ["#1a56db","#3b82f6","#93c5fd"],
        "teal" : ["#0694a2","#0891b2","#67e8f9"],
        "amber": ["#b45309","#d97706","#fbbf24"],
    }
    cl = palettes.get(palette, palettes["blue"])
    fig, ax = plt.subplots(figsize=(5, 3.2), facecolor="white")
    ax.set_facecolor("#f7f8fa")
    for i, c in enumerate(cols):
        if c in df.columns:
            ax.plot(df[c].values, label=c.split("_")[-1] if "_" in c else c,
                    linewidth=2, alpha=0.88, color=cl[i % len(cl)])
    ax.set_title(title, fontsize=9.5, fontweight="bold", color="#0f172a", pad=9)
    ax.set_xlabel("Sample", fontsize=7.5, color="#9ca3af")
    ax.legend(fontsize=7.5, framealpha=0.95, loc="best", frameon=True,
              facecolor="white", edgecolor="#e5e9f0")
    ax.grid(True, alpha=0.22, linestyle="--", linewidth=0.5, color="#dde3ed")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#dde3ed")
    ax.spines["bottom"].set_color("#dde3ed")
    ax.tick_params(labelsize=7.5, colors="#9ca3af")
    fig.tight_layout(pad=0.9)
    return fig

# ══════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style="padding:.2rem 0 1.5rem;border-bottom:1px solid rgba(255,255,255,.09);margin-bottom:1.4rem;">
      <div style="font-size:1.05rem;font-weight:700;color:#f1f5f9;letter-spacing:-.01em;line-height:1.2;">
        Vibration Data<br><span style="color:#60a5fa;">Converter</span>
      </div>
      <div style="font-size:.62rem;color:#374151;margin-top:.4rem;letter-spacing:.1em;text-transform:uppercase;">
        pump_project · v4.0
      </div>
    </div>
    """, unsafe_allow_html=True)

    file_prefix = st.text_input(
        "Output file prefix",
        placeholder="e.g. pump_bearing_01",
        key="fp",
        help="Prefix used for all downloaded CSV filenames",
    )

    st.markdown("""
    <div style="margin:1.2rem 0;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.08);
         border-radius:8px;padding:.9rem 1rem;">
      <div style="font-size:.62rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;
           color:#374151;margin-bottom:.6rem;">Output Formats</div>
      <div style="color:#64748b;font-size:.8rem;line-height:1.7;">
        <strong style="color:#94a3b8;">57-feature CSV</strong><br>
        Time + Param-1..19 × X, Y, Z<br><br>
        <strong style="color:#94a3b8;">19-feature CSV</strong><br>
        Axes stacked as rows (×3 rows)
      </div>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.api_sessions:
        st.markdown('<div style="font-size:.62rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#374151;margin:1.2rem 0 .5rem;">API Sessions</div>', unsafe_allow_html=True)
        for s in st.session_state.api_sessions:
            st.markdown(f'<div style="font-size:.75rem;color:#64748b;padding:.3rem 0;border-bottom:1px solid rgba(255,255,255,.05);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">📡 {s["name"][:30]}</div>', unsafe_allow_html=True)
        st.markdown('<div style="margin-top:.8rem;"></div>', unsafe_allow_html=True)
        st.markdown('<div class="btn-sm">', unsafe_allow_html=True)
        if st.button("Clear API Sessions", use_container_width=True, key="clr_api"):
            st.session_state.api_sessions = []
            st.session_state.fetch_msg    = None
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
# TOP BAR
# ══════════════════════════════════════════════════════════════════════
n_total = len(st.session_state.api_sessions)
if hasattr(st.session_state, "fu") and st.session_state.fu:
    n_total += len(st.session_state.fu)

st.markdown(f"""
<div class="topbar">
  <div class="topbar-brand">
    <h1 class="topbar-title">Vibration Data <span>Converter</span></h1>
    <p class="topbar-sub">Upload TXT files · Fetch from device API · Configure time window · Export 57-feat &amp; 19-feat CSVs · Merge all</p>
  </div>
  <div class="topbar-badges">
    <span class="sbadge sbadge-blue"><span class="sbadge-dot"></span>pump_project</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
# STEP 1 — LOAD DATA
# ══════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="step-h">
  <div class="step-num">1</div>
  <div class="step-label">Load Data</div>
  <div class="step-line"></div>
</div>
""", unsafe_allow_html=True)

col_upload, col_fetch = st.columns(2, gap="large")

# ── Upload panel ────────────────────────────────────────────────────
with col_upload:
    st.markdown("""
    <div class="src-panel">
      <div class="src-title">
        <span class="src-title-dot" style="background:#1a56db;"></span>
        Upload TXT Files
      </div>
    </div>
    """, unsafe_allow_html=True)
    uploaded_files = st.file_uploader(
        "Drop TXT files here or click to browse",
        type=["txt"], accept_multiple_files=True,
        key="fu", label_visibility="collapsed",
        help="Upload one or more vibration log TXT files",
    )
    st.markdown('<p style="font-size:.75rem;color:#9ca3af;margin:.4rem 0 0;">Supports multiple files — each processed independently</p>', unsafe_allow_html=True)

# ── Fetch panel ─────────────────────────────────────────────────────
with col_fetch:
    st.markdown(f"""
    <div class="src-panel">
      <div class="src-title">
        <span class="src-title-dot" style="background:#0694a2;"></span>
        Fetch from Device API
      </div>
      <code style="font-size:.72rem;color:#0694a2;background:#e0f7fa;
            border:1px solid #b2ebf2;border-radius:5px;padding:.22rem .65rem;
            display:inline-block;margin-bottom:.7rem;">GET {API_BASE}/latest</code>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="btn-teal">', unsafe_allow_html=True)
    fetch_clicked = st.button("📡  Fetch Latest Device Session", use_container_width=True, key="fetch_btn")
    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.fetch_msg:
        css  = {"success":"ok","error":"error","warning":"warn"}.get(st.session_state.fetch_type,"info")
        icon = {"ok":"✅","error":"❌","warn":"⚠️","info":"ℹ️"}.get(css,"ℹ️")
        st.markdown(f'<div class="ax {css}" style="margin-top:.5rem;">{icon} {st.session_state.fetch_msg}</div>', unsafe_allow_html=True)

    if fetch_clicked:
        with st.spinner("Connecting to device API…"):
            try:
                resp    = requests.get(f"{API_BASE}/latest", timeout=15)
                if resp.status_code == 200:
                    payload = resp.json()
                    content = payload.get("content", "").strip()
                    if content:
                        meta  = extract_meta(content, payload)
                        dn    = meta["device_name"]
                        sname = f"{dn} @ {meta['fetched_at']}" if dn != "—" else f"API Session @ {meta['fetched_at']}"
                        if sname not in [s["name"] for s in st.session_state.api_sessions]:
                            st.session_state.api_sessions.append({"name": sname, "txt": content, "meta": meta})
                            st.session_state.fetch_msg  = f"Added <strong>{sname}</strong> — {meta['records']:,} records, {meta['size_kb']} KB"
                            st.session_state.fetch_type = "success"
                        else:
                            st.session_state.fetch_msg  = f"Already loaded: {sname}"
                            st.session_state.fetch_type = "warning"
                    else:
                        st.session_state.fetch_msg  = "No data available yet. Run the Device Simulator first."
                        st.session_state.fetch_type = "warning"
                else:
                    st.session_state.fetch_msg  = f"Server returned HTTP {resp.status_code}."
                    st.session_state.fetch_type = "error"
            except requests.exceptions.ConnectionError:
                st.session_state.fetch_msg  = f"Cannot reach {API_BASE}. Ensure api_server.py is running."
                st.session_state.fetch_type = "error"
            except requests.exceptions.Timeout:
                st.session_state.fetch_msg  = "Request timed out. Please try again."
                st.session_state.fetch_type = "error"
            except Exception as e:
                st.session_state.fetch_msg  = f"Error: {e}"
                st.session_state.fetch_type = "error"
        st.rerun()

# ══════════════════════════════════════════════════════════════════════
# BUILD UNIFIED FILE LIST
# ══════════════════════════════════════════════════════════════════════
file_list = []
if uploaded_files:
    for f in uploaded_files:
        content = f.read().decode("utf-8", errors="replace")
        file_list.append({"name": f.name, "txt": content, "source": "upload", "meta": None})
for api_s in st.session_state.api_sessions:
    file_list.append({"name": api_s["name"], "txt": api_s["txt"], "source": "api", "meta": api_s.get("meta")})

# ══════════════════════════════════════════════════════════════════════
# STEP 2 — PROCESS & EXPORT
# ══════════════════════════════════════════════════════════════════════
if not file_list:
    st.markdown("""
    <div style="text-align:center;padding:4.5rem 2rem;background:white;border:1px solid #dde3ed;
         border-radius:12px;margin:1.8rem 0;box-shadow:0 1px 3px rgba(15,23,42,.05);">
      <div style="font-size:2.5rem;margin-bottom:.8rem;opacity:.25;">📊</div>
      <div style="font-size:1rem;font-weight:700;color:#0d1b3e;margin-bottom:.5rem;">No data loaded yet</div>
      <div style="font-size:.85rem;color:#9ca3af;max-width:460px;margin:0 auto;line-height:1.65;">
        Upload vibration TXT files above or fetch the latest session from the device API.
        Each file becomes its own section — configure the time window, view feature charts,
        and download 57-feature and 19-feature CSVs individually. A merged download
        appears at the bottom once all sessions are ready.
      </div>
    </div>
    """, unsafe_allow_html=True)
else:
    n = len(file_list)
    st.markdown(f"""
    <div class="step-h">
      <div class="step-num">2</div>
      <div class="step-label">Configure &amp; Export</div>
      <div class="step-line"></div>
      <span class="step-count">{n} session{"s" if n!=1 else ""}</span>
    </div>
    """, unsafe_allow_html=True)

    all_dfs_57  = []
    all_dfs_19  = []
    merge_rows  = []

    for file in file_list:
        fname  = file["name"]
        src    = file["source"]
        meta   = file.get("meta")
        is_api = src == "api"
        icon   = "📡" if is_api else "📄"

        # ── Panel header ─────────────────────────────────────────
        icon_cls = "teal" if is_api else "blue"
        src_badge_color = "#0694a2" if is_api else "#1a56db"
        src_badge_bg    = "#e0f7fa" if is_api else "#eef2ff"
        src_badge_bd    = "#b2ebf2" if is_api else "#c7d7fc"
        src_label       = "API"    if is_api else "File"

        st.markdown(f"""
        <div class="panel">
          <div class="panel-header">
            <div class="panel-icon {icon_cls}">{icon}</div>
            <div class="panel-name">{fname}</div>
            <span style="font-size:.65rem;font-weight:600;letter-spacing:.05em;text-transform:uppercase;
                  padding:.2rem .65rem;border-radius:100px;background:{src_badge_bg};
                  color:{src_badge_color};border:1px solid {src_badge_bd};">{src_label}</span>
          </div>
          <div class="panel-body">
        """, unsafe_allow_html=True)

        # ── Remove button for API sessions ────────────────────────
        if is_api:
            r1, r2 = st.columns([6,1])
            with r2:
                st.markdown('<div class="btn-sm">', unsafe_allow_html=True)
                if st.button("Remove", key=f"rm_{fname}"):
                    st.session_state.api_sessions = [
                        s for s in st.session_state.api_sessions if s["name"] != fname
                    ]
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

        # ── Device info (API) ─────────────────────────────────────
        if meta:
            # Core metrics
            st.markdown('<div class="row-lbl">Device Information</div>', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="info-grid">
              <div class="info-cell">
                <div class="info-k">Device Name</div>
                <div class="info-v accent">{meta['device_name']}</div>
              </div>
              <div class="info-cell">
                <div class="info-k">Sampling Rate</div>
                <div class="info-v">{meta['sampling_rate']}</div>
              </div>
              <div class="info-cell">
                <div class="info-k">Configured Duration</div>
                <div class="info-v">{meta['duration']}</div>
              </div>
              <div class="info-cell">
                <div class="info-k">Records in File</div>
                <div class="info-v accent">{meta['records']:,}</div>
              </div>
              <div class="info-cell">
                <div class="info-k">Expected Records</div>
                <div class="info-v">{meta['expected_rec']}</div>
              </div>
              <div class="info-cell">
                <div class="info-k">Records / Hour</div>
                <div class="info-v">{meta['rec_per_hour']}</div>
              </div>
              <div class="info-cell">
                <div class="info-k">Session Start</div>
                <div class="info-v small">{meta['t_start']}</div>
              </div>
              <div class="info-cell">
                <div class="info-k">Session End</div>
                <div class="info-v small">{meta['t_end']}</div>
              </div>
              <div class="info-cell">
                <div class="info-k">File Size</div>
                <div class="info-v">{meta['size_kb']} KB</div>
              </div>
              <div class="info-cell">
                <div class="info-k">Fetched</div>
                <div class="info-v small">{meta['fetched_date']} {meta['fetched_at']}</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

        # ── TXT preview ───────────────────────────────────────────
        st.markdown('<div class="row-lbl">Raw Data Preview</div>', unsafe_allow_html=True)
        raw_prev = file["txt"][:1100] + ("\n…[truncated]" if len(file["txt"])>1100 else "")
        st.markdown(f'<div class="txt-pre">{hl_txt(raw_prev)}</div>', unsafe_allow_html=True)

        # ── Label ─────────────────────────────────────────────────
        st.markdown('<div class="row-lbl">Label Configuration</div>', unsafe_allow_html=True)
        lc1, lc2 = st.columns([1,2])
        with lc1:
            use_label = st.checkbox("Attach fault label", key=f"chk_{fname}")
        with lc2:
            label_value = None
            if use_label:
                label_value = LABEL_MAP[st.selectbox(
                    "Fault type", list(LABEL_MAP.keys()),
                    key=f"lbl_{fname}", label_visibility="collapsed",
                )]

        # ── Parse ─────────────────────────────────────────────────
        df = parse_vibration(file["txt"])
        if df.empty:
            st.markdown('<div class="ax error">❌ No vibration records found. Please verify the file format.</div>', unsafe_allow_html=True)
            st.markdown('</div></div>', unsafe_allow_html=True)
            continue

        df_57 = reorder_columns_57(df)

        # ── Time window ───────────────────────────────────────────
        st.markdown('<div class="row-lbl">Time Window Selection</div>', unsafe_allow_html=True)
        df_57["Time_dt"] = pd.to_datetime(df_57["Time"], format="%d/%m/%Y %H:%M:%S")
        time_list = df_57["Time_dt"].tolist()
        tmin = df_57["Time_dt"].min().to_pydatetime()
        tmax = df_57["Time_dt"].max().to_pydatetime()
        N    = len(time_list)

        method = st.radio(
            "Method", ["⚡ Quick Slider", "🎯 Precise Time Input"],
            horizontal=True, key=f"tw_{fname}", label_visibility="collapsed",
        )

        if method == "⚡ Quick Slider":
            cs, cm = st.columns([4, 1])
            with cs:
                si, ei = st.slider("Range", 0, N-1, (0, N-1),
                                   key=f"sl_{fname}", label_visibility="collapsed")
                start = time_list[si]; end = time_list[ei]
                st.caption(f"From  {start.strftime('%d/%m/%Y %H:%M:%S')}   to   {end.strftime('%d/%m/%Y %H:%M:%S')}")
            with cm:
                st.metric("Total", N)
                st.metric("Selected", ei - si + 1)
        else:
            c1, c2, c3 = st.columns([2, 2, 1])
            with c1:
                sd = st.date_input("Start Date", tmin.date(), tmin.date(), tmax.date(), key=f"sd_{fname}")
                sv = st.time_input("Start Time", tmin.time(), key=f"sv_{fname}")
                start = datetime.combine(sd, sv)
            with c2:
                ed = st.date_input("End Date", tmax.date(), tmin.date(), tmax.date(), key=f"ed_{fname}")
                ev = st.time_input("End Time", tmax.time(), key=f"ev_{fname}")
                end = datetime.combine(ed, ev)
            with c3:
                sn = len(df_57[(df_57["Time_dt"] >= start) & (df_57["Time_dt"] <= end)])
                st.metric("Total", N); st.metric("Selected", sn)
            if start > end:
                st.markdown('<div class="ax error">⚠️ Start must be before end time.</div>', unsafe_allow_html=True)
                start, end = tmin, tmax

        df_57 = df_57[(df_57["Time_dt"] >= start) & (df_57["Time_dt"] <= end)]
        df_57 = df_57.drop(columns="Time_dt").reset_index(drop=True)

        if use_label:
            df_57["Label"] = label_value

        if df_57.empty:
            st.markdown('<div class="ax warn">⚠️ No records in the selected time window. Please adjust the range.</div>', unsafe_allow_html=True)
            st.markdown('</div></div>', unsafe_allow_html=True)
            continue

        df_19 = convert_to_19_features(df_57)

        # ── Charts ────────────────────────────────────────────────
        st.markdown('<div class="row-lbl">Feature Visualization</div>', unsafe_allow_html=True)
        vc1, vc2, vc3 = st.columns(3)
        with vc1:
            st.pyplot(make_chart(df_57, ["Parameter-1_X","Parameter-1_Y","Parameter-1_Z"],
                                 "Parameter-1 · RMS", "blue"), use_container_width=True)
        with vc2:
            st.pyplot(make_chart(df_57, ["Parameter-2_X","Parameter-2_Y","Parameter-2_Z"],
                                 "Parameter-2 · Peak-to-Peak", "teal"), use_container_width=True)
        with vc3:
            st.pyplot(make_chart(df_57, ["Parameter-3_X","Parameter-3_Y","Parameter-3_Z"],
                                 "Parameter-3 · Kurtosis", "amber"), use_container_width=True)

        # ── Data tables ───────────────────────────────────────────
        st.markdown('<div class="row-lbl">57-Feature Table</div>', unsafe_allow_html=True)
        st.dataframe(df_57, height=270, use_container_width=True)

        st.markdown('<div class="row-lbl">19-Feature Table</div>', unsafe_allow_html=True)
        st.markdown('<div class="ax info">ℹ️ Each record expands to 3 rows — one per axis (X, Y, Z). Same timestamp, axis-specific parameter values.</div>', unsafe_allow_html=True)
        st.dataframe(df_19, height=270, use_container_width=True)

        # ── Download ──────────────────────────────────────────────
        st.markdown('<div class="row-lbl">Download</div>', unsafe_allow_html=True)
        pfx   = file_prefix.strip() if file_prefix.strip() else re.sub(r'[^\w\-.]','_',fname.replace(".txt",""))[:35]
        clean = re.sub(r'[^\w\-.]','_', fname)[:22]
        f57   = f"{pfx}_{clean}_57feat.csv" if file_prefix.strip() else f"{clean}_57feat.csv"
        f19   = f"{pfx}_{clean}_19feat.csv" if file_prefix.strip() else f"{clean}_19feat.csv"

        st.markdown(f'<div class="ax ok">✅ Ready — <strong>{len(df_57):,} records</strong> · {len(df_57.columns)} cols (57-feat) · {len(df_19):,} rows (19-feat)</div>', unsafe_allow_html=True)

        dc1, dc2 = st.columns(2)
        with dc1:
            st.download_button("📥  Download 57-Feature CSV",
                               df_57.to_csv(index=False), f57, "text/csv",
                               key=f"dl57_{fname}", use_container_width=True)
            st.caption(f"{f57}  ·  {len(df_57):,} rows  ·  {len(df_57.columns)} cols")
        with dc2:
            st.markdown('<div class="dl-teal">', unsafe_allow_html=True)
            st.download_button("📥  Download 19-Feature CSV",
                               df_19.to_csv(index=False), f19, "text/csv",
                               key=f"dl19_{fname}", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            st.caption(f"{f19}  ·  {len(df_19):,} rows  ·  20 cols")

        st.markdown('</div></div>', unsafe_allow_html=True)   # close panel-body + panel

        # Collect for merge
        all_dfs_57.append(df_57)
        all_dfs_19.append(df_19)
        lbl_str = next((k for k,v in LABEL_MAP.items() if v==label_value), "None") if use_label else "None"
        merge_rows.append({"name": fname, "src": "API" if is_api else "File",
                           "records": len(df_57), "label": lbl_str})

    # ══════════════════════════════════════════════════════════════
    # STEP 3 — MERGED DOWNLOAD
    # ══════════════════════════════════════════════════════════════
    if all_dfs_57:
        merged_57 = pd.concat(all_dfs_57, ignore_index=True)
        merged_19 = pd.concat(all_dfs_19, ignore_index=True)
        pfx_m     = (file_prefix.strip() + "_") if file_prefix.strip() else ""
        mf57      = f"{pfx_m}Merged_Data_57feat.csv"
        mf19      = f"{pfx_m}Merged_Data_19feat.csv"

        st.markdown("""
        <div class="step-h">
          <div class="step-num" style="background:#047857;">3</div>
          <div class="step-label">Merged Dataset</div>
          <div class="step-line"></div>
        </div>
        """, unsafe_allow_html=True)

        # Build summary table HTML
        rows_html = ""
        for m in merge_rows:
            icon_m = "📡" if m["src"]=="API" else "📄"
            rows_html += f'<tr><td>{icon_m} {m["name"][:46]}</td><td>{m["records"]:,}</td><td>{m["label"]}</td></tr>'

        st.markdown(f"""
        <div class="merge-section">
          <div class="merge-title">🗂 Merged Dataset Download</div>
          <div class="merge-sub">
            All sessions merged into one CSV — only the filtered records (per your time window settings) are included.
          </div>
          <table class="merge-table">
            <thead><tr><th>Session</th><th>Records (filtered)</th><th>Label</th></tr></thead>
            <tbody>{rows_html}</tbody>
          </table>
        </div>
        """, unsafe_allow_html=True)

        mc1, mc2, mc3, mc4 = st.columns(4)
        with mc1: st.metric("Sessions Merged", len(all_dfs_57))
        with mc2: st.metric("57-feat Total Rows", f"{len(merged_57):,}")
        with mc3: st.metric("19-feat Total Rows", f"{len(merged_19):,}")
        with mc4: st.metric("Columns (57-feat)", len(merged_57.columns))

        st.markdown(f'<div class="ax info" style="margin:.9rem 0;">📋 Output files: <strong>{mf57}</strong> and <strong>{mf19}</strong></div>', unsafe_allow_html=True)

        dl1, dl2 = st.columns(2)
        with dl1:
            st.markdown('<div class="merge-dl-banner b"><div class="merge-dl-title">57-Feature Merged CSV</div><div class="merge-dl-sub">Time + Parameter-1..19 × X, Y, Z</div></div>', unsafe_allow_html=True)
            st.markdown('<div class="dl-merge-b">', unsafe_allow_html=True)
            st.download_button(f"📥  Download {mf57}",
                               merged_57.to_csv(index=False), mf57, "text/csv",
                               key="dl_m57", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with dl2:
            st.markdown('<div class="merge-dl-banner t"><div class="merge-dl-title">19-Feature Merged CSV</div><div class="merge-dl-sub">Time + Parameter-1..19, axes stacked</div></div>', unsafe_allow_html=True)
            st.markdown('<div class="dl-merge-t">', unsafe_allow_html=True)
            st.download_button(f"📥  Download {mf19}",
                               merged_19.to_csv(index=False), mf19, "text/csv",
                               key="dl_m19", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════════════
st.markdown('<div class="pg-footer">Vibration Data Converter · pump_project · Professional Edition v4.0</div>', unsafe_allow_html=True)