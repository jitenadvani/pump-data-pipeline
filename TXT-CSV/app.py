import streamlit as st
import pandas as pd
import re
import time
import requests
from datetime import datetime
import matplotlib.pyplot as plt

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="VibroConvert · Vibration Data Converter",
    page_icon="〰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS — Dark Precision Dashboard
# ============================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg:        #080d14;
    --bg-panel:  #0c1422;
    --bg-card:   #101b2e;
    --bg-card2:  #142035;
    --border:    #1a2d45;
    --border-hi: #1f3a5c;
    --teal:      #00c9a7;
    --teal-dim:  rgba(0,201,167,0.10);
    --teal-glow: rgba(0,201,167,0.22);
    --blue:      #3d9be9;
    --blue-dim:  rgba(61,155,233,0.10);
    --amber:     #f5a623;
    --red:       #f25c5c;
    --text-h:    #f0f6ff;
    --text-b:    #8fa8c8;
    --text-m:    #3d5a78;
    --serif:     'DM Serif Display', Georgia, serif;
    --sans:      'DM Sans', system-ui, sans-serif;
    --mono:      'JetBrains Mono', monospace;
}

html, body, [class*="css"] { font-family: var(--sans); }

.stApp {
    background: var(--bg);
    background-image: radial-gradient(ellipse 80% 40% at 50% -5%,
        rgba(0,201,167,0.06) 0%, transparent 60%);
}
.block-container { padding: 2rem 2.5rem 4rem; max-width: 1400px; }
#MainMenu, footer, header { visibility: hidden; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--bg-panel) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] .block-container { padding: 1.4rem 1rem; }
[data-testid="stSidebar"] label {
    color: var(--text-b) !important;
    font-family: var(--sans) !important;
    font-size: 0.8rem !important;
}
[data-testid="stSidebar"] h1,[data-testid="stSidebar"] h2,[data-testid="stSidebar"] h3 {
    color: var(--text-h) !important;
}
[data-testid="stSidebar"] .stTextInput > div > div > input {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-hi) !important;
    color: var(--text-h) !important;
    border-radius: 8px !important;
    font-family: var(--mono) !important;
    font-size: 0.82rem !important;
}
[data-testid="stSidebar"] .stTextInput > div > div > input:focus {
    border-color: var(--teal) !important;
    box-shadow: 0 0 0 3px var(--teal-dim) !important;
}

.sidebar-logo {
    display: flex; align-items: center; gap: 0.6rem;
    padding: 0.4rem 0 1.4rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 1.4rem;
}
.sidebar-logo-mark {
    width:32px;height:32px;background:linear-gradient(135deg,var(--teal),#006f5c);
    border-radius:8px;display:flex;align-items:center;justify-content:center;
    font-size:1rem;flex-shrink:0;
}
.sidebar-logo-text { font-family:var(--serif);font-size:1.05rem;color:var(--text-h);line-height:1.1; }
.sidebar-logo-sub  { font-size:0.6rem;color:var(--text-m);font-family:var(--mono);letter-spacing:0.1em;text-transform:uppercase; }
.sidebar-section   { font-family:var(--mono);font-size:0.58rem;letter-spacing:0.18em;color:var(--text-m);text-transform:uppercase;margin:1.4rem 0 0.5rem; }

/* ── Radio ── */
.stRadio > div { flex-direction:row !important; gap:0.5rem !important; flex-wrap:wrap; }
.stRadio > div > label {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-hi) !important;
    border-radius: 10px !important;
    padding: 0.65rem 1.2rem !important;
    color: var(--text-b) !important;
    font-family: var(--sans) !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    cursor: pointer !important;
    transition: all 0.18s !important;
}
.stRadio > div > label:hover {
    border-color: var(--teal) !important; color: var(--text-h) !important;
    background: var(--teal-dim) !important;
}

/* ── Cards ── */
.vc-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.4rem;
    margin-bottom: 1rem;
    position: relative;
    overflow: hidden;
}
.vc-card::after {
    content:''; position:absolute; top:0;left:0;right:0;height:1px;
    background:linear-gradient(90deg,transparent,var(--teal),transparent);
    opacity:0.35;
}
.vc-card-title {
    font-family: var(--mono); font-size: 0.6rem; letter-spacing: 0.18em;
    color: var(--teal); text-transform: uppercase; margin-bottom: 1rem;
    display: flex; align-items: center; gap: 0.5rem;
}
.vc-card-title::after { content:''; flex:1; height:1px; background:var(--border); }

/* ── Section label ── */
.sec-label {
    font-family: var(--mono); font-size: 0.6rem; letter-spacing: 0.2em;
    color: var(--text-m); text-transform: uppercase;
    display: flex; align-items: center; gap: 0.7rem;
    margin: 2rem 0 0.9rem;
}
.sec-label::before { content:''; width:16px; height:1px; background:var(--teal); }
.sec-label::after  { content:''; flex:1;     height:1px; background:var(--border); }

/* ── Stat pills ── */
.stat-row { display:flex;gap:0.6rem;flex-wrap:wrap;margin:0.8rem 0; }
.stat-pill {
    background:var(--bg-card2);border:1px solid var(--border-hi);
    border-radius:10px;padding:0.65rem 1rem;min-width:85px;
}
.stat-pill-val { font-family:var(--mono);font-size:1.05rem;color:var(--teal);font-weight:500;line-height:1.1; }
.stat-pill-key { font-size:0.6rem;color:var(--text-m);letter-spacing:0.08em;text-transform:uppercase;margin-top:0.2rem; }

/* ── Device meta grid ── */
.device-grid {
    display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));
    gap:0.6rem;margin:0.8rem 0;
}
.device-item {
    background:var(--bg-panel);border:1px solid var(--border);
    border-radius:10px;padding:0.7rem 0.9rem;
}
.device-key { font-family:var(--mono);font-size:0.58rem;letter-spacing:0.12em;color:var(--text-m);text-transform:uppercase;margin-bottom:0.2rem; }
.device-val { font-family:var(--mono);font-size:0.85rem;color:var(--text-h);font-weight:500; }
.device-val.accent { color:var(--teal); }

/* ── Fetch history ── */
.fh-item {
    display:flex;align-items:center;gap:0.6rem;background:var(--bg-card);
    border:1px solid var(--border);border-radius:9px;padding:0.6rem 0.8rem;margin-bottom:0.4rem;
    transition:border-color 0.18s;
}
.fh-item.active { border-color:var(--teal);background:var(--teal-dim); }
.fh-dot { width:7px;height:7px;border-radius:50%;background:var(--teal);flex-shrink:0; }
.fh-name { font-family:var(--mono);font-size:0.78rem;color:var(--text-h);font-weight:500;flex:1; }
.fh-meta { font-family:var(--mono);font-size:0.62rem;color:var(--text-m); }

/* ── TXT preview ── */
.txt-pre {
    background:#060b12;border:1px solid var(--border-hi);border-radius:12px;
    padding:1.1rem 1.2rem;font-family:var(--mono);font-size:0.73rem;
    color:#5a8a6e;max-height:220px;overflow-y:auto;line-height:1.7;
    white-space:pre;margin:0.4rem 0;letter-spacing:0.01em;
}
.txt-pre::-webkit-scrollbar{width:4px;}
.txt-pre::-webkit-scrollbar-track{background:var(--border);}
.txt-pre::-webkit-scrollbar-thumb{background:var(--teal);border-radius:2px;}

/* ── Alerts ── */
.a-ok   {background:rgba(0,201,167,0.08);border:1px solid rgba(0,201,167,0.28);border-radius:9px;padding:0.8rem 1.1rem;color:var(--teal);font-family:var(--sans);font-size:0.85rem;margin:0.5rem 0;}
.a-err  {background:rgba(242,92,92,0.08);border:1px solid rgba(242,92,92,0.28);border-radius:9px;padding:0.8rem 1.1rem;color:#f25c5c;font-family:var(--sans);font-size:0.85rem;margin:0.5rem 0;}
.a-warn {background:rgba(245,166,35,0.08);border:1px solid rgba(245,166,35,0.28);border-radius:9px;padding:0.8rem 1.1rem;color:var(--amber);font-family:var(--sans);font-size:0.85rem;margin:0.5rem 0;}
.a-info {background:rgba(61,155,233,0.08);border:1px solid rgba(61,155,233,0.28);border-radius:9px;padding:0.8rem 1.1rem;color:var(--blue);font-family:var(--sans);font-size:0.85rem;margin:0.5rem 0;}

/* ── Results banner ── */
.rb {
    background:linear-gradient(135deg,var(--bg-card2),var(--bg-card));
    border:1px solid var(--border-hi);border-radius:16px;
    padding:1.6rem 2rem;margin:1rem 0;
    display:flex;align-items:center;gap:2rem;flex-wrap:wrap;
}
.rb-title { font-family:var(--serif);font-size:1.55rem;color:var(--text-h);margin:0 0 0.2rem; }
.rb-meta  { font-family:var(--mono);font-size:0.68rem;color:var(--text-m);letter-spacing:0.04em; }
.rb-stats { display:flex;gap:1.4rem;flex-wrap:wrap;margin-left:auto; }
.rb-stat  { text-align:center; }
.rb-stat-v { font-family:var(--serif);font-size:1.7rem;color:var(--teal);line-height:1; }
.rb-stat-k { font-family:var(--mono);font-size:0.58rem;color:var(--text-m);letter-spacing:0.1em;text-transform:uppercase;margin-top:0.15rem; }

/* ── Buttons ── */
.stButton > button {
    background: var(--teal) !important; color:#040a0f !important;
    font-family:var(--sans) !important; font-weight:600 !important;
    font-size:0.88rem !important; border:none !important; border-radius:10px !important;
    padding:0.65rem 1.5rem !important; letter-spacing:0.02em !important;
    transition:all 0.18s !important; box-shadow:0 4px 14px var(--teal-glow) !important;
}
.stButton > button:hover {
    background:#00e8c1 !important;
    box-shadow:0 6px 22px var(--teal-glow) !important;
    transform:translateY(-1px) !important;
}
.stButton > button:active { transform:translateY(0) !important; }

.btn-ghost > button {
    background:transparent !important; color:var(--text-b) !important;
    border:1px solid var(--border-hi) !important; box-shadow:none !important;
}
.btn-ghost > button:hover {
    border-color:var(--teal) !important; color:var(--teal) !important;
    background:var(--teal-dim) !important; box-shadow:none !important;
}
.btn-danger > button {
    background:transparent !important; color:var(--red) !important;
    border:1px solid rgba(242,92,92,0.3) !important; box-shadow:none !important;
}
.btn-danger > button:hover {
    background:rgba(242,92,92,0.08) !important; border-color:var(--red) !important; box-shadow:none !important;
}

/* ── Download buttons ── */
.stDownloadButton > button {
    background:var(--bg-card2) !important; color:var(--teal) !important;
    border:1px solid rgba(0,201,167,0.3) !important; border-radius:10px !important;
    font-family:var(--sans) !important; font-weight:600 !important;
    font-size:0.85rem !important; padding:0.65rem 1.2rem !important;
    width:100% !important; box-shadow:none !important; transition:all 0.18s !important;
}
.stDownloadButton > button:hover {
    background:var(--teal-dim) !important; border-color:var(--teal) !important;
    box-shadow:0 4px 14px var(--teal-glow) !important; transform:translateY(-1px) !important;
}

/* ── Slider ── */
.stSlider > div > div > div > div { background:var(--teal) !important; }
.stSlider > div > div > div { background:var(--border-hi) !important; height:4px !important; }

/* ── Metrics ── */
[data-testid="metric-container"] {
    background:var(--bg-card) !important; border:1px solid var(--border) !important;
    border-radius:10px !important; padding:0.85rem 1rem !important;
}
[data-testid="metric-container"] label { color:var(--text-m) !important; font-family:var(--mono) !important; font-size:0.62rem !important; letter-spacing:0.1em !important; }
[data-testid="metric-container"] [data-testid="stMetricValue"] { color:var(--text-h) !important; font-family:var(--mono) !important; font-size:1.25rem !important; }

/* ── Dataframe ── */
.stDataFrame { border-radius:12px; overflow:hidden; }

/* ── Checkbox / Selectbox ── */
.stCheckbox label { color:var(--text-b) !important; font-family:var(--sans) !important; font-size:0.86rem !important; }
.stSelectbox > div > div {
    background:var(--bg-card) !important; border:1px solid var(--border-hi) !important;
    border-radius:8px !important; color:var(--text-h) !important;
    font-family:var(--mono) !important; font-size:0.83rem !important;
}
.stSelectbox label { color:var(--text-b) !important; font-family:var(--mono) !important; font-size:0.68rem !important; letter-spacing:0.08em !important; text-transform:uppercase !important; }

/* ── Expander ── */
.streamlit-expanderHeader {
    background:var(--bg-card) !important; border:1px solid var(--border) !important;
    border-radius:10px !important; color:var(--text-b) !important;
    font-family:var(--sans) !important; font-size:0.85rem !important;
}
.streamlit-expanderContent {
    background:var(--bg-card) !important; border:1px solid var(--border) !important;
    border-top:none !important; border-radius:0 0 10px 10px !important; padding:1rem !important;
}

/* ── Progress ── */
.stProgress > div > div > div > div { background:var(--teal) !important; }
.stProgress > div > div > div { background:var(--border-hi) !important; height:4px !important; border-radius:100px !important; }

/* ── Caption / small ── */
.stCaption { color:var(--text-m) !important; font-family:var(--mono) !important; font-size:0.7rem !important; }

hr { border:none;height:1px;background:linear-gradient(90deg,transparent,var(--border-hi),transparent);margin:2rem 0; }

.app-footer {
    text-align:center;padding:2rem 0 1rem;font-family:var(--mono);
    font-size:0.6rem;letter-spacing:0.12em;color:var(--text-m);text-transform:uppercase;
}
::-webkit-scrollbar{width:5px;height:5px;}
::-webkit-scrollbar-track{background:var(--bg);}
::-webkit-scrollbar-thumb{background:var(--border-hi);border-radius:3px;}
::-webkit-scrollbar-thumb:hover{background:var(--teal);}
</style>
""", unsafe_allow_html=True)

# ============================================================
# SESSION STATE
# ============================================================

DEFAULTS = {
    "txt_content":        None,
    "source_label":       None,
    "device_meta":        None,
    "fetch_history":      [],
    "selected_fetch_idx": None,
    "df_57_base":         None,
    "df_19_base":         None,
    "conversion_done":    False,
    "conversion_time":    None,
    "num_records":        0,
    "label_value":        None,
    "fetch_msg":          None,
    "fetch_msg_type":     None,
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ============================================================
# CONFIG
# ============================================================

api_base = "https://pumpdata.duckdns.org/api"

LABEL_MAP = {
    "Normal_Mode(0)": 0,
    "Seal Failure(1)": 1,
    "Bearing(2)": 2,
    "Shaft Misalignment(3)": 3,
    "Unbalance_impeller(4)": 4,
    "Cavitation(5)": 5,
}

# ============================================================
# FUNCTIONS
# ============================================================

def normalize_time(t: str) -> str:
    return datetime.strptime(t.strip(), "%m/%d/%Y %I:%M:%S %p").strftime("%d/%m/%Y %H:%M:%S")

def parse_vibration(txt: str) -> pd.DataFrame:
    rows = []
    lines = [l.strip() for l in txt.splitlines() if l.strip()]
    i = 0
    time_re     = re.compile(r"\d+/\d+/\d+\s+\d+:\d+:\d+\s+(AM|PM)")
    peak_new_re = re.compile(r"Peak\s+(\d+)\s+Parameter-\d+\s+([-\d.]+)\s+Parameter-\d+\s+([-\d.]+)")
    peak_old_re = re.compile(r"Peak\s+(\d+)\s+Freq\s+([-\d.]+)\s+Mag\s+([-\d.]+)")
    def try_float(tokens, idx):
        try:    return float(tokens[idx])
        except: return None
    while i < len(lines):
        if time_re.match(lines[i]):
            row = {"Time": normalize_time(lines[i])}
            i += 1
            for axis in ["X","Y","Z"]:
                while i < len(lines) and f"{axis} Axis" not in lines[i]: i += 1
                i += 1
                peaks = {}
                while i < len(lines) and not lines[i].endswith("Axis:") and not time_re.match(lines[i]):
                    line = lines[i]; tokens = line.split()
                    if tokens and re.match(r"^Parameter-(\d+)$", tokens[0]):
                        pn = int(tokens[0].split("-")[1]); val = try_float(tokens,1)
                        if pn==1: row[f"Parameter-1_{axis}"]=val
                        elif pn==2: row[f"Parameter-2_{axis}"]=val
                        elif pn==3: row[f"Parameter-3_{axis}"]=val
                        i+=1; continue
                    if   line.startswith("RMS"):      row[f"Parameter-1_{axis}"]=try_float(tokens,1)
                    elif line.startswith("PP"):        row[f"Parameter-2_{axis}"]=try_float(tokens,1)
                    elif line.startswith("Kurtosis"):  row[f"Parameter-3_{axis}"]=try_float(tokens,1)
                    else:
                        m = peak_new_re.match(line) or peak_old_re.match(line)
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
    cols_19=["Time"]+[f"Parameter-{n}" for n in range(1,20)]
    df_19=pd.DataFrame(rows_19)
    if has_label: cols_19.append("Label")
    return df_19[cols_19]

def do_conversion(txt, label_value=None):
    t0=time.time()
    try: df_raw=parse_vibration(txt)
    except Exception as e: return False, f"Parse error: {e}"
    if df_raw.empty: return False,"No vibration records found. Check the file format."
    df_57=reorder_columns_57(df_raw.copy())
    if label_value is not None: df_57["Label"]=label_value
    df_19=convert_to_19_features(df_57)
    st.session_state.df_57_base=df_57; st.session_state.df_19_base=df_19
    st.session_state.conversion_done=True; st.session_state.conversion_time=round(time.time()-t0,2)
    st.session_state.num_records=len(df_57); st.session_state.label_value=label_value
    return True,None

def clear_data():
    for k in ["txt_content","source_label","device_meta","df_57_base","df_19_base",
              "conversion_done","conversion_time","num_records","label_value",
              "fetch_msg","fetch_msg_type","selected_fetch_idx"]:
        st.session_state[k]=DEFAULTS.get(k,None)

def make_plot(df, columns, title, palette):
    pals={
        'p1':['#00c9a7','#009e84','#006f5c'],
        'p2':['#3d9be9','#2678c0','#145a97'],
        'p3':['#f5a623','#c07d10','#8a5a00'],
    }
    clrs=pals.get(palette,pals['p1'])
    fig,ax=plt.subplots(figsize=(5.5,3),facecolor='#101b2e')
    ax.set_facecolor('#0c1422')
    for idx,c in enumerate(columns):
        if c in df.columns:
            lbl=c.split('_')[-1] if '_' in c else c
            ax.plot(df[c].values,label=lbl,linewidth=1.8,alpha=0.9,color=clrs[idx%len(clrs)])
    ax.set_title(title,fontsize=10,color='#8fa8c8',pad=10)
    ax.set_xlabel('Sample',fontsize=8,color='#3d5a78')
    ax.set_ylabel('Value',fontsize=8,color='#3d5a78')
    ax.legend(fontsize=7,framealpha=0,labelcolor='#8fa8c8',loc='best')
    ax.grid(True,alpha=0.1,linestyle='--',linewidth=0.5,color='#1a2d45')
    for sp in ax.spines.values(): sp.set_color('#1a2d45')
    ax.tick_params(labelsize=7,colors='#3d5a78')
    fig.tight_layout(pad=1.2)
    return fig

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <div class="sidebar-logo-mark">〰</div>
        <div>
            <div class="sidebar-logo-text">VibroConvert</div>
            <div class="sidebar-logo-sub">v2.1 · Professional</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section">Output Settings</div>', unsafe_allow_html=True)
    file_prefix = st.text_input(
        "File prefix",
        placeholder="e.g. pump_test_01",
        key="file_prefix_input",
    )

    st.markdown('<div class="sidebar-section">Actions</div>', unsafe_allow_html=True)
    st.markdown('<div class="btn-ghost">', unsafe_allow_html=True)
    if st.button("🗑  Clear All Data", use_container_width=True, key="sidebar_clear"):
        clear_data()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # Fetch history
    if st.session_state.fetch_history:
        st.markdown('<div class="sidebar-section">Session History</div>', unsafe_allow_html=True)
        for i, entry in enumerate(reversed(st.session_state.fetch_history)):
            real_idx = len(st.session_state.fetch_history) - 1 - i
            is_active = (st.session_state.selected_fetch_idx == real_idx)
            ac = "active" if is_active else ""
            st.markdown(f"""
            <div class="fh-item {ac}">
                <div class="fh-dot"></div>
                <div style="flex:1;min-width:0;">
                    <div class="fh-name" style="white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">
                        {entry.get('device_name','Unknown')}
                    </div>
                    <div class="fh-meta">{entry.get('fetched_at','—')} · {entry.get('records','?'):,} rec</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown('<div class="btn-ghost">', unsafe_allow_html=True)
            if st.button(f"Load", key=f"load_hist_{i}", use_container_width=True):
                e = st.session_state.fetch_history[real_idx]
                st.session_state.txt_content      = e['content']
                st.session_state.source_label     = e.get('device_name','Session')
                st.session_state.device_meta      = e
                st.session_state.conversion_done  = False
                st.session_state.df_57_base       = None
                st.session_state.df_19_base       = None
                st.session_state.selected_fetch_idx = real_idx
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# HEADER
# ============================================================

col_h, col_b = st.columns([4, 1])
with col_h:
    st.markdown("""
    <div style="padding-bottom:1.4rem;border-bottom:1px solid var(--border);margin-bottom:1.8rem;">
        <h1 style="font-family:var(--serif);font-size:2.4rem;color:var(--text-h);margin:0;line-height:1.05;">
            Vibration Data <span style="color:var(--teal);font-style:italic;">Converter</span>
        </h1>
        <p style="font-size:0.83rem;color:var(--text-b);margin:0.3rem 0 0;font-weight:300;letter-spacing:0.02em;">
            Transform raw vibration TXT logs into structured 57-feature and 19-feature CSV datasets
        </p>
    </div>
    """, unsafe_allow_html=True)
with col_b:
    done = st.session_state.conversion_done
    pill_cls = "ready" if done else "idle"
    pill_txt = "Converted" if done else "Awaiting Data"
    st.markdown(f"""
    <div style="padding-top:0.9rem;text-align:right;">
        <span style="display:inline-flex;align-items:center;gap:0.35rem;padding:0.3rem 0.85rem;
              border-radius:100px;font-family:var(--mono);font-size:0.62rem;letter-spacing:0.12em;
              text-transform:uppercase;{'background:var(--teal-dim);border:1px solid rgba(0,201,167,0.3);color:var(--teal);' if done else 'background:var(--bg-card);border:1px solid var(--border);color:var(--text-m);'}">
            <span style="width:6px;height:6px;border-radius:50%;background:currentColor;
                  animation:pdot 2s ease-in-out infinite;"></span>
            {pill_txt}
        </span>
    </div>
    <style>@keyframes pdot{{0%,100%{{opacity:1;transform:scale(1)}}50%{{opacity:.3;transform:scale(.7)}}}}</style>
    """, unsafe_allow_html=True)

# ============================================================
# SOURCE SELECTION
# ============================================================

st.markdown('<div class="sec-label">Data Source</div>', unsafe_allow_html=True)

source_choice = st.radio(
    "Source",
    ["📁  Upload TXT File", "📡  Fetch from Device Simulator"],
    horizontal=True,
    key="source_radio",
    label_visibility="collapsed",
)

# ============================================================
# LOAD DATA
# ============================================================

st.markdown('<div class="sec-label">Load Data</div>', unsafe_allow_html=True)

# ── Upload ─────────────────────────────────────────────────────
if source_choice == "📁  Upload TXT File":
    uploaded_files = st.file_uploader(
        "Drop TXT files here or click to browse",
        type=["txt"],
        accept_multiple_files=True,
        key="file_uploader",
    )
    if uploaded_files:
        combined = "".join(f.read().decode("utf-8", errors="replace") + "\n" for f in uploaded_files)
        new_label = f"{len(uploaded_files)} file{'s' if len(uploaded_files)>1 else ''} uploaded"
        if st.session_state.txt_content != combined:
            st.session_state.txt_content     = combined
            st.session_state.source_label    = new_label
            st.session_state.device_meta     = None
            st.session_state.conversion_done = False
            st.session_state.df_57_base      = None
            st.session_state.df_19_base      = None

# ── Fetch ──────────────────────────────────────────────────────
else:
    st.markdown(f"""
    <div class="vc-card">
        <div class="vc-card-title">Device Simulator API</div>
        <div style="font-family:var(--mono);font-size:0.77rem;color:var(--blue);
             background:var(--blue-dim);border:1px solid rgba(61,155,233,0.18);
             border-radius:8px;padding:0.45rem 0.8rem;margin-bottom:1rem;word-break:break-all;">
            GET {api_base}/latest
        </div>
        <p style="font-family:var(--sans);font-size:0.82rem;color:var(--text-b);margin:0 0 0.8rem;line-height:1.55;">
            Pulls the latest vibration session. Up to
            <strong style="color:var(--text-h);">5 sessions</strong> are cached in the sidebar for reload.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col_f, col_c = st.columns([3,1])
    with col_f:
        fetch_clicked = st.button("📡  Fetch Latest Device Data", use_container_width=True, key="fetch_btn")
    with col_c:
        st.markdown('<div class="btn-danger">', unsafe_allow_html=True)
        if st.button("Clear", use_container_width=True, key="inline_clear"):
            clear_data(); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.fetch_msg:
        css = {"success":"a-ok","error":"a-err","warning":"a-warn"}.get(st.session_state.fetch_msg_type,"a-info")
        st.markdown(f'<div class="{css}">{st.session_state.fetch_msg}</div>', unsafe_allow_html=True)

    if fetch_clicked:
        with st.spinner("Connecting to ingestion service…"):
            try:
                resp = requests.get(f"{api_base}/latest", timeout=15)
                if resp.status_code == 200:
                    payload = resp.json()
                    content = payload.get("content","").strip()
                    if content:
                        time_re_l = re.compile(r"(\d+/\d+/\d+)\s+(\d+:\d+:\d+)\s+(AM|PM)")
                        ts_matches = time_re_l.findall(content)
                        t_start = f"{ts_matches[0][0]} {ts_matches[0][1]} {ts_matches[0][2]}" if ts_matches else "—"
                        t_end   = f"{ts_matches[-1][0]} {ts_matches[-1][1]} {ts_matches[-1][2]}" if ts_matches else "—"
                        rec_count = content.count("#Vibration Value")
                        sz_kb = len(content)/1024

                        samp_rate = payload.get("sampling_rate","—")
                        if samp_rate == "—" and len(ts_matches) >= 2:
                            try:
                                fmt="%m/%d/%Y %I:%M:%S %p"
                                t1=datetime.strptime(f"{ts_matches[0][0]} {ts_matches[0][1]} {ts_matches[0][2]}",fmt)
                                t2=datetime.strptime(f"{ts_matches[1][0]} {ts_matches[1][1]} {ts_matches[1][2]}",fmt)
                                samp_rate=f"{int((t2-t1).total_seconds())}s"
                            except: pass

                        meta = {
                            "device_name":  payload.get("device_name", payload.get("device_id","Device-Unknown")),
                            "sampling_rate": samp_rate,
                            "duration":     payload.get("duration","—"),
                            "records":      rec_count,
                            "t_start":      t_start,
                            "t_end":        t_end,
                            "size_kb":      round(sz_kb,1),
                            "fetched_at":   datetime.now().strftime("%H:%M:%S"),
                            "content":      content,
                        }
                        history = st.session_state.fetch_history.copy()
                        history.append(meta)
                        if len(history) > 5: history = history[-5:]
                        st.session_state.fetch_history      = history
                        st.session_state.selected_fetch_idx = len(history)-1
                        st.session_state.txt_content        = content
                        st.session_state.source_label       = meta["device_name"]
                        st.session_state.device_meta        = meta
                        st.session_state.conversion_done    = False
                        st.session_state.df_57_base         = None
                        st.session_state.df_19_base         = None
                        st.session_state.fetch_msg          = f"✅ Fetched {rec_count:,} records from <strong>{meta['device_name']}</strong>"
                        st.session_state.fetch_msg_type     = "success"
                    else:
                        st.session_state.fetch_msg      = "ℹ️ No data available yet. Run the Device Simulator first."
                        st.session_state.fetch_msg_type = "warning"
                else:
                    st.session_state.fetch_msg      = f"⚠️ Server returned HTTP {resp.status_code}."
                    st.session_state.fetch_msg_type = "error"
            except requests.exceptions.ConnectionError:
                st.session_state.fetch_msg      = f"🔌 Cannot reach {api_base}. Ensure api_server.py is running."
                st.session_state.fetch_msg_type = "error"
            except requests.exceptions.Timeout:
                st.session_state.fetch_msg      = "⏱ Request timed out. Server may be busy — retry."
                st.session_state.fetch_msg_type = "error"
            except Exception as e:
                st.session_state.fetch_msg      = f"❌ Unexpected error: {e}"
                st.session_state.fetch_msg_type = "error"
        st.rerun()

# ============================================================
# DATA OVERVIEW
# ============================================================

if st.session_state.txt_content:
    txt = st.session_state.txt_content
    rec_count  = txt.count("#Vibration Value")
    line_count = txt.count("\n")
    sz_kb      = len(txt)/1024

    st.markdown('<div class="sec-label">Data Overview</div>', unsafe_allow_html=True)

    meta = st.session_state.device_meta
    if meta:
        # Rich device info card
        st.markdown(f"""
        <div class="vc-card">
            <div class="vc-card-title">Session Details</div>
            <div class="device-grid">
                <div class="device-item">
                    <div class="device-key">Device ID</div>
                    <div class="device-val accent">{meta.get('device_name','—')}</div>
                </div>
                <div class="device-item">
                    <div class="device-key">Sampling Rate</div>
                    <div class="device-val">{meta.get('sampling_rate','—')}</div>
                </div>
                <div class="device-item">
                    <div class="device-key">Duration</div>
                    <div class="device-val">{meta.get('duration','—')}</div>
                </div>
                <div class="device-item">
                    <div class="device-key">Total Records</div>
                    <div class="device-val accent">{meta.get('records',rec_count):,}</div>
                </div>
                <div class="device-item">
                    <div class="device-key">Start Time</div>
                    <div class="device-val" style="font-size:0.78rem;">{meta.get('t_start','—')}</div>
                </div>
                <div class="device-item">
                    <div class="device-key">End Time</div>
                    <div class="device-val" style="font-size:0.78rem;">{meta.get('t_end','—')}</div>
                </div>
                <div class="device-item">
                    <div class="device-key">File Size</div>
                    <div class="device-val">{meta.get('size_kb',round(sz_kb,1))} KB</div>
                </div>
                <div class="device-item">
                    <div class="device-key">Fetched At</div>
                    <div class="device-val">{meta.get('fetched_at','—')}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="stat-row">
            <div class="stat-pill"><div class="stat-pill-val">{rec_count:,}</div><div class="stat-pill-key">Records</div></div>
            <div class="stat-pill"><div class="stat-pill-val">{line_count:,}</div><div class="stat-pill-key">Lines</div></div>
            <div class="stat-pill"><div class="stat-pill-val">{sz_kb:.1f} KB</div><div class="stat-pill-key">File Size</div></div>
        </div>
        """, unsafe_allow_html=True)

    # Syntax-highlighted preview
    preview_raw = txt[:2000] + ("\n…[truncated]" if len(txt)>2000 else "")
    hl_lines = []
    for line in preview_raw.splitlines():
        ls = line.strip()
        if re.match(r"\d+/\d+/\d+\s+\d+:\d+:\d+", ls):
            hl_lines.append(f'<span style="color:#3d9be9;font-weight:500;">{line}</span>')
        elif "Axis:" in ls:
            hl_lines.append(f'<span style="color:#00c9a7;">{line}</span>')
        elif ls.startswith("Peak"):
            hl_lines.append(f'<span style="color:#8fa8c8;">{line}</span>')
        elif ls.startswith("#"):
            hl_lines.append(f'<span style="color:#3d5a78;">{line}</span>')
        else:
            hl_lines.append(f'<span style="color:#5a8a6e;">{line}</span>')

    with st.expander("📄  TXT Preview — first 2 000 characters", expanded=False):
        st.markdown(f'<div class="txt-pre">{"<br>".join(hl_lines)}</div>', unsafe_allow_html=True)

    # ============================================================
    # CONVERT
    # ============================================================

    if not st.session_state.conversion_done:
        st.markdown('<div class="sec-label">Convert</div>', unsafe_allow_html=True)

        with st.expander("🏷  Label Configuration — optional, for ML training", expanded=False):
            use_label = st.checkbox("Attach a label column to output CSVs", value=False, key="chk_use_label")
            if use_label:
                st.selectbox("Fault Label", list(LABEL_MAP.keys()), key="sel_label")
            st.markdown('<div class="a-info">Integer label appended as the final column to both 57-feat and 19-feat CSVs.</div>', unsafe_allow_html=True)

        col_cv, _ = st.columns([1,3])
        with col_cv:
            convert_clicked = st.button("⚡  Convert to CSV", use_container_width=True, key="convert_btn")

        if convert_clicked:
            label_val = None
            if st.session_state.get("chk_use_label", False):
                raw = st.session_state.get("sel_label", list(LABEL_MAP.keys())[0])
                label_val = LABEL_MAP.get(raw, 0)
            with st.spinner("Parsing vibration records…"):
                ok, err = do_conversion(txt, label_val)
            if ok:
                st.markdown('<div class="a-ok">✅ Conversion complete — results ready below.</div>', unsafe_allow_html=True)
                st.rerun()
            else:
                st.markdown(f'<div class="a-err">❌ {err}</div>', unsafe_allow_html=True)

# ============================================================
# RESULTS
# ============================================================

if st.session_state.conversion_done and st.session_state.df_57_base is not None:
    df_57_base = st.session_state.df_57_base
    df_19_base = st.session_state.df_19_base
    ct = st.session_state.conversion_time

    st.markdown('<div class="sec-label">Results</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="rb">
        <div>
            <div class="rb-title">Conversion Complete</div>
            <div class="rb-meta">Processed in {ct}s &nbsp;·&nbsp; {st.session_state.source_label or 'Unknown Source'}</div>
        </div>
        <div class="rb-stats">
            <div class="rb-stat"><div class="rb-stat-v">{st.session_state.num_records:,}</div><div class="rb-stat-k">Records</div></div>
            <div class="rb-stat"><div class="rb-stat-v">{len(df_57_base.columns)}</div><div class="rb-stat-k">Columns</div></div>
            <div class="rb-stat"><div class="rb-stat-v">{len(df_19_base):,}</div><div class="rb-stat-k">19-feat rows</div></div>
            <div class="rb-stat"><div class="rb-stat-v">{ct}s</div><div class="rb-stat-k">Parse time</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Time Window ─────────────────────────────────────────────
    st.markdown('<div class="sec-label">Time Window</div>', unsafe_allow_html=True)

    df_57_base["Time_dt"] = pd.to_datetime(df_57_base["Time"], format="%d/%m/%Y %H:%M:%S")
    time_list = df_57_base["Time_dt"].tolist()
    tmin = df_57_base["Time_dt"].min().to_pydatetime()
    tmax = df_57_base["Time_dt"].max().to_pydatetime()
    n = len(time_list)

    tw_method = st.radio(
        "Time window method",
        ["⚡ Quick Slider", "🎯 Precise Time Input"],
        horizontal=True,
        key="sel_method",
        label_visibility="collapsed",
    )

    if tw_method == "⚡ Quick Slider":
        col_sl, col_m = st.columns([4,1])
        with col_sl:
            start_idx, end_idx = st.slider(
                "Time range", min_value=0, max_value=n-1,
                value=(0, n-1), key="time_slider",
                label_visibility="collapsed",
            )
            start_dt = time_list[start_idx]
            end_dt   = time_list[end_idx]
            st.caption(f"From  {start_dt.strftime('%d/%m/%Y %H:%M:%S')}  →  {end_dt.strftime('%d/%m/%Y %H:%M:%S')}")
        with col_m:
            st.metric("Total", n)
            st.metric("Selected", end_idx - start_idx + 1)
    else:
        c1,c2,c3 = st.columns([2,2,1])
        with c1:
            sd=st.date_input("Start Date",value=tmin.date(),min_value=tmin.date(),max_value=tmax.date(),key="prec_sd")
            st_=st.time_input("Start Time",value=tmin.time(),key="prec_st")
            start_dt=datetime.combine(sd,st_)
        with c2:
            ed=st.date_input("End Date",value=tmax.date(),min_value=tmin.date(),max_value=tmax.date(),key="prec_ed")
            et=st.time_input("End Time",value=tmax.time(),key="prec_et")
            end_dt=datetime.combine(ed,et)
        with c3:
            sn=len(df_57_base[(df_57_base["Time_dt"]>=start_dt)&(df_57_base["Time_dt"]<=end_dt)])
            st.metric("Total",n); st.metric("Selected",sn)
        if start_dt>end_dt:
            st.markdown('<div class="a-err">⚠ Start must be before End.</div>',unsafe_allow_html=True)
            start_dt,end_dt=tmin,tmax

    mask    = (df_57_base["Time_dt"]>=start_dt)&(df_57_base["Time_dt"]<=end_dt)
    df_57_f = df_57_base[mask].drop(columns="Time_dt").reset_index(drop=True)
    df_19_f = convert_to_19_features(df_57_f)

    if df_57_f.empty:
        st.markdown('<div class="a-warn">⚠ No data in selected window — adjust the range.</div>', unsafe_allow_html=True)
    else:
        # ── Plots ────────────────────────────────────────────────
        st.markdown('<div class="sec-label">Feature Visualization</div>', unsafe_allow_html=True)
        c1,c2,c3 = st.columns(3)
        with c1:
            st.markdown('<div class="vc-card" style="padding:0.7rem;">', unsafe_allow_html=True)
            st.pyplot(make_plot(df_57_f,["Parameter-1_X","Parameter-1_Y","Parameter-1_Z"],"Parameter-1  (RMS)","p1"),use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="vc-card" style="padding:0.7rem;">', unsafe_allow_html=True)
            st.pyplot(make_plot(df_57_f,["Parameter-2_X","Parameter-2_Y","Parameter-2_Z"],"Parameter-2  (PP)","p2"),use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with c3:
            st.markdown('<div class="vc-card" style="padding:0.7rem;">', unsafe_allow_html=True)
            st.pyplot(make_plot(df_57_f,["Parameter-3_X","Parameter-3_Y","Parameter-3_Z"],"Parameter-3  (Kurtosis)","p3"),use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # ── Tables ───────────────────────────────────────────────
        st.markdown('<div class="sec-label">57-Feature Table</div>', unsafe_allow_html=True)
        st.dataframe(df_57_f, height=280, use_container_width=True)

        st.markdown('<div class="sec-label">19-Feature Table</div>', unsafe_allow_html=True)
        st.markdown('<div class="a-info">Each timestamp row expands to 3 rows (X, Y, Z axes stacked).</div>', unsafe_allow_html=True)
        st.dataframe(df_19_f, height=280, use_container_width=True)

        # ── Export ───────────────────────────────────────────────
        st.markdown('<div class="sec-label">Export</div>', unsafe_allow_html=True)
        ts_sfx  = datetime.now().strftime("%Y%m%d_%H%M%S")
        base    = file_prefix if file_prefix else f"vibration_{ts_sfx}"
        f57     = f"{base}_57feat.csv"
        f19     = f"{base}_19feat.csv"

        dl1,dl2,_ = st.columns([2,2,1])
        with dl1:
            st.download_button(f"⬇  {f57}", data=df_57_f.to_csv(index=False),
                               file_name=f57, mime="text/csv", key="dl_57", use_container_width=True)
            st.markdown(f'<div style="font-family:var(--mono);font-size:0.62rem;color:var(--text-m);text-align:center;margin-top:0.25rem;">{len(df_57_f):,} rows · {len(df_57_f.columns)} cols</div>', unsafe_allow_html=True)
        with dl2:
            st.download_button(f"⬇  {f19}", data=df_19_f.to_csv(index=False),
                               file_name=f19, mime="text/csv", key="dl_19", use_container_width=True)
            st.markdown(f'<div style="font-family:var(--mono);font-size:0.62rem;color:var(--text-m);text-align:center;margin-top:0.25rem;">{len(df_19_f):,} rows · 20 cols</div>', unsafe_allow_html=True)

    # ── Re-convert ────────────────────────────────────────────────
    with st.expander("🔁  Re-convert with different label", expanded=False):
        st.markdown('<div class="a-info">Reapplies conversion with a new label to the full dataset.</div>', unsafe_allow_html=True)
        rl=st.checkbox("Attach label",value=False,key="chk_relabel")
        lv2=None
        if rl: lv2=LABEL_MAP[st.selectbox("Label",list(LABEL_MAP.keys()),key="sel_relabel")]
        st.markdown('<div class="btn-ghost">', unsafe_allow_html=True)
        if st.button("🔄  Re-convert",key="reconvert_btn"):
            with st.spinner("Re-converting…"):
                ok,err=do_conversion(st.session_state.txt_content,lv2 if rl else None)
            if ok:
                st.markdown('<div class="a-ok">✅ Re-conversion successful.</div>',unsafe_allow_html=True)
                st.rerun()
            else:
                st.markdown(f'<div class="a-err">❌ {err}</div>',unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# LANDING
# ============================================================

elif not st.session_state.txt_content:
    st.markdown("""
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin:2.5rem 0;">
        <div class="vc-card" style="padding:2rem;">
            <div style="font-size:1.6rem;margin-bottom:0.7rem;">📁</div>
            <div style="font-family:var(--serif);font-size:1.15rem;color:var(--text-h);margin-bottom:0.4rem;">Upload TXT Files</div>
            <div style="font-size:0.82rem;color:var(--text-b);line-height:1.55;">
                Upload one or more local vibration log files. Multiple files are merged automatically into a single dataset.
            </div>
        </div>
        <div class="vc-card" style="padding:2rem;border-color:rgba(0,201,167,0.22);">
            <div style="font-size:1.6rem;margin-bottom:0.7rem;">📡</div>
            <div style="font-family:var(--serif);font-size:1.15rem;color:var(--teal);margin-bottom:0.4rem;">Fetch from API</div>
            <div style="font-size:0.82rem;color:var(--text-b);line-height:1.55;">
                Pull the latest session from the FastAPI ingestion service. Up to 5 sessions cached in the sidebar.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="app-footer">
    VibroConvert v2.1 &nbsp;·&nbsp; pump_project &nbsp;·&nbsp; Vibration Analysis Pipeline
</div>
""", unsafe_allow_html=True)