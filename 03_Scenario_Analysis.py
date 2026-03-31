import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

df = st.session_state.scenarios

# Payoff chart
fig = px.line(df, x='final_spot_pct*100', y='return_pct', 
              title="Total Return vs Final Performance",
              labels={'x': 'Final Spot Performance (%)', 'return_pct': 'Total Return (%)'})

fig.add_hline(y=0, line_dash="dash", line_color="red", annotation_text="Break-even")
fig.add_vline(x=df['final_barrier'][0]*100, line_dash="dash", line_color="orange", 
              annotation_text="Final Barrier")
fig.add_vline(x=100, line_dash="dot", line_color="gray", annotation_text="Initial Spot")

fig.update_layout(height=500, showlegend=False)
st.plotly_chart(fig, use_container_width=True)

# Autocall heatmap
st.subheader("Autocall Probability by Observation")
autocall_prob = df.groupby((df['final_spot_pct']*100).round(0))['autocall'].mean()
fig2 = px.bar(x=autocall_prob.index, y=autocall_prob.values*100, 
              title="Autocall Probability",
              labels={'x': 'Final Performance %', 'y': 'Autocall Prob %'})
st.plotly_chart(fig2, use_container_width=True)
