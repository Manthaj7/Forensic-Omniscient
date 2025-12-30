import streamlit as st
import plotly.graph_objects as go
from utils import safe_div

def show_financial_phase():
    # --- 1. CSS FOR HIGH VISIBILITY & CARDS ---
    st.markdown("""
    <style>
        /* Increase global font size */
        p, .stMarkdown, li, div {
            font-size: 18px !important;
        }
        
        /* Custom Score Cards */
        .score-card {
            background: linear-gradient(145deg, #161b22, #0d1117);
            padding: 20px;
            border-radius: 10px;
            border: 1px solid #333;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
            margin-bottom: 10px;
        }
        .score-val {
            font-size: 36px !important;
            font-weight: 700;
            margin: 10px 0;
            text-shadow: 0 0 10px rgba(255,255,255,0.1);
        }
        .score-label {
            font-size: 16px !important;
            color: #8b949e;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        /* Status Colors */
        .safe {color: #00e676; border-bottom: 3px solid #00e676;}
        .risk {color: #ff5252; border-bottom: 3px solid #ff5252;}
        .warn {color: #ffab00; border-bottom: 3px solid #ffab00;}
        
        /* Table/Grid styling */
        .metric-row {
            display: flex; justify-content: space-between;
            padding: 12px 0;
            border-bottom: 1px solid #333;
            font-size: 16px !important;
        }
        .metric-row:last-child {border-bottom: none;}
    </style>
    """, unsafe_allow_html=True)

    st.markdown("## 💎 Phase 1: Forensic Triangulation Model")
    
    # --- 2. SIDEBAR INPUTS ---
    with st.sidebar:
        st.header("1. Financial Inputs (₹ Cr)")
        st.info("Preloaded sample data. Adjust as per requirement.")
        
        with st.expander("Profit & Loss", expanded=True):
            rev_cy = st.number_input("Revenue (CY)", value=162990.0)
            rev_py = st.number_input("Revenue (PY)", value=153670.0)
            cogs = st.number_input("COGS / Op. Expenses", value=123754.0)
            ni = st.number_input("Net Income", value=26713.0)
            ebit = rev_cy - cogs

        with st.expander("Balance Sheet", expanded=False):
            ta = st.number_input("Total Assets", value=147795.0)
            tl = st.number_input("Total Liabilities", value=51977.0)
            ca = st.number_input("Current Assets", value=95000.0) 
            cl = st.number_input("Current Liabilities", value=43750.0)
            rec_cy = st.number_input("Receivables (CY)", value=31158.0)
            rec_py = st.number_input("Receivables (PY)", value=30193.0)
            re = st.number_input("Retained Earnings", value=93745.0)
            mve = st.number_input("Market Value Equity", value=667000.0) 

        with st.expander("Cash Flow", expanded=False):
            cfo = st.number_input("Operating Cash Flow", value=35694.0)

    # --- 3. CALCULATIONS ---
    # Z-Score Components
    wc = ca - cl
    A = safe_div(wc, ta)
    B = safe_div(re, ta)
    C = safe_div(ebit, ta)
    D = safe_div(mve, tl)
    E = safe_div(rev_cy, ta)
    z_score = (1.2*A) + (1.4*B) + (3.3*C) + (0.6*D) + (1.0*E)

    # M-Score Components
    dsri = safe_div(safe_div(rec_cy, rev_cy), safe_div(rec_py, rev_py))
    sgi = safe_div(rev_cy, rev_py)
    m_score = -4.84 + (0.92 * dsri) + (0.71 * sgi)

    # Quality Ratio
    q_ratio = safe_div(cfo, ni)

    # --- 4. TOP ROW: PROMINENT SCORE CARDS ---
    c1, c2, c3 = st.columns(3)
    
    # Helper to generate HTML card (Corrected Indentation)
    def make_card(label, val, status, threshold_text):
        color_class = "safe" if status == "Safe" else ("risk" if status == "Risk" else "warn")
        val_color = '#00e676' if status=='Safe' else '#ff5252'
        
        return f"""
<div class="score-card {color_class}">
<div class="score-label">{label}</div>
<div class="score-val" style="color: {val_color}">{val}</div>
<div style="font-size:14px; opacity:0.8;">{threshold_text}</div>
</div>
"""

    with c1:
        status = "Safe" if z_score > 3.0 else ("Risk" if z_score < 1.8 else "Warn")
        st.markdown(make_card("Solvency (Z-Score)", f"{z_score:.2f}", status, "Target > 3.0"), unsafe_allow_html=True)
        
    with c2:
        status = "Safe" if m_score < -2.22 else "Risk"
        st.markdown(make_card("Integrity (M-Score)", f"{m_score:.2f}", status, "Target < -2.22"), unsafe_allow_html=True)
        
    with c3:
        status = "Safe" if q_ratio > 1.0 else ("Risk" if q_ratio < 0.8 else "Warn")
        st.markdown(make_card("Quality (CFO/NI)", f"{q_ratio:.2f}x", status, "Target > 1.0"), unsafe_allow_html=True)

    st.markdown("---")

    # --- 5. MIDDLE ROW: CHART & VERDICT ---
    col_chart, col_verdict = st.columns([1.5, 1])

    with col_chart:
        st.subheader("📊 Forensic Radar View")
        
        # Normalize (0-100 scale)
        n_z = min(max((z_score/3)*100, 0), 100)
        n_m = min(max(((-2.0 - m_score)+5)*20, 0), 100) # Inverted
        n_q = min(max(q_ratio*100, 0), 100)
        
        # Detailed Radar Chart
        fig = go.Figure()
        
        # Green Safe Zone Overlay
        fig.add_trace(go.Scatterpolar(
            r=[100, 100, 100, 100],
            theta=['Solvency', 'Integrity', 'Quality', 'Solvency'],
            fill='toself', name='Safe Zone',
            line=dict(color='rgba(0, 230, 118, 0.2)', width=0),
            fillcolor='rgba(0, 230, 118, 0.1)'
        ))
        
        # The Data Line
        fig.add_trace(go.Scatterpolar(
            r=[n_z, n_m, n_q, n_z],
            theta=['Solvency', 'Integrity', 'Quality', 'Solvency'],
            fill='toself', name='Target Co',
            line=dict(color='#00e5ff', width=3),
            fillcolor='rgba(0, 229, 255, 0.2)'
        ))

        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100], gridcolor='#333', tickfont=dict(color='gray')),
                angularaxis=dict(gridcolor='#333', tickfont=dict(size=14, color='white')),
                bgcolor='rgba(0,0,0,0)'
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            height=350,
            showlegend=False,
            margin=dict(l=40, r=40, t=20, b=20)
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_verdict:
        st.subheader("🤖 AI Auditor Verdict")
        
        # Logic Tree
        if z_score < 1.8:
            title = "CRITICAL RISK"; color = "#ff5252"; msg = "Company is mathematically insolvent."
        elif m_score > -2.22:
            title = "HIGH FRAUD RISK"; color = "#ff5252"; msg = "Earnings manipulation markers detected."
        elif q_ratio < 0.8:
            title = "QUALITY WARNING"; color = "#ffab00"; msg = "Profits are not backed by cash flow."
        else:
            title = "LOW RISK"; color = "#00e676"; msg = "Financial structure appears robust and honest."

        st.markdown(f"""
<div style="background-color: #1e2530; border-left: 5px solid {color}; padding: 20px; border-radius: 5px;">
<h2 style="color:{color}; margin:0; font-size: 28px;">{title}</h2>
<p style="margin-top:10px; font-size: 18px;">{msg}</p>
</div>
""", unsafe_allow_html=True)

    # --- 6. BOTTOM ROW: DEEP DIVE DIAGNOSTICS (Fills Empty Space) ---
    st.markdown("---")
    st.subheader("🔍 Deep Dive Diagnostics")
    
    d1, d2 = st.columns(2)
    
    with d1:
        st.markdown("**Z-Score Breakdown (Solvency Drivers)**")
        st.markdown(f"""
<div style="background-color: #0d1117; padding: 15px; border-radius: 8px;">
<div class="metric-row"><span>Liquidity (A)</span> <span style="color:#00e5ff">{A:.2f}</span></div>
<div class="metric-row"><span>Retained Earnings (B)</span> <span style="color:#00e5ff">{B:.2f}</span></div>
<div class="metric-row"><span>Op. Efficiency (C)</span> <span style="color:#00e5ff">{C:.2f}</span></div>
<div class="metric-row"><span>Market Leverage (D)</span> <span style="color:#00e5ff">{D:.2f}</span></div>
<div class="metric-row"><span>Asset Turnover (E)</span> <span style="color:#00e5ff">{E:.2f}</span></div>
</div>
""", unsafe_allow_html=True)
        
    with d2:
        st.markdown("**M-Score Breakdown (Fraud Flags)**")
        # Check colors
        dsri_col = '#ff5252' if dsri > 1.1 else '#00e5ff'
        sgi_col = '#ff5252' if sgi > 1.2 else '#00e5ff'
        
        st.markdown(f"""
<div style="background-color: #0d1117; padding: 15px; border-radius: 8px;">
<div class="metric-row">
<span>DSRI (Receivables Growth)</span> 
<span style="color:{dsri_col}">{dsri:.2f}x</span>
</div>
<div style="font-size:14px; color:gray; margin-bottom:10px;">*If > 1.0, receivables growing faster than sales.*</div>

<div class="metric-row">
<span>SGI (Sales Growth)</span> 
<span style="color:{sgi_col}">{sgi:.2f}x</span>
</div>
<div style="font-size:14px; color:gray;">*If > 1.2, pressure to manipulate increases.*</div>
</div>
""", unsafe_allow_html=True)