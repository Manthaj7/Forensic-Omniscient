import streamlit as st
from utils import inject_custom_css
from views_financial import show_financial_phase
from views_narrative import show_narrative_phase
from views_about import show_about_tab

# 1. Page Config
st.set_page_config(page_title="Forensic Omniscient", layout="wide", page_icon="🔍")

# 2. Inject CSS
inject_custom_css()

# --- HEADER SECTION (CENTERED) ---
# Using a professional Audit/Forensic Icon
st.markdown("""
    <div style="text-align: center; margin-bottom: 20px;">
        <img src="https://cdn-icons-png.flaticon.com/512/2822/2822622.png" width="100" style="filter: drop-shadow(0 0 10px #00e5ff);">
        <h1 class="main-title">FORENSIC OMNISCIENT</h1>
        <div class="sub-title">AI-Powered Integrated Audit System</div>
    </div>
""", unsafe_allow_html=True)

# 3. Sidebar Nav (Cleaned up)
with st.sidebar:
    st.markdown("### 🧭 Navigation Module")
    page = st.radio("", ["💎 Financial Analysis", "📝 Narrative Decoder", "📘 About & Methodology"], label_visibility="collapsed")
    st.markdown("---")
    st.info("**Status:** System Online \n**v3.5 Stable**")

# 4. Route
if page == "💎 Financial Analysis":
    show_financial_phase()
elif page == "📝 Narrative Decoder":
    show_narrative_phase()
elif page == "📘 About & Methodology":
    show_about_tab()

# 5. BIG PROMINENT FOOTER
st.markdown('<div class="footer">⚡ Created by Manthaj Morajker ⚡</div>', unsafe_allow_html=True)