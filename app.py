import streamlit as st
from utils.payoff import validate_inputs, calculate_payoff_scenarios
import pandas as pd

st.set_page_config(
    page_title="Autocall Note Calculator",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'inputs' not in st.session_state:
    st.session_state.inputs = {}
if 'scenarios' not in st.session_state:
    st.session_state.scenarios = None
if 'validation_errors' not in st.session_state:
    st.session_state.validation_errors = []

# Sidebar disclaimer
with st.sidebar:
    st.markdown("### ⚠️ Disclaimer")
    st.markdown("""
    This calculator is for **illustrative purposes only** and does not constitute 
    investment advice. All calculations are simplified models. Consult your 
    structuring desk for production use.
    """)
    st.divider()
    if st.button("Reset All Inputs"):
        st.session_state.inputs = {}
        st.session_state.scenarios = None
        st.session_state.validation_errors = []
        st.rerun()

# Page routing
page = st.sidebar.selectbox(
    "Navigate",
    ["🏠 Home", "📝 Deal Inputs", "⚙️ Payoff Engine", 
     "📊 Scenario Analysis", "⚠️ Risk Analysis", "📤 Export"]
)

if page == "🏠 Home":
    st.markdown('<h1 class="main-header">Autocallable Fixed Coupon Note Calculator</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    ## Professional Structured Product Calculator
    
    **Enter deal terms once → Instantly see all payoff scenarios → Export for clients**
    
    **Key Features:**
    - Early autocall scenarios
    - Coupon barrier tracking  
    - Maturity redemption logic
    - Memory coupon support
    - Sensitivity analysis
    - CSV/Excel exports
    """)
    
    # Show summary cards if inputs exist
    if st.session_state.inputs:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Notional", f"{st.session_state.inputs.get('notional', 0):,.0f}")
            st.markdown('</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Coupon Rate", f"{st.session_state.inputs.get('coupon_rate', 0)*100:.1f}%")
            st.markdown('</div>', unsafe_allow_html=True)
        with col3:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Tenor", f"{st.session_state.inputs.get('tenor', 0):.1f}Y")
            st.markdown('</div>', unsafe_allow_html=True)
        with col4:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Autocall Trigger", f"{st.session_state.inputs.get('autocall_trigger', 0)*100:.0f}%")
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.info("✅ Inputs saved. Check Payoff Engine for calculations!")

elif page == "📝 Deal Inputs":
    st.header("Deal Inputs")
    import pages._01_Deal_Inputs  # Dynamic import for multipage

elif page == "⚙️ Payoff Engine":
    st.header("Payoff Engine")
    if st.session_state.inputs:
        st.info("Calculating payoffs...")
        # Trigger calculation
        if st.button("🔄 Recalculate Payoffs"):
            st.session_state.scenarios = calculate_payoff_scenarios(st.session_state.inputs)
        import pages._02_Payoff_Engine
    else:
        st.warning("👈 Please enter deal terms first")

elif page == "📊 Scenario Analysis":
    st.header("Scenario Analysis")
    if st.session_state.scenarios is not None:
        import pages._03_Scenario_Analysis
    else:
        st.warning("👈 Run payoff calculations first")

elif page == "⚠️ Risk Analysis":
    st.header("Risk & Sensitivities")
    if st.session_state.scenarios is not None:
        import pages._04_Risk_Sensitivity
    else:
        st.warning("👈 Run payoff calculations first")

elif page == "📤 Export":
    st.header("Export & Audit")
    import pages._05_Export
