"""
Vibration Data Converter  ·  pump_project  ·  v8.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Theme  : Neutral gray + blue  (Azure / Figma register)
         Palette = #F7F8FA page · #FFFFFF row fills · #0F62FE blue
         Font   = Sora (headings) + Plus Jakarta Sans (body) + JetBrains Mono (data)
Layout : Horizontal rule–separated full-width bands
         Absolutely NO cards / boxes / shadows around content
"""

import gc, re, requests
from datetime import datetime

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Vibration Data Converter",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ═══════════════════════════════════════════════════════════════════════
#  GLOBAL CSS
#  Philosophy:
#   • Page = cool gray  #F7F8FA
#   • Content sits on white strips separated by 1 px #E5E8ED rules
#   • Blue (#0F62FE) only on interactive / CTAs / step numbers
#   • Teal (#008080) for secondary download actions
#   • Typography hierarchy via weight + size, NOT color
#   • Zero decorative containers — content IS the layout
# ═══════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* ─── Tokens ──────────────────────────────────────────────────────── */
:root {
  --page-bg   : #F7F8FA;
  --row-bg    : #FFFFFF;
  --alt-bg    : #F2F4F7;
  --rule      : #E5E8ED;
  --rule-dark : #CDD2DC;

  --ink-1     : #0C0E12;
  --ink-2     : #2E3440;
  --ink-3     : #5A6478;
  --ink-4     : #8D96A6;
  --ink-5     : #B8BEC9;

  --blue      : #0F62FE;
  --blue-dim  : #EBF1FF;
  --blue-mid  : #C5D6FF;
  --blue-dk   : #0043CE;
  --blue-text : #0043CE;

  --teal      : #007B7B;
  --teal-dim  : #E6F4F4;
  --teal-mid  : #9DD5D5;

  --green     : #0D7240;
  --green-dim : #EAFAF0;
  --green-mid : #A4DFBE;

  --amber     : #8A4E00;
  --amber-dim : #FFF8EE;
  --amber-mid : #FDDCAA;

  --red       : #A1000F;
  --red-dim   : #FFF2F3;
  --red-mid   : #F9AAAD;

  --f-head  : 'Sora', sans-serif;
  --f-body  : 'Plus Jakarta Sans', system-ui, sans-serif;
  --f-mono  : 'JetBrains Mono', 'Fira Code', monospace;
}

/* ─── Reset ───────────────────────────────────────────────────────── */
html, body, [class*="css"] { font-family: var(--f-body); }
.stApp            { background: var(--page-bg); }
.block-container  { padding: 0 0 6rem !important; max-width: 100% !important; }
#MainMenu, footer, header { visibility: hidden; }
* { box-sizing: border-box; }

::-webkit-scrollbar        { width: 5px; height: 5px; }
::-webkit-scrollbar-track  { background: var(--page-bg); }
::-webkit-scrollbar-thumb  { background: var(--rule-dark); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--blue); }

/* ─── Sidebar ─────────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
  background: var(--row-bg) !important;
  border-right: 1px solid var(--rule) !important;
}
[data-testid="stSidebar"] .block-container { padding: 2rem 1.5rem !important; }
[data-testid="stSidebar"] * { color: var(--ink-3); }
[data-testid="stSidebar"] strong { color: var(--ink-2) !important; }
[data-testid="stSidebar"] label {
  font-size: .73rem !important; font-weight: 600 !important;
  letter-spacing: .07em !important; text-transform: uppercase !important;
  color: var(--ink-4) !important;
}

/* sidebar text input */
[data-testid="stSidebar"] .stTextInput > div > div > input {
  background: var(--alt-bg) !important;
  border: 1px solid var(--rule-dark) !important;
  border-radius: 6px !important;
  color: var(--ink-1) !important;
  font-family: var(--f-mono) !important;
  font-size: .84rem !important;
  padding: .46rem .75rem !important;
}
[data-testid="stSidebar"] .stTextInput > div > div > input:focus {
  border-color: var(--blue) !important;
  box-shadow: 0 0 0 3px rgba(15,98,254,.1) !important;
}
[data-testid="stSidebar"] .stTextInput > div > div > input::placeholder {
  color: var(--ink-5) !important;
}

/* ─── Top navigation ──────────────────────────────────────────────── */
.topnav {
  position: sticky; top: 0; z-index: 1000;
  background: var(--row-bg);
  border-bottom: 1px solid var(--rule);
  height: 52px;
  padding: 0 2.5rem;
  display: flex; align-items: center; justify-content: space-between;
}
.topnav-brand { display: flex; align-items: center; gap: .65rem; }
.topnav-mark {
  width: 28px; height: 28px;
  background: var(--blue);
  border-radius: 6px;
  display: flex; align-items: center; justify-content: center;
  font-size: .88rem;
}
.topnav-name {
  font-family: var(--f-head);
  font-size: .95rem; font-weight: 700;
  color: var(--ink-1); letter-spacing: -.015em;
}
.topnav-slash { color: var(--ink-5); margin: 0 .1rem; font-size: 1.1rem; }
.topnav-sub   { font-size: .82rem; color: var(--ink-4); font-weight: 400; }
.topnav-tag {
  font-size: .67rem; font-weight: 700; letter-spacing: .07em; text-transform: uppercase;
  padding: .22rem .65rem; border-radius: 4px;
  background: var(--blue-dim); color: var(--blue-text); border: 1px solid var(--blue-mid);
}

/* ─── Section band ────────────────────────────────────────────────── */
.band {
  background: var(--row-bg);
  border-bottom: 1px solid var(--rule);
  padding: 1.75rem 2.5rem;
}
.band-alt { background: var(--alt-bg); }

.band-title-row {
  display: flex; align-items: center; gap: .75rem;
  margin-bottom: 1.5rem;
}
.band-step {
  font-size: .62rem; font-weight: 700; letter-spacing: .11em; text-transform: uppercase;
  padding: .18rem .58rem; border-radius: 4px;
  background: var(--blue); color: #fff;
  flex-shrink: 0;
}
.band-step.done { background: var(--green); }
.band-title {
  font-family: var(--f-head);
  font-size: .97rem; font-weight: 600;
  color: var(--ink-1); letter-spacing: -.01em;
}
.band-hint { font-size: .8rem; color: var(--ink-4); margin-left: auto; }

/* ─── Sub-label (field divider) ───────────────────────────────────── */
.sub-label {
  font-size: .64rem; font-weight: 700; letter-spacing: .1em; text-transform: uppercase;
  color: var(--ink-4); margin: 1.5rem 0 .65rem;
  display: flex; align-items: center; gap: .55rem;
}
.sub-label::after { content: ''; flex: 1; height: 1px; background: var(--rule); }
.sub-label:first-child { margin-top: 0; }

/* ─── Load-step source columns ────────────────────────────────────── */
.src-name {
  font-size: .64rem; font-weight: 700; letter-spacing: .1em; text-transform: uppercase;
  color: var(--ink-4); margin: 0 0 .7rem;
  display: flex; align-items: center; gap: .4rem;
}
.src-pip  { width: 6px; height: 6px; border-radius: 50%; flex-shrink: 0; }
.code-tag {
  display: inline-block; margin-bottom: .75rem;
  font-family: var(--f-mono); font-size: .72rem;
  color: var(--teal); background: var(--teal-dim); border: 1px solid var(--teal-mid);
  border-radius: 4px; padding: .22rem .65rem;
}

/* ─── Session row ─────────────────────────────────────────────────── */
/* A thick blue top-border marks the start of each session */
.session-start {
  height: 3px; background: var(--blue);
  margin: 0;
}
.session-title-band {
  background: var(--alt-bg);
  border-bottom: 1px solid var(--rule);
  padding: .8rem 2.5rem;
  display: flex; align-items: center; gap: .7rem;
}
.session-icon { font-size: .95rem; }
.session-name {
  font-family: var(--f-head);
  font-size: .92rem; font-weight: 600;
  color: var(--ink-1); flex: 1;
  overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
}
.session-body { background: var(--row-bg); padding: 1.5rem 2.5rem; border-bottom: 1px solid var(--rule); }

/* ─── Chip ────────────────────────────────────────────────────────── */
.chip {
  font-size: .6rem; font-weight: 700; letter-spacing: .07em; text-transform: uppercase;
  padding: .17rem .52rem; border-radius: 4px; flex-shrink: 0;
}
.chip-blue  { background: var(--blue-dim);  color: var(--blue-text);  border: 1px solid var(--blue-mid);  }
.chip-teal  { background: var(--teal-dim);  color: var(--teal);       border: 1px solid var(--teal-mid);  }
.chip-green { background: var(--green-dim); color: var(--green);      border: 1px solid var(--green-mid); }

/* ─── KV table grid ───────────────────────────────────────────────── */
.kv-table {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(148px, 1fr));
  border-top: 1px solid var(--rule);
  border-left: 1px solid var(--rule);
  margin-bottom: 1.1rem;
}
.kv-cell {
  padding: .7rem .95rem;
  border-right: 1px solid var(--rule);
  border-bottom: 1px solid var(--rule);
}
.kv-k {
  font-size: .56rem; font-weight: 700; letter-spacing: .09em; text-transform: uppercase;
  color: var(--ink-5); margin-bottom: .18rem;
}
.kv-v {
  font-family: var(--f-mono); font-size: .82rem; font-weight: 500;
  color: var(--ink-2); line-height: 1.3;
}
.kv-v.accent { color: var(--blue); font-weight: 600; }
.kv-v.small  { font-size: .72rem; }
.kv-v.empty  {
  font-family: var(--f-body); font-style: italic;
  font-size: .79rem; color: var(--ink-5);
}

/* ─── Code preview ────────────────────────────────────────────────── */
.code-preview {
  background: #10151E;
  border: 1px solid #1E2740;
  border-radius: 6px;
  padding: .9rem 1.15rem;
  font-family: var(--f-mono); font-size: .69rem;
  max-height: 165px; overflow-y: auto;
  line-height: 1.8; white-space: pre;
  margin-bottom: .5rem;
}
.code-preview::-webkit-scrollbar       { width: 3px; }
.code-preview::-webkit-scrollbar-thumb { background: #2E3F5C; border-radius: 2px; }

/* ─── Inline alert ────────────────────────────────────────────────── */
.ia {
  display: flex; align-items: flex-start; gap: .55rem;
  border-radius: 5px; padding: .7rem .95rem;
  font-size: .84rem; line-height: 1.5; margin: .55rem 0;
}
.ia.info  { background: var(--blue-dim);  border: 1px solid var(--blue-mid);  color: var(--blue-text); }
.ia.ok    { background: var(--green-dim); border: 1px solid var(--green-mid); color: var(--green); }
.ia.warn  { background: var(--amber-dim); border: 1px solid var(--amber-mid); color: var(--amber); }
.ia.err   { background: var(--red-dim);   border: 1px solid var(--red-mid);   color: var(--red); }

/* ─── Download meta caption ───────────────────────────────────────── */
.dl-meta {
  font-family: var(--f-mono); font-size: .62rem; color: var(--ink-5);
  margin-top: .28rem; letter-spacing: .02em;
}

/* ─── Merge section ───────────────────────────────────────────────── */
.merge-band {
  background: var(--ink-1);
  padding: 2rem 2.5rem 2.5rem;
}
.merge-band-title-row {
  display: flex; align-items: center; gap: .75rem;
  margin-bottom: 1.3rem;
}
.merge-band-title {
  font-family: var(--f-head);
  font-size: .97rem; font-weight: 600;
  color: #F0F4FF; letter-spacing: -.01em;
}
.merge-band-hint { font-size: .8rem; color: var(--ink-3); margin-left: auto; }
.mtbl { width: 100%; border-collapse: collapse; margin: .4rem 0 1.2rem; }
.mtbl th {
  font-size: .58rem; font-weight: 700; letter-spacing: .1em; text-transform: uppercase;
  color: var(--ink-3); padding: .45rem .75rem; border-bottom: 1px solid #2A3347;
  text-align: left;
}
.mtbl td {
  font-size: .82rem; color: var(--ink-3); padding: .45rem .75rem;
  border-bottom: 1px solid #1A2130; font-family: var(--f-mono);
}
.mtbl td:first-child { color: #B0BCCC; font-family: var(--f-body); font-weight: 500; }
.mtbl tr:last-child td { border-bottom: none; }
.merge-dl-sub {
  font-size: .63rem; font-weight: 700; letter-spacing: .09em; text-transform: uppercase;
  color: var(--ink-3); margin-bottom: .4rem;
}

/* ═══ STREAMLIT WIDGET OVERRIDES ════════════════════════════════════ */

/* ── Buttons ── */
.stButton > button {
  font-family: var(--f-body) !important;
  font-weight: 600 !important; font-size: .87rem !important;
  border-radius: 6px !important; padding: .56rem 1.4rem !important;
  border: none !important; transition: all .15s !important;
  letter-spacing: .01em !important;
  background: var(--blue) !important; color: #fff !important;
  box-shadow: 0 1px 4px rgba(15,98,254,.2) !important;
}
.stButton > button:hover  { background: var(--blue-dk) !important; transform: translateY(-1px) !important; box-shadow: 0 3px 12px rgba(15,98,254,.3) !important; }
.stButton > button:active { transform: translateY(0) !important; }

.btn-teal > button   { background: var(--teal) !important; box-shadow: 0 1px 4px rgba(0,123,123,.2) !important; }
.btn-teal > button:hover { background: #006666 !important; box-shadow: 0 3px 12px rgba(0,123,123,.3) !important; }

.btn-ghost > button  {
  background: var(--row-bg) !important; color: var(--ink-2) !important;
  border: 1px solid var(--rule-dark) !important; box-shadow: none !important;
}
.btn-ghost > button:hover { border-color: var(--blue) !important; color: var(--blue) !important; box-shadow: none !important; }

.btn-red > button {
  background: var(--row-bg) !important; color: var(--red) !important;
  border: 1px solid var(--red-mid) !important;
  box-shadow: none !important; font-size: .77rem !important; padding: .36rem .75rem !important;
}
.btn-red > button:hover { background: var(--red-dim) !important; transform: none !important; box-shadow: none !important; }

/* ── Download buttons ── */
.stDownloadButton > button {
  font-family: var(--f-body) !important;
  font-weight: 600 !important; font-size: .87rem !important;
  border-radius: 6px !important; padding: .6rem 1.2rem !important;
  border: none !important; width: 100% !important; transition: all .15s !important;
  background: var(--blue) !important; color: #fff !important;
  box-shadow: 0 1px 4px rgba(15,98,254,.2) !important;
}
.stDownloadButton > button:hover { background: var(--blue-dk) !important; transform: translateY(-1px) !important; }

.dl-teal  .stDownloadButton > button { background: var(--teal) !important; }
.dl-teal  .stDownloadButton > button:hover { background: #006666 !important; }
.dl-mrg-b .stDownloadButton > button { background: var(--blue) !important; font-size: .9rem !important; padding: .65rem 1.2rem !important; }
.dl-mrg-t .stDownloadButton > button { background: var(--teal) !important; font-size: .9rem !important; padding: .65rem 1.2rem !important; }

/* ── Slider ── */
.stSlider > div > div > div > div { background: var(--blue) !important; }
.stSlider > div > div > div       { background: var(--rule-dark) !important; height: 3px !important; }

/* ── Metrics ── */
[data-testid="metric-container"] {
  background: var(--alt-bg) !important;
  border: 1px solid var(--rule) !important; border-radius: 5px !important;
  padding: .65rem .9rem !important;
}
[data-testid="metric-container"] label {
  color: var(--ink-4) !important; font-size: .58rem !important;
  font-weight: 700 !important; letter-spacing: .1em !important; text-transform: uppercase !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
  color: var(--ink-1) !important; font-size: 1.15rem !important; font-weight: 700 !important;
}

/* ── Selectbox ── */
.stSelectbox > div > div {
  background: var(--row-bg) !important; border: 1px solid var(--rule-dark) !important;
  border-radius: 6px !important; color: var(--ink-1) !important; font-size: .86rem !important;
}
.stSelectbox > div > div:focus-within {
  border-color: var(--blue) !important; box-shadow: 0 0 0 3px rgba(15,98,254,.09) !important;
}
.stSelectbox label {
  color: var(--ink-4) !important; font-size: .64rem !important;
  font-weight: 700 !important; letter-spacing: .09em !important; text-transform: uppercase !important;
}

/* ── Radio ── */
.stRadio > div { flex-direction: row !important; gap: .35rem !important; flex-wrap: wrap; }
.stRadio > div > label {
  background: var(--row-bg) !important; border: 1px solid var(--rule-dark) !important;
  border-radius: 6px !important; padding: .4rem .95rem !important;
  color: var(--ink-2) !important; font-size: .84rem !important; font-weight: 500 !important;
  cursor: pointer !important; transition: all .13s !important;
}
.stRadio > div > label:hover { border-color: var(--blue) !important; color: var(--blue) !important; }
.stRadio label { color: var(--ink-2) !important; }

/* ── Checkbox ── */
.stCheckbox label { color: var(--ink-2) !important; font-size: .87rem !important; }
.stCheckbox span  { color: var(--ink-2) !important; }

/* ── Text inputs (main area) ── */
.stTextInput > div > div > input {
  background: var(--row-bg) !important; border: 1px solid var(--rule-dark) !important;
  border-radius: 6px !important; color: var(--ink-1) !important; font-size: .86rem !important;
  padding: .46rem .75rem !important;
}
.stTextInput > div > div > input:focus {
  border-color: var(--blue) !important; box-shadow: 0 0 0 3px rgba(15,98,254,.09) !important;
}
.stTextInput > div > div > input::placeholder { color: var(--ink-5) !important; }
.stTextInput label {
  color: var(--ink-4) !important; font-size: .64rem !important;
  font-weight: 700 !important; letter-spacing: .09em !important; text-transform: uppercase !important;
}

/* ── Dataframe ── */
.stDataFrame { border-radius: 5px !important; overflow: hidden; border: 1px solid var(--rule) !important; }

/* ── File uploader ── */
[data-testid="stFileUploader"] {
  background: var(--row-bg) !important;
  border: 1.5px dashed var(--rule-dark) !important;
  border-radius: 8px !important;
}
[data-testid="stFileUploader"]:hover { border-color: var(--blue) !important; }
[data-testid="stFileUploader"] *     { color: var(--ink-3) !important; }

/* ── Misc ── */
.stCaption  { color: var(--ink-4) !important; font-size: .71rem !important; }
.stSpinner > div { border-top-color: var(--blue) !important; }
p     { color: var(--ink-2) !important; }
label { color: var(--ink-3) !important; }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════
#  CONSTANTS
# ═══════════════════════════════════════════════════════════════════════
API_BASE  = "https://pumpdata.duckdns.org/api"
SR_LABEL  = {5: "5 sec", 10: "10 sec", 15: "15 sec", 30: "30 sec"}
LABEL_MAP = {
    "Normal_Mode (0)":        0,
    "Seal Failure (1)":       1,
    "Bearing (2)":            2,
    "Shaft Misalignment (3)": 3,
    "Unbalance_impeller (4)": 4,
    "Cavitation (5)":         5,
}

# ═══════════════════════════════════════════════════════════════════════
#  SESSION STATE
# ═══════════════════════════════════════════════════════════════════════
for _k, _v in {
    "api_sessions": [],
    "fetch_msg":    None,
    "fetch_type":   None,
}.items():
    if _k not in st.session_state:
        st.session_state[_k] = _v

# ═══════════════════════════════════════════════════════════════════════
#  CACHED PARSING  (prevents exit-132 memory crash)
# ═══════════════════════════════════════════════════════════════════════
@st.cache_data(max_entries=8, show_spinner=False)
def cached_parse_57(txt: str) -> pd.DataFrame:
    rows, i = [], 0
    lines   = [l.strip() for l in txt.splitlines() if l.strip()]
    tre     = re.compile(r"\d+/\d+/\d+\s+\d+:\d+:\d+\s+(AM|PM)")
    pnr     = re.compile(r"Peak\s+(\d+)\s+Parameter-\d+\s+([-\d.]+)\s+Parameter-\d+\s+([-\d.]+)")
    por     = re.compile(r"Peak\s+(\d+)\s+Freq\s+([-\d.]+)\s+Mag\s+([-\d.]+)")

    def _f(tok, j):
        try:    return float(tok[j])
        except: return None

    while i < len(lines):
        if tre.match(lines[i]):
            try:    row = {"Time": datetime.strptime(lines[i].strip(), "%m/%d/%Y %I:%M:%S %p").strftime("%d/%m/%Y %H:%M:%S")}
            except: row = {"Time": lines[i].strip()}
            i += 1
            for axis in ["X", "Y", "Z"]:
                while i < len(lines) and f"{axis} Axis" not in lines[i]: i += 1
                i += 1
                peaks = {}
                while i < len(lines) and not lines[i].endswith("Axis:") and not tre.match(lines[i]):
                    line, tok = lines[i], lines[i].split()
                    if tok and re.match(r"^Parameter-(\d+)$", tok[0]):
                        pn = int(tok[0].split("-")[1])
                        if   pn == 1: row[f"Parameter-1_{axis}"] = _f(tok, 1)
                        elif pn == 2: row[f"Parameter-2_{axis}"] = _f(tok, 1)
                        elif pn == 3: row[f"Parameter-3_{axis}"] = _f(tok, 1)
                        i += 1; continue
                    if   line.startswith("RMS"):     row[f"Parameter-1_{axis}"] = _f(tok, 1)
                    elif line.startswith("PP"):       row[f"Parameter-2_{axis}"] = _f(tok, 1)
                    elif line.startswith("Kurtosis"): row[f"Parameter-3_{axis}"] = _f(tok, 1)
                    else:
                        m = pnr.match(line) or por.match(line)
                        if m: peaks[int(m.group(1))] = (float(m.group(2)), float(m.group(3)))
                    i += 1
                for p in range(1, 9):
                    fp, mp = 2 + p*2, 2 + p*2 + 1
                    row[f"Parameter-{fp}_{axis}"] = peaks.get(p, (None,None))[0]
                    row[f"Parameter-{mp}_{axis}"] = peaks.get(p, (None,None))[1]
            rows.append(row)
        else:
            i += 1

    cols = ["Time"]
    for n in range(1, 4):
        for ax in ["X","Y","Z"]: cols.append(f"Parameter-{n}_{ax}")
    for p in range(1, 9):
        fp, mp = 2+p*2, 2+p*2+1
        for ax in ["X","Y","Z"]: cols.append(f"Parameter-{fp}_{ax}")
        for ax in ["X","Y","Z"]: cols.append(f"Parameter-{mp}_{ax}")
    df = pd.DataFrame(rows)
    for c in cols:
        if c not in df.columns: df[c] = pd.NA
    return df[cols]


@st.cache_data(max_entries=16, show_spinner=False)
def cached_to19(key: str, df57: pd.DataFrame) -> pd.DataFrame:
    rows, hl = [], "Label" in df57.columns
    for _, row in df57.iterrows():
        for axis in ["X","Y","Z"]:
            nr = {"Time": row.get("Time", pd.NA)}
            for n in range(1, 4): nr[f"Parameter-{n}"] = row.get(f"Parameter-{n}_{axis}", pd.NA)
            for p in range(1, 9):
                fp, mp = 2+p*2, 2+p*2+1
                nr[f"Parameter-{fp}"] = row.get(f"Parameter-{fp}_{axis}", pd.NA)
                nr[f"Parameter-{mp}"] = row.get(f"Parameter-{mp}_{axis}", pd.NA)
            if hl: nr["Label"] = row["Label"]
            rows.append(nr)
    c19 = ["Time"] + [f"Parameter-{n}" for n in range(1, 20)]
    d = pd.DataFrame(rows)
    if hl: c19.append("Label")
    return d[c19]

# ═══════════════════════════════════════════════════════════════════════
#  EXTRACT META FROM TXT CONTENT
#  API only sends {"content": "..."} — no device fields in payload.
#  Device name: supplied via manual input before fetch.
#  Sampling rate, duration, all stats derived from TXT timestamps.
# ═══════════════════════════════════════════════════════════════════════
def extract_meta(content: str, device_name_override: str = "",
                 payload: dict = None) -> dict:
    """
    Extract session metadata.
    Priority for each field:
      1. API payload keys  (device_name, sampling_rate, duration_val)  ← from api_server.py
      2. Manual text input (device_name_override)
      3. Auto-detect from TXT timestamps
    """
    payload = payload or {}
    tre  = re.compile(r"(\d+/\d+/\d+)\s+(\d+:\d+:\d+)\s+(AM|PM)")
    ts   = tre.findall(content)
    t_s  = f"{ts[0][0]} {ts[0][1]} {ts[0][2]}"    if ts else "—"
    t_e  = f"{ts[-1][0]} {ts[-1][1]} {ts[-1][2]}" if ts else "—"
    rec  = content.count("#Vibration Value")
    sz   = round(len(content) / 1024, 1)

    # ── Device name ───────────────────────────────────────────
    # payload["device_name"] comes from device.py via api_server.py
    dn = "—"
    raw_dn = payload.get("device_name") or device_name_override
    if raw_dn and str(raw_dn).strip().lower() not in ("", "none", "null", "-"):
        dn = str(raw_dn).strip()

    # ── Sampling rate ─────────────────────────────────────────
    # payload["sampling_rate"] is the int seconds value from device.py
    sr, sr_secs = "—", None
    raw_sr = payload.get("sampling_rate")
    if raw_sr is not None:
        try:
            sr_secs = int(raw_sr)
            sr = SR_LABEL.get(sr_secs, f"{sr_secs} sec")
        except: pass
    # Fallback: auto-detect from consecutive timestamps
    if sr_secs is None and len(ts) >= 2:
        try:
            fmt = "%m/%d/%Y %I:%M:%S %p"
            d   = int(abs((
                datetime.strptime(f"{ts[1][0]} {ts[1][1]} {ts[1][2]}", fmt) -
                datetime.strptime(f"{ts[0][0]} {ts[0][1]} {ts[0][2]}", fmt)
            ).total_seconds()))
            if 1 <= d <= 300:
                sr_secs = d
                sr = SR_LABEL.get(d, f"{d} sec")
        except: pass

    # ── Duration ──────────────────────────────────────────────
    # payload["duration_val"] is int hours from device.py
    dur, dur_hours = "—", None
    raw_dur = payload.get("duration_val")
    if raw_dur is not None:
        try:
            dur_hours = int(raw_dur)
            dur = f"{dur_hours} hour{'s' if dur_hours != 1 else ''}"
        except: pass
    # Fallback: compute from timestamp span
    if dur_hours is None and len(ts) >= 2:
        try:
            fmt  = "%m/%d/%Y %I:%M:%S %p"
            secs = int((
                datetime.strptime(f"{ts[-1][0]} {ts[-1][1]} {ts[-1][2]}", fmt) -
                datetime.strptime(f"{ts[0][0]} {ts[0][1]} {ts[0][2]}",   fmt)
            ).total_seconds())
            if secs > 0:
                h, m = secs // 3600, (secs % 3600) // 60
                dur = f"{h}h {m:02d}m" if h else f"{m}m {secs%60:02d}s"
                dur_hours = max(1, h)
        except: pass

    # ── Derived stats ─────────────────────────────────────────
    rph = exp_rec = completeness = "—"
    if sr_secs:
        rph = f"{3600 // sr_secs:,}"
        if dur_hours:
            exp = (dur_hours * 3600) // sr_secs
            exp_rec = f"{exp:,}"
            if rec > 0 and exp > 0:
                completeness = f"{min(100.0, round(rec / exp * 100, 1))}%"

    return dict(
        device_name=dn,   sampling_rate=sr,  duration=dur,
        records=rec,      expected_rec=exp_rec, rec_per_hour=rph,
        completeness=completeness,
        t_start=t_s,      t_end=t_e,
        size_kb=sz,
        fetched_at=datetime.now().strftime("%H:%M:%S"),
        fetched_date=datetime.now().strftime("%d %b %Y"),
    )


def hl_txt(raw: str) -> str:
    """Syntax-highlight a TXT raw preview for the dark code block."""
    out = []
    for line in raw.splitlines():
        ls = line.strip()
        if re.match(r"\d+/\d+/\d+", ls):
            out.append(f'<span style="color:#7DB8F7;font-weight:500;">{line}</span>')
        elif "Axis:" in ls:
            out.append(f'<span style="color:#5DDCB0;">{line}</span>')
        elif ls.startswith("Peak"):
            out.append(f'<span style="color:#C8A9FA;">{line}</span>')
        elif ls.startswith("#"):
            out.append(f'<span style="color:#2E3F5C;">{line}</span>')
        else:
            out.append(f'<span style="color:#3D5070;">{line}</span>')
    return "<br>".join(out)


def make_chart(df: pd.DataFrame, cols: list, title: str, pal: str) -> plt.Figure:
    pals = {
        "blue" : ["#0F62FE", "#5B8DEF", "#A8C2FD"],
        "teal" : ["#007B7B", "#18A8A8", "#6DD5D5"],
        "amber": ["#A85B00", "#D97706", "#F9BA5D"],
    }
    cl = pals.get(pal, pals["blue"])
    fig, ax = plt.subplots(figsize=(5, 3.1), facecolor="#FFFFFF")
    ax.set_facecolor("#F7F8FA")
    for i, c in enumerate(cols):
        if c in df.columns:
            ax.plot(df[c].values,
                    label=c.split("_")[-1] if "_" in c else c,
                    linewidth=1.9, alpha=0.87, color=cl[i % len(cl)])
    ax.set_title(title, fontsize=9, fontweight="600", color="#2E3440", pad=7)
    ax.set_xlabel("Sample", fontsize=7.5, color="#8D96A6")
    ax.legend(fontsize=7.5, framealpha=0.95, loc="best",
              facecolor="white", edgecolor="#E5E8ED")
    ax.grid(True, alpha=0.28, linestyle="--", linewidth=0.5, color="#E5E8ED")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    for sp in ["left", "bottom"]: ax.spines[sp].set_color("#E5E8ED")
    ax.tick_params(labelsize=7.5, colors="#8D96A6")
    fig.tight_layout(pad=0.9)
    return fig

# ═══════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ═══════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style="padding:.1rem 0 1.4rem; border-bottom:1px solid #E5E8ED; margin-bottom:1.4rem;">
      <div style="font-family:'Sora',sans-serif; font-size:.95rem; font-weight:700;
                  color:#0C0E12; letter-spacing:-.015em; line-height:1.3;">
        Vibration Data<br>Converter
      </div>
      <div style="font-size:.6rem; color:#B8BEC9; margin-top:.35rem;
                  letter-spacing:.1em; text-transform:uppercase;">
        pump_project · v8.0
      </div>
    </div>
    """, unsafe_allow_html=True)

    file_prefix = st.text_input(
        "Output file prefix",
        placeholder="e.g. pump_bearing_01",
        key="fp",
        help="Prefix prepended to all downloaded CSV filenames",
    )

    st.markdown("""
    <div style="margin:1.2rem 0; padding:.9rem 1rem;
                background:#F7F8FA; border-top:1px solid #E5E8ED; border-bottom:1px solid #E5E8ED;">
      <div style="font-size:.6rem; font-weight:700; letter-spacing:.1em; text-transform:uppercase;
                  color:#B8BEC9; margin-bottom:.55rem;">Output formats</div>
      <div style="font-size:.82rem; color:#5A6478; line-height:1.8;">
        <strong style="color:#2E3440;">57-Feature CSV</strong><br>
        Time + Param-1..19 × X, Y, Z<br><br>
        <strong style="color:#2E3440;">19-Feature CSV</strong><br>
        Axes stacked as rows  (×3 per record)
      </div>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.api_sessions:
        st.markdown("""
        <div style="font-size:.6rem; font-weight:700; letter-spacing:.1em; text-transform:uppercase;
                    color:#B8BEC9; margin:1.3rem 0 .5rem;">Loaded API sessions</div>
        """, unsafe_allow_html=True)
        for s in st.session_state.api_sessions:
            nm = (s.get("meta") or {}).get("device_name", "")
            lbl = nm if nm and nm != "—" else s["name"]
            st.markdown(
                f'<div style="font-size:.75rem; color:#8D96A6; padding:.3rem 0;'
                f'border-bottom:1px solid #F2F4F7; white-space:nowrap;'
                f'overflow:hidden; text-overflow:ellipsis;">📡 {lbl[:28]}</div>',
                unsafe_allow_html=True,
            )
        st.markdown('<div style="margin-top:.9rem;"></div>', unsafe_allow_html=True)
        st.markdown('<div class="btn-red">', unsafe_allow_html=True)
        if st.button("Clear all API sessions", use_container_width=True, key="clr"):
            st.session_state.api_sessions = []
            st.session_state.fetch_msg    = None
            cached_parse_57.clear(); cached_to19.clear(); gc.collect()
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════
#  TOP NAV
# ═══════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="topnav">
  <div class="topnav-brand">
    <div class="topnav-mark">⚡</div>
    <span class="topnav-name">VDC</span>
    <span class="topnav-slash">/</span>
    <span class="topnav-sub">Vibration Data Converter</span>
  </div>
  <span class="topnav-tag">pump_project</span>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════
#  STEP 1  ─  LOAD DATA
# ═══════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="band">
  <div class="band-title-row">
    <span class="band-step">Step 1</span>
    <span class="band-title">Load Data</span>
    <span class="band-hint">Upload TXT files  ·  or fetch from device API</span>
  </div>
""", unsafe_allow_html=True)

col_up, col_mid, col_api = st.columns([10, 1, 10])

# ── Upload side ────────────────────────────────────────────────────────
with col_up:
    st.markdown("""
    <div class="src-name">
      <span class="src-pip" style="background:#0F62FE;"></span>Upload TXT files
    </div>
    """, unsafe_allow_html=True)
    uploaded_files = st.file_uploader(
        "Drop files here",
        type=["txt"], accept_multiple_files=True,
        key="fu", label_visibility="collapsed",
    )
    st.caption("Multiple files supported · each becomes a separate section below")

# ── Vertical divider ───────────────────────────────────────────────────
with col_mid:
    st.markdown(
        '<div style="width:1px; min-height:220px; background:#E5E8ED; margin:0 auto;"></div>',
        unsafe_allow_html=True,
    )

# ── API side ───────────────────────────────────────────────────────────
with col_api:
    st.markdown(f"""
    <div class="src-name">
      <span class="src-pip" style="background:#007B7B;"></span>Fetch from device API
    </div>
    <span class="code-tag">GET {API_BASE}/latest</span>
    """, unsafe_allow_html=True)

    device_name_input = st.text_input(
        "Device name  (saved with this session)",
        placeholder="e.g.  PUMP-01  ·  Bearing_Motor_A",
        key="dname",
    )

    st.markdown('<div class="btn-teal">', unsafe_allow_html=True)
    fetch_clicked = st.button("📡  Fetch latest session", use_container_width=True, key="fetch_btn")
    st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.fetch_msg:
        css  = {"success": "ok", "error": "err", "warning": "warn"}.get(
                st.session_state.fetch_type, "info")
        icon = {"ok": "✅", "err": "❌", "warn": "⚠️"}.get(css, "ℹ️")
        st.markdown(
            f'<div class="ia {css}" style="margin-top:.55rem;">'
            f'<span>{icon}</span><span>{st.session_state.fetch_msg}</span></div>',
            unsafe_allow_html=True,
        )

    if fetch_clicked:
        with st.spinner("Connecting to device API…"):
            try:
                resp = requests.get(f"{API_BASE}/latest", timeout=15)
                if resp.status_code == 200:
                    payload = resp.json()
                    content = resp.json().get("content", "").strip()
                    if content:
                        meta  = extract_meta(content, device_name_input, payload)
                        dn    = meta["device_name"] if meta["device_name"] != "—" else "Device"
                        sname = f"{dn} · {meta['fetched_date']} {meta['fetched_at']}"
                        if sname not in [s["name"] for s in st.session_state.api_sessions]:
                            st.session_state.api_sessions.insert(
                                0, {"name": sname, "txt": content, "meta": meta}
                            )
                            gc.collect()
                            st.session_state.fetch_msg  = (
                                f"Loaded <strong>{sname}</strong> — "
                                f"{meta['records']:,} records · {meta['size_kb']} KB"
                            )
                            st.session_state.fetch_type = "success"
                        else:
                            st.session_state.fetch_msg  = f"Already loaded: {sname}"
                            st.session_state.fetch_type = "warning"
                    else:
                        st.session_state.fetch_msg  = "No data yet — run the Device Simulator first."
                        st.session_state.fetch_type = "warning"
                else:
                    st.session_state.fetch_msg  = f"Server returned HTTP {resp.status_code}."
                    st.session_state.fetch_type = "error"
            except requests.exceptions.ConnectionError:
                st.session_state.fetch_msg  = f"Cannot reach {API_BASE} — is api_server.py running?"
                st.session_state.fetch_type = "error"
            except requests.exceptions.Timeout:
                st.session_state.fetch_msg  = "Request timed out — please try again."
                st.session_state.fetch_type = "error"
            except Exception as e:
                st.session_state.fetch_msg  = f"Error: {e}"
                st.session_state.fetch_type = "error"
        st.rerun()

st.markdown("</div>", unsafe_allow_html=True)   # close .band

# ═══════════════════════════════════════════════════════════════════════
#  BUILD UNIFIED FILE LIST
#  Order: API sessions (newest first) then uploaded files
# ═══════════════════════════════════════════════════════════════════════
file_list = []
for s in st.session_state.api_sessions:
    file_list.append({"name": s["name"], "txt": s["txt"],
                      "source": "api",    "meta": s.get("meta")})
if uploaded_files:
    for f in uploaded_files:
        file_list.append({"name": f.name,
                          "txt":  f.read().decode("utf-8", errors="replace"),
                          "source": "upload", "meta": None})

# ═══════════════════════════════════════════════════════════════════════
#  EMPTY STATE
# ═══════════════════════════════════════════════════════════════════════
if not file_list:
    st.markdown("""
    <div style="padding:5rem 2.5rem; text-align:center; border-top:1px solid #E5E8ED; background:#FFFFFF;">
      <div style="font-size:2rem; margin-bottom:.7rem; opacity:.15;">⚡</div>
      <div style="font-family:'Sora',sans-serif; font-size:.95rem; font-weight:600;
                  color:#2E3440; margin-bottom:.4rem;">No sessions loaded</div>
      <div style="font-size:.84rem; color:#8D96A6; max-width:460px;
                  margin:0 auto; line-height:1.75;">
        Upload TXT files or fetch from the device API.
        Each session appears as a full-width section below — configure its time window,
        inspect charts and tables, then download 57-feature and 19-feature CSVs
        individually or as a merged dataset.
      </div>
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════
#  STEP 2  ─  CONFIGURE & EXPORT  (one section per session)
# ═══════════════════════════════════════════════════════════════════════
else:
    n = len(file_list)
    st.markdown(f"""
    <div class="band" style="padding-bottom:.5rem; background:#F7F8FA;">
      <div class="band-title-row" style="margin-bottom:0;">
        <span class="band-step">Step 2</span>
        <span class="band-title">Configure &amp; Export</span>
        <span class="band-hint">{n} session{"s" if n != 1 else ""} loaded</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    all_57, all_19, merge_rows = [], [], []

    for file in file_list:
        fname  = file["name"]
        is_api = file["source"] == "api"
        meta   = file.get("meta")

        # ── Session header ────────────────────────────────────────
        st.markdown(f"""
        <div class="session-start"></div>
        <div class="session-title-band">
          <span class="session-icon">{"📡" if is_api else "📄"}</span>
          <span class="session-name">{fname}</span>
          <span class="chip {"chip-teal" if is_api else "chip-blue"}">
            {"API" if is_api else "File"}
          </span>
        </div>
        <div class="session-body">
        """, unsafe_allow_html=True)

        # ── Remove button (API only) ──────────────────────────────
        if is_api:
            _, rb = st.columns([8, 1])
            with rb:
                st.markdown('<div class="btn-red">', unsafe_allow_html=True)
                if st.button("Remove", key=f"rm_{fname}"):
                    st.session_state.api_sessions = [
                        s for s in st.session_state.api_sessions if s["name"] != fname
                    ]
                    gc.collect(); st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)

        # ── Session information KV table ──────────────────────────
        if meta:
            st.markdown('<div class="sub-label">Session information</div>', unsafe_allow_html=True)

            def _kv(k, v, cls="kv-v"):
                if v in ("—", "", None):
                    return (f'<div class="kv-cell">'
                            f'<div class="kv-k">{k}</div>'
                            f'<div class="kv-v empty">not available</div></div>')
                return (f'<div class="kv-cell">'
                        f'<div class="kv-k">{k}</div>'
                        f'<div class="{cls}">{v}</div></div>')

            st.markdown(f"""
            <div class="kv-table">
              {_kv("Device name",   meta["device_name"],   "kv-v accent")}
              {_kv("Sampling rate", meta["sampling_rate"])}
              {_kv("Duration",      meta["duration"])}
              {_kv("Records",       f"{meta['records']:,}",  "kv-v accent")}
              {_kv("Expected",      meta["expected_rec"])}
              {_kv("Rec / hour",    meta["rec_per_hour"])}
              {_kv("Completeness",  meta["completeness"])}
              {_kv("Start",         meta["t_start"],        "kv-v small")}
              {_kv("End",           meta["t_end"],          "kv-v small")}
              {_kv("File size",     f"{meta['size_kb']} KB")}
              {_kv("Fetched",       f"{meta['fetched_date']} {meta['fetched_at']}", "kv-v small")}
            </div>
            """, unsafe_allow_html=True)

        # ── Raw TXT preview ───────────────────────────────────────
        st.markdown('<div class="sub-label">Raw data preview</div>', unsafe_allow_html=True)
        prev = file["txt"][:900] + ("\n… [truncated]" if len(file["txt"]) > 900 else "")
        st.markdown(f'<div class="code-preview">{hl_txt(prev)}</div>', unsafe_allow_html=True)

        # ── Fault label ───────────────────────────────────────────
        st.markdown('<div class="sub-label">Fault label</div>', unsafe_allow_html=True)
        la, lb = st.columns([1, 2])
        with la:
            use_label = st.checkbox("Attach label column", key=f"chk_{fname}")
        with lb:
            label_value = None
            if use_label:
                label_value = LABEL_MAP[st.selectbox(
                    "Fault type", list(LABEL_MAP.keys()),
                    key=f"lbl_{fname}", label_visibility="collapsed",
                )]

        # ── Parse (cached) ────────────────────────────────────────
        with st.spinner("Parsing records…"):
            df_base = cached_parse_57(file["txt"])

        if df_base.empty:
            st.markdown(
                '<div class="ia err"><span>❌</span><span>No vibration records found. Check the file format.</span></div>',
                unsafe_allow_html=True,
            )
            st.markdown("</div>", unsafe_allow_html=True)
            continue

        # ── Time window ───────────────────────────────────────────
        st.markdown('<div class="sub-label">Time window selection</div>', unsafe_allow_html=True)

        # Copy before adding derived column — fixes SettingWithCopyWarning / pandas crash
        df_57 = df_base.copy()
        df_57["Time_dt"] = pd.to_datetime(df_57["Time"], format="%d/%m/%Y %H:%M:%S")

        time_list = df_57["Time_dt"].tolist()
        tmin, tmax = df_57["Time_dt"].min().to_pydatetime(), df_57["Time_dt"].max().to_pydatetime()
        N = len(time_list)

        method = st.radio(
            "Method", ["⚡  Quick slider", "🎯  Precise input"],
            horizontal=True, key=f"tw_{fname}", label_visibility="collapsed",
        )

        if method == "⚡  Quick slider":
            cs, cm = st.columns([5, 1])
            with cs:
                si, ei = st.slider("Range", 0, N-1, (0, N-1),
                                   key=f"sl_{fname}", label_visibility="collapsed")
                start, end = time_list[si], time_list[ei]
                st.caption(
                    f"From  {start.strftime('%d/%m/%Y %H:%M:%S')}   →   {end.strftime('%d/%m/%Y %H:%M:%S')}"
                )
            with cm:
                st.metric("Total", N)
                st.metric("Selected", ei - si + 1)
        else:
            c1, c2, c3 = st.columns([2, 2, 1])
            with c1:
                sd = st.date_input("Start date", tmin.date(), tmin.date(), tmax.date(), key=f"sd_{fname}")
                sv = st.time_input("Start time", tmin.time(), key=f"sv_{fname}")
                start = datetime.combine(sd, sv)
            with c2:
                ed = st.date_input("End date",   tmax.date(), tmin.date(), tmax.date(), key=f"ed_{fname}")
                ev = st.time_input("End time",   tmax.time(), key=f"ev_{fname}")
                end = datetime.combine(ed, ev)
            with c3:
                sn = len(df_57[(df_57["Time_dt"] >= start) & (df_57["Time_dt"] <= end)])
                st.metric("Total", N); st.metric("Selected", sn)
            if start > end:
                st.markdown(
                    '<div class="ia err"><span>⚠️</span><span>Start must be before End.</span></div>',
                    unsafe_allow_html=True,
                )
                start, end = tmin, tmax

        df_57 = df_57[(df_57["Time_dt"] >= start) & (df_57["Time_dt"] <= end)].copy()
        df_57 = df_57.drop(columns="Time_dt").reset_index(drop=True)

        if use_label:
            df_57 = df_57.copy()
            df_57["Label"] = label_value

        if df_57.empty:
            st.markdown(
                '<div class="ia warn"><span>⚠️</span><span>No records in selected window — adjust the range.</span></div>',
                unsafe_allow_html=True,
            )
            st.markdown("</div>", unsafe_allow_html=True)
            continue

        ck    = f"{fname}|{len(df_57)}|{use_label}|{label_value}"
        df_19 = cached_to19(ck, df_57)

        # ── Feature charts ────────────────────────────────────────
        st.markdown('<div class="sub-label">Feature visualization</div>', unsafe_allow_html=True)
        ch1, ch2, ch3 = st.columns(3)
        with ch1:
            st.pyplot(make_chart(df_57, ["Parameter-1_X","Parameter-1_Y","Parameter-1_Z"],
                                 "Parameter-1 · RMS", "blue"), use_container_width=True)
        with ch2:
            st.pyplot(make_chart(df_57, ["Parameter-2_X","Parameter-2_Y","Parameter-2_Z"],
                                 "Parameter-2 · Peak-to-Peak", "teal"), use_container_width=True)
        with ch3:
            st.pyplot(make_chart(df_57, ["Parameter-3_X","Parameter-3_Y","Parameter-3_Z"],
                                 "Parameter-3 · Kurtosis", "amber"), use_container_width=True)
        plt.close("all")

        # ── Data tables ───────────────────────────────────────────
        st.markdown('<div class="sub-label">57-feature table</div>', unsafe_allow_html=True)
        st.dataframe(df_57, height=240, use_container_width=True)

        st.markdown('<div class="sub-label">19-feature table</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="ia info"><span>ℹ️</span>'
            '<span>Each record expands to 3 rows — one per axis (X, Y, Z). '
            'Axes share the same timestamp.</span></div>',
            unsafe_allow_html=True,
        )
        st.dataframe(df_19, height=240, use_container_width=True)

        # ── Downloads ─────────────────────────────────────────────
        st.markdown('<div class="sub-label">Download this session</div>', unsafe_allow_html=True)

        pfx   = file_prefix.strip() if file_prefix.strip() else re.sub(r'[^\w\-.]','_', fname.replace(".txt",""))[:35]
        clean = re.sub(r'[^\w\-.]', '_', fname)[:22]
        f57n  = f"{pfx}_{clean}_57feat.csv" if file_prefix.strip() else f"{clean}_57feat.csv"
        f19n  = f"{pfx}_{clean}_19feat.csv" if file_prefix.strip() else f"{clean}_19feat.csv"

        st.markdown(
            f'<div class="ia ok"><span>✅</span>'
            f'<span>Ready — <strong>{len(df_57):,} records</strong> selected · '
            f'{len(df_57.columns)} cols (57-feat) · {len(df_19):,} rows (19-feat)</span></div>',
            unsafe_allow_html=True,
        )

        d1, d2 = st.columns(2)
        with d1:
            st.download_button(
                "📥  Download 57-feature CSV",
                df_57.to_csv(index=False), f57n, "text/csv",
                key=f"dl57_{fname}", use_container_width=True,
            )
            st.markdown(
                f'<div class="dl-meta">{f57n}  ·  {len(df_57):,} rows  ·  {len(df_57.columns)} cols</div>',
                unsafe_allow_html=True,
            )
        with d2:
            st.markdown('<div class="dl-teal">', unsafe_allow_html=True)
            st.download_button(
                "📥  Download 19-feature CSV",
                df_19.to_csv(index=False), f19n, "text/csv",
                key=f"dl19_{fname}", use_container_width=True,
            )
            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown(
                f'<div class="dl-meta">{f19n}  ·  {len(df_19):,} rows  ·  20 cols</div>',
                unsafe_allow_html=True,
            )

        st.markdown("</div>", unsafe_allow_html=True)   # close .session-body

        all_57.append(df_57); all_19.append(df_19)
        lbl_str = (
            next((k for k, v in LABEL_MAP.items() if v == label_value), "—")
            if use_label else "None"
        )
        merge_rows.append({
            "name": fname,
            "src":  "API" if is_api else "File",
            "n":    len(df_57),
            "lbl":  lbl_str,
        })

    # ═══════════════════════════════════════════════════════════════
    #  STEP 3  ─  MERGED DOWNLOAD
    # ═══════════════════════════════════════════════════════════════
    if all_57:
        merged_57 = pd.concat(all_57, ignore_index=True)
        merged_19 = pd.concat(all_19, ignore_index=True)
        pfx_m = (file_prefix.strip() + "_") if file_prefix.strip() else ""
        mf57  = f"{pfx_m}Merged_57feat.csv"
        mf19  = f"{pfx_m}Merged_19feat.csv"

        rows_html = "".join(
            f'<tr>'
            f'<td>{"📡" if m["src"]=="API" else "📄"} {m["name"][:52]}</td>'
            f'<td>{m["n"]:,}</td>'
            f'<td>{m["lbl"]}</td>'
            f'</tr>'
            for m in merge_rows
        )

        st.markdown(f"""
        <div class="merge-band">
          <div class="merge-band-title-row">
            <span class="band-step done">Step 3</span>
            <span class="merge-band-title">Merged Dataset Download</span>
            <span class="merge-band-hint">all sessions combined · time-filtered records only</span>
          </div>
          <table class="mtbl">
            <thead>
              <tr><th>Session</th><th>Records (filtered)</th><th>Label</th></tr>
            </thead>
            <tbody>{rows_html}</tbody>
          </table>
        </div>
        """, unsafe_allow_html=True)

        mc1, mc2, mc3, mc4 = st.columns(4)
        with mc1: st.metric("Sessions merged", len(all_57))
        with mc2: st.metric("57-feat rows",    f"{len(merged_57):,}")
        with mc3: st.metric("19-feat rows",    f"{len(merged_19):,}")
        with mc4: st.metric("Columns (57)",    len(merged_57.columns))

        st.markdown(
            f'<div class="ia info" style="margin:1rem 2.5rem 1.5rem;">'
            f'<span>📋</span>'
            f'<span>Files: <strong>{mf57}</strong>  and  <strong>{mf19}</strong></span></div>',
            unsafe_allow_html=True,
        )

        d1, d2 = st.columns(2)
        with d1:
            st.markdown(
                '<div class="merge-dl-sub" style="padding:0 0 .4rem 2.5rem;">'
                '57-feature merged  ·  Time + Param-1..19 × X, Y, Z</div>',
                unsafe_allow_html=True,
            )
            _, bc, _ = st.columns([0.06, 10, 0.06])
            with bc:
                st.markdown('<div class="dl-mrg-b">', unsafe_allow_html=True)
                st.download_button(
                    f"📥  Download {mf57}",
                    merged_57.to_csv(index=False), mf57, "text/csv",
                    key="dl_m57", use_container_width=True,
                )
                st.markdown("</div>", unsafe_allow_html=True)

        with d2:
            st.markdown(
                '<div class="merge-dl-sub" style="padding:0 0 .4rem .1rem;">'
                '19-feature merged  ·  Time + Param-1..19, axes stacked</div>',
                unsafe_allow_html=True,
            )
            _, bc2, _ = st.columns([0.06, 10, 0.06])
            with bc2:
                st.markdown('<div class="dl-mrg-t">', unsafe_allow_html=True)
                st.download_button(
                    f"📥  Download {mf19}",
                    merged_19.to_csv(index=False), mf19, "text/csv",
                    key="dl_m19", use_container_width=True,
                )
                st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div style="height:2rem;"></div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════
#  FOOTER
# ═══════════════════════════════════════════════════════════════════════
st.markdown("""
<div style="padding:1.5rem 2.5rem; border-top:1px solid #E5E8ED; background:#FFFFFF;
            text-align:center; font-size:.72rem; color:#B8BEC9; letter-spacing:.04em;">
  Vibration Data Converter &nbsp;·&nbsp; pump_project &nbsp;·&nbsp; v8.0
</div>
""", unsafe_allow_html=True)
