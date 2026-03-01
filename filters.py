import streamlit as st

def apply_filters(df):
    all_years      = ["All"] + sorted(df["Year"].unique())
    all_cities     = ["All"] + sorted(df["City"].unique())
    all_industries = ["All"] + sorted(df["Industry"].unique())
    all_rounds     = sorted(df["Funding_Round"].unique())

    with st.sidebar:
        st.markdown("## Filters")

        if st.button("Reset Filters"):
            for k in ["f_year","f_city","f_ind","f_round"]:
                if k in st.session_state: del st.session_state[k]

        year_filter  = st.selectbox("Year",            all_years,      index=0)
        ind_filter   = st.selectbox("Industry",        all_industries, index=0)
        city_filter  = st.selectbox("City",           all_cities,     index=0)
        round_filter = st.multiselect("Funding Round", all_rounds,     default=all_rounds)

        active = sum([
            year_filter != "All",
            ind_filter != "All",
            city_filter != "All",
            len(round_filter) < len(all_rounds),
        ])
        if active:
            st.info(f"{active} filter(s) active")

    fdf = df[
        (df["Year"] == year_filter if year_filter != "All" else True) &
        (df["Industry"] == ind_filter if ind_filter != "All" else True) &
        (df["City"] == city_filter if city_filter != "All" else True) &
        df["Funding_Round"].isin(round_filter)
    ]

    if active:
        st.sidebar.info(f"{active} filter(s) active · {len(fdf):,} rows")

    if fdf.empty:
        st.warning("No data matches current filters.")
        st.stop()

    return fdf
