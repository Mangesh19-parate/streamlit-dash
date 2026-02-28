![Streamlit](https://img.shields.io/badge/deployed%20on-streamlit-orange)
## 🚀 Live Demo

🔗 https://startup-investment-dashboard.streamlit.app/

# 💰 Startup Funding Intelligence Dashboard

> An interactive, multi-view analytics dashboard that explores startup funding trends across industries, cities, investors, and time using Python and Streamlit.

This project transforms raw funding data into actionable business intelligence through advanced visual analytics and structured data engineering — simulating a real-world investment analytics platform used by VCs, analysts, and ecosystem researchers.

---

## 📌 Project Overview

The Startup Funding Intelligence Dashboard provides:

- 📊 Ecosystem-level funding insights
- 🚀 Startup-level performance analysis
- 💼 Investor-level portfolio intelligence
- 📈 Time-series funding evolution
- 🔎 Advanced trend and distribution analysis

---

## 🧠 Business Questions Answered

- Which industries attract the most capital?
- Which cities dominate startup funding?
- How has funding evolved year-over-year?
- What is the distribution of deal sizes?
- Which investors deploy capital most effectively?
- How do funding stages evolve over time?
- Who are the top funded startups?

---

## 🏗️ Architecture & Design

The project follows a modular and scalable structure:

```
📦 project/
 ┣ 📜 app.py               # App routing & layout
 ┣ 📜 data_loader.py       # Data cleaning & feature engineering
 ┣ 📜 filters.py           # Sidebar filter logic
 ┣ 📜 analysis.py          # Ecosystem-level analytics
 ┣ 📜 startup_view.py      # Startup-level dashboard
 ┣ 📜 investor_view.py     # Investor-level dashboard
```

**Why this architecture matters:** This mirrors real-world production dashboards through separation of concerns, a clean data pipeline, reusable modules, and a scalable design.

---

## 🛠️ Tech Stack

| Category | Tools |
|----------|-------|
| Language | Python |
| Data Processing | Pandas, NumPy |
| Visualization | Matplotlib, Seaborn |
| Dashboard Framework | Streamlit |

---

## 🔄 Data Engineering & Feature Engineering

- Date parsing & time-series extraction (Year, Month, YearMonth)
- Funding normalization and cleaning
- Industry & investor standardization
- Missing value handling
- Funding category segmentation
- Investor power aggregation

---

## 📊 Key Features

### 📈 Time-Series Analysis
- Year-on-Year funding trend
- Cumulative funding growth
- Monthly seasonality patterns
- Funding stage evolution over time

### 🌍 Ecosystem Analysis
- Top industries by funding
- City-wise capital deployment
- Deal size distribution (log-scale)
- Funding category breakdown

### 🚀 Startup Intelligence
- Funding timeline visualization
- Investor breakdown
- Funding round history
- Startup profile summary

### 💼 Investor Intelligence
- Portfolio industry allocation
- Deployment trends
- Power score analysis
- Influence and ranking metrics

---

## 📸 Dashboard Views

| View | Description |
|------|-------------|
| 📊 Overall Ecosystem Analysis | KPIs, industry and city trends, deal size distributions |
| 🚀 Startup POV | Per-startup funding timeline, round history, and investor breakdown |
| 💼 Investor POV | Portfolio allocation, power scores, and deployment trends |

---

## 📈 Advanced Analytics Implemented

- **Dual-axis visualization** — Funding vs. Deal count on a shared timeline
- **Bubble analysis** — Deal count vs. Funding vs. Average deal size
- **Log-scale distribution modeling** — Captures the skewed nature of funding amounts
- **Stacked funding stage evolution** — Tracks how Seed, Series A/B/C, and later stages shift over time
- **Month × Year funding heatmap** — Reveals seasonality patterns in investment activity
- **Investor power score aggregation** — Composite metric for investor influence and reach

---

## 🚀 Future Enhancements

- [ ] Funding amount prediction model
- [ ] Investor ranking algorithm
- [ ] Startup growth classification
- [ ] Clustering industries by funding patterns
- [ ] Interactive deployment on Streamlit Cloud

---

## 💡 Key Learnings

- Handling real-world noisy financial data
- Designing multi-view analytical dashboards
- Translating raw data into meaningful business insights
- Structuring scalable analytics applications
- Time-series funding analysis techniques

---

## 🎯 Ideal For

This project is particularly relevant for interviews and portfolios targeting:

- Data Analyst roles
- Business Intelligence roles
- Junior Data Scientist positions
- Analytics internship interviews

---

## 📬 Contact

Feel free to reach out or open an issue if you have suggestions, questions, or want to collaborate!
