import streamlit as st
import pandas as pd
import numpy as np

st.subheader("Barrier Sensitivity")
col1, col2 = st.columns(2)

with col1:
    barriers = np.linspace(0.4, 0.9, 6)
    results = []
    for b in barriers:
        temp_inputs = st.session_state.inputs.copy()
        temp_inputs['final_barrier'] = b
        # Simplified sensitivity calc
        worst_return = -b * st.session_state.inputs['downside_participation'] * 100
        results.append({'Barrier %': b*100, 'Worst Return %': worst_return})
    
    st.dataframe(pd.DataFrame(results), use_container_width=True)

with col2:
    st.subheader("Coupon Rate Impact")
    rates = [0.05, 0.06, 0.07, 0.08, 0.09, 0.10]
    impacts = [r*st.session_state.inputs['tenor']*100 for r in rates]
    st.bar_chart(pd.DataFrame({'Rate %': rates, 'Annualized Impact %': impacts}))

st.info("""
**Key Risks:**
- **Barrier breach**: Capital loss if final spot < final barrier
- **Opportunity cost**: High autocall trigger delays redemption
- **Memory coupon**: Provides coupon protection but increases complexity
""")
