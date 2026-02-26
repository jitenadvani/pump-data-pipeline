import streamlit as st
import pandas as pd
import re
import time
import requests
from datetime import datetime
import matplotlib.pyplot as plt
from io import StringIO

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Vibration Data Converter",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Work+Sans:wght@300;400;600&display=swap');

    .main { background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); }

    .custom-header {
        font-family: 'Playfair Display', serif;
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 50%, #06b6d4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 0.5rem;
        padding: 1rem 0;
        letter-spacing: -0.02em;
    }
    .custom-subtitle {
        font-family: 'Work Sans', sans-serif;
        font-size: 1.1rem;
        font-weight: 300;
        color: #64748b;
        text-align: center;
        margin-bottom: 2rem;
        letter-spacing: 0.05em;
    }
    .section-header {
        font-family: 'Work Sans', sans-serif;
        font-size: 1.4rem;
        font-weight: 600;
        color: #1e293b;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #3b82f6;
        display: inline-block;
    }
    .metric-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
        border-left: 4px solid #3b82f6;
        margin: 1rem 0;
    }
    .info-box {
        background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
        border-left: 4px solid #3b82f6;
        border-radius: 8px;
        padding: 1rem 1.5rem;
        margin: 1rem 0;
        font-family: 'Work Sans', sans-serif;
        font-size: 0.95rem;
        color: #1e40af;
    }
    .success-box {
        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
        border-left: 4px solid #22c55e;
        border-radius: 8px;
        padding: 1rem 1.5rem;
        margin: 1rem 0;
        font-family: 'Work Sans', sans-serif;
        font-size: 0.95rem;
        color: #166534;
    }
    .error-box {
        background: linear-gradient(135deg, #fff1f2 0%, #ffe4e6 100%);
        border-left: 4px solid #f43f5e;
        border-radius: 8px;
        padding: 1rem 1.5rem;
        margin: 1rem 0;
        font-family: 'Work Sans', sans-serif;
        font-size: 0.95rem;
        color: #9f1239;
    }
    .warning-box {
        background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
        border-left: 4px solid #f59e0b;
        border-radius: 8px;
        padding: 1rem 1.5rem;
        margin: 1rem 0;
        font-family: 'Work Sans', sans-serif;
        font-size: 0.95rem;
        color: #92400e;
    }
    .pipeline-banner {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        border-radius: 12px;
        padding: 1.2rem 1.8rem;
        margin: 1rem 0 1.5rem 0;
    }
    .pipe-step {
        background: rgba(59,130,246,0.15);
        border: 1px solid rgba(59,130,246,0.3);
        color: #93c5fd;
        padding: 0.3rem 0.8rem;
        border-radius: 100px;
        font-family: 'Work Sans', sans-serif;
        font-size: 0.78rem;
        font-weight: 600;
    }
    .preview-box {
        background: #0f172a;
        border: 1px solid #1e293b;
        border-radius: 10px;
        padding: 1.2rem;
        font-family: 'Courier New', monospace;
        font-size: 0.78rem;
        color: #94a3b8;
        max-height: 280px;
        overflow-y: auto;
        line-height: 1.6;
        white-space: pre;
        margin: 0.5rem 0 1rem 0;
    }
    .preview-box::-webkit-scrollbar { width: 6px; }
    .preview-box::-webkit-scrollbar-track { background: #1e293b; border-radius: 3px; }
    .preview-box::-webkit-scrollbar-thumb { background: #3b82f6; border-radius: 3px; }
    .data-loaded-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        background: #dcfce7;
        border: 1px solid #86efac;
        color: #166534;
        padding: 0.35rem 0.9rem;
        border-radius: 100px;
        font-family: 'Work Sans', sans-serif;
        font-size: 0.78rem;
        font-weight: 600;
    }
    .stDownloadButton > button {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        color: white !important;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-family: 'Work Sans', sans-serif;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s;
        box-shadow: 0 4px 6px -1px rgba(59,130,246,0.3);
        width: 100%;
    }
    .stDownloadButton > button:hover {
        background: linear-gradient(135deg, #1e40af 0%, #2563eb 100%);
        box-shadow: 0 10px 15px -3px rgba(59,130,246,0.4);
        transform: translateY(-2px);
    }
    .graph-container {
        background: white;
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e293b 0%, #334155 100%);
    }
    [data-testid="stSidebar"] label { color: #e2e8f0 !important; font-family: 'Work Sans', sans-serif; }
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 { color: white !important; font-family: 'Work Sans', sans-serif; }
    .fetch-card {
        background: linear-gradient(135deg, #eff6ff 0%, #e0f2fe 100%);
        border: 2px dashed #93c5fd;
        border-radius: 12px;
        padding: 2rem;
        text-align: center;
        margin: 1rem 0;
    }
    hr {
        margin: 2rem 0;
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #3b82f6, transparent);
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# SESSION STATE — initialise ALL keys once at top
# This is the critical fix: every piece of state is declared
# here so widget reruns never wipe them out.
# ============================================================

DEFAULTS = {
    # raw data
    "txt_content":      None,
    "source_label":     None,
    # parsed base dataframes (never mutated after conversion)
    "df_57_base":       None,
    "df_19_base":       None,
    # conversion metadata
    "conversion_done":  False,
    "conversion_time":  None,
    "num_records":      0,
    # label attached during conversion
    "label_value":      None,
    # which tab/source is active
    "active_source":    "📁 Upload TXT File",
    # api fetch message
    "fetch_msg":        None,
    "fetch_msg_type":   None,   # "success" | "error" | "warning"
}

for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ============================================================
# CONFIG
# ============================================================

LABEL_MAP = {
    "Normal_Mode(0)": 0,
    "Seal Failure(1)": 1,
    "Bearing(2)": 2,
    "Shaft Misalignment(3)": 3,
    "Unbalance_impeller(4)": 4,
    "Cavitation(5)": 5,
}

# ============================================================
# CORE PARSING / CONVERSION FUNCTIONS
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
            for axis in ["X", "Y", "Z"]:
                while i < len(lines) and f"{axis} Axis" not in lines[i]:
                    i += 1
                i += 1  # skip axis header line
                peaks = {}
                while i < len(lines) and not lines[i].endswith("Axis:") and not time_re.match(lines[i]):
                    line   = lines[i]
                    tokens = line.split()
                    if tokens and re.match(r"^Parameter-(\d+)$", tokens[0]):
                        param_num = int(tokens[0].split("-")[1])
                        val = try_float(tokens, 1)
                        if   param_num == 1: row[f"Parameter-1_{axis}"] = val
                        elif param_num == 2: row[f"Parameter-2_{axis}"] = val
                        elif param_num == 3: row[f"Parameter-3_{axis}"] = val
                        i += 1
                        continue
                    if   line.startswith("RMS"):     row[f"Parameter-1_{axis}"] = try_float(tokens, 1)
                    elif line.startswith("PP"):       row[f"Parameter-2_{axis}"] = try_float(tokens, 1)
                    elif line.startswith("Kurtosis"): row[f"Parameter-3_{axis}"] = try_float(tokens, 1)
                    else:
                        m = peak_new_re.match(line) or peak_old_re.match(line)
                        if m:
                            peaks[int(m.group(1))] = (float(m.group(2)), float(m.group(3)))
                    i += 1
                for p in range(1, 9):
                    fp = 2 + p * 2
                    mp = 2 + p * 2 + 1
                    row[f"Parameter-{fp}_{axis}"] = peaks.get(p, (None, None))[0]
                    row[f"Parameter-{mp}_{axis}"] = peaks.get(p, (None, None))[1]
            rows.append(row)
        else:
            i += 1
    return pd.DataFrame(rows)


def reorder_columns_57(df: pd.DataFrame) -> pd.DataFrame:
    cols = ["Time"]
    for n in range(1, 4):
        for ax in ["X", "Y", "Z"]:
            cols.append(f"Parameter-{n}_{ax}")
    for p in range(1, 9):
        fp = 2 + p * 2
        mp = 2 + p * 2 + 1
        for ax in ["X", "Y", "Z"]: cols.append(f"Parameter-{fp}_{ax}")
        for ax in ["X", "Y", "Z"]: cols.append(f"Parameter-{mp}_{ax}")
    for c in cols:
        if c not in df.columns:
            df[c] = pd.NA
    return df[cols]


def convert_to_19_features(df: pd.DataFrame) -> pd.DataFrame:
    rows_19 = []
    has_label = "Label" in df.columns
    for _, row in df.iterrows():
        for axis in ["X", "Y", "Z"]:
            new_row = {"Time": row.get("Time", pd.NA)}
            for n in range(1, 4):
                new_row[f"Parameter-{n}"] = row.get(f"Parameter-{n}_{axis}", pd.NA)
            for p in range(1, 9):
                fp = 2 + p * 2
                mp = 2 + p * 2 + 1
                new_row[f"Parameter-{fp}"] = row.get(f"Parameter-{fp}_{axis}", pd.NA)
                new_row[f"Parameter-{mp}"] = row.get(f"Parameter-{mp}_{axis}", pd.NA)
            if has_label:
                new_row["Label"] = row["Label"]
            rows_19.append(new_row)
    cols_19 = ["Time"] + [f"Parameter-{n}" for n in range(1, 20)]
    df_19 = pd.DataFrame(rows_19)
    if has_label:
        cols_19.append("Label")
    return df_19[cols_19]


def create_professional_plot(df, columns, title, color_scheme):
    fig, ax = plt.subplots(figsize=(6, 3.5), facecolor='white')
    palettes = {
        'Parameter-1': ['#3b82f6', '#60a5fa', '#93c5fd'],
        'Parameter-2': ['#10b981', '#34d399', '#6ee7b7'],
        'Parameter-3': ['#f59e0b', '#fbbf24', '#fcd34d'],
    }
    clrs = palettes.get(color_scheme, ['#3b82f6', '#60a5fa', '#93c5fd'])
    for idx, c in enumerate(columns):
        if c in df.columns:
            ax.plot(df[c].values, label=c, linewidth=2, alpha=0.8, color=clrs[idx % len(clrs)])
    ax.set_title(title, fontsize=12, fontweight='bold', color='#1e293b', pad=15)
    ax.set_xlabel('Sample', fontsize=9, color='#64748b')
    ax.set_ylabel('Value', fontsize=9, color='#64748b')
    ax.legend(fontsize=8, framealpha=0.9, loc='best')
    ax.grid(True, alpha=0.2, linestyle='--', linewidth=0.5)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#cbd5e1')
    ax.spines['bottom'].set_color('#cbd5e1')
    ax.tick_params(labelsize=8, colors='#64748b')
    fig.tight_layout()
    return fig


def do_conversion(txt: str, label_value=None):
    """
    Parse → reorder → store in session_state.
    Returns (success: bool, error_msg: str|None)
    """
    t0 = time.time()
    try:
        df_raw = parse_vibration(txt)
    except Exception as e:
        return False, f"Parse error: {e}"

    if df_raw.empty:
        return False, "No vibration records could be parsed. Check the file format."

    df_57 = reorder_columns_57(df_raw.copy())
    if label_value is not None:
        df_57["Label"] = label_value

    df_19 = convert_to_19_features(df_57)

    st.session_state.df_57_base      = df_57
    st.session_state.df_19_base      = df_19
    st.session_state.conversion_done = True
    st.session_state.conversion_time = round(time.time() - t0, 2)
    st.session_state.num_records     = len(df_57)
    st.session_state.label_value     = label_value
    return True, None


def clear_data():
    """Reset all data-related session state."""
    for k in ["txt_content", "source_label", "df_57_base", "df_19_base",
              "conversion_done", "conversion_time", "num_records",
              "label_value", "fetch_msg", "fetch_msg_type"]:
        st.session_state[k] = DEFAULTS.get(k, None)

# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.markdown("## ⚙️ Configuration")
st.sidebar.markdown("---")

file_prefix = st.sidebar.text_input(
    "📝 Output File Prefix (optional)",
    placeholder="e.g., test_data",
    help="Leave empty for auto-timestamped name",
    key="file_prefix_input",
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🔌 API Server")
api_base = "https://pumpdata.duckdns.org/api"

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style="background:rgba(59,130,246,0.1);padding:1rem;border-radius:8px;border-left:3px solid #3b82f6;">
    <p style="color:#e2e8f0;margin:0;font-size:0.85rem;">
        <strong>📌 Output Formats:</strong><br>
        • 57-feature CSV (Time + Parameter-1..19 × X,Y,Z)<br>
        • 19-feature CSV (X,Y,Z stacked rows)
    </p>
</div>
""", unsafe_allow_html=True)

if st.sidebar.button("🗑️ Clear All Data", use_container_width=True, key="sidebar_clear"):
    clear_data()
    st.rerun()

# ============================================================
# HEADER
# ============================================================

st.markdown('<h1 class="custom-header">Vibration Data Converter</h1>', unsafe_allow_html=True)
st.markdown('<p class="custom-subtitle">Process device vibration logs into structured data</p>', unsafe_allow_html=True)

st.markdown("""
<div class="pipeline-banner">
    <div style="display:flex;align-items:center;gap:0.6rem;flex-wrap:wrap;">
        <span style="color:#64748b;font-size:1rem;">⚡</span>
        <span class="pipe-step">Device Simulator</span>
        <span style="color:#475569;">→</span>
        <span class="pipe-step">FastAPI Ingestion</span>
        <span style="color:#475569;">→</span>
        <span class="pipe-step" style="background:rgba(59,130,246,0.35);border-color:rgba(59,130,246,0.6);color:#bfdbfe;">
            Converter UI ◀ You are here
        </span>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# SECTION 1 — DATA SOURCE
# ============================================================

st.markdown('<h3 class="section-header">① Select Data Source</h3>', unsafe_allow_html=True)

source_choice = st.radio(
    "Data source",
    ["📁 Upload TXT File", "📡 Fetch from Device Simulator"],
    horizontal=True,
    key="source_radio",
    label_visibility="collapsed",
)

# ============================================================
# SECTION 2 — LOAD DATA
# ============================================================

st.markdown('<h3 class="section-header">② Load Data</h3>', unsafe_allow_html=True)

# ── PATH A: Upload ────────────────────────────────────────────
if source_choice == "📁 Upload TXT File":
    st.markdown('<div class="info-box">📁 Upload one or more vibration TXT files to begin processing</div>', unsafe_allow_html=True)

    uploaded_files = st.file_uploader(
        "Select Files",
        type=["txt"],
        accept_multiple_files=True,
        key="file_uploader",
        help="Upload one or more vibration data files in TXT format",
        label_visibility="collapsed",
    )

    if uploaded_files:
        combined = ""
        for f in uploaded_files:
            combined += f.read().decode("utf-8", errors="replace") + "\n"

        # Only update state if the content actually changed (avoid wiping on slider reruns)
        new_label = f"{len(uploaded_files)} file(s) uploaded"
        if st.session_state.txt_content != combined:
            st.session_state.txt_content     = combined
            st.session_state.source_label    = new_label
            # Reset conversion when new file is loaded
            st.session_state.conversion_done = False
            st.session_state.df_57_base      = None
            st.session_state.df_19_base      = None

# ── PATH B: Fetch from API ─────────────────────────────────────
else:
    st.markdown('<div class="fetch-card">', unsafe_allow_html=True)
    st.markdown(f"""
    <p style="font-family:'Work Sans',sans-serif;color:#1e40af;font-size:1rem;margin-bottom:0.3rem;">
        <strong>📡 Device Simulator API</strong>
    </p>
    <p style="font-family:'Work Sans',sans-serif;color:#3b82f6;font-size:0.85rem;margin-bottom:1.2rem;">
        Endpoint: <code style="background:#dbeafe;padding:2px 6px;border-radius:4px;">{api_base}/latest</code>
    </p>
    """, unsafe_allow_html=True)

    col_f, col_c = st.columns([3, 1])
    with col_f:
        fetch_clicked = st.button("📡 Fetch Latest Device Data", use_container_width=True, key="fetch_btn")
    with col_c:
        if st.button("🗑 Clear", use_container_width=True, key="inline_clear_btn"):
            clear_data()
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    # Show any previous fetch message
    if st.session_state.fetch_msg:
        mtype = st.session_state.fetch_msg_type
        css   = "success-box" if mtype == "success" else ("error-box" if mtype == "error" else "warning-box")
        st.markdown(f'<div class="{css}">{st.session_state.fetch_msg}</div>', unsafe_allow_html=True)

    if fetch_clicked:
        with st.spinner("🔄 Connecting to ingestion service…"):
            try:
                resp = requests.get(f"{api_base}/latest", timeout=15)
                if resp.status_code == 200:
                    payload = resp.json()
                    content = payload.get("content", "").strip()
                    if content:
                        st.session_state.txt_content     = content
                        st.session_state.source_label    = "Device Simulator API"
                        st.session_state.conversion_done = False
                        st.session_state.df_57_base      = None
                        st.session_state.df_19_base      = None
                        st.session_state.fetch_msg       = "✅ Data fetched successfully from device simulator!"
                        st.session_state.fetch_msg_type  = "success"
                    else:
                        st.session_state.fetch_msg      = "ℹ️ No device data available yet. Run the Device Simulator first."
                        st.session_state.fetch_msg_type = "warning"
                else:
                    st.session_state.fetch_msg      = f"⚠️ Server returned status {resp.status_code}. Check the ingestion service."
                    st.session_state.fetch_msg_type = "error"
            except requests.exceptions.ConnectionError:
                st.session_state.fetch_msg      = f"🔌 Unable to connect to <strong>{api_base}</strong>. Ensure api_server.py is running."
                st.session_state.fetch_msg_type = "error"
            except requests.exceptions.Timeout:
                st.session_state.fetch_msg      = "⏱️ Request timed out. The server may be busy — please retry."
                st.session_state.fetch_msg_type = "error"
            except Exception as e:
                st.session_state.fetch_msg      = f"❌ Unexpected error: {e}"
                st.session_state.fetch_msg_type = "error"
        st.rerun()

# ============================================================
# SECTION 3 — TXT PREVIEW  (only if data is loaded)
# ============================================================

if st.session_state.txt_content:
    txt = st.session_state.txt_content

    st.markdown('<h3 class="section-header">③ Data Preview</h3>', unsafe_allow_html=True)

    record_est = txt.count("#Vibration Value")
    line_count = txt.count("\n")
    sz_kb      = len(txt) / 1024

    col_badge, col_s1, col_s2, col_s3 = st.columns([2, 1, 1, 1])
    with col_badge:
        st.markdown(f"""
        <div style="padding-top:0.6rem;">
            <span class="data-loaded-badge">✅ {st.session_state.source_label}</span>
        </div>""", unsafe_allow_html=True)
    with col_s1:
        st.metric("Records", f"{record_est:,}")
    with col_s2:
        st.metric("Lines", f"{line_count:,}")
    with col_s3:
        st.metric("Size", f"{sz_kb:.1f} KB" if sz_kb < 1024 else f"{sz_kb/1024:.2f} MB")

    preview_text = txt[:2000] + ("\n…[truncated]" if len(txt) > 2000 else "")
    st.markdown("**TXT Preview** (first 2 000 characters)")
    st.markdown(f'<div class="preview-box">{preview_text}</div>', unsafe_allow_html=True)

    # ============================================================
    # SECTION 4 — LABEL + CONVERT
    # Only shown when data is loaded but NOT yet converted
    # ============================================================

    if not st.session_state.conversion_done:
        st.markdown('<h3 class="section-header">④ Convert to CSV</h3>', unsafe_allow_html=True)

        with st.expander("🏷️ Label Configuration (optional — for ML training)", expanded=False):
            use_label = st.checkbox("Attach a label column", value=False, key="chk_use_label")
            lv = None
            if use_label:
                lv = LABEL_MAP[st.selectbox("Label Type", list(LABEL_MAP.keys()), key="sel_label")]
            st.markdown('<div class="info-box">Labels are appended as an integer column to both CSV exports.</div>', unsafe_allow_html=True)

        col_conv, _ = st.columns([1, 2])
        with col_conv:
            convert_clicked = st.button("🔄 Convert to CSV", use_container_width=True, key="convert_btn")

        if convert_clicked:
            lv = st.session_state.get("sel_label", None)
            # re-resolve label value
            label_val = None
            if st.session_state.get("chk_use_label", False):
                raw = st.session_state.get("sel_label", list(LABEL_MAP.keys())[0])
                label_val = LABEL_MAP.get(raw, 0)

            with st.spinner("⚙️ Parsing and converting vibration data…"):
                ok, err = do_conversion(txt, label_val)

            if ok:
                st.markdown('<div class="success-box">✅ Conversion successful! Results are shown below.</div>', unsafe_allow_html=True)
                st.rerun()   # rerun so results section renders cleanly
            else:
                st.markdown(f'<div class="error-box">❌ Conversion failed: {err}</div>', unsafe_allow_html=True)

# ============================================================
# SECTION 5 — RESULTS  (persists across all reruns)
# ============================================================

if st.session_state.conversion_done and st.session_state.df_57_base is not None:

    df_57_base = st.session_state.df_57_base
    df_19_base = st.session_state.df_19_base
    ct         = st.session_state.conversion_time

    st.markdown("---")

    # Summary banner
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#1e293b 0%,#334155 100%);
                border-radius:16px;padding:2rem;margin:1rem 0;">
        <h2 style="color:white;font-family:'Work Sans',sans-serif;margin:0 0 0.4rem;font-size:1.8rem;">
            📊 Conversion Results
        </h2>
        <p style="color:#94a3b8;margin:0;font-size:0.9rem;">
            Processed in {ct}s &nbsp;·&nbsp;
            {st.session_state.num_records:,} records &nbsp;·&nbsp;
            {len(df_57_base.columns)} columns (57-feat) &nbsp;·&nbsp;
            {len(df_19_base):,} rows (19-feat)
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Time Window ─────────────────────────────────────────────
    st.markdown('<h3 class="section-header">⏱️ Time Window Selection</h3>', unsafe_allow_html=True)

    # Build datetime index once (from base df, never from filtered)
    df_57_base["Time_dt"] = pd.to_datetime(df_57_base["Time"], format="%d/%m/%Y %H:%M:%S")
    time_list = df_57_base["Time_dt"].tolist()
    tmin = df_57_base["Time_dt"].min().to_pydatetime()
    tmax = df_57_base["Time_dt"].max().to_pydatetime()
    n    = len(time_list)

    sel_method = st.radio(
        "Selection Method",
        ["Slider (Quick)", "Precise Time Input"],
        horizontal=True,
        key="sel_method",   # stable key — value preserved across reruns
    )

    if sel_method == "Slider (Quick)":
        col_sl, col_met = st.columns([3, 1])
        with col_sl:
            # Key is stable → slider position is preserved on every rerun
            start_idx, end_idx = st.slider(
                "Select time range by sample index",
                min_value=0,
                max_value=n - 1,
                value=(0, n - 1),
                key="time_slider",       # stable key
            )
            start_dt = time_list[start_idx]
            end_dt   = time_list[end_idx]
            st.caption(
                f"📅 **Start:** {start_dt.strftime('%d/%m/%Y %H:%M:%S')} "
                f"| **End:** {end_dt.strftime('%d/%m/%Y %H:%M:%S')}"
            )
        with col_met:
            st.metric("Total Samples", n)
            st.metric("Selected", end_idx - start_idx + 1)

    else:  # Precise Time Input
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            start_date = st.date_input("Start Date", value=tmin.date(),
                                       min_value=tmin.date(), max_value=tmax.date(), key="prec_sd")
            start_time = st.time_input("Start Time", value=tmin.time(), key="prec_st")
            start_dt   = datetime.combine(start_date, start_time)
        with col2:
            end_date = st.date_input("End Date", value=tmax.date(),
                                     min_value=tmin.date(), max_value=tmax.date(), key="prec_ed")
            end_time = st.time_input("End Time", value=tmax.time(), key="prec_et")
            end_dt   = datetime.combine(end_date, end_time)
        with col3:
            sel_n = len(df_57_base[
                (df_57_base["Time_dt"] >= start_dt) & (df_57_base["Time_dt"] <= end_dt)
            ])
            st.metric("Total Samples", n)
            st.metric("Selected", sel_n)

        if start_dt > end_dt:
            st.markdown('<div class="error-box">⚠️ Start time must be before end time!</div>', unsafe_allow_html=True)
            start_dt, end_dt = tmin, tmax

    # ── Apply time filter (in-memory, never re-parses) ───────────
    if sel_method == "Slider (Quick)":
        mask     = (df_57_base["Time_dt"] >= start_dt) & (df_57_base["Time_dt"] <= end_dt)
    else:
        mask     = (df_57_base["Time_dt"] >= start_dt) & (df_57_base["Time_dt"] <= end_dt)

    df_57_f = df_57_base[mask].drop(columns="Time_dt").reset_index(drop=True)
    df_19_f = convert_to_19_features(df_57_f)

    # ── Visualizations ───────────────────────────────────────────
    st.markdown('<h3 class="section-header">📈 Feature Visualization</h3>', unsafe_allow_html=True)

    if df_57_f.empty:
        st.markdown('<div class="warning-box">⚠️ No data in selected time window. Adjust the slider.</div>', unsafe_allow_html=True)
    else:
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown('<div class="graph-container">', unsafe_allow_html=True)
            st.pyplot(create_professional_plot(
                df_57_f, ["Parameter-1_X","Parameter-1_Y","Parameter-1_Z"],
                "Parameter-1 Values", "Parameter-1"), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="graph-container">', unsafe_allow_html=True)
            st.pyplot(create_professional_plot(
                df_57_f, ["Parameter-3_X","Parameter-3_Y","Parameter-3_Z"],
                "Parameter-3 Values", "Parameter-3"), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with c3:
            st.markdown('<div class="graph-container">', unsafe_allow_html=True)
            st.pyplot(create_professional_plot(
                df_57_f, ["Parameter-2_X","Parameter-2_Y","Parameter-2_Z"],
                "Parameter-2 Values", "Parameter-2"), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

    # ── Data Previews ─────────────────────────────────────────────
    st.markdown('<h3 class="section-header">📄 57-Feature Preview</h3>', unsafe_allow_html=True)
    st.dataframe(df_57_f, height=300, use_container_width=True)

    st.markdown('<h3 class="section-header">📄 19-Feature Preview</h3>', unsafe_allow_html=True)
    st.markdown('<div class="info-box">ℹ️ Each original row expands to 3 rows (X, Y, Z) with the same timestamp.</div>', unsafe_allow_html=True)
    st.dataframe(df_19_f, height=300, use_container_width=True)

    # ── Export ────────────────────────────────────────────────────
    st.markdown('<h3 class="section-header">⑥ Export</h3>', unsafe_allow_html=True)

    if df_57_f.empty:
        st.markdown('<div class="warning-box">⚠️ The current selection is empty — adjust the time window before downloading.</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="success-box">✅ Files ready for download</div>', unsafe_allow_html=True)

        ts_suffix = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = file_prefix if file_prefix else f"converted_{ts_suffix}"
        fname_57  = f"{base_name}_57.csv"
        fname_19  = f"{base_name}_19.csv"

        dl1, dl2 = st.columns(2)
        with dl1:
            st.download_button(
                label=f"📥 Download {fname_57}",
                data=df_57_f.to_csv(index=False),
                file_name=fname_57,
                mime="text/csv",
                key="dl_57",
                use_container_width=True,
            )
        with dl2:
            st.download_button(
                label=f"📥 Download {fname_19}",
                data=df_19_f.to_csv(index=False),
                file_name=fname_19,
                mime="text/csv",
                key="dl_19",
                use_container_width=True,
            )

        st.markdown(f"""
        <div style="background:white;border-radius:10px;padding:1rem 1.5rem;
                    border:1px solid #e2e8f0;margin:1rem 0;
                    font-family:'Work Sans',sans-serif;font-size:0.85rem;color:#64748b;">
            ⏱️ Converted in <strong>{ct}s</strong> &nbsp;·&nbsp;
            📄 <strong>{len(df_57_f):,}</strong> records (57-feat) &nbsp;·&nbsp;
            📄 <strong>{len(df_19_f):,}</strong> rows (19-feat) &nbsp;·&nbsp;
            📊 <strong>{len(df_57_f.columns)}</strong> columns
        </div>
        """, unsafe_allow_html=True)

    # ── Re-convert with new label ─────────────────────────────────
    st.markdown("---")
    with st.expander("🔁 Re-convert with different label", expanded=False):
        st.markdown('<div class="info-box">Re-running conversion will apply a new label to the full dataset.</div>', unsafe_allow_html=True)
        use_label2 = st.checkbox("Attach label", value=False, key="chk_relabel")
        lv2        = None
        if use_label2:
            lv2 = LABEL_MAP[st.selectbox("Label Type", list(LABEL_MAP.keys()), key="sel_relabel")]
        if st.button("🔄 Re-convert", key="reconvert_btn"):
            with st.spinner("Re-converting…"):
                ok, err = do_conversion(st.session_state.txt_content, lv2 if use_label2 else None)
            if ok:
                st.markdown('<div class="success-box">✅ Re-conversion successful!</div>', unsafe_allow_html=True)
                st.rerun()
            else:
                st.markdown(f'<div class="error-box">❌ {err}</div>', unsafe_allow_html=True)

# ============================================================
# LANDING STATE — nothing loaded yet
# ============================================================

elif not st.session_state.txt_content:
    st.markdown("""
    <div style="text-align:center;padding:4rem 2rem;background:white;border-radius:16px;
                box-shadow:0 4px 6px -1px rgba(0,0,0,0.1);margin:2rem 0;">
        <div style="font-size:3rem;margin-bottom:1rem;">📡</div>
        <h2 style="color:#1e3a8a;font-family:'Work Sans',sans-serif;margin-bottom:1rem;">
            Ready to Process Vibration Data
        </h2>
        <p style="color:#64748b;font-size:1rem;max-width:600px;margin:0 auto 1.5rem;">
            Upload a TXT file from your computer or fetch the latest data directly
            from the device simulator API to get started.
        </p>
        <div style="display:inline-flex;gap:1rem;flex-wrap:wrap;justify-content:center;">
            <div style="background:#eff6ff;border:1px solid #bfdbfe;border-radius:10px;
                        padding:1rem 1.5rem;max-width:220px;text-align:left;">
                <div style="font-size:1.5rem;margin-bottom:0.4rem;">📁</div>
                <strong style="color:#1e40af;">Upload TXT</strong>
                <p style="color:#3b82f6;font-size:0.82rem;margin:0.3rem 0 0;">
                    Manual upload of one or more local vibration log files
                </p>
            </div>
            <div style="background:#f0fdf4;border:1px solid #86efac;border-radius:10px;
                        padding:1rem 1.5rem;max-width:220px;text-align:left;">
                <div style="font-size:1.5rem;margin-bottom:0.4rem;">📡</div>
                <strong style="color:#166534;">Fetch from API</strong>
                <p style="color:#16a34a;font-size:0.82rem;margin:0.3rem 0 0;">
                    Pull latest data from the FastAPI ingestion service
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# FOOTER
# ============================================================

st.markdown("---")
st.markdown("""
<div style="text-align:center;color:#94a3b8;font-size:0.85rem;
            padding:1rem;font-family:'Work Sans',sans-serif;">
    Vibration Data Converter v2.1 · Professional Edition · pump_project pipeline
</div>
""", unsafe_allow_html=True)