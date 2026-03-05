import streamlit as st
import pandas as pd
import re
import requests
from datetime import datetime
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ─────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Vibration Data Converter",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────
# CSS — Clean Professional Dark-Sidebar / White-Main
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,300;0,14..32,400;0,14..32,500;0,14..32,600;0,14..32,700;1,14..32,400&family=Merriweather:wght@700&display=swap');

/* ── Tokens ───────────────────────────────────────────────── */
:root {
  --bg:        #f1f5f9;
  --white:     #ffffff;
  --surface:   #f8fafc;
  --bd:        #e2e8f0;
  --bd2:       #cbd5e1;
  --navy:      #0f2044;
  --navy2:     #1e3a5f;
  --blue:      #1d4ed8;
  --blue-h:    #1e40af;
  --blue-lt:   #eff6ff;
  --blue-md:   #dbeafe;
  --teal:      #0d9488;
  --teal-lt:   #f0fdfa;
  --green:     #15803d;
  --green-lt:  #f0fdf4;
  --green-md:  #bbf7d0;
  --amber:     #b45309;
  --amber-lt:  #fffbeb;
  --red:       #b91c1c;
  --red-lt:    #fef2f2;
  --t1:        #0f172a;
  --t2:        #334155;
  --t3:        #64748b;
  --t4:        #94a3b8;
  --t5:        #cbd5e1;
  --inter:     'Inter', system-ui, sans-serif;
  --serif:     'Merriweather', Georgia, serif;
  --r:         10px;
  --sh1: 0 1px 3px rgba(0,0,0,.08), 0 1px 2px rgba(0,0,0,.04);
  --sh2: 0 4px 12px rgba(0,0,0,.08), 0 2px 4px rgba(0,0,0,.04);
  --sh3: 0 8px 24px rgba(0,0,0,.10), 0 3px 8px rgba(0,0,0,.05);
}

/* ── Reset ────────────────────────────────────────────────── */
html, body, [class*="css"] { font-family: var(--inter); }
.stApp { background: var(--bg); }
.block-container { padding: 0 2.5rem 5rem; max-width: 1280px; }
#MainMenu, footer, header { visibility: hidden; }
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--bd2); border-radius: 3px; }

/* ── Sidebar ──────────────────────────────────────────────── */
[data-testid="stSidebar"] {
  background: var(--navy) !important;
  border-right: none !important;
}
[data-testid="stSidebar"] .block-container { padding: 1.8rem 1.3rem; }
[data-testid="stSidebar"] label {
  color: #94a3b8 !important;
  font-size: .78rem !important;
  font-weight: 500 !important;
}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] li { color: #94a3b8 !important; font-size: .82rem !important; }
[data-testid="stSidebar"] strong { color: #e2e8f0 !important; }
[data-testid="stSidebar"] .stTextInput > div > div > input {
  background: rgba(255,255,255,.07) !important;
  border: 1px solid rgba(255,255,255,.12) !important;
  color: #f1f5f9 !important;
  border-radius: 7px !important;
  font-size: .84rem !important;
}
[data-testid="stSidebar"] .stTextInput > div > div > input:focus {
  border-color: #60a5fa !important;
  box-shadow: 0 0 0 3px rgba(96,165,250,.15) !important;
}

/* ── Page Header ──────────────────────────────────────────── */
.pg-header {
  background: var(--white);
  border-bottom: 1px solid var(--bd);
  padding: 1.6rem 0 1.3rem;
  margin: 0 -2.5rem 2rem;
  padding-left: 2.5rem; padding-right: 2.5rem;
  box-shadow: var(--sh1);
}
.pg-title {
  font-family: var(--serif);
  font-size: 1.9rem;
  font-weight: 700;
  color: var(--navy);
  margin: 0;
  letter-spacing: -.02em;
  line-height: 1.1;
}
.pg-title em { font-style: normal; color: var(--blue); }
.pg-sub {
  margin: .35rem 0 0;
  font-size: .85rem;
  color: var(--t4);
  font-weight: 400;
}
.pg-header-row {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 1rem;
}

/* ── Section heading ──────────────────────────────────────── */
.sec-h {
  display: flex;
  align-items: center;
  gap: .75rem;
  margin: 2rem 0 .9rem;
}
.sec-h-dot {
  width: 8px; height: 8px;
  border-radius: 50%;
  background: var(--blue);
  flex-shrink: 0;
}
.sec-h-text {
  font-size: .7rem;
  font-weight: 700;
  letter-spacing: .1em;
  text-transform: uppercase;
  color: var(--t3);
}
.sec-h-line { flex: 1; height: 1px; background: var(--bd); }

/* ── Cards ────────────────────────────────────────────────── */
.card {
  background: var(--white);
  border: 1px solid var(--bd);
  border-radius: var(--r);
  box-shadow: var(--sh1);
}
.card-inner { padding: 1.4rem 1.5rem; }

/* File session card — left accent bar */
.file-card {
  background: var(--white);
  border: 1px solid var(--bd);
  border-left: 4px solid var(--blue);
  border-radius: var(--r);
  box-shadow: var(--sh1);
  margin-bottom: 1.5rem;
  overflow: hidden;
  transition: box-shadow .2s;
}
.file-card:hover { box-shadow: var(--sh2); }
.file-card-head {
  background: var(--surface);
  border-bottom: 1px solid var(--bd);
  padding: .9rem 1.4rem;
  display: flex;
  align-items: center;
  gap: .8rem;
}
.file-icon {
  width: 34px; height: 34px;
  background: var(--blue-lt);
  border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
  font-size: .95rem;
  flex-shrink: 0;
}
.file-icon.api { background: var(--teal-lt); }
.file-name {
  font-weight: 600;
  font-size: .95rem;
  color: var(--navy);
  flex: 1;
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.file-card-body { padding: 1.4rem 1.5rem; }

/* ── Badge ────────────────────────────────────────────────── */
.badge {
  display: inline-flex;
  align-items: center;
  font-size: .65rem;
  font-weight: 600;
  letter-spacing: .05em;
  text-transform: uppercase;
  padding: .18rem .6rem;
  border-radius: 100px;
  flex-shrink: 0;
}
.badge-blue  { background: var(--blue-md);   color: #1e40af;  border: 1px solid #bfdbfe; }
.badge-teal  { background: #ccfbf1;           color: #0f766e;  border: 1px solid #99f6e4; }
.badge-green { background: var(--green-md);   color: var(--green); border: 1px solid #86efac; }
.badge-gray  { background: var(--surface);    color: var(--t3);    border: 1px solid var(--bd2); }

/* ── Meta grid ────────────────────────────────────────────── */
.meta-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(145px, 1fr));
  gap: .55rem;
  margin: .8rem 0 1.1rem;
}
.meta-cell {
  background: var(--surface);
  border: 1px solid var(--bd);
  border-radius: 8px;
  padding: .6rem .85rem;
}
.meta-k {
  font-size: .6rem;
  font-weight: 600;
  letter-spacing: .08em;
  text-transform: uppercase;
  color: var(--t4);
  margin-bottom: .15rem;
}
.meta-v {
  font-size: .84rem;
  font-weight: 600;
  color: var(--t1);
}
.meta-v.hi { color: var(--blue); }

/* ── Inline heading inside card ───────────────────────────── */
.inh {
  font-size: .68rem;
  font-weight: 700;
  letter-spacing: .09em;
  text-transform: uppercase;
  color: var(--t3);
  margin: 1.3rem 0 .55rem;
  display: flex; align-items: center; gap: .5rem;
}
.inh::after { content: ''; flex: 1; height: 1px; background: var(--bd); }

/* ── TXT preview ──────────────────────────────────────────── */
.txt-pre {
  background: #0f172a;
  border-radius: 8px;
  padding: .9rem 1.1rem;
  font-family: 'Fira Code', 'Courier New', monospace;
  font-size: .7rem;
  max-height: 170px;
  overflow-y: auto;
  line-height: 1.7;
  white-space: pre;
  margin-bottom: .5rem;
}
.txt-pre::-webkit-scrollbar { width: 3px; }
.txt-pre::-webkit-scrollbar-thumb { background: #334155; }

/* ── Alert boxes ──────────────────────────────────────────── */
.ax {
  border-radius: 8px;
  padding: .8rem 1.1rem;
  font-size: .84rem;
  line-height: 1.5;
  margin: .6rem 0;
}
.ax.info  { background: var(--blue-lt);  border: 1px solid #bfdbfe; color: #1e40af; }
.ax.ok    { background: var(--green-lt); border: 1px solid var(--green-md); color: #14532d; }
.ax.warn  { background: var(--amber-lt); border: 1px solid #fde68a; color: #78350f; }
.ax.error { background: var(--red-lt);   border: 1px solid #fecaca; color: #7f1d1d; }

/* ── Stat row ─────────────────────────────────────────────── */
.stat-row {
  display: flex; gap: .6rem; flex-wrap: wrap; margin: .5rem 0;
}
.stat-block {
  flex: 1; min-width: 80px;
  background: var(--surface);
  border: 1px solid var(--bd);
  border-radius: 8px;
  padding: .6rem .9rem;
  text-align: center;
}
.stat-v { font-size: 1.25rem; font-weight: 700; color: var(--navy); line-height: 1; }
.stat-k { font-size: .6rem; font-weight: 600; letter-spacing: .07em; text-transform: uppercase; color: var(--t4); margin-top: .12rem; }

/* ── Merge section ────────────────────────────────────────── */
.merge-wrap {
  background: linear-gradient(135deg, #0f2044 0%, #1e3a6e 100%);
  border-radius: 14px;
  padding: 2rem 2.2rem;
  margin-top: 2.5rem;
}
.merge-title {
  font-family: var(--serif);
  font-size: 1.4rem;
  font-weight: 700;
  color: #f1f5f9;
  margin: 0 0 .25rem;
}
.merge-sub { font-size: .84rem; color: #64748b; margin: 0 0 1.4rem; }
.merge-stat {
  background: rgba(255,255,255,.07);
  border: 1px solid rgba(255,255,255,.1);
  border-radius: 8px;
  padding: .65rem 1rem;
  text-align: center;
}
.merge-stat-v { font-size: 1.35rem; font-weight: 700; color: #93c5fd; line-height: 1; }
.merge-stat-k { font-size: .6rem; font-weight: 600; letter-spacing: .07em; text-transform: uppercase; color: #475569; margin-top: .12rem; }
.merge-dl-banner {
  border-radius: 10px;
  padding: 1.1rem 1.3rem .75rem;
  text-align: center;
  margin-bottom: .5rem;
}
.merge-dl-banner.blue { background: linear-gradient(135deg, #1e3a8a, #2563eb); border: 1px solid rgba(147,197,253,.2); }
.merge-dl-banner.teal { background: linear-gradient(135deg, #134e4a, #0d9488); border: 1px solid rgba(153,246,228,.2); }
.merge-dl-title { color: #f1f5f9; font-weight: 600; font-size: .95rem; margin-bottom: .2rem; }
.merge-dl-sub   { color: rgba(255,255,255,.45); font-size: .75rem; }
.merge-table {
  width: 100%; border-collapse: collapse; margin: 1rem 0;
}
.merge-table th {
  font-size: .62rem; font-weight: 700; letter-spacing: .08em; text-transform: uppercase;
  color: #475569; padding: .45rem .7rem; border-bottom: 1px solid rgba(255,255,255,.08); text-align: left;
}
.merge-table td {
  font-size: .82rem; color: #94a3b8;
  padding: .45rem .7rem; border-bottom: 1px solid rgba(255,255,255,.05);
}
.merge-table td:first-child { color: #e2e8f0; font-weight: 500; }
.merge-table tr:last-child td { border-bottom: none; }

/* ── Streamlit widget overrides ───────────────────────────── */
.stButton > button {
  background: var(--blue) !important;
  color: white !important;
  font-family: var(--inter) !important;
  font-weight: 600 !important;
  font-size: .86rem !important;
  border: none !important;
  border-radius: 8px !important;
  padding: .6rem 1.5rem !important;
  transition: all .18s !important;
  box-shadow: 0 2px 8px rgba(29,78,216,.25) !important;
}
.stButton > button:hover {
  background: var(--blue-h) !important;
  box-shadow: 0 4px 16px rgba(29,78,216,.4) !important;
  transform: translateY(-1px) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

.btn-teal > button {
  background: var(--teal) !important;
  box-shadow: 0 2px 8px rgba(13,148,136,.25) !important;
}
.btn-teal > button:hover {
  background: #0f766e !important;
  box-shadow: 0 4px 16px rgba(13,148,136,.4) !important;
}

.btn-ghost > button {
  background: white !important;
  color: var(--t2) !important;
  border: 1px solid var(--bd2) !important;
  box-shadow: var(--sh1) !important;
}
.btn-ghost > button:hover {
  border-color: var(--blue) !important;
  color: var(--blue) !important;
  box-shadow: var(--sh1) !important;
}

.btn-sm > button {
  font-size: .78rem !important;
  padding: .4rem .85rem !important;
  background: white !important;
  color: var(--red) !important;
  border: 1px solid #fecaca !important;
  box-shadow: none !important;
}
.btn-sm > button:hover {
  background: var(--red-lt) !important;
  box-shadow: none !important;
  transform: none !important;
}

/* Download */
.stDownloadButton > button {
  background: var(--blue) !important;
  color: white !important;
  border: none !important;
  border-radius: 8px !important;
  font-weight: 600 !important;
  font-size: .86rem !important;
  padding: .65rem 1.2rem !important;
  width: 100% !important;
  transition: all .18s !important;
  box-shadow: 0 2px 8px rgba(29,78,216,.25) !important;
}
.stDownloadButton > button:hover {
  background: var(--blue-h) !important;
  box-shadow: 0 4px 16px rgba(29,78,216,.4) !important;
  transform: translateY(-1px) !important;
}

.dl-teal .stDownloadButton > button {
  background: var(--teal) !important;
  box-shadow: 0 2px 8px rgba(13,148,136,.25) !important;
}
.dl-teal .stDownloadButton > button:hover {
  background: #0f766e !important;
  box-shadow: 0 4px 16px rgba(13,148,136,.4) !important;
}
.dl-merge-blue .stDownloadButton > button {
  background: linear-gradient(135deg, #1e3a8a, #2563eb) !important;
  font-size: .9rem !important; padding: .7rem 1.2rem !important;
  box-shadow: 0 3px 12px rgba(29,78,216,.35) !important;
}
.dl-merge-teal .stDownloadButton > button {
  background: linear-gradient(135deg, #134e4a, #0d9488) !important;
  font-size: .9rem !important; padding: .7rem 1.2rem !important;
  box-shadow: 0 3px 12px rgba(13,148,136,.35) !important;
}

/* Slider */
.stSlider > div > div > div > div { background: var(--blue) !important; }
.stSlider > div > div > div { background: var(--bd2) !important; height: 4px !important; }

/* Metrics */
[data-testid="metric-container"] {
  background: var(--surface) !important;
  border: 1px solid var(--bd) !important;
  border-radius: 8px !important;
  padding: .7rem .9rem !important;
}
[data-testid="metric-container"] label {
  color: var(--t4) !important;
  font-size: .62rem !important;
  font-weight: 600 !important;
  letter-spacing: .07em !important;
  text-transform: uppercase !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
  color: var(--navy) !important;
  font-size: 1.2rem !important;
  font-weight: 700 !important;
}

/* Selectbox */
.stSelectbox > div > div {
  background: white !important;
  border: 1px solid var(--bd2) !important;
  border-radius: 7px !important;
  color: var(--t1) !important;
  font-size: .85rem !important;
}
.stSelectbox label {
  color: var(--t2) !important;
  font-size: .72rem !important;
  font-weight: 600 !important;
  text-transform: uppercase !important;
  letter-spacing: .05em !important;
}

/* Radio */
.stRadio > div { flex-direction: row !important; gap: .4rem !important; flex-wrap: wrap; }
.stRadio > div > label {
  background: white !important;
  border: 1px solid var(--bd2) !important;
  border-radius: 7px !important;
  padding: .45rem .95rem !important;
  color: var(--t2) !important;
  font-size: .83rem !important;
  font-weight: 500 !important;
  cursor: pointer !important;
  transition: all .15s !important;
  box-shadow: var(--sh1) !important;
}
.stRadio > div > label:hover {
  border-color: var(--blue) !important;
  color: var(--blue) !important;
}

/* Checkbox */
.stCheckbox label { color: var(--t2) !important; font-size: .86rem !important; }

/* Expander */
.streamlit-expanderHeader {
  background: white !important;
  border: 1px solid var(--bd) !important;
  border-radius: 8px !important;
  color: var(--t2) !important;
  font-size: .86rem !important;
  font-weight: 500 !important;
  box-shadow: var(--sh1) !important;
}
.streamlit-expanderContent {
  background: white !important;
  border: 1px solid var(--bd) !important;
  border-top: none !important;
  border-radius: 0 0 8px 8px !important;
}

/* Dataframe */
.stDataFrame { border-radius: 8px; overflow: hidden; box-shadow: var(--sh1); }

/* File uploader */
[data-testid="stFileUploader"] {
  background: var(--surface) !important;
  border: 1.5px dashed var(--bd2) !important;
  border-radius: 9px !important;
  padding: .4rem !important;
  transition: border-color .18s !important;
}
[data-testid="stFileUploader"]:hover { border-color: var(--blue) !important; }

/* Caption */
.stCaption { color: var(--t4) !important; font-size: .7rem !important; }

/* Spinner */
.stSpinner > div { border-top-color: var(--blue) !important; }

hr { border: none; height: 1px; background: var(--bd); margin: 2rem 0; }

.pg-footer {
  text-align: center;
  padding: 2rem 0 1rem;
  font-size: .76rem;
  color: var(--t4);
  letter-spacing: .04em;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────────────────────
API_BASE  = "https://pumpdata.duckdns.org/api"
LABEL_MAP = {
    "Normal_Mode (0)":        0,
    "Seal Failure (1)":       1,
    "Bearing (2)":            2,
    "Shaft Misalignment (3)": 3,
    "Unbalance_impeller (4)": 4,
    "Cavitation (5)":         5,
}

# ─────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────
for k, v in {
    "api_sessions":    [],   # [{name, txt, meta}]
    "fetch_msg":       None,
    "fetch_type":      None,
    "last_upload_sig": None,
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ─────────────────────────────────────────────────────────────
# CORE FUNCTIONS  (identical logic to reference)
# ─────────────────────────────────────────────────────────────
def normalize_time(t):
    return datetime.strptime(t.strip(), "%m/%d/%Y %I:%M:%S %p").strftime("%d/%m/%Y %H:%M:%S")

def parse_vibration(txt):
    rows=[]; lines=[l.strip() for l in txt.splitlines() if l.strip()]; i=0
    time_re = re.compile(r"\d+/\d+/\d+\s+\d+:\d+:\d+\s+(AM|PM)")
    pnr = re.compile(r"Peak\s+(\d+)\s+Parameter-\d+\s+([-\d.]+)\s+Parameter-\d+\s+([-\d.]+)")
    por = re.compile(r"Peak\s+(\d+)\s+Freq\s+([-\d.]+)\s+Mag\s+([-\d.]+)")
    def tf(tok, j):
        try: return float(tok[j])
        except: return None
    while i < len(lines):
        if time_re.match(lines[i]):
            row = {"Time": normalize_time(lines[i])}; i += 1
            for axis in ["X","Y","Z"]:
                while i < len(lines) and f"{axis} Axis" not in lines[i]: i += 1
                i += 1; peaks = {}
                while i < len(lines) and not lines[i].endswith("Axis:") and not time_re.match(lines[i]):
                    line = lines[i]; tok = line.split()
                    if tok and re.match(r"^Parameter-(\d+)$", tok[0]):
                        pn = int(tok[0].split("-")[1]); val = tf(tok, 1)
                        if   pn == 1: row[f"Parameter-1_{axis}"] = val
                        elif pn == 2: row[f"Parameter-2_{axis}"] = val
                        elif pn == 3: row[f"Parameter-3_{axis}"] = val
                        i += 1; continue
                    if   line.startswith("RMS"):     row[f"Parameter-1_{axis}"] = tf(tok, 1)
                    elif line.startswith("PP"):       row[f"Parameter-2_{axis}"] = tf(tok, 1)
                    elif line.startswith("Kurtosis"): row[f"Parameter-3_{axis}"] = tf(tok, 1)
                    else:
                        m = pnr.match(line) or por.match(line)
                        if m: peaks[int(m.group(1))] = (float(m.group(2)), float(m.group(3)))
                    i += 1
                for p in range(1, 9):
                    fp = 2+p*2; mp = 2+p*2+1
                    row[f"Parameter-{fp}_{axis}"] = peaks.get(p, (None,None))[0]
                    row[f"Parameter-{mp}_{axis}"] = peaks.get(p, (None,None))[1]
            rows.append(row)
        else: i += 1
    return pd.DataFrame(rows)

def reorder_columns_57(df):
    cols = ["Time"]
    for n in range(1, 4):
        for ax in ["X","Y","Z"]: cols.append(f"Parameter-{n}_{ax}")
    for p in range(1, 9):
        fp = 2+p*2; mp = 2+p*2+1
        for ax in ["X","Y","Z"]: cols.append(f"Parameter-{fp}_{ax}")
        for ax in ["X","Y","Z"]: cols.append(f"Parameter-{mp}_{ax}")
    for c in cols:
        if c not in df.columns: df[c] = pd.NA
    return df[cols]

def convert_to_19_features(df):
    rows_19 = []; has_label = "Label" in df.columns
    for _, row in df.iterrows():
        for axis in ["X","Y","Z"]:
            nr = {"Time": row.get("Time", pd.NA)}
            for n in range(1, 4): nr[f"Parameter-{n}"] = row.get(f"Parameter-{n}_{axis}", pd.NA)
            for p in range(1, 9):
                fp = 2+p*2; mp = 2+p*2+1
                nr[f"Parameter-{fp}"] = row.get(f"Parameter-{fp}_{axis}", pd.NA)
                nr[f"Parameter-{mp}"] = row.get(f"Parameter-{mp}_{axis}", pd.NA)
            if has_label: nr["Label"] = row["Label"]
            rows_19.append(nr)
    c19 = ["Time"] + [f"Parameter-{n}" for n in range(1, 20)]
    d = pd.DataFrame(rows_19)
    if has_label: c19.append("Label")
    return d[c19]

def extract_meta(content, payload=None):
    tre = re.compile(r"(\d+/\d+/\d+)\s+(\d+:\d+:\d+)\s+(AM|PM)")
    ts  = tre.findall(content)
    t_s = f"{ts[0][0]} {ts[0][1]} {ts[0][2]}"    if ts else "—"
    t_e = f"{ts[-1][0]} {ts[-1][1]} {ts[-1][2]}" if ts else "—"
    rec = content.count("#Vibration Value")
    sz  = round(len(content)/1024, 1)
    sr  = "—"
    if payload:
        sr = payload.get("sampling_rate") or payload.get("sample_rate") or payload.get("interval") or "—"
    if sr == "—" and len(ts) >= 2:
        try:
            fmt = "%m/%d/%Y %I:%M:%S %p"
            t1 = datetime.strptime(f"{ts[0][0]} {ts[0][1]} {ts[0][2]}", fmt)
            t2 = datetime.strptime(f"{ts[1][0]} {ts[1][1]} {ts[1][2]}", fmt)
            d  = int((t2-t1).total_seconds())
            if d > 0: sr = f"{d}s"
        except: pass
    dur = "—"
    if payload:
        raw = payload.get("duration") or payload.get("duration_hours") or payload.get("hours") or "—"
        if raw != "—":
            try:
                dv = float(str(raw)); dur = f"{dv:.0f}h" if dv==int(dv) else f"{dv}h"
            except: dur = str(raw)
    if dur == "—" and len(ts) >= 2:
        try:
            fmt = "%m/%d/%Y %I:%M:%S %p"
            t1 = datetime.strptime(f"{ts[0][0]} {ts[0][1]} {ts[0][2]}", fmt)
            te = datetime.strptime(f"{ts[-1][0]} {ts[-1][1]} {ts[-1][2]}", fmt)
            secs = int((te-t1).total_seconds())
            if secs > 0:
                h = secs//3600; m = (secs%3600)//60
                dur = f"{h}h {m}m" if h else f"{m}m"
        except: pass
    dn = "—"
    if payload:
        for k in ["device_name","deviceName","device_id","deviceId","name",
                  "sensor_name","sensorName","id","device","unit"]:
            val = payload.get(k)
            if val and str(val).strip().lower() not in ("","none","null","unknown","-"):
                dn = str(val).strip(); break
    return {"device_name": dn, "sampling_rate": sr, "duration": dur,
            "records": rec, "t_start": t_s, "t_end": t_e,
            "size_kb": sz, "fetched_at": datetime.now().strftime("%H:%M:%S")}

def hl_txt(raw):
    out = []
    for line in raw.splitlines():
        ls = line.strip()
        if re.match(r"\d+/\d+/\d+\s+\d+:\d+:\d+", ls):
            out.append(f'<span style="color:#60a5fa;font-weight:600;">{line}</span>')
        elif "Axis:" in ls:
            out.append(f'<span style="color:#34d399;">{line}</span>')
        elif ls.startswith("Peak"):
            out.append(f'<span style="color:#a78bfa;">{line}</span>')
        elif ls.startswith("#"):
            out.append(f'<span style="color:#334155;">{line}</span>')
        else:
            out.append(f'<span style="color:#475569;">{line}</span>')
    return "<br>".join(out)

def make_chart(df, cols, title, palette):
    p = {
        "blue":  ["#1d4ed8","#3b82f6","#93c5fd"],
        "teal":  ["#0d9488","#14b8a6","#5eead4"],
        "amber": ["#b45309","#d97706","#fcd34d"],
    }
    cl = p.get(palette, p["blue"])
    fig, ax = plt.subplots(figsize=(5, 3.2), facecolor="white")
    ax.set_facecolor("#f8fafc")
    for i, c in enumerate(cols):
        if c in df.columns:
            ax.plot(df[c].values, label=c.split("_")[-1] if "_" in c else c,
                    linewidth=2, alpha=0.85, color=cl[i % len(cl)])
    ax.set_title(title, fontsize=10, fontweight="bold", color="#0f172a", pad=10)
    ax.set_xlabel("Sample", fontsize=8, color="#94a3b8")
    ax.legend(fontsize=7.5, framealpha=0.95, loc="best",
              frameon=True, facecolor="white", edgecolor="#e2e8f0")
    ax.grid(True, alpha=0.25, linestyle="--", linewidth=0.5, color="#e2e8f0")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#e2e8f0")
    ax.spines["bottom"].set_color("#e2e8f0")
    ax.tick_params(labelsize=7.5, colors="#94a3b8")
    fig.tight_layout(pad=0.9)
    return fig

# ─────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:.2rem 0 1.4rem; border-bottom:1px solid rgba(255,255,255,.1); margin-bottom:1.3rem;">
        <div style="font-size:1rem; font-weight:700; color:#f1f5f9; letter-spacing:-.01em;">Vibration Converter</div>
        <div style="font-size:.65rem; color:#475569; margin-top:.2rem; letter-spacing:.08em; text-transform:uppercase;">Configuration Panel</div>
    </div>
    """, unsafe_allow_html=True)

    file_prefix = st.text_input("Output file prefix", placeholder="e.g. pump_run_01",
                                 key="fp", help="Prefix added to all downloaded CSV filenames")
    st.markdown("---")
    st.markdown("""
    <div style="background:rgba(255,255,255,.05); border:1px solid rgba(255,255,255,.09);
         border-radius:8px; padding:.9rem 1rem;">
        <div style="font-size:.65rem; font-weight:700; letter-spacing:.08em; text-transform:uppercase;
             color:#475569; margin-bottom:.5rem;">Output Formats</div>
        <p style="color:#64748b; font-size:.8rem; margin:.25rem 0;">
            <strong style="color:#94a3b8;">57-feature CSV</strong><br>
            Time + Parameter-1..19 × X, Y, Z
        </p>
        <p style="color:#64748b; font-size:.8rem; margin:.25rem 0 0;">
            <strong style="color:#94a3b8;">19-feature CSV</strong><br>
            Axes stacked as rows (×3 row count)
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown('<div class="btn-sm">', unsafe_allow_html=True)
    if st.button("✕  Clear API Sessions", use_container_width=True, key="clr_api"):
        st.session_state.api_sessions = []
        st.session_state.fetch_msg    = None
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# PAGE HEADER
# ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="pg-header">
  <div class="pg-header-row">
    <div>
      <h1 class="pg-title">Vibration Data <em>Converter</em></h1>
      <p class="pg-sub">Upload TXT files or fetch from device API · Configure time window per session · Download 57-feature and 19-feature CSVs individually or merged</p>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# SECTION 1 — DATA SOURCES
# ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="sec-h">
  <div class="sec-h-dot"></div>
  <div class="sec-h-text">Step 1 — Load Data</div>
  <div class="sec-h-line"></div>
</div>
""", unsafe_allow_html=True)

col_up, col_api = st.columns(2, gap="large")

with col_up:
    st.markdown('<p style="font-size:.75rem;font-weight:600;letter-spacing:.07em;text-transform:uppercase;color:#64748b;margin:0 0 .5rem;">📁 Upload TXT Files</p>', unsafe_allow_html=True)
    uploaded_files = st.file_uploader(
        "Upload",
        type=["txt"],
        accept_multiple_files=True,
        key="fu",
        label_visibility="collapsed",
        help="Upload one or more vibration log TXT files",
    )

with col_api:
    st.markdown(f'<p style="font-size:.75rem;font-weight:600;letter-spacing:.07em;text-transform:uppercase;color:#64748b;margin:0 0 .5rem;">📡 Fetch from Device API</p>', unsafe_allow_html=True)
    st.markdown(f'<code style="font-size:.72rem;color:#0d9488;background:#f0fdfa;border:1px solid #99f6e4;border-radius:5px;padding:.25rem .6rem;">GET {API_BASE}/latest</code>', unsafe_allow_html=True)
    st.markdown('<div style="margin-top:.5rem;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="btn-teal">', unsafe_allow_html=True)
    fetch_clicked = st.button("📡  Fetch Latest Device Session", use_container_width=True, key="fetch_btn")
    st.markdown('</div>', unsafe_allow_html=True)
    if st.session_state.fetch_msg:
        css  = {"success":"ok","error":"error","warning":"warn"}.get(st.session_state.fetch_type, "info")
        icon = {"ok":"✅","error":"❌","warn":"⚠️","info":"ℹ️"}.get(css,"ℹ️")
        st.markdown(f'<div class="ax {css}" style="margin-top:.5rem;">{icon} {st.session_state.fetch_msg}</div>', unsafe_allow_html=True)
    if fetch_clicked:
        with st.spinner("Connecting to device API…"):
            try:
                resp = requests.get(f"{API_BASE}/latest", timeout=15)
                if resp.status_code == 200:
                    payload = resp.json(); content = payload.get("content","").strip()
                    if content:
                        meta  = extract_meta(content, payload)
                        dn    = meta["device_name"]
                        sname = f"{dn} @ {meta['fetched_at']}" if dn != "—" else f"API Session @ {meta['fetched_at']}"
                        if sname not in [s["name"] for s in st.session_state.api_sessions]:
                            st.session_state.api_sessions.append({"name": sname, "txt": content, "meta": meta})
                            st.session_state.fetch_msg  = f"Added <strong>{sname}</strong> — {meta['records']:,} records"
                            st.session_state.fetch_type = "success"
                        else:
                            st.session_state.fetch_msg  = f"Session already loaded: {sname}"
                            st.session_state.fetch_type = "warning"
                    else:
                        st.session_state.fetch_msg  = "No data yet. Please run the Device Simulator first."
                        st.session_state.fetch_type = "warning"
                else:
                    st.session_state.fetch_msg  = f"Server returned HTTP {resp.status_code}."
                    st.session_state.fetch_type = "error"
            except requests.exceptions.ConnectionError:
                st.session_state.fetch_msg  = f"Cannot connect to {API_BASE}. Ensure the ingestion server is running."
                st.session_state.fetch_type = "error"
            except requests.exceptions.Timeout:
                st.session_state.fetch_msg  = "Request timed out. Please retry."
                st.session_state.fetch_type = "error"
            except Exception as e:
                st.session_state.fetch_msg  = f"Unexpected error: {e}"
                st.session_state.fetch_type = "error"
        st.rerun()

# ─────────────────────────────────────────────────────────────
# BUILD UNIFIED FILE LIST: uploaded + API sessions
# ─────────────────────────────────────────────────────────────
file_list = []  # each: {"name", "txt", "source", "meta" or None}

if uploaded_files:
    for f in uploaded_files:
        content = f.read().decode("utf-8", errors="replace")
        file_list.append({"name": f.name, "txt": content, "source": "upload", "meta": None})

for api_sess in st.session_state.api_sessions:
    file_list.append({"name": api_sess["name"], "txt": api_sess["txt"],
                      "source": "api", "meta": api_sess.get("meta")})

# ─────────────────────────────────────────────────────────────
# SECTION 2 — PROCESS EACH FILE
# ─────────────────────────────────────────────────────────────
if not file_list:
    st.markdown("""
    <div style="text-align:center; padding:4.5rem 2rem; background:white;
         border:1px solid #e2e8f0; border-radius:12px; margin:1.5rem 0;
         box-shadow:0 1px 3px rgba(0,0,0,.06);">
      <div style="font-size:2rem; margin-bottom:.8rem; opacity:.35;">📊</div>
      <div style="font-size:1rem; font-weight:700; color:#0f2044; margin-bottom:.4rem;">No data loaded</div>
      <div style="font-size:.85rem; color:#94a3b8; max-width:440px; margin:0 auto; line-height:1.6;">
        Upload one or more vibration TXT files above, or fetch the latest session from the
        device API. Each file will be processed independently — configure time window, view
        charts, and download CSVs. A merged download appears at the bottom once files are loaded.
      </div>
    </div>
    """, unsafe_allow_html=True)
else:
    n = len(file_list)
    st.markdown(f"""
    <div class="sec-h">
      <div class="sec-h-dot"></div>
      <div class="sec-h-text">Step 2 — Configure & Export</div>
      <div class="sec-h-line"></div>
      <span style="font-size:.65rem;color:#94a3b8;background:white;border:1px solid #e2e8f0;
            padding:.18rem .55rem;border-radius:100px;">{n} session{"s" if n!=1 else ""}</span>
    </div>
    """, unsafe_allow_html=True)

    # Collectors for merged download
    all_dfs_57 = []
    all_dfs_19 = []
    merge_rows  = []   # for summary table

    for file in file_list:
        fname  = file["name"]
        src    = file["source"]
        meta   = file.get("meta")
        icon   = "📡" if src == "api" else "📄"
        src_lbl = "API" if src == "api" else "File"

        # ── Expander = one session ────────────────────────────────
        with st.expander(f"{icon}  {fname}", expanded=True):

            # Remove API session button
            if src == "api":
                col_rm_h, col_rm_b = st.columns([5, 1])
                with col_rm_b:
                    st.markdown('<div class="btn-sm">', unsafe_allow_html=True)
                    if st.button("Remove", key=f"rm_{fname}"):
                        st.session_state.api_sessions = [
                            s for s in st.session_state.api_sessions if s["name"] != fname
                        ]
                        st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)

            # ── Device meta (API sessions only) ───────────────────
            if meta:
                st.markdown(f"""
                <div class="meta-grid">
                  <div class="meta-cell"><div class="meta-k">Device</div><div class="meta-v hi">{meta.get('device_name','—')}</div></div>
                  <div class="meta-cell"><div class="meta-k">Sample Rate</div><div class="meta-v">{meta.get('sampling_rate','—')}</div></div>
                  <div class="meta-cell"><div class="meta-k">Duration</div><div class="meta-v">{meta.get('duration','—')}</div></div>
                  <div class="meta-cell"><div class="meta-k">Records</div><div class="meta-v hi">{meta.get('records',0):,}</div></div>
                  <div class="meta-cell"><div class="meta-k">Start</div><div class="meta-v" style="font-size:.75rem;">{meta.get('t_start','—')}</div></div>
                  <div class="meta-cell"><div class="meta-k">End</div><div class="meta-v" style="font-size:.75rem;">{meta.get('t_end','—')}</div></div>
                  <div class="meta-cell"><div class="meta-k">Size</div><div class="meta-v">{meta.get('size_kb','—')} KB</div></div>
                  <div class="meta-cell"><div class="meta-k">Fetched At</div><div class="meta-v">{meta.get('fetched_at','—')}</div></div>
                </div>
                """, unsafe_allow_html=True)

            # ── TXT preview ───────────────────────────────────────
            raw_prev = file["txt"][:1100] + ("\n…[truncated]" if len(file["txt"]) > 1100 else "")
            st.markdown('<div class="inh">Raw Data Preview</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="txt-pre">{hl_txt(raw_prev)}</div>', unsafe_allow_html=True)

            # ── Label ─────────────────────────────────────────────
            st.markdown('<div class="inh">Label Configuration</div>', unsafe_allow_html=True)
            lc1, lc2 = st.columns([1, 2])
            with lc1:
                use_label = st.checkbox("Add fault label column", key=f"chk_{fname}")
            with lc2:
                label_value = None
                if use_label:
                    label_value = LABEL_MAP[st.selectbox(
                        "Fault type",
                        list(LABEL_MAP.keys()),
                        key=f"lbl_{fname}",
                        label_visibility="collapsed",
                    )]

            # ── Parse ─────────────────────────────────────────────
            txt = file["txt"]
            df  = parse_vibration(txt)
            if df.empty:
                st.markdown('<div class="ax error">❌ No vibration records found. Please verify the file format.</div>', unsafe_allow_html=True)
                continue

            df_57 = reorder_columns_57(df)

            # ── Time window ───────────────────────────────────────
            st.markdown('<div class="inh">Time Window Selection</div>', unsafe_allow_html=True)
            df_57["Time_dt"] = pd.to_datetime(df_57["Time"], format="%d/%m/%Y %H:%M:%S")
            time_list = df_57["Time_dt"].tolist()
            tmin = df_57["Time_dt"].min().to_pydatetime()
            tmax = df_57["Time_dt"].max().to_pydatetime()
            N    = len(time_list)

            method = st.radio(
                "Method",
                ["⚡ Quick Slider", "🎯 Precise Time Input"],
                horizontal=True, key=f"tw_{fname}", label_visibility="collapsed",
            )

            if method == "⚡ Quick Slider":
                cs, cm = st.columns([4, 1])
                with cs:
                    si, ei = st.slider("Range", 0, N-1, (0, N-1),
                                       key=f"sl_{fname}", label_visibility="collapsed")
                    start = time_list[si]; end = time_list[ei]
                    st.caption(f"Start: {start.strftime('%d/%m/%Y %H:%M:%S')}   →   End: {end.strftime('%d/%m/%Y %H:%M:%S')}")
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
                    st.markdown('<div class="ax error">⚠️ Start time must be before end time.</div>', unsafe_allow_html=True)
                    start, end = tmin, tmax

            # Apply filter
            df_57 = df_57[(df_57["Time_dt"] >= start) & (df_57["Time_dt"] <= end)]
            df_57 = df_57.drop(columns="Time_dt").reset_index(drop=True)

            if use_label:
                df_57["Label"] = label_value

            if df_57.empty:
                st.markdown('<div class="ax warn">⚠️ No records in selected window. Adjust the range.</div>', unsafe_allow_html=True)
                continue

            # ── Charts ────────────────────────────────────────────
            st.markdown('<div class="inh">Feature Visualization</div>', unsafe_allow_html=True)
            vc1, vc2, vc3 = st.columns(3)
            with vc1:
                st.pyplot(make_chart(df_57, ["Parameter-1_X","Parameter-1_Y","Parameter-1_Z"], "Parameter-1 · RMS", "blue"), use_container_width=True)
            with vc2:
                st.pyplot(make_chart(df_57, ["Parameter-2_X","Parameter-2_Y","Parameter-2_Z"], "Parameter-2 · Peak-to-Peak", "teal"), use_container_width=True)
            with vc3:
                st.pyplot(make_chart(df_57, ["Parameter-3_X","Parameter-3_Y","Parameter-3_Z"], "Parameter-3 · Kurtosis", "amber"), use_container_width=True)

            # ── 19-feature ────────────────────────────────────────
            df_19 = convert_to_19_features(df_57)

            # ── Data preview tabs ─────────────────────────────────
            st.markdown('<div class="inh">57-Feature Preview</div>', unsafe_allow_html=True)
            st.dataframe(df_57, height=270, use_container_width=True)

            st.markdown('<div class="inh">19-Feature Preview</div>', unsafe_allow_html=True)
            st.markdown('<div class="ax info">ℹ️ Each record expands to 3 rows — one per axis (X, Y, Z). Same timestamp, axis-specific parameters.</div>', unsafe_allow_html=True)
            st.dataframe(df_19, height=270, use_container_width=True)

            # ── Downloads ─────────────────────────────────────────
            st.markdown('<div class="inh">Download</div>', unsafe_allow_html=True)
            base = file_prefix.strip() if file_prefix.strip() else fname.replace(".txt","").replace(" ","_")[:35]
            clean = re.sub(r'[^\w\-.]', '_', fname)[:25]
            f57   = f"{base}_{clean}_57feat.csv" if file_prefix.strip() else f"{clean}_57feat.csv"
            f19   = f"{base}_{clean}_19feat.csv" if file_prefix.strip() else f"{clean}_19feat.csv"

            st.markdown(f'<div class="ax ok">✅ Ready — <strong>{len(df_57):,} records</strong> selected · {len(df_57.columns)} columns (57-feat) · {len(df_19):,} rows (19-feat)</div>', unsafe_allow_html=True)

            dc1, dc2 = st.columns(2)
            with dc1:
                st.download_button(f"📥  Download 57-Feature CSV",
                                   df_57.to_csv(index=False), f57, "text/csv",
                                   key=f"dl57_{fname}", use_container_width=True)
                st.caption(f"{f57}  ·  {len(df_57):,} rows  ·  {len(df_57.columns)} cols")
            with dc2:
                st.markdown('<div class="dl-teal">', unsafe_allow_html=True)
                st.download_button(f"📥  Download 19-Feature CSV",
                                   df_19.to_csv(index=False), f19, "text/csv",
                                   key=f"dl19_{fname}", use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
                st.caption(f"{f19}  ·  {len(df_19):,} rows  ·  20 cols")

            # Collect for merge
            all_dfs_57.append(df_57)
            all_dfs_19.append(df_19)
            lbl_name = next((k for k, v in LABEL_MAP.items() if v == label_value), "—") if use_label else "None"
            merge_rows.append({"name": fname, "source": src_lbl,
                                "records": len(df_57), "label": lbl_name})

    # ─────────────────────────────────────────────────────────
    # SECTION 3 — MERGED DOWNLOAD  (exact reference logic)
    # ─────────────────────────────────────────────────────────
    if all_dfs_57:
        merged_57 = pd.concat(all_dfs_57, ignore_index=True)
        merged_19 = pd.concat(all_dfs_19, ignore_index=True)

        merged_prefix  = (file_prefix + "_") if file_prefix.strip() else ""
        merged_name_57 = f"{merged_prefix}Merged_Data_57feat.csv"
        merged_name_19 = f"{merged_prefix}Merged_Data_19feat.csv"

        st.markdown("""
        <div class="sec-h">
          <div class="sec-h-dot" style="background:#15803d;"></div>
          <div class="sec-h-text">Step 3 — Merged Dataset</div>
          <div class="sec-h-line"></div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="merge-wrap">
          <div class="merge-title">🗂 Merged Dataset Download</div>
          <div class="merge-sub">
            Combines all sessions' filtered selections into a single CSV.
            Each session's active time window is respected — only selected records are included.
          </div>
        """, unsafe_allow_html=True)

        # Summary table inside the dark block
        rows_html = ""
        for m in merge_rows:
            rows_html += f'<tr><td>{"📡" if m["source"]=="API" else "📄"} {m["name"][:45]}</td><td>{m["records"]:,}</td><td>{m["label"]}</td></tr>'

        st.markdown(f"""
          <table class="merge-table">
            <thead><tr><th>Session</th><th>Records (filtered)</th><th>Label</th></tr></thead>
            <tbody>{rows_html}</tbody>
          </table>
        </div>
        """, unsafe_allow_html=True)

        # Stats row
        mc1, mc2, mc3, mc4 = st.columns(4)
        with mc1: st.metric("Sessions Merged", len(all_dfs_57))
        with mc2: st.metric("57-feat Total Rows", f"{len(merged_57):,}")
        with mc3: st.metric("19-feat Total Rows", f"{len(merged_19):,}")
        with mc4: st.metric("Columns (57-feat)", len(merged_57.columns))

        st.markdown(f'<div class="ax info" style="margin:.8rem 0;">📋 Files: <strong>{merged_name_57}</strong> and <strong>{merged_name_19}</strong></div>', unsafe_allow_html=True)

        dl1, dl2 = st.columns(2)
        with dl1:
            st.markdown("""
            <div style="background:linear-gradient(135deg,#1e3a8a,#2563eb);border-radius:10px;
                 padding:1.2rem 1.4rem .8rem;text-align:center;margin-bottom:.5rem;">
              <div style="color:white;font-weight:700;font-size:.95rem;margin-bottom:.18rem;">57-Feature Merged CSV</div>
              <div style="color:#bfdbfe;font-size:.76rem;">Time + Parameter-1..19 × X, Y, Z</div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown('<div class="dl-merge-blue">', unsafe_allow_html=True)
            st.download_button(f"📥  Download {merged_name_57}",
                               merged_57.to_csv(index=False), merged_name_57, "text/csv",
                               key="dl_m57", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with dl2:
            st.markdown("""
            <div style="background:linear-gradient(135deg,#134e4a,#0d9488);border-radius:10px;
                 padding:1.2rem 1.4rem .8rem;text-align:center;margin-bottom:.5rem;">
              <div style="color:white;font-weight:700;font-size:.95rem;margin-bottom:.18rem;">19-Feature Merged CSV</div>
              <div style="color:#a7f3d0;font-size:.76rem;">Time + Parameter-1..19, axes stacked</div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown('<div class="dl-merge-teal">', unsafe_allow_html=True)
            st.download_button(f"📥  Download {merged_name_19}",
                               merged_19.to_csv(index=False), merged_name_19, "text/csv",
                               key="dl_m19", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────
st.markdown('<div class="pg-footer">Vibration Data Converter · pump_project · Professional Edition</div>', unsafe_allow_html=True)