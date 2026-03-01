import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    df = pd.read_csv("StartUp.csv")

    # Date
    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True, errors="coerce")
    df = df.dropna(subset=["Date"])
    df["Year"]       = df["Date"].dt.year.astype(int)
    df["Month"]      = df["Date"].dt.month.astype(int)
    df["Month_Name"] = df["Date"].dt.strftime("%b")
    df["YearMonth"]  = df["Date"].dt.to_period("M").dt.to_timestamp()

    # Amount
    df["Amount"] = pd.to_numeric(df["Amount in USD"], errors="coerce").fillna(0)

    # Clean strings
    df["Investors"]         = df["Investors"].fillna("Undisclosed").str.strip().str.strip('"')
    df["Industry Vertical"] = df["Industry Vertical"].fillna("Unknown").str.strip()
    df["City"]              = df["City"].fillna("Unknown").str.strip().str.rstrip(",")
    df["Investment Type"]   = df["Investment Type"].fillna("Unknown").str.strip().str.title()
    df["Startup Name"]      = df["Startup Name"].fillna("Unknown").str.strip()
    df["Funding_Category"]  = df["Funding_Category"].fillna("Unknown")
    df["Funding_Round"]     = df["Funding_Round"].fillna("Other")
    df["SubVertical"]       = df["SubVertical"].fillna("N/A").str.strip()

    # Aliases
    df["Industry"]       = df["Industry Vertical"]
    df["Startup"]        = df["Startup Name"]
    df["InvestmentType"] = df["Investment Type"]

    return df


def fmt(n):
    """Human-readable money format."""
    if n >= 1e9:  return f"${n/1e9:.2f}B"
    if n >= 1e6:  return f"${n/1e6:.1f}M"
    if n >= 1e3:  return f"${n/1e3:.0f}K"
    return f"${n:,.0f}"
