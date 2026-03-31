import streamlit as st
import pandas as pd
from io import BytesIO
import base64

if st.session_state.scenarios is not None:
    # CSV Download
    csv = st.session_state.scenarios.to_csv(index=False)
    st.download_button(
        label="📥 Download Scenarios CSV",
        data=csv,
        file_name=f"autocall_scenarios_{pd.Timestamp.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )
    
    # Summary Excel
    with BytesIO() as buffer:
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            st.session_state.scenarios.to_excel(writer, sheet_name='Scenarios', index=False)
            pd.DataFrame([st.session_state.inputs]).T.to_excel(writer, sheet_name='Inputs')
        
        st.download_button(
            label="📊 Download Summary Excel",
            data=buffer.getvalue(),
            file_name=f"autocall_summary_{pd.Timestamp.now().strftime('%Y%m%d')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    
    st.subheader("Audit Trail")
    st.json({
        "inputs_snapshot": st.session_state.inputs,
        "calculation_timestamp": pd.Timestamp.now().isoformat(),
        "model_version": "v1.0",
        "disclaimer": "Illustrative calculator only"
    })
    
    if st.button("🗑️ Reset All Data"):
        st.session_state.inputs = {}
        st.session_state.scenarios = None
        st.rerun()
else:
    st.warning("Please run payoff calculations first")
