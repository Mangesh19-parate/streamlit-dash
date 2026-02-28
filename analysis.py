import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.patches as mpatches
import seaborn as sns
import io

from data_loader import fmt

# Style constants 
PRIMARY   = "#6C63FF"
SECONDARY = "#FF6584"
ACCENT    = "#43C6AC"
BG        = "#F8F9FB"
COLORS    = [PRIMARY, SECONDARY, ACCENT, "#F7B731", "#20BF6B", "#EB3B5A",
             "#2D98DA", "#FD9644", "#A55EEA", "#26de81"]

def _despine(ax):
    for spine in ["top","right"]:
        ax.spines[spine].set_visible(False)

def _yax_fmt(ax):
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: fmt(x)))

def _dl_csv(df, label):
    buf = io.BytesIO(); df.to_csv(buf, index=False)
    st.download_button(f"Download {label}", buf.getvalue(),
                       f"{label.replace(' ','_')}.csv", "text/csv")

# Overall Analysis Page
def load_overall_analysis(df):
    st.title("Overall Ecosystem Analysis")

    # SECTION 1: Dataset Record 
    st.markdown("### Dataset Record")
    period_start = df["Date"].min().strftime("%b %Y")
    period_end   = df["Date"].max().strftime("%b %Y")
    c1,c2,c3 = st.columns(3)
    c1.metric("Period",         f"{period_start} → {period_end}")
    c2.metric("Total Records",  f"{len(df):,}")
    c3.metric("Visualization Types", "12")

    st.markdown("---")

    # SECTION 2: Top KPIs 
    st.markdown("### Key Metrics")
    k1,k2,k3,k4 = st.columns(4)
    k1.metric("Total Funding",    fmt(df["Amount"].sum()))
    k2.metric("Unique Startups",  f"{df['Startup'].nunique():,}")
    k3.metric("Industry Sectors", f"{df['Industry'].nunique():,}")
    k4.metric("Cities",           f"{df['City'].nunique():,}")

    st.markdown("---")

    # CHART 1: Top Industries by Funding 
    st.subheader("Top Industries by Funding")
    ind_fund = (df.groupby("Industry")["Amount"].sum()
                  .sort_values(ascending=False).head(12))
    fig, ax = plt.subplots(figsize=(12, 4))
    bars = ax.bar(ind_fund.index, ind_fund.values, color=COLORS[:len(ind_fund)], edgecolor="white")
    for bar in bars:
        ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()*1.01,
                fmt(bar.get_height()), ha="center", va="bottom", fontsize=7.5, fontweight="bold")
    ax.set_xticklabels(ind_fund.index, rotation=30, ha="right", fontsize=9)
    _yax_fmt(ax); _despine(ax)
    ax.set_ylabel("Total Funding")
    plt.tight_layout()
    st.pyplot(fig)

    st.markdown("---")

    # CHART 2: City-wise Funding Map (bar chart) 
    st.subheader("City-wise Funding")
    col_a, col_b = st.columns(2)

    with col_a:
        city_fund = (df.groupby("City")["Amount"].sum()
                       .sort_values(ascending=False).head(10))
        fig2, ax2 = plt.subplots(figsize=(6,4))
        city_fund.sort_values().plot(kind="barh", ax=ax2, color=PRIMARY, alpha=0.85)
        ax2.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: fmt(x)))
        ax2.set_xlabel("Total Funding"); ax2.set_ylabel("")
        ax2.set_title("Top 10 Cities by Funding", fontweight="bold")
        _despine(ax2); plt.tight_layout()
        st.pyplot(fig2)

    with col_b:
        city_deal = df["City"].value_counts().head(10)
        fig3, ax3 = plt.subplots(figsize=(6,4))
        city_deal.sort_values().plot(kind="barh", ax=ax3, color=SECONDARY, alpha=0.85)
        ax3.set_xlabel("Number of Deals"); ax3.set_ylabel("")
        ax3.set_title("Top 10 Cities by Deal Count", fontweight="bold")
        _despine(ax3); plt.tight_layout()
        st.pyplot(fig3)

    st.markdown("---")

    # CHART 3: Funding Round State (Funding_Category) 
    st.subheader("Funding Round State Distribution")
    col_c, col_d = st.columns(2)

    with col_c:
        cat_counts = df["Funding_Category"].value_counts()
        fig4, ax4 = plt.subplots(figsize=(5,4))
        wedges, texts, autotexts = ax4.pie(
            cat_counts.values, labels=cat_counts.index,
            autopct="%1.1f%%", startangle=140,
            colors=COLORS[:len(cat_counts)], pctdistance=0.8
        )
        for t in autotexts: t.set_fontsize(9)
        ax4.set_title("By Funding Category", fontweight="bold")
        st.pyplot(fig4)

    with col_d:
        round_counts = df["Funding_Round"].value_counts()
        fig5, ax5 = plt.subplots(figsize=(5,4))
        round_counts.sort_values().plot(kind="barh", ax=ax5,
                                        color=COLORS[:len(round_counts)], alpha=0.9)
        ax5.set_xlabel("Number of Deals")
        ax5.set_title("By Funding Round", fontweight="bold")
        _despine(ax5); plt.tight_layout()
        st.pyplot(fig5)

    st.markdown("---")

    # CHART 4: Top Funded Startups 
    st.subheader("Top 15 Funded Startups")
    top_start = (df.groupby("Startup")["Amount"].sum()
                   .sort_values(ascending=False).head(15))
    fig6, ax6 = plt.subplots(figsize=(12, 4))
    bars6 = ax6.bar(top_start.index, top_start.values,
                    color=[COLORS[i % len(COLORS)] for i in range(len(top_start))],
                    edgecolor="white")
    for bar in bars6:
        ax6.text(bar.get_x()+bar.get_width()/2, bar.get_height()*1.01,
                 fmt(bar.get_height()), ha="center", va="bottom", fontsize=7, fontweight="bold")
    ax6.set_xticklabels(top_start.index, rotation=35, ha="right", fontsize=8.5)
    _yax_fmt(ax6); _despine(ax6)
    ax6.set_ylabel("Total Raised")
    plt.tight_layout()
    st.pyplot(fig6)

    st.markdown("---")

    # CHART 5: Deal Size Distribution 
    st.subheader("Deal Size Distribution")
    col_e, col_f = st.columns(2)

    with col_e:
        nonzero = df[df["Amount"] > 0]["Amount"]
        fig7, ax7 = plt.subplots(figsize=(6,4))
        ax7.hist(np.log10(nonzero), bins=40, color=PRIMARY, alpha=0.8, edgecolor="white")
        ax7.set_xlabel("Log₁₀ (Deal Size in USD)")
        ax7.set_ylabel("Number of Deals")
        ax7.set_title("Distribution of Deal Sizes (log scale)", fontweight="bold")
        _despine(ax7); plt.tight_layout()
        st.pyplot(fig7)

    with col_f:
        cat_amt = df.groupby("Funding_Category")["Amount"].sum()
        cat_order = ["Small","Medium","Large","Very Large"]
        cat_amt = cat_amt.reindex([c for c in cat_order if c in cat_amt.index])
        fig8, ax8 = plt.subplots(figsize=(6,4))
        ax8.bar(cat_amt.index, cat_amt.values,
                color=[COLORS[i] for i in range(len(cat_amt))], alpha=0.9, edgecolor="white")
        for bar in ax8.patches:
            ax8.text(bar.get_x()+bar.get_width()/2, bar.get_height()*1.02,
                     fmt(bar.get_height()), ha="center", va="bottom", fontsize=9, fontweight="bold")
        _yax_fmt(ax8); _despine(ax8)
        ax8.set_title("Total Funding by Category", fontweight="bold")
        plt.tight_layout()
        st.pyplot(fig8)

    st.markdown("---")

    # SECTION: Year-on-Year Analysis 
    st.markdown("## Year-on-Year Analysis")

    yoy = df.groupby("Year").agg(
        Total=("Amount","sum"),
        Deals=("Amount","count"),
        AvgDeal=("Amount","mean"),
        Startups=("Startup","nunique")
    ).reset_index()

    # YoY Trend
    st.subheader("Year-on-Year Funding Trend")
    fig9, ax9 = plt.subplots(figsize=(12,4))
    ax9.fill_between(yoy["Year"], yoy["Total"], alpha=0.18, color=PRIMARY)
    ax9.plot(yoy["Year"], yoy["Total"], marker="o", color=PRIMARY,
             linewidth=2.5, markersize=8, label="Total Funding")
    for _, row in yoy.iterrows():
        ax9.annotate(fmt(row["Total"]), (row["Year"], row["Total"]),
                     textcoords="offset points", xytext=(0,8),
                     ha="center", fontsize=9, fontweight="bold", color=PRIMARY)
    ax9_twin = ax9.twinx()
    ax9_twin.bar(yoy["Year"], yoy["Deals"], alpha=0.2, color=SECONDARY, width=0.4, label="Deal Count")
    ax9_twin.set_ylabel("Deal Count", color=SECONDARY)
    _yax_fmt(ax9); ax9.set_ylabel("Total Funding"); ax9.set_xlabel("Year")
    ax9.set_xticks(yoy["Year"])
    _despine(ax9)
    lines1, labels1 = ax9.get_legend_handles_labels()
    lines2, labels2 = ax9_twin.get_legend_handles_labels()
    ax9.legend(lines1+lines2, labels1+labels2, loc="upper left")
    plt.tight_layout()
    st.pyplot(fig9)

    # Avg Deal Size vs Total Deals
    st.subheader("Avg Deal Size vs Total Deals per Year")
    fig10, ax10 = plt.subplots(figsize=(12,4))
    x = np.arange(len(yoy))
    w = 0.35
    bars_a = ax10.bar(x-w/2, yoy["Total"],   width=w, label="Total Funding", color=PRIMARY,   alpha=0.85)
    bars_b = ax10.bar(x+w/2, yoy["AvgDeal"], width=w, label="Avg Deal Size", color=SECONDARY, alpha=0.85)
    ax10.set_xticks(x); ax10.set_xticklabels(yoy["Year"])
    _yax_fmt(ax10); _despine(ax10)
    ax10.legend(); ax10.set_ylabel("Amount (USD)")
    plt.tight_layout()
    st.pyplot(fig10)

    # Funding Stage Evolution over years
    st.subheader("Funding Stage Evolution (Year-wise)")
    stage_year = df.groupby(["Year","Funding_Round"])["Amount"].sum().unstack(fill_value=0)
    fig11, ax11 = plt.subplots(figsize=(12,5))
    stage_year.plot(kind="bar", stacked=True, ax=ax11,
                    color=COLORS[:len(stage_year.columns)], edgecolor="white", alpha=0.9)
    _yax_fmt(ax11); _despine(ax11)
    ax11.set_xlabel("Year"); ax11.set_ylabel("Total Funding")
    ax11.legend(title="Stage", bbox_to_anchor=(1.01,1), loc="upper left")
    plt.xticks(rotation=0)
    plt.tight_layout()
    st.pyplot(fig11)

    st.markdown("---")

    # Advanced Charts
    st.markdown("## Advanced Analysis")

    # Cumulative Funding Growth
    st.subheader("Cumulative Funding Growth")
    monthly = (df.groupby("YearMonth")["Amount"].sum()
                 .reset_index().sort_values("YearMonth"))
    monthly["Cumulative"] = monthly["Amount"].cumsum()
    fig12, ax12 = plt.subplots(figsize=(12,4))
    ax12.fill_between(monthly["YearMonth"], monthly["Cumulative"], alpha=0.2, color=ACCENT)
    ax12.plot(monthly["YearMonth"], monthly["Cumulative"], color=ACCENT, linewidth=2)
    _yax_fmt(ax12); _despine(ax12)
    ax12.set_xlabel("Month"); ax12.set_ylabel("Cumulative Funding")
    plt.xticks(rotation=30)
    plt.tight_layout()
    st.pyplot(fig12)

    # Monthly Funding Pattern
    st.subheader("Monthly Funding Pattern")
    month_order = ["Jan","Feb","Mar","Apr","May","Jun",
                   "Jul","Aug","Sep","Oct","Nov","Dec"]
    monthly_avg = df.groupby("Month_Name")["Amount"].sum().reindex(
        [m for m in month_order if m in df["Month_Name"].unique()]
    )
    fig13, ax13 = plt.subplots(figsize=(12,4))
    ax13.fill_between(range(len(monthly_avg)), monthly_avg.values, alpha=0.2, color=PRIMARY)
    ax13.plot(range(len(monthly_avg)), monthly_avg.values, marker="o", color=PRIMARY, linewidth=2)
    ax13.set_xticks(range(len(monthly_avg)))
    ax13.set_xticklabels(monthly_avg.index)
    _yax_fmt(ax13); _despine(ax13)
    ax13.set_ylabel("Total Funding"); ax13.set_xlabel("Month")
    plt.tight_layout()
    st.pyplot(fig13)

    # Industry Bubble Analysis
    st.subheader("Industry Bubble Analysis")
    ind_bubble = df.groupby("Industry").agg(
        TotalFunding=("Amount","sum"),
        DealCount=("Amount","count"),
        AvgDeal=("Amount","mean")
    ).reset_index().sort_values("TotalFunding", ascending=False).head(20)

    fig14, ax14 = plt.subplots(figsize=(12,6))
    scatter = ax14.scatter(
        ind_bubble["DealCount"],
        ind_bubble["TotalFunding"],
        s=ind_bubble["AvgDeal"]/1e4,
        c=range(len(ind_bubble)),
        cmap="viridis", alpha=0.75, edgecolors="white", linewidths=1
    )
    for _, row in ind_bubble.iterrows():
        ax14.annotate(row["Industry"],
                      (row["DealCount"], row["TotalFunding"]),
                      fontsize=7.5, ha="center", va="bottom",
                      xytext=(0,6), textcoords="offset points")
    ax14.set_xlabel("Number of Deals")
    ax14.set_ylabel("Total Funding")
    _yax_fmt(ax14); _despine(ax14)
    ax14.set_title("Bubble size = Avg Deal Size", fontsize=9, color="gray")
    plt.tight_layout()
    st.pyplot(fig14)

    # Top Investors Power Score
    st.subheader("Top Investors by Power Score")
    inv_power = (
        df[["Investors","Power_Score_x","Influence_Index","Amount"]]
        .copy()
    )
    inv_power["Investors"] = inv_power["Investors"].str.strip().str.strip('"')
    inv_agg = inv_power.groupby("Investors").agg(
        AvgPowerScore=("Power_Score_x","mean"),
        AvgInfluence=("Influence_Index","mean"),
        TotalInvested=("Amount","sum"),
        Deals=("Amount","count")
    ).reset_index()
    inv_agg = inv_agg[inv_agg["Investors"] != "Undisclosed"]
    top_inv = inv_agg.sort_values("AvgPowerScore", ascending=False).head(15)

    fig15, ax15 = plt.subplots(figsize=(12,5))
    bars15 = ax15.barh(top_inv["Investors"], top_inv["AvgPowerScore"],
                       color=COLORS[:len(top_inv)], alpha=0.9)
    for bar in bars15:
        ax15.text(bar.get_width()+0.005, bar.get_y()+bar.get_height()/2,
                  f"{bar.get_width():.3f}", va="center", fontsize=8, fontweight="bold")
    ax15.set_xlabel("Average Power Score")
    ax15.set_title("Top 15 Investors by Power Score", fontweight="bold")
    ax15.invert_yaxis()
    _despine(ax15)
    plt.tight_layout()
    st.pyplot(fig15)

    # Funding Heatmap (Month x Year)
    st.subheader("Monthly Funding Heatmap (Month × Year)")
    heatmap_data = df.pivot_table(
        index="Month_Name", columns="Year",
        values="Amount", aggfunc="sum"
    ).fillna(0)
    heatmap_data = heatmap_data.reindex(
        [m for m in month_order if m in heatmap_data.index]
    )
    fig16, ax16 = plt.subplots(figsize=(12,5))
    sns.heatmap(heatmap_data/1e6, cmap="YlOrRd", ax=ax16,
                fmt=".0f", linewidths=0.5, annot=True,
                cbar_kws={"label":"Funding ($M)"})
    ax16.set_xlabel("Year"); ax16.set_ylabel("Month")
    plt.tight_layout()
    st.pyplot(fig16)

    st.markdown("---")

    # Top 10 Deals Table 
    st.subheader("Top 10 Largest Deals")
    top10 = (df.nlargest(10,"Amount")
               [["Date","Startup","Industry","City","Funding_Round","Investors","Amount"]]
               .copy())
    top10["Amount_fmt"] = top10["Amount"].apply(fmt)
    top10["Date"] = top10["Date"].dt.date
    st.dataframe(top10.drop(columns=["Amount"]).rename(columns={"Amount_fmt":"Amount"}),
                 use_container_width=True)

    _dl_csv(df, "startup_funding_filtered")
