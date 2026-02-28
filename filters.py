import streamlit as st

def apply_filters(df):
    st.sidebar.markdown("## Filters")

    all_years      = ["All"] + sorted(df["Year"].unique())
    all_cities     = ["All"] + sorted(df["City"].unique())
    all_industries = ["All"] + sorted(df["Industry"].unique())
    all_rounds     = sorted(df["Funding_Round"].unique())

    if st.sidebar.button("Reset Filters"):
        for k in ["f_year","f_city","f_ind","f_round"]:
            if k in st.session_state: del st.session_state[k]

    year_filter  = st.sidebar.selectbox("Year",            all_years,      index=0)
    ind_filter   = st.sidebar.selectbox("Industry",        all_industries, index=0)
    city_filter  = st.sidebar.selectbox("City",           all_cities,     index=0)
    round_filter = st.sidebar.multiselect("Funding Round", all_rounds,     default=all_rounds)

    fdf = df[
        (df["Year"] == year_filter if year_filter != "All" else True) &
        (df["Industry"] == ind_filter if ind_filter != "All" else True) &
        (df["City"] == city_filter if city_filter != "All" else True) &
        df["Funding_Round"].isin(round_filter)
    ]

    active = sum([
        year_filter != "All",
        ind_filter != "All",
        city_filter != "All",
        len(round_filter) < len(all_rounds),
    ])
    if active:
        st.sidebar.info(f"{active} filter(s) active · {len(fdf):,} rows")

    if fdf.empty:
        st.warning("No data matches current filters.")
        st.stop()

    return fdf
