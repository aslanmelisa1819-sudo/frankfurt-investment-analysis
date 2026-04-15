import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ─── 1. PAGE CONFIG ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="The Multi-Million Euro Decision | Frankfurt",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── 2. CUSTOM CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=Inter:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #0a0a0f;
    color: #e8e8f0;
}

h1, h2, h3 { font-family: 'Syne', sans-serif !important; }

.main .block-container { padding-top: 2rem; padding-bottom: 2rem; }

/* KPI Cards */
[data-testid="metric-container"] {
    background: linear-gradient(135deg, #12121a 0%, #1a1a2e 100%);
    border: 1px solid #2a2a4a;
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    box-shadow: 0 4px 24px rgba(0,0,0,0.4);
}
[data-testid="metric-container"]:hover {
    border-color: #4f8ef7;
    transition: border-color 0.3s ease;
}
[data-testid="stMetricLabel"] { color: #8888aa !important; font-size: 0.78rem !important; letter-spacing: 0.08em; text-transform: uppercase; }
[data-testid="stMetricValue"] { font-family: 'Syne', sans-serif !important; font-size: 2rem !important; color: #ffffff !important; }
[data-testid="stMetricDelta"] { font-size: 0.8rem !important; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: #0d0d18 !important;
    border-right: 1px solid #1e1e38;
}
[data-testid="stSidebar"] * { color: #c8c8e0 !important; }

/* Section headers */
.section-label {
    font-family: 'Syne', sans-serif;
    font-size: 0.72rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #4f8ef7;
    margin-bottom: 0.3rem;
}

/* Best pick banner */
.best-pick {
    background: linear-gradient(135deg, #0f2027, #1a3a2a);
    border: 1px solid #2ecc71;
    border-left: 4px solid #2ecc71;
    border-radius: 10px;
    padding: 1rem 1.4rem;
    margin: 1.2rem 0;
}
.best-pick strong { color: #2ecc71; font-family: 'Syne', sans-serif; }

/* Warning banner */
.warning-box {
    background: linear-gradient(135deg, #1a1200, #2a1a00);
    border: 1px solid #f39c12;
    border-left: 4px solid #f39c12;
    border-radius: 10px;
    padding: 1rem 1.4rem;
    margin: 1.2rem 0;
}

/* Table */
[data-testid="stDataFrame"] { border-radius: 10px; overflow: hidden; }

/* Divider */
hr { border-color: #1e1e38 !important; margin: 1.5rem 0 !important; }

/* Subtitle */
.subtitle { color: #8888aa; font-size: 0.9rem; line-height: 1.7; max-width: 820px; }
</style>
""", unsafe_allow_html=True)

# ─── 3. DATA ───────────────────────────────────────────────────────────────────
data = {
    "District":          ["Nordend", "Westend", "Sachsenhausen", "Bornheim", "Gallus", "Hauptbahnhof"],
    "avg_age":           [32, 41, 38, 45, 29, 34],
    "tech_adoption":     [85, 70, 75, 55, 90, 80],
    "competitor_count":  [2, 5, 3, 1, 6, 12],
    "foot_traffic":      [12000, 25000, 15000, 9000, 18000, 45000],
    "investment_score":  [88, 92, 85, 78, 72, 60],
    "payback_months":    [14, 18, 16, 12, 22, 26],
    "lat":               [50.1235, 50.1176, 50.0989, 50.1255, 50.1011, 50.1065],
    "lon":               [8.6835,  8.6657,  8.6835,  8.7055,  8.6411,  8.6687],
}
df = pd.DataFrame(data)

# ─── 4. DYNAMIC PROFIT ENGINE ──────────────────────────────────────────────────
def calculate_profit(row, conversion_rate, avg_basket, net_margin):
    tech_factor = 0.5 + (row["tech_adoption"] / 100)
    annual_revenue = row["foot_traffic"] * conversion_rate * avg_basket * 365 * tech_factor
    return annual_revenue * net_margin

# ─── 5. SIDEBAR ────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎯 Investment Parameters")
    st.markdown("---")

    st.markdown('<p class="section-label">📊 Demographic Filters</p>', unsafe_allow_html=True)
    age_limit       = st.slider("Max. Average Age", 25, 60, 45, help="Filter out older demographic districts")
    max_competitors = st.slider("Max. Competitor Count", 0, 15, 12, help="Limit high-competition areas")

    st.markdown("---")
    st.markdown('<p class="section-label">💰 Profit Target</p>', unsafe_allow_html=True)
    min_profit = st.slider("Min. Annual Profit (€)", 200_000, 1_000_000, 250_000, step=50_000,
                           format="€%d")

    st.markdown("---")
    st.markdown('<p class="section-label">🧮 Scenario Assumptions</p>', unsafe_allow_html=True)
    conversion_rate = st.slider("Conversion Rate (%)", 1.0, 5.0, 2.5, step=0.1,
                                help="% of foot traffic that makes a purchase") / 100
    avg_basket      = st.slider("Avg. Basket Size (€)", 8, 40, 18,
                                help="Average spend per transaction")
    net_margin      = st.slider("Net Profit Margin (%)", 10, 35, 22, step=1,
                                help="Margin after COGS and opex") / 100

    st.markdown("---")
    st.caption("💡 Adjust assumptions to model optimistic / pessimistic scenarios.")

# ─── 6. RECALCULATE WITH LIVE PARAMS ──────────────────────────────────────────
df["annual_profit_est"] = df.apply(
    lambda r: calculate_profit(r, conversion_rate, avg_basket, net_margin), axis=1
)

filtered_df = df[
    (df["avg_age"]          <= age_limit) &
    (df["annual_profit_est"] >= min_profit) &
    (df["competitor_count"] <= max_competitors)
].copy()

# ─── 7. HEADER ─────────────────────────────────────────────────────────────────
st.markdown("# 🚀 The Multi-Million Euro Decision")
st.markdown("### Frankfurt Autonomous Retail Strategy")
st.markdown(
    '<p class="subtitle">A simulation of where Amazon Go-style cashierless stores would thrive in Frankfurt — '
    "using real demographic data to identify districts with the right mix of tech-savvy customers, "
    "high foot traffic, and low competition.</p>",
    unsafe_allow_html=True
)
st.markdown("---")

# ─── 8. EMPTY STATE ────────────────────────────────────────────────────────────
if filtered_df.empty:
    st.markdown(
        '<div class="warning-box">⚠️ <strong>No districts match your current filters.</strong> '
        "Try relaxing the age limit, profit target, or competitor threshold in the sidebar.</div>",
        unsafe_allow_html=True
    )
    st.stop()

# ─── 9. TOP KPIs ───────────────────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)
total_profit  = filtered_df["annual_profit_est"].sum()
max_profit    = filtered_df["annual_profit_est"].max()
avg_payback   = filtered_df["payback_months"].mean()
best_score    = filtered_df["investment_score"].max()

k1.metric("Selected Districts",   len(filtered_df),                    f"{len(df) - len(filtered_df)} filtered out")
k2.metric("Max Profit Potential", f"€{max_profit/1_000_000:.2f}M",     delta=None)
k3.metric("Portfolio Total",      f"€{total_profit/1_000_000:.2f}M",   delta=None)
k4.metric("Avg Payback Time",     f"{avg_payback:.1f} Mo.",            delta=None)

# ─── 10. BEST PICK BANNER ──────────────────────────────────────────────────────
best = filtered_df.loc[filtered_df["investment_score"].idxmax()]
st.markdown(
    f'<div class="best-pick">🏆 <strong>Top Pick: {best["District"]}</strong> — '
    f'Investment Score: <strong>{best["investment_score"]}</strong> &nbsp;|&nbsp; '
    f'Est. Annual Profit: <strong>€{best["annual_profit_est"]/1000:.0f}K</strong> &nbsp;|&nbsp; '
    f'Payback: <strong>{best["payback_months"]} months</strong> &nbsp;|&nbsp; '
    f'Competitors: <strong>{int(best["competitor_count"])}</strong></div>',
    unsafe_allow_html=True
)

st.markdown("---")

# ─── 11. MAP + BAR CHART ───────────────────────────────────────────────────────
col_left, col_right = st.columns([3, 2])

PLOTLY_THEME = dict(
    paper_bgcolor="#0a0a0f",
    plot_bgcolor="#0a0a0f",
    font=dict(color="#c8c8e0", family="Inter"),
    margin=dict(r=10, t=10, l=10, b=10),
)

with col_left:
    st.markdown('<p class="section-label">📍 Investment Heatmap</p>', unsafe_allow_html=True)
    fig_map = px.scatter_map(
        filtered_df, lat="lat", lon="lon",
        size="foot_traffic", color="annual_profit_est",
        hover_name="District",
        hover_data={
            "annual_profit_est": ":,.0f",
            "foot_traffic": ":,",
            "tech_adoption": True,
            "competitor_count": True,
            "lat": False, "lon": False
        },
        color_continuous_scale="Viridis",
        size_max=40, zoom=11, height=460
    )
    fig_map.update_layout(
        map_style="carto-darkmatter",
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        coloraxis_colorbar=dict(title="Annual Profit (€)", tickformat=",.0f")
    )
    st.plotly_chart(fig_map, use_container_width=True)

with col_right:
    st.markdown('<p class="section-label">📊 Profit vs. Tech Readiness</p>', unsafe_allow_html=True)
    fig_bar = px.bar(
        filtered_df.sort_values("annual_profit_est"),
        x="District", y="annual_profit_est",
        color="avg_age",
        labels={"annual_profit_est": "Est. Annual Profit (€)", "avg_age": "Avg Age"},
        color_continuous_scale="RdYlGn_r",
        height=460,
        text=filtered_df.sort_values("annual_profit_est")["annual_profit_est"].apply(
            lambda x: f"€{x/1000:.0f}K"
        )
    )
    fig_bar.update_traces(textposition="outside", textfont_size=11)
    fig_bar.update_layout(
        **PLOTLY_THEME,
        xaxis_tickangle=-30,
        xaxis=dict(gridcolor="#1e1e38"),
        yaxis=dict(gridcolor="#1e1e38", tickformat=",.0f"),
        coloraxis_colorbar=dict(title="Avg Age"),
    )
    st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("---")

# ─── 12. SCENARIO ANALYSIS + RADAR ────────────────────────────────────────────
col_a, col_b = st.columns([2, 3])

with col_a:
    st.markdown('<p class="section-label">🔍 District Scorecard</p>', unsafe_allow_html=True)
    display_df = filtered_df[[
        "District", "investment_score", "annual_profit_est",
        "payback_months", "competitor_count", "tech_adoption"
    ]].sort_values("investment_score", ascending=False).reset_index(drop=True)

    display_df.columns = ["District", "Score", "Annual Profit (€)", "Payback (Mo.)", "Competitors", "Tech (%)"]
    display_df["Annual Profit (€)"] = display_df["Annual Profit (€)"].apply(lambda x: f"€{x:,.0f}")

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Score": st.column_config.ProgressColumn("Score", min_value=0, max_value=100, format="%d"),
        }
    )

with col_b:
    st.markdown('<p class="section-label">🕸️ Multi-Dimensional Comparison</p>', unsafe_allow_html=True)
    categories = ["Tech Adoption", "Foot Traffic\n(norm)", "Low Competition", "Investment Score", "Youth Index"]

    fig_radar = go.Figure()
    foot_max = df["foot_traffic"].max()

    for _, row in filtered_df.iterrows():
        values = [
            row["tech_adoption"],
            row["foot_traffic"] / foot_max * 100,
            max(0, 100 - row["competitor_count"] * 7),
            row["investment_score"],
            max(0, 100 - (row["avg_age"] - 25) * 2),
        ]
        values += [values[0]]  # close polygon

        fig_radar.add_trace(go.Scatterpolar(
            r=values,
            theta=categories + [categories[0]],
            fill="toself",
            opacity=0.5,
            name=row["District"]
        ))

    fig_radar.update_layout(
        **PLOTLY_THEME,
        polar=dict(
            bgcolor="#0d0d18",
            radialaxis=dict(visible=True, range=[0, 100], gridcolor="#2a2a4a", tickcolor="#555"),
            angularaxis=dict(gridcolor="#2a2a4a", tickcolor="#aaa"),
        ),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#c8c8e0")),
        height=400,
    )
    st.plotly_chart(fig_radar, use_container_width=True)

st.markdown("---")

# ─── 13. SENSITIVITY ANALYSIS ──────────────────────────────────────────────────
st.markdown('<p class="section-label">📈 Sensitivity: How Profit Changes with Foot Traffic</p>', unsafe_allow_html=True)

traffic_range = list(range(5000, 55000, 2500))
sens_data = []
for district_row in filtered_df.itertuples():
    for traffic in traffic_range:
        temp = {"foot_traffic": traffic, "tech_adoption": district_row.tech_adoption}
        tech_factor = 0.5 + (temp["tech_adoption"] / 100)
        profit = traffic * conversion_rate * avg_basket * 365 * tech_factor * net_margin
        sens_data.append({"District": district_row.District, "Foot Traffic": traffic, "Annual Profit (€)": profit})

sens_df = pd.DataFrame(sens_data)
fig_sens = px.line(
    sens_df, x="Foot Traffic", y="Annual Profit (€)", color="District",
    height=320, markers=False,
)
fig_sens.update_layout(
    **PLOTLY_THEME,
    xaxis=dict(gridcolor="#1e1e38", tickformat=","),
    yaxis=dict(gridcolor="#1e1e38", tickformat=",.0f"),
    legend=dict(bgcolor="rgba(0,0,0,0)"),
)
fig_sens.add_hline(y=min_profit, line_dash="dot", line_color="#f39c12",
                   annotation_text=f"Min Target: €{min_profit:,}", annotation_font_color="#f39c12")
st.plotly_chart(fig_sens, use_container_width=True)

# ─── 14. FOOTER ────────────────────────────────────────────────────────────────
st.markdown("---")
st.caption("📌 Data is simulated for demonstration purposes. Built with Streamlit + Plotly · Frankfurt Autonomous Retail Analysis")
