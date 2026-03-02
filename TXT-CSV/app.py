import streamlit as st
import pandas as pd
import re, time, requests
from datetime import datetime
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="VibroConvert",
    page_icon="〰",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Outfit:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Variables ── */
:root {
    --bg:         #05080f;
    --bg1:        #090e19;
    --bg2:        #0d1525;
    --bg3:        #111d35;
    --border:     #162040;
    --border2:    #1e2f52;
    --cyan:       #22d3ee;
    --cyan-dim:   rgba(34,211,238,.08);
    --cyan-glow:  rgba(34,211,238,.18);
    --violet:     #a78bfa;
    --violet-dim: rgba(167,139,250,.08);
    --green:      #34d399;
    --amber:      #fbbf24;
    --red:        #f87171;
    --tx1:        #e2eeff;
    --tx2:        #7a9cc8;
    --tx3:        #304468;
    --syne:       'Syne', sans-serif;
    --out:        'Outfit', sans-serif;
    --mono:       'JetBrains Mono', monospace;
}

/* ── Base ── */
html,body,[class*="css"]{ font-family:var(--out); }
.stApp{
    background:var(--bg);
    background-image:
        radial-gradient(ellipse 60% 30% at 20% 0%,rgba(34,211,238,.05) 0%,transparent 60%),
        radial-gradient(ellipse 40% 20% at 80% 100%,rgba(167,139,250,.05) 0%,transparent 60%);
    min-height:100vh;
}
.block-container{ padding:1.8rem 2rem 4rem; max-width:1440px; }
#MainMenu,footer,header{ visibility:hidden; }
::-webkit-scrollbar{ width:4px; height:4px; }
::-webkit-scrollbar-track{ background:var(--bg1); }
::-webkit-scrollbar-thumb{ background:var(--border2); border-radius:2px; }
::-webkit-scrollbar-thumb:hover{ background:var(--cyan); }

/* ── Sidebar ── */
[data-testid="stSidebar"]{ background:var(--bg1) !important; border-right:1px solid var(--border) !important; }
[data-testid="stSidebar"] .block-container{ padding:1.2rem 0.9rem; }
[data-testid="stSidebar"] label{ color:var(--tx2) !important; font-family:var(--out) !important; font-size:0.78rem !important; }
[data-testid="stSidebar"] .stTextInput>div>div>input{
    background:var(--bg2) !important; border:1px solid var(--border2) !important;
    color:var(--tx1) !important; border-radius:7px !important;
    font-family:var(--mono) !important; font-size:0.8rem !important;
}
[data-testid="stSidebar"] .stTextInput>div>div>input:focus{
    border-color:var(--cyan) !important; box-shadow:0 0 0 2px var(--cyan-dim) !important;
}

/* ── Top header bar ── */
.topbar{
    display:flex; align-items:center; justify-content:space-between;
    padding-bottom:1.2rem; border-bottom:1px solid var(--border);
    margin-bottom:1.8rem;
}
.logo-wrap{ display:flex; align-items:center; gap:0.75rem; }
.logo-icon{
    width:36px; height:36px;
    background:linear-gradient(135deg,var(--cyan),#0891b2);
    border-radius:9px; display:flex; align-items:center;
    justify-content:center; font-size:1.1rem; flex-shrink:0;
    box-shadow:0 0 16px var(--cyan-glow);
}
.logo-name{ font-family:var(--syne); font-size:1.45rem; font-weight:800; color:var(--tx1); letter-spacing:-.02em; line-height:1; }
.logo-tag{ font-family:var(--mono); font-size:0.55rem; color:var(--tx3); letter-spacing:.15em; text-transform:uppercase; margin-top:1px; }
.topbar-right{ display:flex; align-items:center; gap:0.8rem; }

/* ── Status chip ── */
.chip{
    display:inline-flex; align-items:center; gap:0.35rem;
    padding:0.28rem 0.8rem; border-radius:100px;
    font-family:var(--mono); font-size:0.6rem; letter-spacing:.12em; text-transform:uppercase;
}
.chip.idle{ background:var(--bg2); border:1px solid var(--border2); color:var(--tx3); }
.chip.active{ background:var(--cyan-dim); border:1px solid rgba(34,211,238,.25); color:var(--cyan); }
.chip.done{ background:rgba(52,211,153,.08); border:1px solid rgba(52,211,153,.25); color:var(--green); }
.chip-dot{ width:5px; height:5px; border-radius:50%; background:currentColor; animation:blink 2s ease-in-out infinite; }
@keyframes blink{ 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:.3;transform:scale(.6)} }

/* ── Input row (top action bar) ── */
.input-strip{
    display:grid; grid-template-columns:1fr 1fr; gap:1px;
    background:var(--border); border-radius:14px; overflow:hidden;
    border:1px solid var(--border); margin-bottom:1.5rem;
}
.input-panel{
    background:var(--bg1); padding:1.2rem 1.4rem; position:relative;
}
.input-panel::after{
    content:''; position:absolute; top:0; left:0; right:0; height:2px;
}
.input-panel.upload::after{ background:linear-gradient(90deg,transparent,var(--cyan),transparent); }
.input-panel.fetch::after{ background:linear-gradient(90deg,transparent,var(--violet),transparent); }
.panel-title{
    font-family:var(--syne); font-size:0.8rem; font-weight:700;
    letter-spacing:.06em; text-transform:uppercase; margin-bottom:0.6rem;
    display:flex; align-items:center; gap:0.4rem;
}
.panel-title.cyan{ color:var(--cyan); }
.panel-title.violet{ color:var(--violet); }
.endpoint-tag{
    font-family:var(--mono); font-size:0.7rem; color:var(--violet);
    background:var(--violet-dim); border:1px solid rgba(167,139,250,.2);
    border-radius:5px; padding:0.28rem 0.6rem; margin-bottom:0.7rem;
    display:inline-block; word-break:break-all;
}

/* ── Section divider ── */
.sec{
    font-family:var(--mono); font-size:0.58rem; letter-spacing:.2em; text-transform:uppercase;
    color:var(--tx3); display:flex; align-items:center; gap:0.6rem; margin:1.8rem 0 0.9rem;
}
.sec::before{ content:''; width:14px; height:1px; background:var(--cyan); }
.sec::after{ content:''; flex:1; height:1px; background:var(--border); }

/* ── Session card ── */
.sess-card{
    background:var(--bg1); border:1px solid var(--border);
    border-radius:12px; overflow:hidden; margin-bottom:1rem;
    transition:border-color .2s;
}
.sess-card:hover{ border-color:var(--border2); }
.sess-header{
    display:flex; align-items:center; gap:0.8rem;
    padding:0.75rem 1rem; border-bottom:1px solid var(--border);
    background:var(--bg2);
}
.sess-icon{ font-size:1rem; flex-shrink:0; }
.sess-name{ font-family:var(--syne); font-size:0.88rem; font-weight:700; color:var(--tx1); flex:1; min-width:0; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.sess-badges{ display:flex; gap:0.4rem; flex-shrink:0; }
.badge{
    font-family:var(--mono); font-size:0.58rem; letter-spacing:.08em; text-transform:uppercase;
    padding:0.18rem 0.5rem; border-radius:4px;
}
.badge.upload{ background:var(--cyan-dim); color:var(--cyan); border:1px solid rgba(34,211,238,.2); }
.badge.api{ background:var(--violet-dim); color:var(--violet); border:1px solid rgba(167,139,250,.2); }
.badge.converted{ background:rgba(52,211,153,.08); color:var(--green); border:1px solid rgba(52,211,153,.2); }
.sess-body{ padding:0.9rem 1rem; }

/* ── Meta grid ── */
.meta-grid{ display:grid; grid-template-columns:repeat(auto-fill,minmax(130px,1fr)); gap:0.5rem; margin-bottom:0.8rem; }
.meta-item{ background:var(--bg2); border:1px solid var(--border); border-radius:8px; padding:0.55rem 0.75rem; }
.meta-key{ font-family:var(--mono); font-size:0.55rem; letter-spacing:.1em; text-transform:uppercase; color:var(--tx3); margin-bottom:0.15rem; }
.meta-val{ font-family:var(--mono); font-size:0.8rem; color:var(--tx1); font-weight:500; }
.meta-val.hi{ color:var(--cyan); }

/* ── TXT preview ── */
.pre-box{
    background:#030608; border:1px solid var(--border2); border-radius:8px;
    padding:0.8rem 1rem; font-family:var(--mono); font-size:0.7rem;
    color:#3a6b4e; max-height:160px; overflow-y:auto; line-height:1.65;
    white-space:pre; margin-bottom:0.8rem;
}
.pre-box::-webkit-scrollbar{width:3px;}
.pre-box::-webkit-scrollbar-thumb{background:var(--cyan);border-radius:2px;}

/* ── Stat pills ── */
.pills{ display:flex; gap:0.5rem; flex-wrap:wrap; margin:0.5rem 0; }
.pill{ background:var(--bg3); border:1px solid var(--border2); border-radius:8px; padding:0.5rem 0.75rem; min-width:70px; }
.pill-v{ font-family:var(--mono); font-size:0.95rem; color:var(--cyan); font-weight:500; line-height:1.1; }
.pill-k{ font-size:0.58rem; color:var(--tx3); letter-spacing:.06em; text-transform:uppercase; margin-top:0.15rem; }

/* ── Download group ── */
.dl-group{
    display:grid; grid-template-columns:1fr 1fr; gap:0.5rem; margin-top:0.5rem;
}
.dl-group.single{ grid-template-columns:1fr 1fr 1fr 1fr; }

/* ── Merge section ── */
.merge-zone{
    background:linear-gradient(135deg,rgba(34,211,238,.04),rgba(167,139,250,.04));
    border:1px solid var(--border2); border-radius:14px; padding:1.4rem;
    margin-top:1.5rem; position:relative; overflow:hidden;
}
.merge-zone::before{
    content:''; position:absolute; top:0; left:0; right:0; height:2px;
    background:linear-gradient(90deg,var(--cyan),var(--violet));
}
.merge-title{ font-family:var(--syne); font-size:1.05rem; font-weight:700; color:var(--tx1); margin-bottom:0.3rem; }
.merge-sub{ font-family:var(--out); font-size:0.8rem; color:var(--tx2); margin-bottom:0.9rem; }

/* ── Result banner ── */
.res-banner{
    background:var(--bg2); border:1px solid var(--border2); border-radius:12px;
    padding:1.2rem 1.4rem; display:flex; align-items:center; gap:1.5rem;
    flex-wrap:wrap; margin-bottom:1rem;
}
.res-title{ font-family:var(--syne); font-size:1.1rem; font-weight:700; color:var(--tx1); margin:0; }
.res-meta{ font-family:var(--mono); font-size:0.65rem; color:var(--tx3); margin:0.15rem 0 0; }
.res-nums{ display:flex; gap:1.2rem; margin-left:auto; }
.res-num{ text-align:center; }
.res-num-v{ font-family:var(--syne); font-size:1.5rem; font-weight:800; color:var(--cyan); line-height:1; }
.res-num-k{ font-family:var(--mono); font-size:0.55rem; color:var(--tx3); letter-spacing:.1em; text-transform:uppercase; margin-top:0.1rem; }

/* ── Alerts ── */
.ax{ border-radius:8px; padding:0.7rem 1rem; font-family:var(--out); font-size:0.83rem; margin:0.4rem 0; }
.ax.ok  { background:rgba(52,211,153,.07); border:1px solid rgba(52,211,153,.25); color:var(--green); }
.ax.err { background:rgba(248,113,113,.07); border:1px solid rgba(248,113,113,.25); color:var(--red); }
.ax.warn{ background:rgba(251,191,36,.07);  border:1px solid rgba(251,191,36,.25);  color:var(--amber); }
.ax.info{ background:var(--violet-dim);     border:1px solid rgba(167,139,250,.25); color:var(--violet); }

/* ── Streamlit overrides ── */
.stButton>button{
    background:linear-gradient(135deg,#0e7490,var(--cyan)) !important;
    color:#020c14 !important; font-family:var(--syne) !important; font-weight:700 !important;
    font-size:0.83rem !important; border:none !important; border-radius:8px !important;
    padding:0.6rem 1.3rem !important; letter-spacing:.03em !important;
    transition:all .18s !important; box-shadow:0 3px 12px var(--cyan-glow) !important;
}
.stButton>button:hover{ filter:brightness(1.15) !important; box-shadow:0 5px 20px var(--cyan-glow) !important; transform:translateY(-1px) !important; }
.stButton>button:active{ transform:translateY(0) !important; }
.btn-violet>button{ background:linear-gradient(135deg,#6d28d9,var(--violet)) !important; box-shadow:0 3px 12px rgba(167,139,250,.2) !important; color:#fff !important; }
.btn-violet>button:hover{ box-shadow:0 5px 20px rgba(167,139,250,.35) !important; }
.btn-ghost>button{ background:transparent !important; color:var(--tx2) !important; border:1px solid var(--border2) !important; box-shadow:none !important; }
.btn-ghost>button:hover{ border-color:var(--cyan) !important; color:var(--cyan) !important; background:var(--cyan-dim) !important; box-shadow:none !important; }
.btn-red>button{ background:transparent !important; color:var(--red) !important; border:1px solid rgba(248,113,113,.25) !important; box-shadow:none !important; font-size:0.75rem !important; padding:0.4rem 0.8rem !important; }
.btn-red>button:hover{ background:rgba(248,113,113,.07) !important; border-color:var(--red) !important; box-shadow:none !important; }
.btn-green>button{ background:linear-gradient(135deg,#065f46,var(--green)) !important; box-shadow:0 3px 12px rgba(52,211,153,.18) !important; color:#020c14 !important; }
.stDownloadButton>button{
    background:var(--bg3) !important; color:var(--cyan) !important;
    border:1px solid rgba(34,211,238,.25) !important; border-radius:8px !important;
    font-family:var(--out) !important; font-weight:600 !important; font-size:0.8rem !important;
    padding:0.55rem 1rem !important; width:100% !important; box-shadow:none !important; transition:all .18s !important;
}
.stDownloadButton>button:hover{ background:var(--cyan-dim) !important; border-color:var(--cyan) !important; box-shadow:0 3px 12px var(--cyan-glow) !important; transform:translateY(-1px) !important; }
.dl-violet .stDownloadButton>button{ color:var(--violet) !important; border-color:rgba(167,139,250,.25) !important; }
.dl-violet .stDownloadButton>button:hover{ background:var(--violet-dim) !important; border-color:var(--violet) !important; box-shadow:0 3px 12px rgba(167,139,250,.2) !important; }
.dl-green .stDownloadButton>button{ color:var(--green) !important; border-color:rgba(52,211,153,.25) !important; }
.dl-green .stDownloadButton>button:hover{ background:rgba(52,211,153,.07) !important; border-color:var(--green) !important; }
.stSlider>div>div>div>div{ background:var(--cyan) !important; }
.stSlider>div>div>div{ background:var(--border2) !important; height:3px !important; }
[data-testid="metric-container"]{background:var(--bg2) !important;border:1px solid var(--border) !important;border-radius:8px !important;padding:0.7rem 0.9rem !important;}
[data-testid="metric-container"] label{color:var(--tx3) !important;font-family:var(--mono) !important;font-size:0.58rem !important;letter-spacing:.1em !important;}
[data-testid="metric-container"] [data-testid="stMetricValue"]{color:var(--tx1) !important;font-family:var(--mono) !important;font-size:1.1rem !important;}
.stDataFrame{border-radius:10px;overflow:hidden;}
.stCheckbox label{color:var(--tx2) !important;font-family:var(--out) !important;font-size:0.84rem !important;}
.stSelectbox>div>div{background:var(--bg2) !important;border:1px solid var(--border2) !important;border-radius:7px !important;color:var(--tx1) !important;font-family:var(--mono) !important;font-size:0.8rem !important;}
.stSelectbox label{color:var(--tx2) !important;font-family:var(--mono) !important;font-size:0.62rem !important;letter-spacing:.08em !important;text-transform:uppercase !important;}
.stRadio>div{flex-direction:row !important;gap:0.4rem !important;flex-wrap:wrap;}
.stRadio>div>label{background:var(--bg2) !important;border:1px solid var(--border2) !important;border-radius:7px !important;padding:0.5rem 1rem !important;color:var(--tx2) !important;font-family:var(--out) !important;font-size:0.82rem !important;font-weight:500 !important;cursor:pointer !important;transition:all .15s !important;}
.stRadio>div>label:hover{border-color:var(--cyan) !important;color:var(--tx1) !important;background:var(--cyan-dim) !important;}
.streamlit-expanderHeader{background:var(--bg2) !important;border:1px solid var(--border) !important;border-radius:8px !important;color:var(--tx2) !important;font-family:var(--out) !important;font-size:0.83rem !important;}
.streamlit-expanderContent{background:var(--bg2) !important;border:1px solid var(--border) !important;border-top:none !important;border-radius:0 0 8px 8px !important;padding:0.8rem !important;}
.stProgress>div>div>div>div{background:var(--cyan) !important;}
.stProgress>div>div>div{background:var(--border2) !important;height:3px !important;border-radius:100px !important;}
.stCaption{color:var(--tx3) !important;font-family:var(--mono) !important;font-size:0.67rem !important;}
hr{border:none;height:1px;background:linear-gradient(90deg,transparent,var(--border2),transparent);margin:1.5rem 0;}
.app-footer{text-align:center;padding:2.5rem 0 1rem;font-family:var(--mono);font-size:0.55rem;letter-spacing:.14em;color:var(--tx3);text-transform:uppercase;}
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE ─────────────────────────────────────────────────────────────
DEFAULTS = {
    "sessions":       [],     # list of session dicts
    "fetch_msg":      None,
    "fetch_msg_type": None,
    "last_upload_sig":None,
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── CONFIG ────────────────────────────────────────────────────────────────────
API_BASE = "https://pumpdata.duckdns.org/api"
LABEL_MAP = {
    "None":                 None,
    "Normal_Mode(0)":       0,
    "Seal Failure(1)":      1,
    "Bearing(2)":           2,
    "Shaft Misalignment(3)":3,
    "Unbalance_impeller(4)":4,
    "Cavitation(5)":        5,
}

# ── PARSE / CONVERT FUNCTIONS ─────────────────────────────────────────────────
def normalize_time(t):
    return datetime.strptime(t.strip(), "%m/%d/%Y %I:%M:%S %p").strftime("%d/%m/%Y %H:%M:%S")

def parse_vibration(txt):
    rows=[]; lines=[l.strip() for l in txt.splitlines() if l.strip()]; i=0
    tre=re.compile(r"\d+/\d+/\d+\s+\d+:\d+:\d+\s+(AM|PM)")
    pnr=re.compile(r"Peak\s+(\d+)\s+Parameter-\d+\s+([-\d.]+)\s+Parameter-\d+\s+([-\d.]+)")
    por=re.compile(r"Peak\s+(\d+)\s+Freq\s+([-\d.]+)\s+Mag\s+([-\d.]+)")
    def tf(tok,idx):
        try: return float(tok[idx])
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
                        if pn==1: row[f"Parameter-1_{ax}"]=val
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

def convert_session(sess_idx):
    sess = st.session_state.sessions[sess_idx]
    t0 = time.time()
    try:
        df_raw = parse_vibration(sess["txt"])
    except Exception as e:
        return False, str(e)
    if df_raw.empty:
        return False, "No records found — check file format."
    df57 = reorder57(df_raw.copy())
    lv = sess.get("label")
    if lv is not None: df57["Label"] = lv
    df19 = to19(df57)
    st.session_state.sessions[sess_idx]["df57"] = df57
    st.session_state.sessions[sess_idx]["df19"] = df19
    st.session_state.sessions[sess_idx]["converted"] = True
    st.session_state.sessions[sess_idx]["conv_time"] = round(time.time()-t0, 2)
    return True, None

def extract_meta(content, payload=None):
    tre = re.compile(r"(\d+/\d+/\d+)\s+(\d+:\d+:\d+)\s+(AM|PM)")
    ts  = tre.findall(content)
    t_s = f"{ts[0][0]} {ts[0][1]} {ts[0][2]}"  if ts else "—"
    t_e = f"{ts[-1][0]} {ts[-1][1]} {ts[-1][2]}" if ts else "—"
    rec = content.count("#Vibration Value")
    sz  = round(len(content)/1024, 1)

    # Sample rate
    sr = "—"
    if payload: sr = payload.get("sampling_rate") or payload.get("sample_rate") or payload.get("interval") or "—"
    if sr == "—" and len(ts) >= 2:
        try:
            fmt="%m/%d/%Y %I:%M:%S %p"
            t1=datetime.strptime(f"{ts[0][0]} {ts[0][1]} {ts[0][2]}",fmt)
            t2=datetime.strptime(f"{ts[1][0]} {ts[1][1]} {ts[1][2]}",fmt)
            d=int((t2-t1).total_seconds())
            if d>0: sr=f"{d}s"
        except: pass

    # Duration
    dur = "—"
    if payload:
        dur = (payload.get("duration") or payload.get("duration_hours")
               or payload.get("hours") or payload.get("duration_min") or "—")
        if dur != "—":
            try:
                dv = float(str(dur))
                dur = f"{dv:.0f}h" if dv == int(dv) else f"{dv}h"
            except: dur = str(dur)
    if dur == "—" and len(ts) >= 2:
        try:
            fmt="%m/%d/%Y %I:%M:%S %p"
            t1=datetime.strptime(f"{ts[0][0]}  {ts[0][1]} {ts[0][2]}",fmt)
            te=datetime.strptime(f"{ts[-1][0]} {ts[-1][1]} {ts[-1][2]}",fmt)
            secs=int((te-t1).total_seconds())
            if secs>0:
                h=secs//3600; m=(secs%3600)//60
                dur=f"{h}h {m}m" if h else f"{m}m"
        except: pass

    # Device name — try every possible key
    dn = "—"
    if payload:
        for key in ["device_name","deviceName","device_id","deviceId","name","id","device","sensor_id","sensorId","sensor_name"]:
            val = payload.get(key)
            if val and str(val).strip() and str(val).strip().lower() not in ("none","null","","unknown"):
                dn = str(val).strip(); break

    return {"device_name":dn,"sampling_rate":sr,"duration":dur,"records":rec,
            "t_start":t_s,"t_end":t_e,"size_kb":sz,"fetched_at":datetime.now().strftime("%H:%M:%S")}

def make_plot(df, cols, title, pal):
    ps={'c':['#22d3ee','#0891b2','#164e63'],'v':['#a78bfa','#7c3aed','#4c1d95'],'g':['#34d399','#059669','#064e3b']}
    cl=ps.get(pal,ps['c'])
    fig,ax=plt.subplots(figsize=(5,2.8),facecolor='#090e19')
    ax.set_facecolor('#05080f')
    for idx,c in enumerate(cols):
        if c in df.columns:
            ax.plot(df[c].values,label=c.split('_')[-1] if '_' in c else c,
                    linewidth=1.6,alpha=0.9,color=cl[idx%len(cl)])
    ax.set_title(title,fontsize=9,color='#7a9cc8',pad=8)
    ax.set_xlabel('Sample',fontsize=7,color='#304468')
    ax.legend(fontsize=6,framealpha=0,labelcolor='#7a9cc8',loc='best')
    ax.grid(True,alpha=0.08,linestyle='--',linewidth=0.4,color='#162040')
    for sp in ax.spines.values(): sp.set_color('#162040')
    ax.tick_params(labelsize=6,colors='#304468')
    fig.tight_layout(pad=1)
    return fig

def hl_txt(raw):
    lines=[]
    for line in raw.splitlines():
        ls=line.strip()
        if re.match(r"\d+/\d+/\d+\s+\d+:\d+:\d+",ls):
            lines.append(f'<span style="color:#38bdf8;font-weight:500;">{line}</span>')
        elif "Axis:" in ls:
            lines.append(f'<span style="color:#22d3ee;">{line}</span>')
        elif ls.startswith("Peak"):
            lines.append(f'<span style="color:#a78bfa;">{line}</span>')
        elif ls.startswith("#"):
            lines.append(f'<span style="color:#304468;">{line}</span>')
        else:
            lines.append(f'<span style="color:#3a6b4e;">{line}</span>')
    return "<br>".join(lines)

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:0.5rem 0 1.2rem;border-bottom:1px solid var(--border);margin-bottom:1.2rem;">
        <div style="font-family:var(--syne);font-size:1rem;font-weight:800;color:var(--tx1);">⚙ Settings</div>
    </div>
    """, unsafe_allow_html=True)
    file_prefix = st.text_input("Output file prefix", placeholder="e.g. pump_run_01", key="file_prefix_input")
    st.markdown("---")
    st.markdown('<div class="btn-red">', unsafe_allow_html=True)
    if st.button("🗑  Clear All Sessions", use_container_width=True, key="clr_all"):
        st.session_state.sessions = []
        st.session_state.last_upload_sig = None
        st.session_state.fetch_msg = None
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    if st.session_state.sessions:
        st.markdown("---")
        st.markdown('<div style="font-family:var(--mono);font-size:0.58rem;color:var(--tx3);letter-spacing:.15em;text-transform:uppercase;margin-bottom:0.6rem;">Active Sessions</div>', unsafe_allow_html=True)
        for sess in st.session_state.sessions:
            icon = "📡" if sess["source"]=="api" else "📄"
            conv = "✓ " if sess.get("converted") else ""
            st.markdown(f'<div style="font-family:var(--mono);font-size:0.72rem;color:{"var(--green)" if sess.get("converted") else "var(--tx2)"};padding:0.3rem 0;border-bottom:1px solid var(--border);">{icon} {conv}{sess["name"][:28]}</div>', unsafe_allow_html=True)

# ── TOP BAR ───────────────────────────────────────────────────────────────────
n_sess  = len(st.session_state.sessions)
n_conv  = sum(1 for s in st.session_state.sessions if s.get("converted"))
status  = "done" if (n_sess > 0 and n_conv == n_sess) else ("active" if n_sess > 0 else "idle")
stat_lbl = f"{n_conv}/{n_sess} converted" if n_sess > 0 else "No sessions"

st.markdown(f"""
<div class="topbar">
    <div class="logo-wrap">
        <div class="logo-icon">〰</div>
        <div>
            <div class="logo-name">VibroConvert</div>
            <div class="logo-tag">Vibration Analysis Pipeline · v3.1</div>
        </div>
    </div>
    <div class="topbar-right">
        <span class="chip {status}">
            <span class="chip-dot"></span>
            {stat_lbl}
        </span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── INPUT STRIP (always visible) ─────────────────────────────────────────────
st.markdown("""<div class="input-strip">""", unsafe_allow_html=True)

col_up, col_api = st.columns(2)

with col_up:
    st.markdown("""
    <div class="input-panel upload">
        <div class="panel-title cyan">📁 Upload TXT Files</div>
    </div>
    """, unsafe_allow_html=True)
    uploaded = st.file_uploader(
        "Drop files",
        type=["txt"], accept_multiple_files=True,
        key="fu", label_visibility="collapsed",
    )
    if uploaded:
        sig = str(sorted([(f.name, f.size) for f in uploaded]))
        if st.session_state.last_upload_sig != sig:
            st.session_state.last_upload_sig = sig
            added = 0
            for f in uploaded:
                existing = [s["name"] for s in st.session_state.sessions]
                if f.name not in existing:
                    content = f.read().decode("utf-8", errors="replace")
                    rec = content.count("#Vibration Value")
                    sz  = round(len(content)/1024, 1)
                    st.session_state.sessions.append({
                        "name": f.name, "source": "upload", "txt": content,
                        "label": None, "records": rec, "size_kb": sz,
                        "meta": None, "converted": False, "df57": None, "df19": None,
                    })
                    added += 1
            if added:
                st.rerun()

with col_api:
    st.markdown(f"""
    <div class="input-panel fetch">
        <div class="panel-title violet">📡 Fetch from Device API</div>
        <div class="endpoint-tag">GET {API_BASE}/latest</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="btn-violet">', unsafe_allow_html=True)
    fetch_btn = st.button("📡  Fetch Latest Session", use_container_width=True, key="fetch_btn")
    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.fetch_msg:
        css = {"success":"ok","error":"err","warning":"warn"}.get(st.session_state.fetch_msg_type,"info")
        st.markdown(f'<div class="ax {css}" style="margin-top:0.5rem;">{st.session_state.fetch_msg}</div>', unsafe_allow_html=True)

    if fetch_btn:
        with st.spinner("Connecting…"):
            try:
                resp = requests.get(f"{API_BASE}/latest", timeout=15)
                if resp.status_code == 200:
                    payload = resp.json()
                    content = payload.get("content","").strip()
                    if content:
                        meta = extract_meta(content, payload)
                        dn   = meta["device_name"]
                        sess_name = f"{dn} @ {meta['fetched_at']}" if dn != "—" else f"API Session @ {meta['fetched_at']}"
                        existing  = [s["name"] for s in st.session_state.sessions]
                        if sess_name not in existing:
                            st.session_state.sessions.append({
                                "name": sess_name, "source": "api", "txt": content,
                                "label": None, "records": meta["records"],
                                "size_kb": meta["size_kb"], "meta": meta,
                                "converted": False, "df57": None, "df19": None,
                            })
                            st.session_state.fetch_msg      = f"✅ Added: <strong>{sess_name}</strong> — {meta['records']:,} records"
                            st.session_state.fetch_msg_type = "success"
                        else:
                            st.session_state.fetch_msg      = f"ℹ Already in queue: {sess_name}"
                            st.session_state.fetch_msg_type = "warning"
                    else:
                        st.session_state.fetch_msg      = "ℹ No data yet — run the Device Simulator first."
                        st.session_state.fetch_msg_type = "warning"
                else:
                    st.session_state.fetch_msg      = f"⚠ HTTP {resp.status_code}"
                    st.session_state.fetch_msg_type = "error"
            except requests.exceptions.ConnectionError:
                st.session_state.fetch_msg      = f"🔌 Cannot reach {API_BASE}"
                st.session_state.fetch_msg_type = "error"
            except requests.exceptions.Timeout:
                st.session_state.fetch_msg      = "⏱ Timeout — retry"
                st.session_state.fetch_msg_type = "error"
            except Exception as e:
                st.session_state.fetch_msg      = f"❌ {e}"
                st.session_state.fetch_msg_type = "error"
        st.rerun()

st.markdown("</div>", unsafe_allow_html=True)

# ── PER-SESSION PROCESSING ────────────────────────────────────────────────────
if not st.session_state.sessions:
    st.markdown("""
    <div style="text-align:center;padding:4rem 2rem;">
        <div style="font-size:3rem;margin-bottom:1rem;opacity:0.3;">〰</div>
        <div style="font-family:var(--syne);font-size:1.2rem;font-weight:700;color:var(--tx2);margin-bottom:0.5rem;">No sessions yet</div>
        <div style="font-family:var(--out);font-size:0.83rem;color:var(--tx3);max-width:420px;margin:0 auto;">
            Upload TXT files or fetch from the device API above. Each file/fetch becomes an independent session
            you can process, label, and download separately — then merge all at the bottom.
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown('<div class="sec">Sessions</div>', unsafe_allow_html=True)

    to_remove = []

    for idx, sess in enumerate(st.session_state.sessions):
        src  = sess["source"]
        icon = "📡" if src=="api" else "📄"
        meta = sess.get("meta")
        conv = sess.get("converted", False)

        # ── Session card header ──────────────────────────────────
        badge_src  = f'<span class="badge {src}">{src.upper()}</span>'
        badge_conv = '<span class="badge converted">✓ Converted</span>' if conv else ""
        st.markdown(f"""
        <div class="sess-card">
            <div class="sess-header">
                <span class="sess-icon">{icon}</span>
                <span class="sess-name">{sess['name']}</span>
                <div class="sess-badges">{badge_src}{badge_conv}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Session card body (using expander) ───────────────────
        with st.expander("", expanded=not conv):
            # Meta info
            if meta:
                st.markdown(f"""
                <div class="meta-grid">
                    <div class="meta-item"><div class="meta-key">Device</div><div class="meta-val hi">{meta.get('device_name','—')}</div></div>
                    <div class="meta-item"><div class="meta-key">Sample Rate</div><div class="meta-val">{meta.get('sampling_rate','—')}</div></div>
                    <div class="meta-item"><div class="meta-key">Duration</div><div class="meta-val">{meta.get('duration','—')}</div></div>
                    <div class="meta-item"><div class="meta-key">Records</div><div class="meta-val hi">{meta.get('records',sess['records']):,}</div></div>
                    <div class="meta-item"><div class="meta-key">Start</div><div class="meta-val" style="font-size:.72rem;">{meta.get('t_start','—')}</div></div>
                    <div class="meta-item"><div class="meta-key">End</div><div class="meta-val" style="font-size:.72rem;">{meta.get('t_end','—')}</div></div>
                    <div class="meta-item"><div class="meta-key">Size</div><div class="meta-val">{meta.get('size_kb','—')} KB</div></div>
                    <div class="meta-item"><div class="meta-key">Fetched</div><div class="meta-val">{meta.get('fetched_at','—')}</div></div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="pills">
                    <div class="pill"><div class="pill-v">{sess['records']:,}</div><div class="pill-k">Records</div></div>
                    <div class="pill"><div class="pill-v">{sess['size_kb']} KB</div><div class="pill-k">Size</div></div>
                </div>
                """, unsafe_allow_html=True)

            # TXT preview
            raw_prev = sess["txt"][:1200] + ("\n…[truncated]" if len(sess["txt"])>1200 else "")
            st.markdown(f'<div class="pre-box">{hl_txt(raw_prev)}</div>', unsafe_allow_html=True)

            # Label + action row
            c_lbl, c_btn, c_rm = st.columns([3,2,1])
            with c_lbl:
                lbl_key = f"lbl_{idx}_{sess['name'][:15]}"
                cur_lbl = next((k for k,v in LABEL_MAP.items() if v==sess["label"]), "None")
                sel = st.selectbox("Fault Label", list(LABEL_MAP.keys()),
                                   index=list(LABEL_MAP.keys()).index(cur_lbl), key=lbl_key)
                new_lv = LABEL_MAP[sel]
                if new_lv != sess["label"]:
                    st.session_state.sessions[idx]["label"]     = new_lv
                    st.session_state.sessions[idx]["converted"] = False
                    st.session_state.sessions[idx]["df57"]      = None
                    st.session_state.sessions[idx]["df19"]      = None
            with c_btn:
                st.markdown("&nbsp;", unsafe_allow_html=True)
                if st.button(f"⚡  Convert Session", key=f"conv_{idx}", use_container_width=True):
                    with st.spinner("Converting…"):
                        ok, err = convert_session(idx)
                    if ok:
                        st.rerun()
                    else:
                        st.markdown(f'<div class="ax err">❌ {err}</div>', unsafe_allow_html=True)
            with c_rm:
                st.markdown("&nbsp;", unsafe_allow_html=True)
                st.markdown('<div class="btn-red">', unsafe_allow_html=True)
                if st.button("🗑", key=f"rm_{idx}", use_container_width=True):
                    to_remove.append(idx)
                st.markdown('</div>', unsafe_allow_html=True)

            # ── Results for this session ─────────────────────────
            if conv and sess.get("df57") is not None:
                df57_base = sess["df57"].copy()
                df19_base = sess["df19"].copy()
                ct = sess.get("conv_time", "—")

                st.markdown(f"""
                <div class="res-banner" style="margin-top:0.8rem;">
                    <div>
                        <p class="res-title">Conversion Complete</p>
                        <p class="res-meta">Processed in {ct}s · {len(df57_base):,} records</p>
                    </div>
                    <div class="res-nums">
                        <div class="res-num"><div class="res-num-v">{len(df57_base):,}</div><div class="res-num-k">Records</div></div>
                        <div class="res-num"><div class="res-num-v">{len(df57_base.columns)}</div><div class="res-num-k">57-cols</div></div>
                        <div class="res-num"><div class="res-num-v">{len(df19_base):,}</div><div class="res-num-k">19-rows</div></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Time window
                df57_base["Time_dt"] = pd.to_datetime(df57_base["Time"], format="%d/%m/%Y %H:%M:%S")
                tl  = df57_base["Time_dt"].tolist()
                tmn = df57_base["Time_dt"].min().to_pydatetime()
                tmx = df57_base["Time_dt"].max().to_pydatetime()
                nn  = len(tl)

                tw = st.radio("tw", ["⚡ Slider","🎯 Precise"],
                              horizontal=True, key=f"tw_{idx}", label_visibility="collapsed")

                if tw == "⚡ Slider":
                    cs, cm = st.columns([4,1])
                    with cs:
                        si, ei = st.slider("r", 0, nn-1, (0,nn-1),
                                           key=f"sl_{idx}", label_visibility="collapsed")
                        sdt=tl[si]; edt=tl[ei]
                        st.caption(f"{sdt.strftime('%d/%m/%Y %H:%M:%S')}  →  {edt.strftime('%d/%m/%Y %H:%M:%S')}")
                    with cm:
                        st.metric("Total", nn); st.metric("Selected", ei-si+1)
                else:
                    c1,c2,c3 = st.columns([2,2,1])
                    with c1:
                        sd=st.date_input("Start Date",tmn.date(),tmn.date(),tmx.date(),key=f"sd_{idx}")
                        st_=st.time_input("Start Time",tmn.time(),key=f"st_{idx}")
                        sdt=datetime.combine(sd,st_)
                    with c2:
                        ed=st.date_input("End Date",tmx.date(),tmn.date(),tmx.date(),key=f"ed_{idx}")
                        et=st.time_input("End Time",tmx.time(),key=f"et_{idx}")
                        edt=datetime.combine(ed,et)
                    with c3:
                        sn=len(df57_base[(df57_base["Time_dt"]>=sdt)&(df57_base["Time_dt"]<=edt)])
                        st.metric("Total",nn); st.metric("Selected",sn)
                    if sdt>edt:
                        st.markdown('<div class="ax err">⚠ Start must be before End.</div>',unsafe_allow_html=True)
                        sdt,edt=tmn,tmx

                mask   = (df57_base["Time_dt"]>=sdt)&(df57_base["Time_dt"]<=edt)
                df57_f = df57_base[mask].drop(columns="Time_dt").reset_index(drop=True)
                df19_f = to19(df57_f)

                if df57_f.empty:
                    st.markdown('<div class="ax warn">⚠ Empty selection — adjust range.</div>',unsafe_allow_html=True)
                else:
                    # Plots
                    p1,p2,p3 = st.columns(3)
                    with p1:
                        st.pyplot(make_plot(df57_f,["Parameter-1_X","Parameter-1_Y","Parameter-1_Z"],"Param-1 RMS","c"),use_container_width=True)
                    with p2:
                        st.pyplot(make_plot(df57_f,["Parameter-2_X","Parameter-2_Y","Parameter-2_Z"],"Param-2 PP","v"),use_container_width=True)
                    with p3:
                        st.pyplot(make_plot(df57_f,["Parameter-3_X","Parameter-3_Y","Parameter-3_Z"],"Param-3 Kurtosis","g"),use_container_width=True)

                    # Tables
                    with st.expander("📊 57-Feature Table", expanded=False):
                        st.dataframe(df57_f, height=250, use_container_width=True)
                    with st.expander("📊 19-Feature Table", expanded=False):
                        st.dataframe(df19_f, height=250, use_container_width=True)

                    # ── Individual download buttons ──────────────
                    ts_sfx = datetime.now().strftime("%Y%m%d_%H%M%S")
                    pfx    = file_prefix.strip() if file_prefix.strip() else f"session_{idx+1}"
                    clean_name = re.sub(r'[^\w\-.]','_', sess['name'])[:30]
                    f57 = f"{pfx}_{clean_name}_57feat.csv"
                    f19 = f"{pfx}_{clean_name}_19feat.csv"

                    st.markdown(f"""
                    <div style="display:grid;grid-template-columns:1fr 1fr;gap:0.5rem;margin-top:0.6rem;">
                        <div style="font-family:var(--mono);font-size:0.62rem;color:var(--tx3);
                             padding:0.4rem 0.6rem;background:var(--bg3);border-radius:6px;border:1px solid var(--border);">
                            57-FEAT · {len(df57_f):,} rows · {len(df57_f.columns)} cols
                        </div>
                        <div style="font-family:var(--mono);font-size:0.62rem;color:var(--tx3);
                             padding:0.4rem 0.6rem;background:var(--bg3);border-radius:6px;border:1px solid var(--border);">
                            19-FEAT · {len(df19_f):,} rows · 20 cols
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    dc1, dc2 = st.columns(2)
                    with dc1:
                        st.download_button(f"⬇ Download 57-feat", df57_f.to_csv(index=False),
                                          f57, "text/csv", key=f"dl57_{idx}", use_container_width=True)
                    with dc2:
                        st.markdown('<div class="dl-violet">', unsafe_allow_html=True)
                        st.download_button(f"⬇ Download 19-feat", df19_f.to_csv(index=False),
                                          f19, "text/csv", key=f"dl19_{idx}", use_container_width=True)
                        st.markdown('</div>', unsafe_allow_html=True)

    # Process removals
    if to_remove:
        st.session_state.sessions = [s for j,s in enumerate(st.session_state.sessions) if j not in to_remove]
        st.rerun()

    # ── MERGE ALL (bottom) ────────────────────────────────────────────────────
    converted_sessions = [s for s in st.session_state.sessions if s.get("converted") and s.get("df57") is not None]

    if len(converted_sessions) >= 1:
        st.markdown("""
        <div class="merge-zone">
            <div class="merge-title">⬡ Merge All Converted Sessions</div>
            <div class="merge-sub">
                Combine all individually-converted sessions into one unified dataset.
                Each session's label is preserved in the merged output.
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Summary table
        rows_html = ""
        for s in converted_sessions:
            lbl_name = next((k for k,v in LABEL_MAP.items() if v==s.get("label")), "None")
            rows_html += f"""
            <tr>
                <td>{'📡' if s['source']=='api' else '📄'} {s['name'][:45]}</td>
                <td>{len(s['df57']):,}</td>
                <td style="color:{'var(--violet)' if lbl_name!='None' else 'var(--tx3)'};">{lbl_name}</td>
            </tr>"""

        st.markdown(f"""
        <table class="sq-table" style="margin-bottom:1rem;">
            <thead><tr><th>Session</th><th>Records</th><th>Label</th></tr></thead>
            <tbody>{rows_html}</tbody>
        </table>
        """, unsafe_allow_html=True)

        merged57 = pd.concat([s["df57"] for s in converted_sessions], ignore_index=True)
        merged19 = pd.concat([s["df19"] for s in converted_sessions], ignore_index=True)

        total_rec = len(merged57)
        st.markdown(f"""
        <div class="pills">
            <div class="pill"><div class="pill-v">{len(converted_sessions)}</div><div class="pill-k">Sessions</div></div>
            <div class="pill"><div class="pill-v">{total_rec:,}</div><div class="pill-k">Total Records</div></div>
            <div class="pill"><div class="pill-v">{len(merged57.columns)}</div><div class="pill-k">57-feat cols</div></div>
            <div class="pill"><div class="pill-v">{len(merged19):,}</div><div class="pill-k">19-feat rows</div></div>
        </div>
        """, unsafe_allow_html=True)

        ts_sfx = datetime.now().strftime("%Y%m%d_%H%M%S")
        pfx    = file_prefix.strip() if file_prefix.strip() else f"merged_{ts_sfx}"
        mf57   = f"{pfx}_MERGED_57feat.csv"
        mf19   = f"{pfx}_MERGED_19feat.csv"

        st.markdown('<div style="display:grid;grid-template-columns:1fr 1fr;gap:0.5rem;margin-top:0.5rem;">', unsafe_allow_html=True)
        mc1, mc2 = st.columns(2)
        with mc1:
            st.markdown('<div class="dl-green">', unsafe_allow_html=True)
            st.download_button(f"⬇ Download Merged 57-feat  ({total_rec:,} rows)",
                              merged57.to_csv(index=False), mf57, "text/csv",
                              key="dl_merge57", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with mc2:
            st.markdown('<div class="dl-green">', unsafe_allow_html=True)
            st.download_button(f"⬇ Download Merged 19-feat  ({len(merged19):,} rows)",
                              merged19.to_csv(index=False), mf19, "text/csv",
                              key="dl_merge19", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    elif len(st.session_state.sessions) > 0:
        not_conv = len(st.session_state.sessions) - len(converted_sessions)
        st.markdown(f'<div class="ax info" style="margin-top:1rem;">ℹ Convert {not_conv} remaining session{"s" if not_conv>1 else ""} above to enable the merged download.</div>', unsafe_allow_html=True)

# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown('<div class="app-footer">VibroConvert v3.1 &nbsp;·&nbsp; pump_project &nbsp;·&nbsp; Vibration Analysis Pipeline</div>', unsafe_allow_html=True)