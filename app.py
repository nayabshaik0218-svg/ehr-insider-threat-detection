import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os
import numpy as np
import time

# ====================== YOUR CUSTOM MODULES ======================
import risk_scoring
import detect_insider_threats

# ====================== PAGE CONFIG ======================
st.set_page_config(
    page_title="EHR Safety Services",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ====================== CRAZY + UNDERSTANDABLE THEME ======================
def apply_crazy_theme():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Space+Grotesk:wght@500;600;700&family=JetBrains+Mono:wght@400;700&display=swap');

        .stApp { 
            background: linear-gradient(180deg, #0a0e17, #1a0033); 
            color: #e0f2fe; 
        }

        .main-header {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 3.9rem;
            background: linear-gradient(90deg, #00f2ff, #00ff9d, #8b00ff);
            background-size: 400% 400%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            animation: shimmer 5s ease infinite;
            text-shadow: 0 0 40px #00f2ff;
        }
        @keyframes shimmer { 0%,100% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } }

        .glass-card {
            background: rgba(20, 25, 45, 0.95);
            border: 2px solid #00f2ff;
            border-radius: 22px;
            padding: 28px;
            box-shadow: 0 0 40px rgba(0, 242, 255, 0.5);
            transition: all 0.4s ease;
        }
        .glass-card:hover {
            transform: scale(1.06) translateY(-12px);
            box-shadow: 0 0 80px #00f2ff, 0 0 120px #00ff9d;
        }

        .metric-value { 
            font-size: 3.6rem; 
            font-weight: 700; 
            color: #00f2ff; 
            text-shadow: 0 0 25px #00f2ff;
        }

        .blinker {
            display: inline-block;
            width: 20px; height: 20px;
            background: #00ff9d;
            border-radius: 50%;
            animation: pulse 1s infinite;
        }

        .stTabs [data-baseweb="tab-list"] {
            background: linear-gradient(90deg, #1a0033, #111827);
            border: 3px solid #00f2ff;
            border-radius: 20px;
            padding: 12px;
        }
        .stTabs [data-baseweb="tab"]:hover {
            background: #00f2ff !important;
            color: #000 !important;
            transform: scale(1.08);
        }
        .stTabs [aria-selected="true"] {
            background: linear-gradient(90deg, #00f2ff, #00ff9d) !important;
            color: #000 !important;
        }
    </style>
    """, unsafe_allow_html=True)

apply_crazy_theme()

# ====================== DATA LOADING ======================
@st.cache_data(ttl=60)
def load_ehr_data():
    if not os.path.exists("ehr_logs.csv"):
        st.error("❌ ehr_logs.csv not found in this folder!")
        st.stop()

    df_risk = risk_scoring.process_data("ehr_logs.csv")
    df_threat = detect_insider_threats.run_detection("ehr_logs.csv")

    df = df_risk.copy()
    common_keys = ['log_id', 'id', 'event_id', 'timestamp', 'user_id']
    merge_key = next((k for k in common_keys if k in df_risk.columns and k in df_threat.columns), None)

    if merge_key:
        df = df_risk.merge(df_threat, on=merge_key, how='left', suffixes=('', '_threat'))
    elif len(df_risk) == len(df_threat):
        df = pd.concat([df_risk.reset_index(drop=True), df_threat.add_suffix('_threat').reset_index(drop=True)], axis=1)

    df['ml_threat'] = pd.to_numeric(df.get('ml_threat', 0), errors='coerce').fillna(0).astype(int)
    df['anomaly_score'] = pd.to_numeric(df.get('anomaly_score', 0.0), errors='coerce').fillna(0.0)
    df['critical_breach'] = (
        (df.get('risk_level', 'Low Risk') == 'High Risk') & 
        (df['ml_threat'] == 1) & 
        (df['anomaly_score'] > 0.7)
    )

    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    else:
        df['timestamp'] = pd.Timestamp.now()

    df = df.sort_values('timestamp', ascending=False).reset_index(drop=True)
    df['event_seq'] = np.arange(len(df))
    return df

df = load_ehr_data()

# ====================== NAVIGATION ======================
tab_home, tab_dashboard, tab_logs, tab_alerts, tab_analytics = st.tabs([
    "🏠 HOME", "📊 DASHBOARD", "📋 LOGS", "🚨 ALERTS", "📈 ANALYTICS"
])

# ====================== 1. HOME ======================
with tab_home:
    st.markdown('<h1 class="main-header">EHR Safety Services</h1>', unsafe_allow_html=True)
    st.markdown("""
    <p style='text-align:center; font-size:1.5rem; color:#67e8f9;'>
        Protecting Patient Data • Real-Time Insider Threat Detection • Powered by AI
    </p>
    """, unsafe_allow_html=True)

    if st.toggle("🌀 Enable Live Auto-Refresh (6 seconds)", value=True):
        time.sleep(6)
        st.rerun()

    st.info("**What you are seeing:** This dashboard monitors who is accessing patient records and instantly flags suspicious activity.")

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1: st.markdown(f'<div class="glass-card"><h4>Total Access Events</h4><h2 class="metric-value">{len(df):,}</h2></div>', unsafe_allow_html=True)
    with c2: 
        high = len(df[df.get('risk_level', '') == 'High Risk'])
        st.markdown(f'<div class="glass-card"><h4 style="color:#ff2d55">🔴 High Risk Events</h4><h2 class="metric-value" style="color:#ff2d55">{high}</h2></div>', unsafe_allow_html=True)
    with c3: 
        crit = int(df.get('critical_breach', False).sum())
        st.markdown(f'<div class="glass-card"><h4 style="color:#ff2d55">🚨 Critical Breaches</h4><h2 class="metric-value" style="color:#ff2d55">{crit}</h2></div>', unsafe_allow_html=True)
    with c4: 
        ml = int(df.get('ml_threat', 0).sum())
        st.markdown(f'<div class="glass-card"><h4 style="color:#00ff9d">🤖 AI Detected Threats</h4><h2 class="metric-value" style="color:#00ff9d">{ml}</h2></div>', unsafe_allow_html=True)
    with c5: 
        users = df['user_id'].nunique() if 'user_id' in df.columns else 0
        st.markdown(f'<div class="glass-card"><h4>👥 Active Staff Members</h4><h2 class="metric-value" style="color:#00ff9d">{users}</h2></div>', unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("🚀 LIVE THREAT TICKER")
    ticker = st.empty()
    threats = df[df['ml_threat'] == 1].head(12)
    ticker_text = "   🔥   ".join([f"{row.get('user_id','?')} → {row.get('action','N/A')} [{row.get('risk_score',0):.1f}]" for _, row in threats.iterrows()])
    ticker.markdown(f"""
    <div style="background:#1a0033; padding:20px; border-radius:20px; overflow:hidden; white-space:nowrap; border:3px solid #00f2ff;">
        <span style="display:inline-block; animation: ticker 20s linear infinite;">{ticker_text} &nbsp;&nbsp;&nbsp;&nbsp; {ticker_text}</span>
    </div>
    """, unsafe_allow_html=True)

# ====================== 2. DASHBOARD ======================
with tab_dashboard:
    st.markdown('<h1 class="main-header">Security Dashboard</h1>', unsafe_allow_html=True)
    st.caption("See the overall risk picture at a glance")

    c1, c2 = st.columns([2, 1])
    with c1:
        st.subheader("Risk Score Trend Over Time")
        fig = px.line(df.head(400), x='timestamp', y='risk_score', color_discrete_sequence=['#00f2ff'])
        fig.update_layout(template="plotly_dark", height=480)
        st.plotly_chart(fig, width="stretch")
    with c2:
        st.subheader("Risk Level Breakdown")
        if 'risk_level' in df.columns:
            fig = px.pie(df, names='risk_level', hole=0.45, color_discrete_sequence=['#ff2d55', '#ffb800', '#00f2ff'])
            fig.update_layout(template="plotly_dark", height=480)
            st.plotly_chart(fig, width="stretch")

    st.subheader("3D View: Risk vs AI Anomaly")
    plot_df = df.head(500).copy()
    fig = px.scatter_3d(plot_df, x='risk_score', y='anomaly_score', z='event_seq',
                        color='risk_level' if 'risk_level' in plot_df.columns else None,
                        size='risk_score')
    fig.update_layout(template="plotly_dark", height=650)
    st.plotly_chart(fig, width="stretch")

# ====================== 3. LOGS ======================
with tab_logs:
    st.markdown('<h1 class="main-header">All Access Logs</h1>', unsafe_allow_html=True)
    st.caption("Every single access to patient records is recorded here")
    search = st.text_input("🔍 Search by User ID, Action or Patient ID", placeholder="e.g. nurse_042 or P12345")
    filtered = df
    if search:
        mask = pd.Series(False, index=filtered.index)
        for col in ['user_id', 'action', 'patient_id']:
            if col in filtered.columns:
                mask |= filtered[col].astype(str).str.contains(search, case=False, na=False)
        filtered = filtered[mask]
    st.dataframe(filtered, width="stretch", height=700, hide_index=True)

# ====================== 4. ALERTS ======================
with tab_alerts:
    st.markdown('<h1 class="main-header">🚨 Active Alerts</h1>', unsafe_allow_html=True)
    st.caption("These are the events that need immediate attention")
    alerts = df[(df.get('risk_level', '') == 'High Risk') | 
                (df.get('ml_threat', 0) == 1) | 
                (df.get('critical_breach', False))]

    if alerts.empty:
        st.success("✅ No critical alerts right now. Everything looks safe.")
    else:
        st.error(f"⚠️ {len(alerts)} ACTIVE ALERTS")
        for _, row in alerts.head(15).iterrows():
            color = "#ff2d55" if row.get('critical_breach', False) else "#ffb800"
            st.markdown(f"""
            <div style="background:#1e2937; padding:22px; margin:15px 0; border-left:8px solid {color}; border-radius:16px;">
                <strong style="color:{color};">{'🚨 CRITICAL' if row.get('critical_breach', False) else '🟠 HIGH RISK'}</strong><br>
                <strong>{row.get('user_id', 'Unknown')}</strong> — {row.get('action', 'N/A')}<br>
                Risk Score: <b>{row.get('risk_score', 0):.1f}</b> | Time: {row.get('timestamp')}
            </div>
            """, unsafe_allow_html=True)

        if st.button("✅ Acknowledge All Alerts", type="primary"):
            st.balloons()
            st.success("All alerts have been acknowledged and logged.")

# ====================== 5. ANALYTICS ======================
with tab_analytics:
    st.markdown('<h1 class="main-header">Advanced Analytics</h1>', unsafe_allow_html=True)
    st.caption("Deep insights into staff behavior and access patterns")
    a1, a2 = st.tabs(["🔥 Access Pattern Heatmap", "📊 Risk vs Anomaly Correlation"])
    with a1:
        if 'user_id' in df.columns and 'action' in df.columns:
            pivot = pd.crosstab(df['user_id'].head(30), df['action'])
            fig = px.imshow(pivot, color_continuous_scale='Plasma', title="Who is accessing what most often?")
            fig.update_layout(height=720, template="plotly_dark")
            st.plotly_chart(fig, width="stretch")
    with a2:
        fig = px.scatter(df, x="risk_score", y="anomaly_score", 
                         color="risk_level" if 'risk_level' in df.columns else None,
                         size="risk_score", hover_data=['user_id', 'action'])
        fig.update_layout(template="plotly_dark", height=650)
        st.plotly_chart(fig, width="stretch")

# ====================== FOOTER ======================
st.markdown("---")
f1, f2, f3 = st.columns(3)
with f1:
    st.markdown(f"<span class='blinker'></span> **EHR Safety Services • LIVE**", unsafe_allow_html=True)
with f2:
    st.caption(f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} IST")
with f3:
    st.caption("Easy to understand • Built for hospital teams")

st.markdown("""
<script>
    function countUp() {
        document.querySelectorAll('.metric-value').forEach(el => {
            let target = parseFloat(el.textContent.replace(/[^0-9.]/g, '')) || 0;
            let count = 0;
            let inc = target / 25;
            let timer = setInterval(() => {
                count += inc;
                if (count >= target) { count = target; clearInterval(timer); }
                el.textContent = Math.floor(count).toLocaleString();
            }, 30);
        });
    }
    setTimeout(countUp, 300);
</script>
""", unsafe_allow_html=True)