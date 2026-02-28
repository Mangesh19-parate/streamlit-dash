import streamlit as st
from data_loader import load_data
from filters import apply_filters
from analysis import load_overall_analysis
from startup_view import load_startup_details
from investor_view import load_investor_details

st.set_page_config(
    layout="wide",
    page_title="Startup Funding Dashboard",
    page_icon="💰",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
  .block-container{padding-top:1.2rem;}
  [data-testid="metric-container"]{
    background:#f0f2f6;border-radius:10px;padding:10px 14px;
  }
  [data-testid="stSidebar"]{background-color:#1a1a2e;}
  [data-testid="stSidebar"] label,
  [data-testid="stSidebar"] .stMarkdown,
  [data-testid="stSidebar"] p {color:#e0e0e0 !important;}
  [data-testid="stSidebar"] .stRadio label {color:#ffffff !important;}
</style>
""", unsafe_allow_html=True)

# Load & filter
df = load_data()
filtered_df = apply_filters(df)

# Navigation
st.sidebar.markdown("---")
st.sidebar.markdown("## Navigation")
option = st.sidebar.radio(
    "", ["Overall Analysis", " Startup POV", "Investor POV"]
)

if option == "Overall Analysis":
    load_overall_analysis(filtered_df)

elif option == "Startup POV":
    st.sidebar.markdown("### Search Startup")
    search = st.sidebar.text_input("Type to search...", "")
    startup_list = sorted(filtered_df["Startup"].unique())
    if search:
        startup_list = [s for s in startup_list if search.lower() in s.lower()]
    if not startup_list:
        st.warning("No startups found.")
    else:
        startup = st.sidebar.selectbox("Select Startup", startup_list)
        load_startup_details(filtered_df, startup)

elif option == " Investor POV":
    st.sidebar.markdown("### Search Investor")
    search = st.sidebar.text_input("Type to search...", "")
    inv_list = sorted(
        filtered_df["Investors"].str.split(",").explode()
        .str.strip().str.strip('"').dropna().unique()
    )
    if search:
        inv_list = [i for i in inv_list if search.lower() in i.lower()]
    if not inv_list:
        st.warning("No investors found.")
    else:
        investor = st.sidebar.selectbox("Select Investor", inv_list)
        load_investor_details(filtered_df, investor)
