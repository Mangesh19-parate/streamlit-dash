import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout="wide", page_title="Startup Funding Analysis", page_icon="💰")

@st.cache_data
def load_data():
    df = pd.read_csv('startup_cleaned.csv')
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df['month'] = df['date'].dt.month
    df['year'] = df['date'].dt.year
    df['investors'] = df['investors'].fillna('Undisclosed')
    return df

df = load_data()

def get_similar_entities(name, type='startup'):
    if type == 'startup':
        # Logic for similar companies based on Vertical 
        vertical = df[df['Startup'] == name]['vertical'].iloc[0]
        similar = df[(df['vertical'] == vertical) & (df['Startup'] != name)]
        return similar['Startup'].unique()[:5].tolist()
    else:
        # Logic for similar investors based on Vertical overlap 
        df_exp = df.assign(investors=df['investors'].str.split(',')).explode('investors')
        df_exp['investors'] = df_exp['investors'].str.strip()
        target_v = df_exp[df_exp['investors'] == name]['vertical'].unique()
        similar = df_exp[(df_exp['vertical'].isin(target_v)) & (df_exp['investors'] != name)]
        return similar['investors'].value_counts().head(5).index.tolist()

#  Company (StartUp) POV  
def load_startup_details(startup):
    st.title(f"Company Profile: {startup}")
    s_df = df[df['Startup'] == startup]
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("General Information")
        st.write(f"**Industry:** {s_df['vertical'].iloc[0]}")
        st.write(f"**Subindustry:** {s_df['subver'].iloc[0]}")
        st.write(f"**Location:** {s_df['city'].iloc[0]}")
    
    st.subheader("Funding Rounds")
    st.table(s_df[['date', 'round', 'investors', 'amount']])

    st.subheader("Similar Companies")
    similar = get_similar_entities(startup, 'startup')
    if similar:
        st.write(", ".join(similar))

# Investor POV 
def load_investor_details(investor):
    st.title(f"Investor Profile: {investor}")
    inv_df = df[df['investors'].str.contains(investor, na=False)]
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Recent Investment", inv_df.sort_values('date', ascending=False)['Startup'].iloc[0])
    col2.metric("Total Invested", f"₹{round(inv_df['amount'].sum()):,} Cr")
    
    st.subheader("Investment Distribution")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.write("**Sector (Pie)**")
        fig, ax = plt.subplots()
        inv_df.groupby('vertical')['amount'].sum().plot(kind='pie', autopct='%1.1f%%', ax=ax)
        st.pyplot(fig)
    with c2:
        st.write("**Stage (Pie)**")
        fig, ax = plt.subplots()
        inv_df.groupby('round')['amount'].sum().plot(kind='pie', autopct='%1.1f%%', ax=ax)
        st.pyplot(fig)
    with c3:
        st.write("**City (Pie)**")
        fig, ax = plt.subplots()
        inv_df.groupby('city')['amount'].sum().plot(kind='pie', autopct='%1.1f%%', ax=ax)
        st.pyplot(fig)

    st.subheader("YoY Investment Graph")
    yoy = inv_df.groupby('year')['amount'].sum()
    st.line_chart(yoy)

    st.subheader("Similar Investors")
    st.write(", ".join(get_similar_entities(investor, 'investor')))

#  General Analysis 
def load_overall_analysis():
    st.title("Overall Ecosystem Analysis")
    
    # Columns for KPIs
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Funding", f"₹{round(df['amount'].sum()):,} Cr")
    c2.metric("Max Investment", f"₹{df['amount'].max():,} Cr")
    c3.metric("Avg Funding", f"₹{round(df['amount'].mean()):,} Cr")
    c4.metric("Funded Startups", df['Startup'].nunique())

    # MoM Chart
    st.subheader("MoM Funding Trend")
    metric = st.selectbox("Select Metric", ["Total Amount", "Deal Count"])
    mom = df.groupby(['year', 'month'])['amount'].sum().reset_index() if metric == "Total Amount" else df.groupby(['year', 'month'])['Startup'].count().reset_index()
    mom['date'] = pd.to_datetime(mom['year'].astype(str) + '-' + mom['month'].astype(str) + '-01')
    st.line_chart(mom.set_index('date').iloc[:, -1])

    # Top Entities
    st.subheader("Top Performers")
    col_a, col_b = st.columns(2)
    with col_a:
        st.write("**Top Startups (Overall)**")
        st.table(df.groupby('Startup')['amount'].sum().sort_values(ascending=False).head(5))
    with col_b:
        st.write("**Top Investors**")
        st.table(df['investors'].str.split(',').explode().value_counts().head(5))

    # Heatmap 
    st.subheader("Funding Heatmap (Year vs Month)")
    heatmap_data = df.pivot_table(index='month', columns='year', values='amount', aggfunc='sum').fillna(0)
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.heatmap(heatmap_data, annot=True, fmt=".0f", cmap="seismic", ax=ax)
    st.pyplot(fig)

#  Sidebar Navigation
st.sidebar.title("StartUp Funding Dashboard")
opt = st.sidebar.selectbox("Navigate", ["Overall Analysis", "Company (StartUp) POV", "Investor POV"])

if opt == "Overall Analysis":
    load_overall_analysis()

elif opt == "Company (StartUp) POV":
    startup = st.sidebar.selectbox("Select Company", sorted(df['Startup'].unique()))
    if st.sidebar.button("Show Profile"):
        load_startup_details(startup)

elif opt == "Investor POV":
    inv_list = sorted(df['investors'].str.split(',').explode().str.strip().unique().tolist())
    investor = st.sidebar.selectbox("Select Investor", inv_list)
    if st.sidebar.button("Show Profile"):
        load_investor_details(investor)
    