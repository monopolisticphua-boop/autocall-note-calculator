import streamlit as st
import pandas as pd

if st.session_state.scenarios is not None:
    df = st.session_state.scenarios
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Max Return", f"{df['return_pct'].max():.1f}%")
    with col2:
        st.metric("Break-even", f"{df[df['return_pct']>=0]['final_spot_pct'].min()*100:.1f}%")
    with col3:
        st.metric("Autocall Prob >100%", f"{(df['autocall'] & (df['final_spot_pct']>=1.0)).mean()*100:.0f}%")
    with col4:
        st.metric("Worst Case Loss", f"-{(-df['return_pct']).max():.1f}%")
    
    # Scenario table
    st.subheader("Payoff Scenarios")
    scenario_df = df[['final_spot_pct', 'autocall', 'total_coupons', 'final_redemption', 'total_payoff', 'return_pct']].copy()
    scenario_df['Final Spot %'] = (scenario_df['final_spot_pct']*100).round(0)
    scenario_df['Autocall'] = scenario_df['autocall'].map({True: 'Yes', False: 'No'})
    scenario_df['Total Payoff'] = scenario_df['total_payoff'].round(0)
    scenario_df['Return %'] = scenario_df['return_pct'].round(1)
    
    # Highlight key scenarios
    def highlight_scenarios(row):
        color = ''
        if row['Final Spot %'] == 100:
            color = 'background-color: #ffeb3b'
        elif row['Final Spot %'] <= 60:
            color = 'background-color: #ffcdd2'
        elif row['Final Spot %'] >= 120:
            color = 'background-color: #c8e6c9'
        return [color] * len(row)
    
    st.dataframe(
        scenario_df[::5].style.apply(highlight_scenarios, axis=1),  # Every 5th row
        use_container_width=True,
        height=400
    )
    
    st.info("🟡 Base Case (100%) | 🔴 Worst Case (<60%) | 🟢 Best Case (>120%)")
