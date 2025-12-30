import streamlit as st
import plotly.graph_objects as go
import re

def show_narrative_phase():
    st.markdown("## 📝 Phase 2: Narrative Decoder")
    
    mode = st.radio("Select Analysis Mode:", ["📋 Text Analysis (Copy-Paste)", "🎛️ Auditor Simulation (Dropdowns)"], horizontal=True)
    st.divider()

    if mode == "📋 Text Analysis (Copy-Paste)":
        col1, col2 = st.columns([1, 1])
        with col1:
            # A realistic, complex MD message with "Foggy" language
            default_text = """Fiscal 2025 has been a year of strategic recalibration amidst a visibly challenging macroeconomic landscape. While the organization encountered significant headwinds in our legacy verticals—primarily driven by geopolitical volatilities and persistent inflationary pressures—our commitment to long-term value creation remained unwavering. 

We have endeavored to mitigate contingent liabilities through a comprehensive rationalization of our cost structures and the synergistic integration of our recent acquisitions. Notwithstanding the aforementioned uncertainties, the Company remains cautiously optimistic regarding its forward-looking guidance, contingent upon the stabilization of global supply chains. 

Furthermore, the amortization of intangible assets has been realigned with our revised capital allocation framework to better reflect the underlying economic reality. We believe that these proactive measures will precipitate a robust recovery in shareholder value, although we acknowledge that near-term visibility remains constrained by external variables beyond our control."""
            
            st.info("👇 **Paste Annual Report Excerpt below:**")
            raw_text = st.text_area("Managing Director's Statement / MD&A", height=350, value=default_text)
        
        with col2:
            st.subheader("🤖 AI Text Audit")
            
            # --- ANALYSIS LOGIC ---
            # 1. Fog Index Calculation
            words = re.findall(r'\w+', raw_text)
            sentences = max(len(re.split(r'[.!?]+', raw_text)) - 1, 1) 
            num_words = len(words) if words else 1
            
            # Complex words: Words with > 7 letters as proxy for 3+ syllables
            complex_words = len([w for w in words if len(w) > 7]) 
            
            # Gunning Fog Formula
            fog = 0.4 * ((num_words / sentences) + 100 * (complex_words / num_words))
            
            # 2. Keyword Highlighting
            highlighted = raw_text
            
            # Red Flags (Negative/Risk)
            risks = ['loss', 'decline', 'challenging', 'headwinds', 'litigation', 'fail', 'unable', 'volatilities', 'constrained', 'pressures']
            # Yellow Flags (Vague/Obfuscation)
            vague = ['believe', 'estimate', 'anticipate', 'maybe', 'could', 'contingent', 'endeavored', 'mitigate', 'aforementioned', 'synergistic', 'rationalization', 'precipitate']
            
            # Case-insensitive replacement with HTML wrappers
            for w in risks:
                pattern = re.compile(rf"\b({w})\b", re.IGNORECASE)
                highlighted = pattern.sub(r'<span class="risk-high">\1</span>', highlighted)
            for w in vague:
                pattern = re.compile(rf"\b({w})\b", re.IGNORECASE)
                highlighted = pattern.sub(r'<span class="risk-med">\1</span>', highlighted)

            # --- DISPLAY RESULTS ---
            
            # Fog Index Gauge - FIXED VISIBILITY
            fig = go.Figure(go.Indicator(
                mode = "gauge+number", value = fog,
                title = {'text': "Fog Index (Complexity)", 'font': {'size': 24, 'color': 'white'}}, # FORCE WHITE
                number = {'font': {'size': 40, 'color': 'white'}}, # FORCE WHITE
                gauge = {
                    'axis': {'range': [0, 30], 'tickwidth': 1, 'tickcolor': "white"},
                    'bar': {'color': "#ff5252" if fog > 18 else "#00e5ff"},
                    'bgcolor': "rgba(0,0,0,0)",
                    'steps': [
                        {'range': [0, 14], 'color': "#1e2530"},
                        {'range': [14, 18], 'color': "#2d333b"},
                        {'range': [18, 30], 'color': "#3d0000"}
                    ],
                    'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 18}
                }
            ))
            fig.update_layout(height=250, margin=dict(t=50, b=10, l=20, r=20), paper_bgcolor='rgba(0,0,0,0)', font={'color': "white"})
            st.plotly_chart(fig, use_container_width=True)

            # Text Verdict
            if fog > 18:
                st.error("🚨 **VERDICT: OBFUSCATED**")
                st.caption("The text is highly complex, often used to hide poor performance.")
            elif fog > 14:
                st.warning("⚠️ **VERDICT: COMPLEX**")
                st.caption("Standard corporate language, but lacks clarity.")
            else:
                st.success("✅ **VERDICT: CLEAR**")
                st.caption("Communication is direct and transparent.")

            # Scrollable X-Ray View
            st.markdown("#### 🔍 X-Ray View")
            st.markdown(f"""
            <div class="report-card" style="height: 200px; overflow-y: scroll; font-size: 16px; line-height: 1.8;">
                {highlighted}
            </div>
            """, unsafe_allow_html=True)
            
            st.caption("🔴 Red = Risk/Negative | 🟡 Yellow = Vague/Jargon")

    else:
        # ADVANCED SIMULATION (Dropdowns)
        st.info("👨‍💻 **Simulation Mode:** Configure the linguistic profile of the report.")
        
        c1, c2, c3 = st.columns(3)
        
        with c1:
            tone = st.selectbox("1. Executive Tone", [
                "Optimistic & Data-Driven (Low Risk)",
                "Neutral / Professional (Low Risk)",
                "Cautious / Hedging (Medium Risk)",
                "Defensive / Blaming Externals (High Risk)",
                "Aggressive / Boastful (High Risk)",
                "Confused / Contradictory (Critical Risk)"
            ])
            
        with c2:
            complexity = st.selectbox("2. Sentence Structure", [
                "Simple & Direct (Fog < 12)",
                "Standard Business (Fog 12-16)",
                "Academic / Technical (Fog 16-18)",
                "Complex / Legalese (Fog 18-22)",
                "Incomprehensible Word Salad (Fog > 22)"
            ])
            
        with c3:
            focus = st.selectbox("3. Primary Content Focus", [
                "Core Operations & Cash Flow",
                "Strategic Growth Initiatives",
                "Non-GAAP / Adjusted Metrics",
                "One-time Events & Excuses",
                "Future Promises (Little Current Data)"
            ])
            
        # Scoring Logic
        score = 0
        reasons = []
        
        # Tone Scoring
        if "Defensive" in tone: score += 25; reasons.append("Defensive tone suggests hiding bad news.")
        if "Aggressive" in tone: score += 35; reasons.append("Aggressive promotion is a fraud marker.")
        if "Confused" in tone: score += 50; reasons.append("Contradictions indicate lack of control.")
        
        # Complexity Scoring
        if "Legalese" in complexity: score += 20; reasons.append("High complexity obscures truth.")
        if "Word Salad" in complexity: score += 40; reasons.append("Extreme obfuscation detected.")
        
        # Focus Scoring
        if "Non-GAAP" in focus: score += 20; reasons.append("Focus on 'Adjusted' numbers vs real profit.")
        if "Excuses" in focus: score += 30; reasons.append("Externalizing blame.")
        if "Future" in focus: score += 25; reasons.append("Distracting from current performance.")

        # Result
        st.divider()
        c_meter, c_details = st.columns([1, 2])
        
        with c_meter:
            # Gauge for Simulation - FIXED VISIBILITY
            fig = go.Figure(go.Indicator(
                mode = "gauge+number", value = score,
                title = {'text': "Deception Risk Score", 'font': {'size': 24, 'color': 'white'}}, # FORCE WHITE
                number = {'font': {'size': 40, 'color': 'white'}}, # FORCE WHITE
                gauge = {
                    'axis': {'range': [0, 100], 'tickcolor': "white"},
                    'bar': {'color': "red" if score > 50 else "#00e5ff"},
                    'bgcolor': "rgba(0,0,0,0)"
                }
            ))
            fig.update_layout(height=250, margin=dict(t=50, b=10), paper_bgcolor='rgba(0,0,0,0)', font={'color': "white"})
            st.plotly_chart(fig, use_container_width=True)
            
        with c_details:
            st.subheader("Auditor Conclusion")
            if score > 50:
                st.error("🚨 HIGH RISK: DECEPTION LIKELY")
                st.write("The linguistic profile matches patterns found in historical fraud cases (e.g., Enron, Satyam).")
            elif score > 20:
                st.warning("⚠️ MEDIUM RISK: CAUTION")
                st.write("The reporting lacks transparency. Dig deeper into footnotes.")
            else:
                st.success("✅ LOW RISK: TRANSPARENT")
                st.write("Communication is clear and direct.")
                
            if reasons:
                st.markdown("**Key Risk Drivers:**")
                for r in reasons:
                    st.write(f"- {r}")