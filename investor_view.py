import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import io
from data_loader import fmt

COLORS  = ["#6C63FF","#FF6584","#43C6AC","#F7B731","#20BF6B",
           "#EB3B5A","#2D98DA","#FD9644","#A55EEA","#26de81"]

def _despine(ax):
    for s in ["top","right"]: ax.spines[s].set_visible(False)

def load_investor_details(df, investor):
    st.title(f"{investor}")

    inv_df = df[df["Investors"].str.contains(investor, na=False, case=False)]
    if inv_df.empty:
        st.warning("No data found for this investor."); return

    # KPIs
    c1,c2,c3,c4,c5 = st.columns(5)
    c1.metric("Total Deployed",     fmt(inv_df["Amount"].sum()))
    c2.metric("Largest Bet",        fmt(inv_df["Amount"].max()))
    c3.metric("Portfolio Companies",inv_df["Startup"].nunique())
    c4.metric("Industries",         inv_df["Industry"].nunique())
    c5.metric("Avg Power Score",    f"{inv_df['Power_Score_x'].mean():.3f}")

    st.markdown("---")

    col_a, col_b = st.columns(2)

    # Industry Pie
    with col_a:
        st.subheader("Portfolio by Industry")
        ind = inv_df.groupby("Industry")["Amount"].sum().sort_values(ascending=False).head(8)
        if ind.sum() > 0:
            fig1, ax1 = plt.subplots(figsize=(5,4))
            ax1.pie(ind.values, labels=ind.index, autopct="%1.1f%%",
                    startangle=140, colors=COLORS[:len(ind)], pctdistance=0.8)
            ax1.set_ylabel("")
            st.pyplot(fig1)

    # YoY dual axis
    with col_b:
        st.subheader("Investment Activity by Year")
        yoy = inv_df.groupby("Year").agg(Total=("Amount","sum"), Deals=("Amount","count")).reset_index()
        fig2, ax2 = plt.subplots(figsize=(5,4))
        ax2.bar(yoy["Year"], yoy["Total"], color="#6C63FF", alpha=0.8, width=0.4)
        ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: fmt(x)))
        ax2_t = ax2.twinx()
        ax2_t.plot(yoy["Year"], yoy["Deals"], marker="o", color="#FF6584", linewidth=2)
        ax2_t.set_ylabel("Deal Count", color="#FF6584")
        ax2.set_ylabel("Amount"); ax2.set_xlabel("Year")
        ax2.set_xticks(yoy["Year"]); _despine(ax2)
        plt.tight_layout(); st.pyplot(fig2)

    # Stage Mix
    st.subheader("Investment Stage Mix")
    stage = inv_df["Funding_Round"].value_counts()
    fig3, ax3 = plt.subplots(figsize=(10,2.5))
    stage.sort_values().plot(kind="barh", ax=ax3, color=COLORS[:len(stage)], alpha=0.85)
    ax3.set_xlabel("Number of Deals"); _despine(ax3)
    plt.tight_layout(); st.pyplot(fig3)

    # Power Score & Influence
    st.subheader("Power Score & Influence")
    col_c, col_d = st.columns(2)
    with col_c:
        st.metric("Avg Power Score",    f"{inv_df['Power_Score_x'].mean():.4f}")
        st.metric("Avg Influence Index",f"{inv_df['Influence_Index'].mean():.4f}")
        st.metric("Avg Final Rank",     f"{inv_df['Final_Rank'].mean():.0f}")
    with col_d:
        # Power score distribution
        fig4, ax4 = plt.subplots(figsize=(5,3))
        ax4.hist(inv_df["Power_Score_x"], bins=15, color="#6C63FF", alpha=0.8, edgecolor="white")
        ax4.set_xlabel("Power Score"); ax4.set_ylabel("Frequency")
        ax4.set_title("Power Score Distribution", fontweight="bold")
        _despine(ax4); plt.tight_layout()
        st.pyplot(fig4)

    # Full Portfolio Table
    st.subheader("Full Portfolio")
    disp = inv_df[["Date","Startup","Industry","City","Funding_Round","Amount","Power_Score_x","Final_Rank"]].copy()
    disp["Amount"]       = disp["Amount"].apply(fmt)
    disp["Date"]         = disp["Date"].dt.date
    disp["Power_Score_x"]= disp["Power_Score_x"].round(4)
    st.dataframe(disp.reset_index(drop=True), use_container_width=True)

    buf = io.BytesIO(); inv_df.to_csv(buf, index=False)
    st.download_button(f"Export {investor} Portfolio", buf.getvalue(),
                       f"{investor.replace(' ','_')}.csv","text/csv")
