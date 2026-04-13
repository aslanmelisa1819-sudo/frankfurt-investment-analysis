import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(page_title="The €3M Decision | Frankfurt", layout="wide")

# 2. Dataset with Final Metrics
data = {
    "District": ["Nordend", "Westend", "Sachsenhausen", "Bornheim", "Gallus", "Hauptbahnhof"],
    "avg_age": [32, 41, 38, 45, 29, 34],
    "tech_adoption": [85, 70, 75, 55, 90, 80],
    "competitor_count": [2, 5, 3, 1, 6, 12],
    "foot_traffic": [12000, 25000, 15000, 9000, 18000, 45000],
    "investment_score": [88, 92, 85, 78, 72, 60],
    "payback_months": [14, 18, 16, 12, 22, 26],
    "lat": [50.1235, 50.1176, 50.0989, 50.1255, 50.1011, 50.1065],
    "lon": [8.6835, 8.6657, 8.6835, 8.7055, 8.6411, 8.6687]
}
df = pd.DataFrame(data)

# 3. Dynamic Profit Calculation Engine
def calculate_dynamic_profit(row):
    conversion_rate = 0.025  
    avg_basket = 18          
    tech_factor = 0.5 + (row['tech_adoption'] / 100)
    annual_revenue = row['foot_traffic'] * conversion_rate * avg_basket * 365 * tech_factor
    net_profit_margin = 0.22  
    return annual_revenue * net_profit_margin

df['annual_profit_est'] = df.apply(calculate_dynamic_profit, axis=1)

# 4. Header Section
st.markdown("# 🚀 The Multi-Million Euro Decision")
st.markdown("### Frankfurt Autonomous Retail Strategy: €280K - €2M Profit Potential")
st.markdown("---")

# 5. Sidebar Filters
st.sidebar.header("🎯 Investment Parameters")
age_limit = st.sidebar.slider("Max. Average Age (Demographic Risk)", 25, 60, 45)
min_profit = st.sidebar.slider("Min. Annual Profit Target (€)", 200000, 1000000, 250000)

filtered_df = df[(df['avg_age'] <= age_limit) & (df['annual_profit_est'] >= min_profit)]

# 6. Top Metrics
m1, m2, m3 = st.columns(3)
m1.metric("Selected Districts", len(filtered_df))
m2.metric("Max Profit Potential", f"€{filtered_df['annual_profit_est'].max()/1000000:.2f}M")
m3.metric("Avg Payback Time", f"{filtered_df['payback_months'].mean():.1f} Mo.")

# 7. Map & Analysis
col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("📍 Investment Heatmap")
    fig = px.scatter_mapbox(filtered_df, lat="lat", lon="lon", size="foot_traffic", 
                             color="annual_profit_est", hover_name="District",
                             color_continuous_scale="Viridis", zoom=11, height=500)
    fig.update_layout(mapbox_style="carto-darkmatter", margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig, use_container_width=True)

with col_right:
    st.subheader("📊 Profit vs. Tech Readiness")
    fig2 = px.bar(filtered_df.sort_values("annual_profit_est"), x="District", y="annual_profit_est", 
                  color="avg_age", labels={"annual_profit_est": "Est. Annual Profit (€)"},
                  color_continuous_scale="RdYlGn_r")
    st.plotly_chart(fig2, use_container_width=True)
