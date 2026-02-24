import streamlit as st
import random
import time
import json
import requests
from datetime import datetime, timedelta
from io import StringIO

# ─── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Device Simulator",
    page_icon="📡",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Barlow:wght@300;400;500;600;700&family=Barlow+Condensed:wght@400;600;700&display=swap');

/* ── Root Variables ── */
:root {
    --bg-deep:       #0a0e14;
    --bg-panel:      #0f1520;
    --bg-card:       #141c2b;
    --bg-card-hover: #18233a;
    --border:        #1e2d45;
    --border-bright: #2a4060;
    --accent:        #00d4ff;
    --accent-dim:    #0098bb;
    --accent-glow:   rgba(0, 212, 255, 0.18);
    --green:         #00ff9d;
    --green-dim:     rgba(0, 255, 157, 0.12);
    --amber:         #ffb830;
    --red:           #ff4757;
    --text-primary:  #e8f4fd;
    --text-secondary:#7a9bbf;
    --text-muted:    #3d5a78;
    --mono:          'Share Tech Mono', monospace;
    --sans:          'Barlow', sans-serif;
    --cond:          'Barlow Condensed', sans-serif;
}

/* ── Global Reset ── */
html, body, [class*="css"] {
    font-family: var(--sans);
    background-color: var(--bg-deep);
    color: var(--text-primary);
}

.stApp {
    background: var(--bg-deep);
    background-image:
        radial-gradient(ellipse at 20% 0%, rgba(0, 212, 255, 0.06) 0%, transparent 50%),
        radial-gradient(ellipse at 80% 100%, rgba(0, 100, 180, 0.08) 0%, transparent 50%);
    min-height: 100vh;
}

/* ── Hide Streamlit Branding ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding: 1rem 1rem 3rem 1rem;
    max-width: 540px;
    margin: 0 auto;
}

/* ── Header ── */
.device-header {
    text-align: center;
    padding: 2.5rem 1rem 1.5rem;
    position: relative;
}
.device-header::before {
    content: '';
    position: absolute;
    top: 0; left: 50%;
    transform: translateX(-50%);
    width: 1px;
    height: 2.5rem;
    background: linear-gradient(to bottom, transparent, var(--accent));
}
.device-eyebrow {
    font-family: var(--mono);
    font-size: 0.65rem;
    letter-spacing: 0.25em;
    color: var(--accent);
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}
.device-title {
    font-family: var(--cond);
    font-size: 2.4rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: var(--text-primary);
    line-height: 1;
    margin-bottom: 0.4rem;
}
.device-subtitle {
    font-size: 0.82rem;
    color: var(--text-secondary);
    font-weight: 300;
    letter-spacing: 0.04em;
}
.status-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    margin-top: 1rem;
    padding: 0.3rem 0.9rem;
    border-radius: 100px;
    font-family: var(--mono);
    font-size: 0.65rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    border: 1px solid var(--border);
    background: var(--bg-card);
}
.status-badge.idle   { color: var(--text-secondary); }
.status-badge.online { color: var(--green); border-color: rgba(0,255,157,0.3); background: var(--green-dim); }
.status-badge.active { color: var(--amber); border-color: rgba(255,184,48,0.3); background: rgba(255,184,48,0.08); }
.dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: currentColor;
    animation: pulse-dot 1.6s ease-in-out infinite;
}
@keyframes pulse-dot {
    0%, 100% { opacity: 1; transform: scale(1); }
    50%       { opacity: 0.4; transform: scale(0.7); }
}

/* ── Cards ── */
.card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.4rem 1.2rem;
    margin-bottom: 1rem;
    position: relative;
    overflow: hidden;
}
.card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--accent-dim), transparent);
}
.card-label {
    font-family: var(--mono);
    font-size: 0.6rem;
    letter-spacing: 0.2em;
    color: var(--accent);
    text-transform: uppercase;
    margin-bottom: 1.1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.card-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
}

/* ── Streamlit Input Overrides ── */
.stTextInput > div > div > input {
    background: var(--bg-panel) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text-primary) !important;
    font-family: var(--mono) !important;
    font-size: 0.9rem !important;
    padding: 0.7rem 1rem !important;
    caret-color: var(--accent);
    transition: border-color 0.2s;
}
.stTextInput > div > div > input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px var(--accent-glow) !important;
}
.stTextInput > div > div > input::placeholder { color: var(--text-muted) !important; }

.stSelectbox > div > div {
    background: var(--bg-panel) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text-primary) !important;
}
.stSelectbox > div > div:focus-within {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px var(--accent-glow) !important;
}

/* ── Labels ── */
.stTextInput label, .stSelectbox label {
    font-family: var(--mono) !important;
    font-size: 0.65rem !important;
    letter-spacing: 0.12em !important;
    color: var(--text-secondary) !important;
    text-transform: uppercase !important;
    margin-bottom: 0.4rem !important;
}

/* ── Primary Button ── */
.stButton > button {
    width: 100% !important;
    background: linear-gradient(135deg, #00c4ef, #0076a8) !important;
    color: #fff !important;
    font-family: var(--cond) !important;
    font-size: 1.05rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.85rem 1.5rem !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 20px rgba(0, 196, 239, 0.25) !important;
    position: relative !important;
    overflow: hidden !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 28px rgba(0, 196, 239, 0.4) !important;
    background: linear-gradient(135deg, #1ad4ff, #0090c8) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}

/* ── Download Button ── */
.stDownloadButton > button {
    width: 100% !important;
    background: transparent !important;
    color: var(--accent) !important;
    font-family: var(--cond) !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    border: 1px solid var(--accent-dim) !important;
    border-radius: 10px !important;
    padding: 0.75rem 1.5rem !important;
    transition: all 0.2s !important;
}
.stDownloadButton > button:hover {
    background: var(--accent-glow) !important;
    border-color: var(--accent) !important;
}

/* ── Progress Bar ── */
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #0076a8, #00d4ff) !important;
    border-radius: 100px !important;
    box-shadow: 0 0 10px rgba(0, 212, 255, 0.5) !important;
}
.stProgress > div > div > div {
    background: var(--border) !important;
    border-radius: 100px !important;
    height: 6px !important;
}

/* ── Metric Grid ── */
.metric-grid {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 0.7rem;
    margin: 0.5rem 0;
}
.metric-box {
    background: var(--bg-panel);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 0.8rem 0.6rem;
    text-align: center;
}
.metric-value {
    font-family: var(--mono);
    font-size: 1.15rem;
    font-weight: 600;
    color: var(--accent);
    line-height: 1.1;
}
.metric-label {
    font-size: 0.6rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 0.25rem;
}

/* ── Axis Bars (visual decoration) ── */
.axis-row {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    margin: 0.35rem 0;
}
.axis-tag {
    font-family: var(--mono);
    font-size: 0.65rem;
    letter-spacing: 0.06em;
    color: var(--text-secondary);
    width: 1.2rem;
    flex-shrink: 0;
}
.axis-bar-bg {
    flex: 1;
    height: 4px;
    background: var(--border);
    border-radius: 100px;
    overflow: hidden;
}
.axis-bar-fill {
    height: 100%;
    border-radius: 100px;
    animation: bar-shimmer 2s ease-in-out infinite;
}
.axis-bar-fill.x { width: 72%; background: linear-gradient(90deg, #0076a8, #00d4ff); }
.axis-bar-fill.y { width: 45%; background: linear-gradient(90deg, #007a5e, #00ff9d); }
.axis-bar-fill.z { width: 88%; background: linear-gradient(90deg, #7a5200, #ffb830); }
@keyframes bar-shimmer {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.6; }
}

/* ── Info Row ── */
.info-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.5rem 0;
    border-bottom: 1px solid var(--border);
    font-size: 0.8rem;
}
.info-row:last-child { border-bottom: none; }
.info-key { color: var(--text-secondary); font-family: var(--mono); font-size: 0.7rem; letter-spacing: 0.08em; }
.info-val { color: var(--text-primary); font-family: var(--mono); font-size: 0.75rem; }

/* ── Success Banner ── */
.success-banner {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    background: var(--green-dim);
    border: 1px solid rgba(0, 255, 157, 0.3);
    border-radius: 10px;
    padding: 1rem 1.1rem;
    margin: 0.5rem 0 1rem;
}
.success-icon { font-size: 1.4rem; flex-shrink: 0; }
.success-text { font-size: 0.82rem; color: var(--green); font-family: var(--mono); letter-spacing: 0.04em; }

/* ── Warning Banner ── */
.warn-banner {
    background: rgba(255,184,48,0.08);
    border: 1px solid rgba(255,184,48,0.3);
    border-radius: 8px;
    padding: 0.7rem 1rem;
    font-size: 0.78rem;
    color: var(--amber);
    font-family: var(--mono);
}

/* ── Collecting Card ── */
.collecting-card {
    background: var(--bg-card);
    border: 1px solid var(--border-bright);
    border-radius: 12px;
    padding: 1.4rem 1.2rem;
    text-align: center;
    margin-bottom: 1rem;
}
.collecting-title {
    font-family: var(--cond);
    font-size: 0.8rem;
    letter-spacing: 0.2em;
    color: var(--accent);
    text-transform: uppercase;
    margin-bottom: 0.8rem;
}

/* ── Waveform Animation ── */
.waveform {
    display: flex;
    justify-content: center;
    align-items: flex-end;
    gap: 3px;
    height: 28px;
    margin: 0.8rem 0;
}
.wave-bar {
    width: 4px;
    background: var(--accent);
    border-radius: 2px;
    animation: wave 1.1s ease-in-out infinite;
    opacity: 0.7;
}
.wave-bar:nth-child(1)  { animation-delay: 0.00s; height: 30%; }
.wave-bar:nth-child(2)  { animation-delay: 0.10s; height: 60%; }
.wave-bar:nth-child(3)  { animation-delay: 0.20s; height: 90%; }
.wave-bar:nth-child(4)  { animation-delay: 0.30s; height: 50%; }
.wave-bar:nth-child(5)  { animation-delay: 0.40s; height: 80%; }
.wave-bar:nth-child(6)  { animation-delay: 0.50s; height: 40%; }
.wave-bar:nth-child(7)  { animation-delay: 0.60s; height: 70%; }
.wave-bar:nth-child(8)  { animation-delay: 0.70s; height: 100%; }
.wave-bar:nth-child(9)  { animation-delay: 0.60s; height: 60%; }
.wave-bar:nth-child(10) { animation-delay: 0.50s; height: 30%; }
.wave-bar:nth-child(11) { animation-delay: 0.40s; height: 85%; }
.wave-bar:nth-child(12) { animation-delay: 0.30s; height: 45%; }
@keyframes wave {
    0%, 100% { transform: scaleY(0.4); opacity: 0.4; }
    50%       { transform: scaleY(1.0); opacity: 1.0; }
}

/* ── Divider ── */
.h-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border), transparent);
    margin: 0.8rem 0;
}

/* ── File Size Hint ── */
.file-hint {
    font-family: var(--mono);
    font-size: 0.65rem;
    color: var(--text-muted);
    text-align: right;
    margin-top: -0.3rem;
    letter-spacing: 0.06em;
}

/* ── Toast ── */
.stAlert {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-bright) !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
}

/* ── Send button specific styling ── */
.send-btn > button {
    background: linear-gradient(135deg, #006622, #00cc44) !important;
    box-shadow: 0 4px 20px rgba(0, 204, 68, 0.2) !important;
}
.send-btn > button:hover {
    box-shadow: 0 6px 28px rgba(0, 204, 68, 0.35) !important;
    background: linear-gradient(135deg, #008830, #00ee55) !important;
}

</style>
""", unsafe_allow_html=True)

# ─── Session State ───────────────────────────────────────────────────────────────
if "generated_data" not in st.session_state:
    st.session_state.generated_data = None
if "generation_done" not in st.session_state:
    st.session_state.generation_done = False
if "device_status" not in st.session_state:
    st.session_state.device_status = "idle"
if "records_count" not in st.session_state:
    st.session_state.records_count = 0
if "time_range" not in st.session_state:
    st.session_state.time_range = ("", "")

# ─── Data Generation Logic ───────────────────────────────────────────────────────
def gen_axis_block(axis_name: str) -> str:
    lines = [f"{axis_name}:"]
    # Parameter-20 (stable baseline, 2 decimal places)
    if axis_name == "X Axis":
        p20 = round(random.uniform(-6, -5), 2)
    elif axis_name == "Y Axis":
        p20 = round(random.uniform(0.08, 0.12), 2)
    else:
        p20 = round(random.uniform(7.9, 8.1), 2)
    lines.append(f"Parameter-20 {p20}")
    # Noise parameters (2 decimal places)
    lines.append(f"Parameter-1 {round(random.uniform(0.05, 0.2), 2)}")
    lines.append(f"Parameter-2 {round(random.uniform(0.3, 1.5), 2)}")
    lines.append(f"Parameter-3 {round(random.uniform(-0.3, 1.5), 2)}")
    # Peaks 1–8 — each peak is a SINGLE line
    for i in range(1, 9):
        param_a = 4 + (i - 1) * 2   # 4,6,8,10,12,14,16,18
        param_b = 5 + (i - 1) * 2   # 5,7,9,11,13,15,17,19
        val_a = random.randint(10, 120)
        val_b = round(random.uniform(-45, -23), 2)
        lines.append(f"Peak {i} Parameter-{param_a} {val_a} Parameter-{param_b} {val_b}")
    return "\n".join(lines)


def generate_txt(device_name: str, sampling_rate: int, duration_hours: int) -> tuple[str, int]:
    total_records = int((duration_hours * 3600) / sampling_rate)
    start_time = datetime.now()
    buffer = StringIO()

    for i in range(total_records):
        ts = start_time + timedelta(seconds=i * sampling_rate)
        # Format: M/D/YYYY H:MM:SS AM/PM (no leading zeros, cross-platform Windows safe)
        month = str(ts.month)
        day   = str(ts.day)
        hour  = str(ts.hour % 12 or 12)
        ampm  = "AM" if ts.hour < 12 else "PM"
        ts_str = f"{month}/{day}/{ts.year} {hour}:{ts.strftime('%M')}:{ts.strftime('%S')} {ampm}"
        buffer.write("#Vibration Value\n")
        buffer.write(f"{ts_str} \n")
        buffer.write(gen_axis_block("X Axis"))
        buffer.write("\n\n")
        buffer.write(gen_axis_block("Y Axis"))
        buffer.write("\n\n")
        buffer.write(gen_axis_block("Z Axis"))
        buffer.write("\n\n")

    return buffer.getvalue(), total_records


def estimate_file_size_kb(duration_hours: int, sampling_rate: int) -> float:
    records = (duration_hours * 3600) / sampling_rate
    # ~420 bytes per record approximate
    return round(records * 420 / 1024, 1)


# ─── Header ─────────────────────────────────────────────────────────────────────
status_html = {
    "idle":       '<span class="status-badge idle"><span class="dot"></span>IDLE</span>',
    "collecting": '<span class="status-badge active"><span class="dot"></span>COLLECTING</span>',
    "ready":      '<span class="status-badge online"><span class="dot"></span>READY</span>',
}

st.markdown(f"""
<div class="device-header">
    <div class="device-eyebrow">SN-7742 · Industrial Vibration Unit</div>
    <div class="device-title">Device Simulator</div>
    <div class="device-subtitle">Simulate vibration sensor data collection</div>
    {status_html[st.session_state.device_status]}
</div>
""", unsafe_allow_html=True)

# ─── Live Axis Decoration (visual only) ─────────────────────────────────────────
st.markdown("""
<div class="card">
    <div class="card-label">⚡ Live Sensor Feed</div>
    <div class="axis-row">
        <span class="axis-tag">X</span>
        <div class="axis-bar-bg"><div class="axis-bar-fill x"></div></div>
        <span style="font-family:var(--mono);font-size:0.65rem;color:var(--text-muted);width:3.5rem;text-align:right;">-5.7423 g</span>
    </div>
    <div class="axis-row">
        <span class="axis-tag">Y</span>
        <div class="axis-bar-bg"><div class="axis-bar-fill y"></div></div>
        <span style="font-family:var(--mono);font-size:0.65rem;color:var(--text-muted);width:3.5rem;text-align:right;">0.0991 g</span>
    </div>
    <div class="axis-row">
        <span class="axis-tag">Z</span>
        <div class="axis-bar-bg"><div class="axis-bar-fill z"></div></div>
        <span style="font-family:var(--mono);font-size:0.65rem;color:var(--text-muted);width:3.5rem;text-align:right;">8.0241 g</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Configuration Card ──────────────────────────────────────────────────────────
st.markdown('<div class="card"><div class="card-label">⚙ Device Configuration</div>', unsafe_allow_html=True)

device_name = st.text_input(
    "Device Name",
    placeholder="Enter device ID",
    key="device_name_input",
)

rate_map = {
    "5 seconds":  5,
    "10 seconds": 10,
    "15 seconds": 15,
    "30 seconds": 30,
}
rate_label = st.selectbox("Sampling Rate", list(rate_map.keys()), key="rate_select")
sampling_rate = rate_map[rate_label]

duration_hours = st.selectbox(
    "Duration",
    [f"{h} hour{'s' if h > 1 else ''}" for h in range(1, 13)],
    key="dur_select",
)
duration_val = int(duration_hours.split()[0])

# File size estimate
est_kb = estimate_file_size_kb(duration_val, sampling_rate)
est_str = f"{est_kb:.0f} KB" if est_kb < 1024 else f"{est_kb/1024:.2f} MB"
records_preview = int((duration_val * 3600) / sampling_rate)

st.markdown(f"""
<div class="metric-grid" style="margin-top:0.8rem;">
    <div class="metric-box">
        <div class="metric-value">{records_preview:,}</div>
        <div class="metric-label">Records</div>
    </div>
    <div class="metric-box">
        <div class="metric-value">{sampling_rate}s</div>
        <div class="metric-label">Interval</div>
    </div>
    <div class="metric-box">
        <div class="metric-value">{est_str}</div>
        <div class="metric-label">Est. Size</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Warning for large datasets
if records_preview > 10000:
    st.markdown(f'<div class="warn-banner">⚠ Large dataset: {records_preview:,} records may take a moment to generate.</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ─── Start Button ────────────────────────────────────────────────────────────────
start_col, _ = st.columns([1, 0.01])
with start_col:
    start_clicked = st.button("▶  Start Data Collection", key="start_btn", use_container_width=True)

# ─── Simulation Logic ─────────────────────────────────────────────────────────────
if start_clicked:
    if not device_name.strip():
        st.markdown('<div class="warn-banner">⚠ Device Name is required before starting collection.</div>', unsafe_allow_html=True)
    else:
        st.session_state.generation_done = False
        st.session_state.generated_data = None
        st.session_state.device_status = "collecting"

        # Collecting UI
        st.markdown("""
        <div class="collecting-card">
            <div class="collecting-title">Collecting Telemetry</div>
            <div class="waveform">
                <div class="wave-bar"></div><div class="wave-bar"></div>
                <div class="wave-bar"></div><div class="wave-bar"></div>
                <div class="wave-bar"></div><div class="wave-bar"></div>
                <div class="wave-bar"></div><div class="wave-bar"></div>
                <div class="wave-bar"></div><div class="wave-bar"></div>
                <div class="wave-bar"></div><div class="wave-bar"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        prog_bar = st.progress(0)
        pct_text = st.empty()
        STEPS = 20

        for step in range(STEPS + 1):
            pct = step / STEPS
            prog_bar.progress(pct)
            pct_text.markdown(
                f'<p style="text-align:center;font-family:var(--mono);font-size:0.75rem;'
                f'color:var(--accent);letter-spacing:0.1em;">'
                f'{int(pct * 100)}% — Sampling sensor channels…</p>',
                unsafe_allow_html=True,
            )
            time.sleep(1)

        pct_text.empty()

        # Generate actual data
        txt_data, num_records = generate_txt(device_name.strip(), sampling_rate, duration_val)
        start_ts = datetime.now()
        end_ts   = start_ts + timedelta(hours=duration_val)

        st.session_state.generated_data = txt_data
        st.session_state.generation_done = True
        st.session_state.device_status = "ready"
        st.session_state.records_count = num_records
        st.session_state.time_range = (
            start_ts.strftime("%m/%d/%Y %I:%M %p"),
            end_ts.strftime("%m/%d/%Y %I:%M %p"),
        )
        st.rerun()

# ─── Results Section ─────────────────────────────────────────────────────────────
if st.session_state.generation_done and st.session_state.generated_data:
    t_start, t_end = st.session_state.time_range
    num_rec = st.session_state.records_count
    txt_size_kb = round(len(st.session_state.generated_data) / 1024, 1)

    st.markdown("""
    <div class="success-banner">
        <div class="success-icon">✅</div>
        <div class="success-text">Data collection complete — telemetry ready</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="card"><div class="card-label">📊 Collection Summary</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="info-row"><span class="info-key">Records Generated</span><span class="info-val">{num_rec:,}</span></div>
    <div class="info-row"><span class="info-key">Start Time</span><span class="info-val">{t_start}</span></div>
    <div class="info-row"><span class="info-key">End Time</span><span class="info-val">{t_end}</span></div>
    <div class="info-row"><span class="info-key">Sampling Rate</span><span class="info-val">{sampling_rate}s</span></div>
    <div class="info-row"><span class="info-key">File Size</span><span class="info-val">{txt_size_kb} KB</span></div>
    <div class="info-row"><span class="info-key">Device ID</span><span class="info-val">{device_name.strip()}</span></div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Action buttons
    st.markdown('<div class="card"><div class="card-label">🚀 Actions</div>', unsafe_allow_html=True)

    # Download
    fname = f"{device_name.strip()}_vibration_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    st.download_button(
        label="⬇  Download TXT File",
        data=st.session_state.generated_data,
        file_name=fname,
        mime="text/plain",
        use_container_width=True,
    )

    st.markdown('<div style="height:0.6rem"></div>', unsafe_allow_html=True)

    # Send button
    st.markdown('<div class="send-btn">', unsafe_allow_html=True)
    send_clicked = st.button("📡  Send to Processing Service", key="send_btn", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if send_clicked:
        SERVER_IP = "localhost"
        with st.spinner("Transmitting data to ingestion service…"):
            try:
                resp = requests.post(
                    f"http://{SERVER_IP}:8000/upload",
                    json={"content": st.session_state.generated_data},
                    timeout=30,
                )
                if resp.status_code == 200:
                    st.markdown("""
                    <div class="success-banner">
                        <div class="success-icon">📡</div>
                        <div class="success-text">Data successfully sent to processing service</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="warn-banner">⚠ Server returned status {resp.status_code}. Please retry.</div>', unsafe_allow_html=True)
            except requests.exceptions.ConnectionError:
                st.markdown('<div class="warn-banner">⚠ Could not reach processing service. Check that the server is running and retry.</div>', unsafe_allow_html=True)
            except requests.exceptions.Timeout:
                st.markdown('<div class="warn-banner">⚠ Request timed out. The server may be busy — please retry.</div>', unsafe_allow_html=True)
            except Exception as e:
                st.markdown(f'<div class="warn-banner">⚠ Unexpected error: {e}. Please retry.</div>', unsafe_allow_html=True)

# ─── Footer ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:2rem 0 1rem;font-family:var(--mono);
            font-size:0.58rem;letter-spacing:0.12em;color:var(--text-muted);">
    PUMP_PROJECT · DEVICE SIMULATOR v1.0 · INDUSTRIAL TELEMETRY UNIT
</div>
""", unsafe_allow_html=True)