import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import io
from data_loader import fmt

PRIMARY = "#6C63FF"; SECONDARY = "#FF6584"

def _despine(ax):
    for s in ["top","right"]: ax.spines[s].set_visible(False)

def load_startup_details(df, startup):
    st.title(f"{startup}")
    s = df[df["Startup"] == startup].sort_values("Date", ascending=False)

    if s.empty:
        st.warning("No data available."); return

    # KPIs
    c1,c2,c3,c4,c5 = st.columns(5)
    c1.metric("Total Raised",    fmt(s["Amount"].sum()))
    c2.metric("Largest Round",   fmt(s["Amount"].max()))
    c3.metric("Funding Rounds",  len(s))
    c4.metric("Industry",        s["Industry"].iloc[0])
    c5.metric("City",            s["City"].iloc[0])

    st.markdown("---")

    # Profile + Investors
    col_a, col_b = st.columns([1,2])
    with col_a:
        st.markdown("### Profile")
        st.write(f"**SubVertical:** {s['SubVertical'].iloc[0]}")
        st.write(f"**Funding Category:** {s['Funding_Category'].iloc[0]}")
        investors = (s["Investors"].str.split(",").explode()
                      .str.strip().str.strip('"').unique())
        st.markdown(f"**Investors ({len(investors)}):**")
        for inv in investors:
            if inv and inv.lower() != "undisclosed":
                st.markdown(f"&nbsp;&nbsp;• {inv}")

    with col_b:
        st.markdown("### Funding Over Time")
        if len(s) > 1:
            fig, ax = plt.subplots(figsize=(7,3))
            ax.bar(s["Date"].dt.strftime("%b %Y"), s["Amount"],
                   color=PRIMARY, alpha=0.85, edgecolor="white")
            ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: fmt(x)))
            plt.xticks(rotation=30, ha="right")
            _despine(ax)
            plt.tight_layout()
            st.pyplot(fig)
        else:
            st.info("Only one round on record.")

    # Rounds Table
    st.markdown("### Funding Rounds")
    disp = s[["Date","Funding_Round","InvestmentType","Investors","Amount","Funding_Category"]].copy()
    disp["Amount"] = disp["Amount"].apply(fmt)
    disp["Date"]   = disp["Date"].dt.date
    st.dataframe(disp.reset_index(drop=True), use_container_width=True)

    buf = io.BytesIO(); s.to_csv(buf, index=False)
    st.download_button(f" Export {startup} Data", buf.getvalue(),
                       f"{startup.replace(' ','_')}.csv", "text/csv")
