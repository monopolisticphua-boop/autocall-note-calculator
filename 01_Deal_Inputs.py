import streamlit as st
from utils.payoff import validate_inputs

st.subheader("Enter Deal Terms")

# Organize inputs in columns
col1, col2 = st.columns(2)

with col1:
    st.text_input("Underlying Name", key="underlying_name", help="e.g., SPX, EUROSTOXX50")
    initial_spot = st.number_input("Initial Spot", min_value=0.01, value=100.0, step=0.01, key="initial_spot")
    notional = st.number_input("Notional Amount", min_value=1000.0, value=1000000.0, step=10000.0, key="notional")
    currency = st.selectbox("Currency", ["USD", "EUR", "GBP", "SGD"], key="currency")

with col2:
    coupon_rate = st.number_input("Coupon Rate (%)", min_value=0.01, value=8.0, step=0.1, 
                                 format="%.2f", key="coupon_rate") / 100
    coupon_frequency = st.selectbox("Coupon Frequency (months)", [1, 3, 6, 12], index=1, key="coupon_frequency")
    tenor = st.number_input("Tenor (Years)", min_value=0.5, value=5.0, step=0.5, key="tenor")

col3, col4, col5 = st.columns(3)

with col3:
    autocall_trigger = st.number_input("Autocall Trigger (%)", min_value=50.0, value=100.0, 
                                      step=1.0, format="%.1f", key="autocall_trigger") / 100
with col4:
    coupon_barrier = st.number_input("Coupon Barrier (%)", min_value=50.0, value=80.0, 
                                    step=1.0, format="%.1f", key="coupon_barrier") / 100
with col5:
    final_barrier = st.number_input("Final Barrier (%)", min_value=40.0, value=60.0, 
                                   step=1.0, format="%.1f", key="final_barrier") / 100

col6, col7 = st.columns(2)

with col6:
    downside_part = st.number_input("Downside Participation (%)", min_value=0.0, value=100.0, 
                                   step=10.0, format="%.0f", key="downside_participation") / 100
with col7:
    call_protection = st.number_input("Call Protection (periods)", min_value=0, value=4, step=1, key="call_protection_period")

st.checkbox("Enable Memory Coupon", key="memory_coupon")

if st.button("💾 Save Inputs & Validate", type="primary"):
    inputs = {
        'underlying_name': st.session_state.underlying_name,
        'initial_spot': initial_spot,
        'notional': notional,
        'currency': currency,
        'coupon_rate': coupon_rate,
        'coupon_frequency': coupon_frequency,
        'autocall_trigger': autocall_trigger,
        'coupon_barrier': coupon_barrier,
        'final_barrier': final_barrier,
        'tenor': tenor,
        'downside_participation': downside_part,
        'memory_coupon': st.session_state.memory_coupon,
        'call_protection_period': call_protection
    }
    
    errors = validate_inputs(inputs)
    st.session_state.inputs = inputs
    st.session_state.validation_errors = errors
    
    if errors:
        st.error("Validation errors: " + "; ".join(errors))
    else:
        st.success("✅ Inputs saved successfully!")
        st.rerun()
