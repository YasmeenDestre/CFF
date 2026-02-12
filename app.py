import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# C40 CFF Brand Colors
C40_GREEN = "#00A651"
C40_DARK_GREEN = "#006837"
C40_LIGHT_GREEN = "#39B54A"
C40_YELLOW = "#FFC107"
C40_DARK = "#1a1a2e"

# Custom color scales for charts
C40_GREENS = [C40_DARK_GREEN, C40_GREEN, C40_LIGHT_GREEN, "#7DC242", "#B5D334"]
C40_PALETTE = [C40_GREEN, C40_DARK_GREEN, C40_LIGHT_GREEN, C40_YELLOW, "#2E7D32", "#81C784"]

# Page configuration
st.set_page_config(
    page_title="C40 CFF Investment Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with C40 CFF branding
st.markdown(f"""
<style>
    /* Main background */
    .stApp {{
        background: linear-gradient(180deg, #f8fdf8 0%, #ffffff 100%);
    }}

    /* Header styling */
    .main-header {{
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, {C40_DARK_GREEN} 0%, {C40_GREEN} 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 10px;
        padding: 20px 0;
    }}

    .sub-header {{
        font-size: 1.3rem;
        color: #555;
        text-align: center;
        margin-bottom: 30px;
        font-weight: 400;
    }}

    /* Sidebar styling */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {C40_DARK_GREEN} 0%, {C40_GREEN} 100%);
    }}

    [data-testid="stSidebar"] * {{
        color: white !important;
    }}

    [data-testid="stSidebar"] .stSelectbox label {{
        color: white !important;
        font-weight: 600;
    }}

    /* Metric cards */
    [data-testid="stMetricValue"] {{
        font-size: 2rem;
        color: {C40_DARK_GREEN};
        font-weight: 700;
    }}

    [data-testid="stMetricLabel"] {{
        font-size: 1rem;
        color: #333;
    }}

    /* Section headers */
    .stSubheader {{
        color: {C40_DARK_GREEN} !important;
        font-weight: 600;
    }}

    h3 {{
        color: {C40_DARK_GREEN} !important;
    }}

    /* Dividers */
    hr {{
        border-color: {C40_GREEN} !important;
        opacity: 0.3;
    }}

    /* Download button */
    .stDownloadButton button {{
        background-color: {C40_GREEN} !important;
        color: white !important;
        border: none;
        font-weight: 600;
    }}

    .stDownloadButton button:hover {{
        background-color: {C40_DARK_GREEN} !important;
    }}

    /* Mobile responsive */
    @media (max-width: 768px) {{
        .main-header {{
            font-size: 2rem;
            padding: 10px 0;
        }}
        .sub-header {{
            font-size: 1rem;
        }}
        [data-testid="stMetricValue"] {{
            font-size: 1.5rem;
        }}
    }}

    /* Footer */
    .footer {{
        text-align: center;
        padding: 20px;
        color: #666;
        font-size: 0.9rem;
    }}

    .footer a {{
        color: {C40_GREEN};
        text-decoration: none;
        font-weight: 600;
    }}
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    df = pd.read_excel('data.xlsx')
    df.columns = df.columns.str.strip()
    df = df.rename(columns={'Investment volume': 'Investment'})
    if 'Investment volume ' in df.columns:
        df = df.rename(columns={'Investment volume ': 'Investment'})
    return df

df = load_data()

# Header
st.markdown('<h1 class="main-header">C40 Cities Finance Facility</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Investment Portfolio Dashboard</p>', unsafe_allow_html=True)

# Sidebar filters
st.sidebar.markdown("## 🔍 Filters")

# Region filter
regions = ['All'] + sorted(df['Region'].unique().tolist())
selected_region = st.sidebar.selectbox('Region', regions)

# Sector filter
sectors = ['All'] + sorted(df['Sector'].unique().tolist())
selected_sector = st.sidebar.selectbox('Sector', sectors)

# Finance status filter
finance_status = ['All'] + sorted(df['Link to finance'].unique().tolist())
selected_finance = st.sidebar.selectbox('Finance Status', finance_status)

# Apply filters
filtered_df = df.copy()
if selected_region != 'All':
    filtered_df = filtered_df[filtered_df['Region'] == selected_region]
if selected_sector != 'All':
    filtered_df = filtered_df[filtered_df['Sector'] == selected_sector]
if selected_finance != 'All':
    filtered_df = filtered_df[filtered_df['Link to finance'] == selected_finance]

# KPI Metrics
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_investment = filtered_df['Investment'].sum()
    st.metric(
        label="💰 Total Investment",
        value=f"${total_investment:,.0f}"
    )

with col2:
    num_projects = len(filtered_df)
    st.metric(
        label="📋 Projects",
        value=num_projects
    )

with col3:
    num_cities = filtered_df['City'].nunique()
    st.metric(
        label="🏙️ Cities",
        value=num_cities
    )

with col4:
    avg_investment = filtered_df['Investment'].mean() if len(filtered_df) > 0 else 0
    st.metric(
        label="📊 Avg. Investment",
        value=f"${avg_investment:,.0f}"
    )

st.markdown("---")

# Charts row 1
col1, col2 = st.columns(2)

with col1:
    st.subheader("Investment by Region")
    region_data = filtered_df.groupby('Region')['Investment'].sum().reset_index()
    fig_region = px.pie(
        region_data,
        values='Investment',
        names='Region',
        color_discrete_sequence=C40_PALETTE,
        hole=0.4
    )
    fig_region.update_traces(
        textposition='inside',
        textinfo='percent+label',
        textfont_size=14
    )
    fig_region.update_layout(
        margin=dict(t=20, b=20, l=20, r=20),
        font=dict(family="Arial", size=12),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_region, use_container_width=True)

with col2:
    st.subheader("Investment by Sector")
    sector_data = filtered_df.groupby('Sector')['Investment'].sum().reset_index()
    fig_sector = px.bar(
        sector_data.sort_values('Investment', ascending=True),
        x='Investment',
        y='Sector',
        orientation='h',
        color='Investment',
        color_continuous_scale=[[0, C40_LIGHT_GREEN], [0.5, C40_GREEN], [1, C40_DARK_GREEN]]
    )
    fig_sector.update_layout(
        margin=dict(t=20, b=20, l=20, r=20),
        showlegend=False,
        coloraxis_showscale=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis=dict(gridcolor='rgba(0,166,81,0.1)'),
        xaxis=dict(gridcolor='rgba(0,166,81,0.1)')
    )
    st.plotly_chart(fig_sector, use_container_width=True)

# Charts row 2
col1, col2 = st.columns(2)

with col1:
    st.subheader("Finance Status")
    finance_data = filtered_df.groupby('Link to finance')['Investment'].sum().reset_index()
    fig_finance = px.bar(
        finance_data,
        x='Link to finance',
        y='Investment',
        color='Link to finance',
        color_discrete_sequence=[C40_GREEN, C40_DARK_GREEN, C40_LIGHT_GREEN]
    )
    fig_finance.update_layout(
        margin=dict(t=20, b=20, l=20, r=20),
        showlegend=False,
        xaxis_tickangle=-45,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis=dict(gridcolor='rgba(0,166,81,0.1)'),
        xaxis=dict(gridcolor='rgba(0,166,81,0.1)')
    )
    st.plotly_chart(fig_finance, use_container_width=True)

with col2:
    st.subheader("Top 10 Projects by Investment")
    top_projects = filtered_df.nlargest(10, 'Investment')[['City', 'Project', 'Investment']]
    fig_top = px.bar(
        top_projects.sort_values('Investment', ascending=True),
        x='Investment',
        y='City',
        orientation='h',
        color='Investment',
        color_continuous_scale=[[0, C40_LIGHT_GREEN], [0.5, C40_GREEN], [1, C40_DARK_GREEN]],
        hover_data=['Project']
    )
    fig_top.update_layout(
        margin=dict(t=20, b=20, l=20, r=20),
        coloraxis_showscale=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis=dict(gridcolor='rgba(0,166,81,0.1)'),
        xaxis=dict(gridcolor='rgba(0,166,81,0.1)')
    )
    st.plotly_chart(fig_top, use_container_width=True)

# Investment by Region and Sector (Treemap)
st.markdown("---")
st.subheader("Investment Distribution (Region & Sector)")
fig_treemap = px.treemap(
    filtered_df,
    path=['Region', 'Sector', 'City'],
    values='Investment',
    color='Investment',
    color_continuous_scale=[[0, "#E8F5E9"], [0.3, C40_LIGHT_GREEN], [0.6, C40_GREEN], [1, C40_DARK_GREEN]]
)
fig_treemap.update_layout(
    margin=dict(t=20, b=20, l=20, r=20),
    paper_bgcolor='rgba(0,0,0,0)'
)
st.plotly_chart(fig_treemap, use_container_width=True)

# Data table
st.markdown("---")
st.subheader("📋 Project Details")

# Format investment column for display
display_df = filtered_df.copy()
display_df['Investment'] = display_df['Investment'].apply(lambda x: f"${x:,.0f}")

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)

# Download button
st.download_button(
    label="📥 Download Filtered Data (CSV)",
    data=filtered_df.to_csv(index=False).encode('utf-8'),
    file_name='cff_filtered_data.csv',
    mime='text/csv'
)

# Footer
st.markdown("---")
st.markdown(
    f'<p class="footer">C40 Cities Finance Facility Dashboard | '
    f'<a href="https://c40cff.org" target="_blank">c40cff.org</a></p>',
    unsafe_allow_html=True
)
