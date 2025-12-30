import streamlit as st

def show_about_tab():
    # --- Custom CSS for High Visibility ---
    st.markdown("""
    <style>
        /* Increase body text size for readability on projectors */
        p, li, .stMarkdown {
            font-size: 18px !important;
            line-height: 1.7 !important;
        }
        /* Make headers stand out */
        h1, h2, h3, h4 {
            color: #00e5ff !important;
            font-weight: 700 !important;
        }
        /* Custom Box Styling */
        .info-box {
            background-color: #161b22;
            padding: 20px;
            border-left: 5px solid #00e5ff;
            border-radius: 5px;
            margin-bottom: 20px;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("## 📘 Methodology & Technical Documentation")
    st.markdown("### 🕵️‍♀️ Project: Forensic Omniscient System")
    
    st.markdown("""
    <div class="info-box">
    <strong>📄 Executive Summary:</strong><br>
    This dashboard is an integrated <strong>Forensic Auditing System</strong> designed to detect early warning signs of corporate fraud and financial distress. 
    It employs a <strong>"Triangulation Approach"</strong>, cross-verifying three distinct pillars of corporate health:
    <ol>
        <li><strong>Solvency (Bankruptcy Risk)</strong> via the Altman Z-Score.</li>
        <li><strong>Integrity (Manipulation Risk)</strong> via the Beneish M-Score.</li>
        <li><strong>Transparency (Deception Risk)</strong> via Linguistic Analysis.</li>
    </ol>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()

    # --- SECTION 1: THE PENTAGON MODELS ---
    st.markdown("### 1️⃣ Quantitative Models (The Financial Pentagon)")
    
    # TABBED INTERFACE
    tab_z, tab_m, tab_q = st.tabs(["📉 Altman Z-Score", "⚖️ Beneish M-Score", "💰 Earnings Quality"])

    # --- Z-SCORE DETAIL ---
    with tab_z:
        st.markdown("#### 📉 The Altman Z-Score Model (1968)")
        st.write("A multivariate statistical formula used to predict the probability that a business will go bankrupt within the next two years. It combines five financial ratios to generate a single 'Health Score'.")
        
        st.markdown("**🧮 The Full Mathematical Formula:**")
        st.latex(r'''
            Z = 1.2A + 1.4B + 3.3C + 0.6D + 1.0E
        ''')
        
        st.markdown("**📊 Component Breakdown:**")
        st.markdown("""
        * **A (Liquidity):** $\\frac{\\text{Working Capital}}{\\text{Total Assets}}$
            * *Logic:* Measures the liquid buffer available to survive short-term shocks.
        * **B (Accumulated Profit):** $\\frac{\\text{Retained Earnings}}{\\text{Total Assets}}$
            * *Logic:* Measures reliance on debt. Young or struggling firms have low 'B'.
        * **C (Efficiency):** $\\frac{\\text{EBIT}}{\\text{Total Assets}}$
            * *Logic:* The raw productive power of the company's assets (Core Profitability).
        * **D (Leverage):** $\\frac{\\text{Market Value of Equity}}{\\text{Total Liabilities}}$
            * *Logic:* The market's confidence vs. the debt load.
        * **E (Activity):** $\\frac{\\text{Sales}}{\\text{Total Assets}}$
            * *Logic:* How fast the company turns assets into revenue.
        """)
        
        st.info("""
        **🚦 Interpreting the Score:**
        * **🟢 > 3.0 (Safe Zone):** Financially robust.
        * **🟡 1.8 – 3.0 (Grey Zone):** Caution warranted.
        * **🔴 < 1.8 (Distress Zone):** High probability of insolvency.
        """)

    # --- M-SCORE DETAIL ---
    with tab_m:
        st.markdown("#### ⚖️ The Beneish M-Score (Modified)")
        st.write("A probabilistic model designed to detect earnings manipulation. This dashboard utilizes the **2-Factor Modified Model**, focusing on the two most common indicators of fraud: Revenue Recognition and Sales Distortion.")
        
        st.markdown("**🧮 The Full Mathematical Formula:**")
        st.latex(r'''
            M = -4.84 + (0.92 \times DSRI) + (0.71 \times SGI)
        ''')
        
        st.markdown("**📊 Component Breakdown:**")
        st.markdown("""
        * **1. DSRI (Days Sales in Receivables Index):** * *Formula:* $\\frac{(\\text{Receivables}_t / \\text{Sales}_t)}{(\\text{Receivables}_{t-1} / \\text{Sales}_{t-1})}$
            * *Logic:* If Receivables grow faster than Sales (Index > 1.0), it suggests the company might be booking **Fake Revenue** (Channel Stuffing) without collecting actual cash.
            
        * **2. SGI (Sales Growth Index):** * *Formula:* $\\frac{\\text{Sales}_t}{\\text{Sales}_{t-1}}$
            * *Logic:* While growth is good, **Rapid Growth (SGI > 1.2)** creates pressure on management to sustain the trend, significantly increasing the temptation to manipulate earnings.
        """)
        
        st.error("""
        **🚦 Interpreting the Score:**
        * **🟢 < -2.22 (Honest):** Financial reporting appears consistent.
        * **🔴 > -2.22 (Manipulator):** High statistical probability of earnings management.
        """)

    # --- QUALITY DETAIL ---
    with tab_q:
        st.markdown("#### 💰 Earnings Quality Ratio")
        st.write("A litmus test for 'Paper Profits'. It compares the profit reported to shareholders vs. the actual cash deposited in the bank.")
        
        st.latex(r'''
            \text{Quality Ratio} = \frac{\text{Operating Cash Flow (CFO)}}{\text{Net Income}}
        ''')
        
        st.success("""
        **🚦 Interpreting the Ratio:**
        * **🟢 > 1.0 (High Quality):** The company generates more cash than profit (Conservative).
        * **🟡 0.8 - 1.0 (Standard):** Normal accrual accounting.
        * **🔴 < 0.8 (Low Quality):** Profits are driven by non-cash items (Accruals), suggesting low sustainability.
        """)

    st.divider()

    # --- SECTION 2: LINGUISTIC MODEL ---
    st.markdown("### 2️⃣ Qualitative Model (The Narrative Decoder)")
    st.markdown("#### 🗣️ The Gunning Fog Index")
    st.write("Based on the **Management Obfuscation Hypothesis**: *'When performance is poor, management writes longer, more complex sentences to confuse the reader.'*")
    
    st.latex(r'''
        \text{Fog Index} = 0.4 \left[ \left( \frac{\text{Total Words}}{\text{Sentences}} \right) + 100 \left( \frac{\text{Complex Words}}{\text{Total Words}} \right) \right]
    ''')
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**🧐 What is a 'Complex Word'?**")
        st.write("Any word with **3 or more syllables** (e.g., 'aforementioned', 'recalibration'), excluding proper nouns and common compound words.")
    with c2:
        st.markdown("**🚦 Thresholds:**")
        st.write("""
        * **🟢 < 14:** Readable (Clear communication).
        * **🟡 14 - 18:** Standard Business (Acceptable).
        * **🔴 > 18:** Obfuscated (Likely hiding information).
        """)

    st.divider()
    
    st.markdown("### 3️⃣ Verdict Logic Matrix")
    st.write("The AI Auditor follows this strict logic tree to determine the final status:")
    
    st.markdown("""
    | Verdict | Trigger Condition | Interpretation |
    | :--- | :--- | :--- |
    | 🔴 **CRITICAL** | **Z-Score < 1.8** | The company is mathematically insolvent. Immediate risk of failure. |
    | 👺 **FRAUD** | **M-Score > -2.22** | Earnings manipulation detected. Financials are likely unreliable. |
    | ⚠️ **WARNING** | **Quality < 0.8** | "Paper Profits" detected. Growth is not funded by cash. |
    | 🟢 **SAFE** | **All Tests Pass** | No significant anomalies found across Solvency, Integrity, or Quality. |
    """)
    
    st.caption("Disclaimer: This tool provides forensic indicators for academic and analytical purposes. It does not constitute legal or investment advice.")