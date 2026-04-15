# 🚀 The Multi-Million Euro Decision
### Frankfurt Autonomous Retail Strategy — Interactive Investment Simulator

> *Where should Amazon Go-style cashierless stores open in Frankfurt?*  
> *This simulator uses real demographic data to find out.*

🔗 **[Live App](https://frankfurt-investment-analysis-mc4vsosvadjzah6ux9nqk4.streamlit.app/)** &nbsp;|&nbsp; 📊 Built with Streamlit + Plotly

---

## 🧠 Problem

Autonomous retail (cashierless stores) is one of the fastest-growing segments in urban retail. But location is everything — the wrong district means low tech adoption, high competition, and a painful payback period.

**This project simulates which Frankfurt districts offer the best risk-adjusted return** for a €280K–€2M investment in autonomous retail infrastructure.

---

## 🔍 Approach

1. **Data** — District-level demographics: avg age, tech adoption rate, foot traffic, competitor density
2. **Profit Engine** — Dynamic formula combining conversion rate, basket size, tech factor, and net margin
3. **Scoring** — Multi-dimensional investment score per district
4. **Scenario Planning** — Live sliders to model optimistic / pessimistic assumptions

---

## 📊 Features

| Feature | Description |
|---|---|
| 🗺️ Investment Heatmap | Interactive map with profit-colored markers sized by foot traffic |
| 📊 Profit vs. Tech Readiness | Bar chart comparing districts by profit potential and demographic risk |
| 🕸️ Radar Chart | 5-axis multi-dimensional comparison across all filtered districts |
| 📈 Sensitivity Analysis | How profit changes with foot traffic — with min target threshold line |
| 🧮 Scenario Planner | Adjust conversion rate, basket size, margin live via sidebar |
| 🏆 Top Pick Banner | Auto-highlights the best district based on investment score |

---

## 🖥️ Screenshots

<table>
  <tr>
    <td><img src="assets/screenshot1.png" alt="Dashboard Overview"/></td>
    <td><img src="assets/screenshot2.png" alt="Scorecard & Radar"/></td>
  </tr>
  <tr>
    <td><em>Investment Heatmap + KPIs</em></td>
    <td><em>District Scorecard + Radar + Sensitivity</em></td>
  </tr>
</table>

---

## 💡 Key Insights

- **Westend** has the highest investment score (92) despite mid-range foot traffic — driven by high income density and low competitor saturation relative to its purchasing power
- **Hauptbahnhof** has 45K daily foot traffic but scores lowest (60) — 12 competitors and a high avg age (34) significantly compress margins
- **Gallus** is the hidden gem for risk-tolerant investors: youngest demographic (avg 29), highest tech adoption (90%), 18-month payback window

---

## ⚙️ Run Locally

```bash
git clone https://github.com/aslanmelisa1819-sudo/frankfurt-investment-analysis
cd frankfurt-investment-analysis
pip install -r requirements.txt
streamlit run app.py
```

---

## 🛠️ Tech Stack

- **Python** — Data processing & profit engine
- **Streamlit** — Interactive web app framework
- **Plotly** — Maps, bar charts, radar, sensitivity plots
- **Pandas** — Data manipulation

---

## 📁 Project Structure

```
frankfurt-investment-analysis/
├── app.py                  # Main Streamlit application
├── requirements.txt        # Dependencies
├── assets/
│   ├── screenshot1.png     # Dashboard screenshot
│   └── screenshot2.png     # Scorecard screenshot
└── README.md
```

---

## 🔮 Future Work

- [ ] Integrate real foot traffic data (Google Places API)
- [ ] Add rental cost per district to refine ROI
- [ ] Monte Carlo simulation for profit confidence intervals
- [ ] Export report as PDF

---

*Built as part of a data analytics portfolio. Data is simulated for demonstration purposes.*
