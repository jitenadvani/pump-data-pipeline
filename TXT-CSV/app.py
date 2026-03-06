"""
Vibration Data Converter  ·  pump_project  ·  v5.0
─────────────────────────────────────────────────────
Dark professional UI · Cached parsing · Memory-safe
"""

import gc
import re
import json
import requests
from datetime import datetime

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

# ── Page config ──────────────────────────────────────────────────
st.set_page_config(
    page_title="VDC · Vibration Data Converter",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ════════════════════════════════════════════════════════════════
#  THEME  ──  Dark professional, zero white-on-white
# ════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Design tokens ─────────────────────────────────────── */
:root{
  --bg0:#0d1117; --bg1:#161c26; --bg2:#1c2438; --bg3:#222d42;
  --bg4:#283350; --bgh:#0d1117cc;

  --bd1:#263045; --bd2:#2f3d58; --bd3:#3d5070;

  --blue:#3b82f6; --blue2:#2563eb; --blue-a:rgba(59,130,246,.13);
  --blue-b:rgba(59,130,246,.28);
  --teal:#14b8a6; --teal2:#0d9488; --teal-a:rgba(20,184,166,.13);
  --green:#10b981; --green-a:rgba(16,185,129,.13); --green-b:rgba(16,185,129,.3);
  --amber:#f59e0b; --amber-a:rgba(245,158,11,.13); --amber-b:rgba(245,158,11,.3);
  --rose:#f43f5e;  --rose-a:rgba(244,63,94,.13);   --rose-b:rgba(244,63,94,.3);

  --t1:#eaf0ff; --t2:#a8bcd8; --t3:#5d7496; --t4:#374560;

  --ff:'Inter',system-ui,sans-serif;
  --fm:'JetBrains Mono','Fira Code',monospace;

  --r8:8px; --r10:10px; --r12:12px;
  --s1:0 1px 3px rgba(0,0,0,.5),0 1px 2px rgba(0,0,0,.4);
  --s2:0 4px 14px rgba(0,0,0,.55),0 2px 4px rgba(0,0,0,.35);
}

/* ── Global ─────────────────────────────────────────────── */
html,body,[class*="css"]{font-family:var(--ff);color:var(--t1);}
.stApp{background:var(--bg0);}
.block-container{padding:0 2.5rem 5rem!important;max-width:1300px!important;}
#MainMenu,footer,header{visibility:hidden;}
*{box-sizing:border-box;}
::-webkit-scrollbar{width:5px;height:5px;}
::-webkit-scrollbar-track{background:var(--bg1);}
::-webkit-scrollbar-thumb{background:var(--bd2);border-radius:3px;}
::-webkit-scrollbar-thumb:hover{background:var(--blue);}

/* ── Sidebar ─────────────────────────────────────────────── */
[data-testid="stSidebar"]{background:var(--bg1)!important;border-right:1px solid var(--bd1)!important;}
[data-testid="stSidebar"] .block-container{padding:1.8rem 1.3rem!important;}
[data-testid="stSidebar"] *{color:var(--t2)!important;}
[data-testid="stSidebar"] strong{color:var(--t1)!important;}
[data-testid="stSidebar"] .stTextInput>div>div>input{
  background:var(--bg3)!important;border:1px solid var(--bd2)!important;
  color:var(--t1)!important;border-radius:var(--r8)!important;
  font-family:var(--fm)!important;font-size:.83rem!important;padding:.45rem .75rem!important;}
[data-testid="stSidebar"] .stTextInput>div>div>input:focus{
  border-color:var(--blue)!important;box-shadow:0 0 0 3px var(--blue-a)!important;}

/* ── Top bar ─────────────────────────────────────────────── */
.topbar{
  background:var(--bg1);border-bottom:1px solid var(--bd1);
  margin:0 -2.5rem 2.5rem;padding:1.3rem 2.5rem;
  display:flex;align-items:center;justify-content:space-between;
}
.topbar-left h1{
  font-size:1.55rem;font-weight:700;color:var(--t1);
  letter-spacing:-.025em;margin:0;line-height:1.15;
}
.topbar-left h1 span{color:var(--blue);}
.topbar-left p{font-size:.78rem;color:var(--t3);margin:.25rem 0 0;}
.topbar-badge{
  font-size:.68rem;font-weight:600;letter-spacing:.06em;
  padding:.3rem .85rem;border-radius:100px;
  background:var(--blue-a);color:var(--blue);border:1px solid var(--blue-b);
}

/* ── Step heading ────────────────────────────────────────── */
.sh{display:flex;align-items:center;gap:.7rem;margin:2.5rem 0 1.1rem;}
.sh-num{
  width:26px;height:26px;border-radius:6px;
  display:flex;align-items:center;justify-content:center;
  font-size:.74rem;font-weight:700;color:#fff;flex-shrink:0;
}
.sh-lbl{font-size:.68rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--t3);}
.sh-line{flex:1;height:1px;background:var(--bd1);}
.sh-cnt{font-size:.62rem;color:var(--t4);background:var(--bg2);border:1px solid var(--bd1);padding:.15rem .55rem;border-radius:100px;}

/* ── Source boxes (Step 1) ───────────────────────────────── */
.src-box{
  background:var(--bg1);border:1px solid var(--bd1);
  border-radius:var(--r12);padding:1.4rem 1.5rem;box-shadow:var(--s1);
}
.src-title{
  font-size:.66rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;
  color:var(--t3);margin:0 0 .8rem;display:flex;align-items:center;gap:.4rem;
}
.src-dot{width:7px;height:7px;border-radius:50%;flex-shrink:0;}
.mono-tag{
  font-family:var(--fm);font-size:.72rem;color:var(--teal);
  background:var(--teal-a);border:1px solid rgba(20,184,166,.25);
  border-radius:5px;padding:.25rem .7rem;display:inline-block;margin-bottom:.75rem;
}

/* ── Session panel ───────────────────────────────────────── */
.sp{background:var(--bg1);border:1px solid var(--bd1);border-radius:var(--r12);margin-bottom:1.8rem;box-shadow:var(--s1);overflow:hidden;}
.sp:hover{border-color:var(--bd2);}
.sp-head{
  background:var(--bg2);border-bottom:1px solid var(--bd1);
  padding:.95rem 1.5rem;display:flex;align-items:center;gap:.85rem;
}
.sp-icon{width:38px;height:38px;border-radius:9px;display:flex;align-items:center;justify-content:center;font-size:1.05rem;flex-shrink:0;}
.sp-icon.u{background:var(--blue-a);border:1px solid var(--blue-b);}
.sp-icon.a{background:var(--teal-a);border:1px solid rgba(20,184,166,.28);}
.sp-name{font-size:.95rem;font-weight:600;color:var(--t1);flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}
.sp-body{padding:1.4rem 1.5rem;}

/* ── Chip ────────────────────────────────────────────────── */
.chip{
  display:inline-flex;align-items:center;font-size:.62rem;font-weight:600;
  letter-spacing:.05em;text-transform:uppercase;padding:.2rem .6rem;border-radius:4px;
}
.chip-b{background:var(--blue-a);color:var(--blue);border:1px solid var(--blue-b);}
.chip-t{background:var(--teal-a);color:var(--teal);border:1px solid rgba(20,184,166,.3);}
.chip-g{background:var(--green-a);color:var(--green);border:1px solid var(--green-b);}

/* ── Row label ───────────────────────────────────────────── */
.rl{
  font-size:.64rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;
  color:var(--t3);margin:1.4rem 0 .65rem;
  display:flex;align-items:center;gap:.5rem;
}
.rl::after{content:'';flex:1;height:1px;background:var(--bd1);}

/* ── Info grid ───────────────────────────────────────────── */
.ig{display:grid;grid-template-columns:repeat(auto-fill,minmax(148px,1fr));gap:.5rem;margin-bottom:.8rem;}
.ic{background:var(--bg2);border:1px solid var(--bd1);border-radius:var(--r8);padding:.65rem .9rem;}
.ik{font-size:.58rem;font-weight:600;letter-spacing:.09em;text-transform:uppercase;color:var(--t3);margin-bottom:.2rem;}
.iv{font-family:var(--fm);font-size:.83rem;font-weight:500;color:var(--t1);}
.iv.hi{color:var(--blue);}  .iv.sm{font-size:.72rem;}
.iv.miss{color:var(--t3);font-style:italic;}

/* ── TXT preview ─────────────────────────────────────────── */
.txp{
  background:#060c14;border:1px solid var(--bd1);border-radius:var(--r8);
  padding:.9rem 1.1rem;font-family:var(--fm);font-size:.7rem;
  max-height:160px;overflow-y:auto;line-height:1.7;white-space:pre;
}
.txp::-webkit-scrollbar{width:3px;}
.txp::-webkit-scrollbar-thumb{background:var(--bd2);}

/* ── Alerts ──────────────────────────────────────────────── */
.ax{border-radius:var(--r8);padding:.8rem 1.1rem;font-size:.84rem;line-height:1.55;margin:.6rem 0;}
.ax.info {background:var(--blue-a);border:1px solid var(--blue-b);color:#93c5fd;}
.ax.ok   {background:var(--green-a);border:1px solid var(--green-b);color:#6ee7b7;}
.ax.warn {background:var(--amber-a);border:1px solid var(--amber-b);color:#fcd34d;}
.ax.err  {background:var(--rose-a); border:1px solid var(--rose-b); color:#fda4af;}

/* ── Debug box ───────────────────────────────────────────── */
.dbg{
  background:#050a10;border:1px solid var(--amber-b);border-radius:var(--r8);
  padding:.85rem 1rem;font-family:var(--fm);font-size:.7rem;color:#fcd34d;
  max-height:220px;overflow-y:auto;line-height:1.65;white-space:pre-wrap;
}

/* ── Merge section ───────────────────────────────────────── */
.merge-wrap{
  background:linear-gradient(135deg,var(--bg2),var(--bg3));
  border:1px solid var(--bd2);border-radius:14px;
  padding:2rem 2.2rem;margin-top:2.5rem;box-shadow:var(--s2);
}
.merge-title{font-size:1.2rem;font-weight:700;color:var(--t1);margin:0 0 .25rem;letter-spacing:-.02em;}
.merge-sub{font-size:.82rem;color:var(--t3);margin:0 0 1.3rem;}
.mtbl{width:100%;border-collapse:collapse;margin:.8rem 0 1.2rem;}
.mtbl th{font-size:.6rem;font-weight:700;letter-spacing:.09em;text-transform:uppercase;color:var(--t3);padding:.45rem .85rem;border-bottom:1px solid var(--bd1);text-align:left;}
.mtbl td{font-size:.82rem;color:var(--t2);padding:.45rem .85rem;border-bottom:1px solid var(--bd1);font-family:var(--fm);}
.mtbl td:first-child{color:var(--t1);font-family:var(--ff);font-weight:500;}
.mtbl tr:last-child td{border-bottom:none;}
.mdb{border-radius:var(--r10);padding:1.1rem 1.4rem .75rem;text-align:center;margin-bottom:.5rem;}
.mdb.b{background:linear-gradient(135deg,#1e3a8a,#2563eb);border:1px solid rgba(147,197,253,.15);}
.mdb.t{background:linear-gradient(135deg,#134e4a,#0f766e);border:1px solid rgba(45,212,191,.15);}
.mdb-t{color:var(--t1);font-weight:600;font-size:.95rem;margin-bottom:.18rem;}
.mdb-s{color:rgba(255,255,255,.35);font-size:.74rem;}

/* ══ STREAMLIT COMPONENT OVERRIDES ══════════════════════ */

/* All text in main area */
p,li,span.stMarkdown{color:var(--t2)!important;}
label{color:var(--t2)!important;}
.stMarkdown h1,.stMarkdown h2,.stMarkdown h3{color:var(--t1)!important;}
.stCaption{color:var(--t3)!important;font-size:.71rem!important;}

/* Buttons */
.stButton>button{
  background:var(--blue)!important;color:#fff!important;
  font-family:var(--ff)!important;font-weight:600!important;font-size:.87rem!important;
  border:none!important;border-radius:var(--r8)!important;padding:.6rem 1.5rem!important;
  transition:all .18s!important;box-shadow:0 2px 8px var(--blue-b)!important;
}
.stButton>button:hover{background:var(--blue2)!important;box-shadow:0 4px 16px var(--blue-b)!important;transform:translateY(-1px)!important;}
.stButton>button:active{transform:translateY(0)!important;}
.btn-teal>button{background:var(--teal)!important;box-shadow:0 2px 8px rgba(20,184,166,.3)!important;}
.btn-teal>button:hover{background:var(--teal2)!important;box-shadow:0 4px 16px rgba(20,184,166,.4)!important;}
.btn-ghost>button{background:var(--bg3)!important;color:var(--t2)!important;border:1px solid var(--bd2)!important;box-shadow:none!important;}
.btn-ghost>button:hover{border-color:var(--blue)!important;color:var(--blue)!important;}
.btn-sm>button{background:var(--bg3)!important;color:var(--rose)!important;border:1px solid var(--rose-b)!important;box-shadow:none!important;font-size:.77rem!important;padding:.38rem .8rem!important;}
.btn-sm>button:hover{background:var(--rose-a)!important;transform:none!important;}

/* Download */
.stDownloadButton>button{
  background:var(--blue)!important;color:#fff!important;border:none!important;
  border-radius:var(--r8)!important;font-family:var(--ff)!important;font-weight:600!important;
  font-size:.87rem!important;padding:.65rem 1.2rem!important;width:100%!important;
  transition:all .18s!important;box-shadow:0 2px 8px var(--blue-b)!important;
}
.stDownloadButton>button:hover{background:var(--blue2)!important;box-shadow:0 4px 16px var(--blue-b)!important;transform:translateY(-1px)!important;}
.dl-teal .stDownloadButton>button{background:var(--teal)!important;box-shadow:0 2px 8px rgba(20,184,166,.3)!important;}
.dl-teal .stDownloadButton>button:hover{background:var(--teal2)!important;box-shadow:0 4px 16px rgba(20,184,166,.4)!important;}
.dl-mb .stDownloadButton>button{background:linear-gradient(135deg,#1e3a8a,#2563eb)!important;font-size:.9rem!important;padding:.7rem 1.2rem!important;box-shadow:0 3px 14px rgba(37,99,235,.45)!important;}
.dl-mt .stDownloadButton>button{background:linear-gradient(135deg,#134e4a,#0f766e)!important;font-size:.9rem!important;padding:.7rem 1.2rem!important;box-shadow:0 3px 14px rgba(15,118,110,.45)!important;}

/* Slider */
.stSlider>div>div>div>div{background:var(--blue)!important;}
.stSlider>div>div>div{background:var(--bd2)!important;height:4px!important;}

/* Metrics */
[data-testid="metric-container"]{background:var(--bg2)!important;border:1px solid var(--bd1)!important;border-radius:var(--r8)!important;padding:.7rem .9rem!important;}
[data-testid="metric-container"] label{color:var(--t3)!important;font-size:.6rem!important;font-weight:600!important;letter-spacing:.08em!important;text-transform:uppercase!important;}
[data-testid="metric-container"] [data-testid="stMetricValue"]{color:var(--t1)!important;font-size:1.15rem!important;font-weight:700!important;}

/* Selectbox */
.stSelectbox>div>div{background:var(--bg3)!important;border:1px solid var(--bd2)!important;border-radius:var(--r8)!important;color:var(--t1)!important;font-size:.85rem!important;}
.stSelectbox>div>div:focus-within{border-color:var(--blue)!important;box-shadow:0 0 0 3px var(--blue-a)!important;}
.stSelectbox label{color:var(--t3)!important;font-size:.68rem!important;font-weight:600!important;letter-spacing:.08em!important;text-transform:uppercase!important;}
[data-baseweb="select"] [data-testid="stMarkdownContainer"] p{color:var(--t1)!important;}

/* Radio */
.stRadio>div{flex-direction:row!important;gap:.4rem!important;flex-wrap:wrap;}
.stRadio>div>label{background:var(--bg3)!important;border:1px solid var(--bd2)!important;border-radius:var(--r8)!important;padding:.45rem 1rem!important;color:var(--t2)!important;font-size:.84rem!important;font-weight:500!important;cursor:pointer!important;transition:all .15s!important;}
.stRadio>div>label:hover{border-color:var(--blue)!important;color:var(--blue)!important;background:var(--blue-a)!important;}
.stRadio label{color:var(--t2)!important;}

/* Checkbox */
.stCheckbox label{color:var(--t2)!important;font-size:.86rem!important;}
.stCheckbox span{color:var(--t2)!important;}

/* File uploader */
[data-testid="stFileUploader"]{background:var(--bg2)!important;border:1.5px dashed var(--bd2)!important;border-radius:9px!important;}
[data-testid="stFileUploader"]:hover{border-color:var(--blue)!important;}
[data-testid="stFileUploader"] *{color:var(--t2)!important;}

/* Dataframe */
.stDataFrame{border-radius:var(--r8);overflow:hidden;box-shadow:var(--s1);}

/* Spinner */
.stSpinner>div{border-top-color:var(--blue)!important;}

/* Expander */
.streamlit-expanderHeader{background:var(--bg2)!important;border:1px solid var(--bd1)!important;border-radius:var(--r8)!important;color:var(--t2)!important;}
.streamlit-expanderHeader p{color:var(--t2)!important;}
.streamlit-expanderContent{background:var(--bg2)!important;border:1px solid var(--bd1)!important;border-top:none!important;border-radius:0 0 var(--r8) var(--r8)!important;}

hr{border:none;height:1px;background:var(--bd1);margin:1.5rem 0;}
.pg-footer{text-align:center;padding:2.5rem 0 1rem;font-size:.73rem;color:var(--t4);}
</style>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
#  CONSTANTS
# ════════════════════════════════════════════════════════════════
API_BASE  = "https://pumpdata.duckdns.org/api"
SR_LABEL  = {5:"5 sec", 10:"10 sec", 15:"15 sec", 30:"30 sec"}
LABEL_MAP = {
    "Normal_Mode (0)":        0,
    "Seal Failure (1)":       1,
    "Bearing (2)":            2,
    "Shaft Misalignment (3)": 3,
    "Unbalance_impeller (4)": 4,
    "Cavitation (5)":         5,
}

# ════════════════════════════════════════════════════════════════
#  SESSION STATE
# ════════════════════════════════════════════════════════════════
for k, v in {
    "api_sessions": [],
    "fetch_msg":    None,
    "fetch_type":   None,
    "last_raw_payload": None,   # for debug display
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ════════════════════════════════════════════════════════════════
#  CORE PARSING  (cached — prevents memory crash / exit 132)
# ════════════════════════════════════════════════════════════════
@st.cache_data(max_entries=8, show_spinner=False)
def cached_parse_57(txt: str) -> pd.DataFrame:
    """Parse TXT → 57-feature DataFrame. Cached per unique file content."""
    rows = []
    lines = [l.strip() for l in txt.splitlines() if l.strip()]
    i = 0
    time_re = re.compile(r"\d+/\d+/\d+\s+\d+:\d+:\d+\s+(AM|PM)")
    pnr = re.compile(r"Peak\s+(\d+)\s+Parameter-\d+\s+([-\d.]+)\s+Parameter-\d+\s+([-\d.]+)")
    por = re.compile(r"Peak\s+(\d+)\s+Freq\s+([-\d.]+)\s+Mag\s+([-\d.]+)")

    def tf(tok, j):
        try: return float(tok[j])
        except: return None

    while i < len(lines):
        if time_re.match(lines[i]):
            ts = lines[i].strip()
            try:
                row = {"Time": datetime.strptime(ts, "%m/%d/%Y %I:%M:%S %p").strftime("%d/%m/%Y %H:%M:%S")}
            except Exception:
                row = {"Time": ts}
            i += 1
            for axis in ["X", "Y", "Z"]:
                while i < len(lines) and f"{axis} Axis" not in lines[i]:
                    i += 1
                i += 1
                peaks = {}
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
                    fp = 2 + p * 2; mp = 2 + p * 2 + 1
                    row[f"Parameter-{fp}_{axis}"] = peaks.get(p, (None, None))[0]
                    row[f"Parameter-{mp}_{axis}"] = peaks.get(p, (None, None))[1]
            rows.append(row)
        else:
            i += 1

    # Build ordered 57-col frame
    cols = ["Time"]
    for n in range(1, 4):
        for ax in ["X", "Y", "Z"]: cols.append(f"Parameter-{n}_{ax}")
    for p in range(1, 9):
        fp = 2 + p * 2; mp = 2 + p * 2 + 1
        for ax in ["X", "Y", "Z"]: cols.append(f"Parameter-{fp}_{ax}")
        for ax in ["X", "Y", "Z"]: cols.append(f"Parameter-{mp}_{ax}")
    df = pd.DataFrame(rows)
    for c in cols:
        if c not in df.columns: df[c] = pd.NA
    return df[cols]


@st.cache_data(max_entries=16, show_spinner=False)
def cached_to19(cache_key: str, df57: pd.DataFrame) -> pd.DataFrame:
    """Convert 57-feat → 19-feat.  cache_key encodes shape+label so cache is invalidated properly."""
    rows = []; hl = "Label" in df57.columns
    for _, row in df57.iterrows():
        for axis in ["X", "Y", "Z"]:
            nr = {"Time": row.get("Time", pd.NA)}
            for n in range(1, 4): nr[f"Parameter-{n}"] = row.get(f"Parameter-{n}_{axis}", pd.NA)
            for p in range(1, 9):
                fp = 2 + p * 2; mp = 2 + p * 2 + 1
                nr[f"Parameter-{fp}"] = row.get(f"Parameter-{fp}_{axis}", pd.NA)
                nr[f"Parameter-{mp}"] = row.get(f"Parameter-{mp}_{axis}", pd.NA)
            if hl: nr["Label"] = row["Label"]
            rows.append(nr)
    c19 = ["Time"] + [f"Parameter-{n}" for n in range(1, 20)]
    d = pd.DataFrame(rows)
    if hl: c19.append("Label")
    return d[c19]

# ════════════════════════════════════════════════════════════════
#  EXTRACT META — reads every possible key the FastAPI server
#  could use for device_name / sampling_rate / duration_val
# ════════════════════════════════════════════════════════════════
def extract_meta(content: str, payload: dict) -> dict:
    tre = re.compile(r"(\d+/\d+/\d+)\s+(\d+:\d+:\d+)\s+(AM|PM)")
    ts  = tre.findall(content)
    t_s = f"{ts[0][0]} {ts[0][1]} {ts[0][2]}"    if ts else "—"
    t_e = f"{ts[-1][0]} {ts[-1][1]} {ts[-1][2]}" if ts else "—"
    rec = content.count("#Vibration Value")
    sz  = round(len(content) / 1024, 1)

    # ── Flatten the payload deeply ────────────────────────────────
    # API servers sometimes nest fields under "data", "device", "metadata", etc.
    flat = {}
    def _flatten(obj, prefix=""):
        if isinstance(obj, dict):
            for k, v in obj.items():
                _flatten(v, k)
        else:
            flat[prefix] = obj
    _flatten(payload)

    # Also keep the original top-level for quick lookup
    flat.update(payload)

    # ── Device name ───────────────────────────────────────────────
    dn = "—"
    for key in [
        "device_name", "deviceName", "device_id", "deviceId",
        "name", "sensor_name", "sensorName", "sensor_id", "sensorId",
        "device", "unit", "id", "label", "tag",
    ]:
        v = flat.get(key)
        if v and str(v).strip().lower() not in ("", "none", "null", "unknown", "-", "n/a", "nan"):
            dn = str(v).strip()
            break

    # ── Sampling rate (device.py sends int seconds) ────────────────
    sr_raw = None
    for key in ["sampling_rate", "sample_rate", "interval", "rate", "samplingRate"]:
        if flat.get(key) is not None:
            sr_raw = flat[key]; break
    sr, sr_secs = "—", None
    if sr_raw is not None:
        try:
            sr_secs = int(float(str(sr_raw)))
            sr = SR_LABEL.get(sr_secs, f"{sr_secs} sec")
        except: sr = str(sr_raw)
    # Auto-detect from timestamps
    if sr_secs is None and len(ts) >= 2:
        try:
            fmt = "%m/%d/%Y %I:%M:%S %p"
            t1  = datetime.strptime(f"{ts[0][0]} {ts[0][1]} {ts[0][2]}", fmt)
            t2  = datetime.strptime(f"{ts[1][0]} {ts[1][1]} {ts[1][2]}", fmt)
            d   = int((t2 - t1).total_seconds())
            if 1 <= d <= 300:
                sr_secs = d
                sr = SR_LABEL.get(d, f"{d} sec")
        except: pass

    # ── Duration (device.py sends int hours as duration_val) ───────
    dur_raw = None
    for key in ["duration_val", "duration", "duration_hours", "hours", "durationHours"]:
        if flat.get(key) is not None:
            dur_raw = flat[key]; break
    dur, dur_hours = "—", None
    if dur_raw is not None:
        try:
            dur_hours = int(float(str(dur_raw)))
            dur = f"{dur_hours} hour{'s' if dur_hours != 1 else ''}"
        except: dur = str(dur_raw)
    # Auto-detect from timestamps
    if dur_hours is None and len(ts) >= 2:
        try:
            fmt  = "%m/%d/%Y %I:%M:%S %p"
            t1   = datetime.strptime(f"{ts[0][0]} {ts[0][1]} {ts[0][2]}", fmt)
            te   = datetime.strptime(f"{ts[-1][0]} {ts[-1][1]} {ts[-1][2]}", fmt)
            secs = int((te - t1).total_seconds())
            if secs > 0:
                h = secs // 3600; m = (secs % 3600) // 60
                dur = f"{h}h {m}m" if h else f"{m}m"
                dur_hours = h or 1
        except: pass

    # ── Derived stats ─────────────────────────────────────────────
    rph, exp_rec, completeness = "—", "—", "—"
    if sr_secs:
        rph = f"{3600 // sr_secs:,}"
        if dur_hours:
            exp = (dur_hours * 3600) // sr_secs
            exp_rec = f"{exp:,}"
            if rec > 0 and exp > 0:
                completeness = f"{min(100, round(rec / exp * 100, 1))}%"

    return {
        "device_name":  dn,    "sampling_rate": sr,
        "duration":     dur,   "records":       rec,
        "expected_rec": exp_rec, "rec_per_hour": rph,
        "completeness": completeness,
        "t_start":      t_s,   "t_end":         t_e,
        "size_kb":      sz,
        "fetched_at":   datetime.now().strftime("%H:%M:%S"),
        "fetched_date": datetime.now().strftime("%d %b %Y"),
        "_payload_keys": sorted(list(flat.keys())),   # for debug
    }

# ════════════════════════════════════════════════════════════════
#  HELPERS
# ════════════════════════════════════════════════════════════════
def hl_txt(raw: str) -> str:
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
            out.append(f'<span style="color:#2d4560;">{line}</span>')
        else:
            out.append(f'<span style="color:#3b5270;">{line}</span>')
    return "<br>".join(out)


def make_chart(df: pd.DataFrame, cols: list, title: str, pal: str) -> plt.Figure:
    p = {
        "blue" : ["#3b82f6","#60a5fa","#93c5fd"],
        "teal" : ["#14b8a6","#2dd4bf","#5eead4"],
        "amber": ["#f59e0b","#fbbf24","#fcd34d"],
    }
    cl = p.get(pal, p["blue"])
    fig, ax = plt.subplots(figsize=(5, 3), facecolor="#1c2438")
    ax.set_facecolor("#161c26")
    for i, c in enumerate(cols):
        if c in df.columns:
            ax.plot(df[c].values,
                    label=c.split("_")[-1] if "_" in c else c,
                    linewidth=1.8, alpha=0.9, color=cl[i % len(cl)])
    ax.set_title(title, fontsize=9, fontweight="600", color="#a8bcd8", pad=8)
    ax.set_xlabel("Sample", fontsize=7.5, color="#374560")
    ax.legend(fontsize=7, framealpha=0, labelcolor="#a8bcd8", loc="best")
    ax.grid(True, alpha=0.14, linestyle="--", linewidth=0.5, color="#263045")
    for sp in ax.spines.values(): sp.set_color("#263045")
    ax.tick_params(labelsize=7, colors="#374560")
    fig.tight_layout(pad=0.8)
    return fig

# ════════════════════════════════════════════════════════════════
#  SIDEBAR
# ════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style="padding:.1rem 0 1.4rem;border-bottom:1px solid #263045;margin-bottom:1.4rem;">
      <div style="font-size:1rem;font-weight:700;color:#eaf0ff;letter-spacing:-.01em;line-height:1.3;">
        Vibration Data<br><span style="color:#3b82f6;">Converter</span>
      </div>
      <div style="font-size:.6rem;color:#374560;margin-top:.4rem;letter-spacing:.12em;text-transform:uppercase;">
        pump_project · v5.0
      </div>
    </div>
    """, unsafe_allow_html=True)

    file_prefix = st.text_input("Output file prefix", placeholder="e.g. pump_brg_01", key="fp")

    st.markdown("""
    <div style="margin:1.2rem 0;background:#1c2438;border:1px solid #263045;border-radius:9px;padding:1rem;">
      <div style="font-size:.6rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#374560;margin-bottom:.6rem;">Output Formats</div>
      <div style="color:#5d7496;font-size:.8rem;line-height:1.8;">
        <span style="color:#a8bcd8;font-weight:600;">57-Feature CSV</span><br>
        Time + Param-1..19 × X, Y, Z<br><br>
        <span style="color:#a8bcd8;font-weight:600;">19-Feature CSV</span><br>
        X/Y/Z stacked as rows (×3)
      </div>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.api_sessions:
        st.markdown('<div style="font-size:.6rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#374560;margin:1.4rem 0 .5rem;">API Sessions</div>', unsafe_allow_html=True)
        for s in st.session_state.api_sessions:
            st.markdown(f'<div style="font-size:.74rem;color:#5d7496;padding:.3rem 0;border-bottom:1px solid #1c2438;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">📡 {s["name"][:30]}</div>', unsafe_allow_html=True)
        st.markdown('<div style="margin-top:.9rem;"></div>', unsafe_allow_html=True)
        st.markdown('<div class="btn-sm">', unsafe_allow_html=True)
        if st.button("Clear API Sessions", use_container_width=True, key="clr"):
            st.session_state.api_sessions = []
            st.session_state.fetch_msg = None
            st.session_state.last_raw_payload = None
            cached_parse_57.clear(); cached_to19.clear(); gc.collect()
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Debug toggle ──────────────────────────────────────────────
    st.markdown('<div style="height:1px;background:#263045;margin:1.4rem 0;"></div>', unsafe_allow_html=True)
    show_debug = st.checkbox("🔍 Show API debug panel", key="dbg_toggle")

# ════════════════════════════════════════════════════════════════
#  TOP BAR
# ════════════════════════════════════════════════════════════════
st.markdown("""
<div class="topbar">
  <div class="topbar-left">
    <h1>Vibration Data <span>Converter</span></h1>
    <p>Upload TXT files · Fetch from device API · Time-window filter · Export 57-feat &amp; 19-feat CSVs · Merge</p>
  </div>
  <span class="topbar-badge">pump_project</span>
</div>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
#  STEP 1 — LOAD DATA
# ════════════════════════════════════════════════════════════════
st.markdown("""
<div class="sh">
  <div class="sh-num" style="background:#3b82f6;">1</div>
  <div class="sh-lbl">Load Data</div>
  <div class="sh-line"></div>
</div>
""", unsafe_allow_html=True)

col_up, col_api = st.columns(2, gap="large")

with col_up:
    st.markdown("""
    <div class="src-box">
      <div class="src-title">
        <span class="src-dot" style="background:#3b82f6;"></span>Upload TXT Files
      </div>
    </div>""", unsafe_allow_html=True)
    uploaded_files = st.file_uploader(
        "Drop files here", type=["txt"],
        accept_multiple_files=True, key="fu", label_visibility="collapsed",
    )
    st.caption("Multiple files supported — each becomes its own section below")

with col_api:
    st.markdown(f"""
    <div class="src-box">
      <div class="src-title">
        <span class="src-dot" style="background:#14b8a6;"></span>Fetch from Device API
      </div>
      <span class="mono-tag">GET {API_BASE}/latest</span>
    </div>""", unsafe_allow_html=True)
    st.markdown('<div class="btn-teal">', unsafe_allow_html=True)
    fetch_clicked = st.button("📡  Fetch Latest Session", use_container_width=True, key="fetch_btn")
    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.fetch_msg:
        css  = {"success":"ok","error":"err","warning":"warn"}.get(st.session_state.fetch_type, "info")
        icon = {"ok":"✅","err":"❌","warn":"⚠️","info":"ℹ️"}.get(css,"ℹ️")
        st.markdown(f'<div class="ax {css}" style="margin-top:.55rem;">{icon} {st.session_state.fetch_msg}</div>', unsafe_allow_html=True)

    if fetch_clicked:
        with st.spinner("Connecting…"):
            try:
                resp = requests.get(f"{API_BASE}/latest", timeout=15)
                if resp.status_code == 200:
                    payload = resp.json()
                    st.session_state.last_raw_payload = payload   # save for debug
                    content = payload.get("content", "").strip()
                    if content:
                        meta  = extract_meta(content, payload)
                        dn    = meta["device_name"]
                        sname = f"{dn} @ {meta['fetched_at']}" if dn != "—" else f"API @ {meta['fetched_at']}"
                        if sname not in [s["name"] for s in st.session_state.api_sessions]:
                            # Insert at front → latest shows first
                            st.session_state.api_sessions.insert(0, {"name": sname, "txt": content, "meta": meta})
                            gc.collect()
                            st.session_state.fetch_msg  = f"Added <strong>{sname}</strong> — {meta['records']:,} records"
                            st.session_state.fetch_type = "success"
                        else:
                            st.session_state.fetch_msg  = f"Already loaded: {sname}"
                            st.session_state.fetch_type = "warning"
                    else:
                        st.session_state.fetch_msg  = "No data yet — run the Device Simulator first."
                        st.session_state.fetch_type = "warning"
                else:
                    st.session_state.fetch_msg  = f"HTTP {resp.status_code} from server."
                    st.session_state.fetch_type = "error"
            except requests.exceptions.ConnectionError:
                st.session_state.fetch_msg  = f"Cannot reach {API_BASE}. Is api_server.py running?"
                st.session_state.fetch_type = "error"
            except requests.exceptions.Timeout:
                st.session_state.fetch_msg  = "Timed out. Try again."
                st.session_state.fetch_type = "error"
            except Exception as e:
                st.session_state.fetch_msg  = f"Error: {e}"
                st.session_state.fetch_type = "error"
        st.rerun()

# ── Debug panel (shown when sidebar checkbox is on) ───────────────
if show_debug and st.session_state.last_raw_payload is not None:
    st.markdown("""
    <div class="sh" style="margin-top:1.2rem;">
      <div class="sh-num" style="background:#f59e0b;">🔍</div>
      <div class="sh-lbl">API Payload Debug</div>
      <div class="sh-line"></div>
    </div>
    """, unsafe_allow_html=True)
    payload_str = json.dumps(st.session_state.last_raw_payload, indent=2, default=str)
    # Hide content field (too long)
    p_display = {k: (v[:80]+"…" if k=="content" and isinstance(v,str) and len(v)>80 else v)
                 for k,v in st.session_state.last_raw_payload.items()}
    st.markdown(f'<div class="dbg">{json.dumps(p_display, indent=2, default=str)}</div>', unsafe_allow_html=True)
    st.caption("↑ These are ALL keys the API returned. If device_name shows '—' above, the key name is shown here so you can tell me the correct one.")

# ════════════════════════════════════════════════════════════════
#  BUILD UNIFIED FILE LIST
# ════════════════════════════════════════════════════════════════
file_list = []
if uploaded_files:
    for f in uploaded_files:
        content = f.read().decode("utf-8", errors="replace")
        file_list.append({"name": f.name, "txt": content, "source": "upload", "meta": None})
# API sessions: already newest-first in state
for s in st.session_state.api_sessions:
    file_list.append({"name": s["name"], "txt": s["txt"], "source": "api", "meta": s.get("meta")})

# ════════════════════════════════════════════════════════════════
#  STEP 2 — PROCESS SESSIONS
# ════════════════════════════════════════════════════════════════
if not file_list:
    st.markdown("""
    <div style="text-align:center;padding:5rem 2rem;background:#161c26;border:1px solid #263045;
         border-radius:14px;margin:2rem 0;">
      <div style="font-size:2.5rem;margin-bottom:.8rem;opacity:.15;">📊</div>
      <div style="font-size:1rem;font-weight:700;color:#a8bcd8;margin-bottom:.5rem;">No sessions loaded</div>
      <div style="font-size:.85rem;color:#374560;max-width:460px;margin:0 auto;line-height:1.7;">
        Upload TXT files above or fetch from the device API.
        Each file becomes its own section — configure time window,
        view charts, download CSVs. Merged download appears at the bottom.
      </div>
    </div>""", unsafe_allow_html=True)
else:
    n = len(file_list)
    st.markdown(f"""
    <div class="sh">
      <div class="sh-num" style="background:#3b82f6;">2</div>
      <div class="sh-lbl">Configure &amp; Export</div>
      <div class="sh-line"></div>
      <span class="sh-cnt">{n} session{"s" if n!=1 else ""}</span>
    </div>""", unsafe_allow_html=True)

    all_dfs_57 = []
    all_dfs_19 = []
    merge_rows = []

    for file in file_list:
        fname   = file["name"]
        src     = file["source"]
        meta    = file.get("meta")
        is_api  = src == "api"
        icon    = "📡" if is_api else "📄"

        # ── Panel open ────────────────────────────────────────────
        st.markdown(f"""
        <div class="sp">
          <div class="sp-head">
            <div class="sp-icon {'a' if is_api else 'u'}">{icon}</div>
            <div class="sp-name">{fname}</div>
            <span class="chip {'chip-t' if is_api else 'chip-b'}">{'API' if is_api else 'File'}</span>
          </div>
          <div class="sp-body">
        """, unsafe_allow_html=True)

        # ── Remove (API only) ─────────────────────────────────────
        if is_api:
            _, rb = st.columns([5, 1])
            with rb:
                st.markdown('<div class="btn-sm">', unsafe_allow_html=True)
                if st.button("Remove", key=f"rm_{fname}"):
                    st.session_state.api_sessions = [
                        s for s in st.session_state.api_sessions if s["name"] != fname]
                    gc.collect(); st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

        # ── Device info ───────────────────────────────────────────
        if meta:
            st.markdown('<div class="rl">Device Information</div>', unsafe_allow_html=True)

            def _cell(k, v, extra_cls=""):
                val_cls = f"iv {extra_cls}".strip()
                missing_cls = "miss" if v == "—" else ""
                display_cls = missing_cls if missing_cls else val_cls
                return f'<div class="ic"><div class="ik">{k}</div><div class="{display_cls}">{v}</div></div>'

            st.markdown(f"""
            <div class="ig">
              {_cell("Device Name",     meta["device_name"],   "hi")}
              {_cell("Sampling Rate",   meta["sampling_rate"])}
              {_cell("Duration",        meta["duration"])}
              {_cell("Records in File", f"{meta['records']:,}", "hi")}
              {_cell("Expected Records",meta["expected_rec"])}
              {_cell("Records / Hour",  meta["rec_per_hour"])}
              {_cell("Completeness",    meta["completeness"])}
              {_cell("Session Start",   meta["t_start"],       "sm")}
              {_cell("Session End",     meta["t_end"],         "sm")}
              {_cell("File Size",       f"{meta['size_kb']} KB")}
              {_cell("Fetched",         f"{meta['fetched_date']} {meta['fetched_at']}", "sm")}
            </div>
            """, unsafe_allow_html=True)

            # If device name is still missing — tell user which keys came from API
            if meta["device_name"] == "—":
                keys_found = meta.get("_payload_keys", [])
                keys_str   = ", ".join(f"<code>{k}</code>" for k in keys_found[:20]) or "none"
                st.markdown(f'<div class="ax warn">⚠️ Could not find device name. API payload keys received: {keys_str}. Enable the debug panel (sidebar) to see full payload and tell me the correct key name.</div>', unsafe_allow_html=True)

        # ── TXT preview ───────────────────────────────────────────
        st.markdown('<div class="rl">Raw Data Preview</div>', unsafe_allow_html=True)
        prev = file["txt"][:1000] + ("\n…[truncated]" if len(file["txt"]) > 1000 else "")
        st.markdown(f'<div class="txp">{hl_txt(prev)}</div>', unsafe_allow_html=True)

        # ── Label ─────────────────────────────────────────────────
        st.markdown('<div class="rl">Label Configuration</div>', unsafe_allow_html=True)
        lc1, lc2 = st.columns([1, 2])
        with lc1: use_label = st.checkbox("Attach fault label", key=f"chk_{fname}")
        with lc2:
            label_value = None
            if use_label:
                label_value = LABEL_MAP[st.selectbox(
                    "Type", list(LABEL_MAP.keys()), key=f"lbl_{fname}", label_visibility="collapsed")]

        # ── Parse (cached) ────────────────────────────────────────
        with st.spinner("Parsing…"):
            df_base = cached_parse_57(file["txt"])

        if df_base.empty:
            st.markdown('<div class="ax err">❌ No records found. Check the file format.</div>', unsafe_allow_html=True)
            st.markdown('</div></div>', unsafe_allow_html=True); continue

        # ── Time window ───────────────────────────────────────────
        st.markdown('<div class="rl">Time Window Selection</div>', unsafe_allow_html=True)

        # FIX: always copy before adding column (avoids SettingWithCopyWarning / crash)
        df_57 = df_base.copy()
        df_57["Time_dt"] = pd.to_datetime(df_57["Time"], format="%d/%m/%Y %H:%M:%S")

        time_list = df_57["Time_dt"].tolist()
        tmin = df_57["Time_dt"].min().to_pydatetime()
        tmax = df_57["Time_dt"].max().to_pydatetime()
        N    = len(time_list)

        method = st.radio("Method", ["⚡ Quick Slider", "🎯 Precise Time Input"],
                          horizontal=True, key=f"tw_{fname}", label_visibility="collapsed")

        if method == "⚡ Quick Slider":
            cs, cm = st.columns([4, 1])
            with cs:
                si, ei = st.slider("Range", 0, N-1, (0, N-1),
                                   key=f"sl_{fname}", label_visibility="collapsed")
                start = time_list[si]; end = time_list[ei]
                st.caption(f"From  {start.strftime('%d/%m/%Y %H:%M:%S')}   →   {end.strftime('%d/%m/%Y %H:%M:%S')}")
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
                st.markdown('<div class="ax err">⚠️ Start must be before End.</div>', unsafe_allow_html=True)
                start, end = tmin, tmax

        # Apply filter — always copy
        df_57 = df_57[(df_57["Time_dt"] >= start) & (df_57["Time_dt"] <= end)].copy()
        df_57 = df_57.drop(columns="Time_dt").reset_index(drop=True)

        if use_label:
            df_57 = df_57.copy()
            df_57["Label"] = label_value

        if df_57.empty:
            st.markdown('<div class="ax warn">⚠️ No records in selected window.</div>', unsafe_allow_html=True)
            st.markdown('</div></div>', unsafe_allow_html=True); continue

        cache_key = f"{fname}|{len(df_57)}|{use_label}|{label_value}"
        df_19 = cached_to19(cache_key, df_57)

        # ── Charts ────────────────────────────────────────────────
        st.markdown('<div class="rl">Feature Visualization</div>', unsafe_allow_html=True)
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
        plt.close("all")

        # ── Tables ───────────────────────────────────────────────
        st.markdown('<div class="rl">57-Feature Table</div>', unsafe_allow_html=True)
        st.dataframe(df_57, height=260, use_container_width=True)
        st.markdown('<div class="rl">19-Feature Table</div>', unsafe_allow_html=True)
        st.markdown('<div class="ax info">ℹ️ Each record expands to 3 rows (X, Y, Z axis). Same timestamp, axis-specific parameters.</div>', unsafe_allow_html=True)
        st.dataframe(df_19, height=260, use_container_width=True)

        # ── Downloads ─────────────────────────────────────────────
        st.markdown('<div class="rl">Download</div>', unsafe_allow_html=True)
        pfx   = file_prefix.strip() if file_prefix.strip() else re.sub(r'[^\w\-.]','_', fname.replace(".txt",""))[:35]
        clean = re.sub(r'[^\w\-.]','_', fname)[:22]
        f57n  = f"{pfx}_{clean}_57feat.csv" if file_prefix.strip() else f"{clean}_57feat.csv"
        f19n  = f"{pfx}_{clean}_19feat.csv" if file_prefix.strip() else f"{clean}_19feat.csv"

        st.markdown(f'<div class="ax ok">✅ Ready — <strong>{len(df_57):,} records</strong> · {len(df_57.columns)} cols (57-feat) · {len(df_19):,} rows (19-feat)</div>', unsafe_allow_html=True)

        dc1, dc2 = st.columns(2)
        with dc1:
            st.download_button("📥  Download 57-Feature CSV",
                               df_57.to_csv(index=False), f57n, "text/csv",
                               key=f"dl57_{fname}", use_container_width=True)
            st.caption(f"{f57n}  ·  {len(df_57):,} rows  ·  {len(df_57.columns)} cols")
        with dc2:
            st.markdown('<div class="dl-teal">', unsafe_allow_html=True)
            st.download_button("📥  Download 19-Feature CSV",
                               df_19.to_csv(index=False), f19n, "text/csv",
                               key=f"dl19_{fname}", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            st.caption(f"{f19n}  ·  {len(df_19):,} rows  ·  20 cols")

        st.markdown('</div></div>', unsafe_allow_html=True)  # close sp-body + sp

        all_dfs_57.append(df_57); all_dfs_19.append(df_19)
        lbl_str = next((k for k,v in LABEL_MAP.items() if v==label_value), "—") if use_label else "None"
        merge_rows.append({"name": fname, "src": "API" if is_api else "File",
                           "records": len(df_57), "label": lbl_str})

    # ════════════════════════════════════════════════════════════
    #  STEP 3 — MERGED DOWNLOAD
    # ════════════════════════════════════════════════════════════
    if all_dfs_57:
        merged_57 = pd.concat(all_dfs_57, ignore_index=True)
        merged_19 = pd.concat(all_dfs_19, ignore_index=True)
        pfx_m = (file_prefix.strip() + "_") if file_prefix.strip() else ""
        mf57  = f"{pfx_m}Merged_57feat.csv"
        mf19  = f"{pfx_m}Merged_19feat.csv"

        st.markdown("""
        <div class="sh">
          <div class="sh-num" style="background:#10b981;">3</div>
          <div class="sh-lbl">Merged Dataset</div>
          <div class="sh-line"></div>
        </div>""", unsafe_allow_html=True)

        rows_html = "".join(
            f'<tr><td>{"📡" if m["src"]=="API" else "📄"} {m["name"][:46]}</td>'
            f'<td>{m["records"]:,}</td><td>{m["label"]}</td></tr>'
            for m in merge_rows
        )
        st.markdown(f"""
        <div class="merge-wrap">
          <div class="merge-title">🗂 Merged Dataset Download</div>
          <div class="merge-sub">All sessions combined — only your filtered time-window records are included from each session.</div>
          <table class="mtbl">
            <thead><tr><th>Session</th><th>Records (filtered)</th><th>Label</th></tr></thead>
            <tbody>{rows_html}</tbody>
          </table>
        </div>""", unsafe_allow_html=True)

        mc1,mc2,mc3,mc4 = st.columns(4)
        with mc1: st.metric("Sessions", len(all_dfs_57))
        with mc2: st.metric("57-feat Rows", f"{len(merged_57):,}")
        with mc3: st.metric("19-feat Rows", f"{len(merged_19):,}")
        with mc4: st.metric("Columns", len(merged_57.columns))

        st.markdown(f'<div class="ax info" style="margin:.9rem 0;">📋 <strong>{mf57}</strong> and <strong>{mf19}</strong></div>', unsafe_allow_html=True)

        dl1, dl2 = st.columns(2)
        with dl1:
            st.markdown('<div class="mdb b"><div class="mdb-t">57-Feature Merged CSV</div><div class="mdb-s">Time + Parameter-1..19 × X, Y, Z</div></div>', unsafe_allow_html=True)
            st.markdown('<div class="dl-mb">', unsafe_allow_html=True)
            st.download_button(f"📥  Download {mf57}", merged_57.to_csv(index=False),
                               mf57, "text/csv", key="dl_m57", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with dl2:
            st.markdown('<div class="mdb t"><div class="mdb-t">19-Feature Merged CSV</div><div class="mdb-s">Time + Parameter-1..19, axes stacked</div></div>', unsafe_allow_html=True)
            st.markdown('<div class="dl-mt">', unsafe_allow_html=True)
            st.download_button(f"📥  Download {mf19}", merged_19.to_csv(index=False),
                               mf19, "text/csv", key="dl_m19", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
#  FOOTER
# ════════════════════════════════════════════════════════════════
st.markdown('<div class="pg-footer">Vibration Data Converter · pump_project · v5.0</div>', unsafe_allow_html=True)
