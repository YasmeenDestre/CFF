import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# C40 CFF Official Brand Colors
CFF_BLUE = "#004f78"
CFF_GREEN = "#009e30"
CFF_PURPLE = "#720c78"
CFF_LIGHT_GREEN = "#7db61c"
CFF_YELLOW = "#ede100"
CFF_GREY = "#d1d3d4"
CFF_WHITE = "#ffffff"

# Color palette for charts (blue, green, purple focus)
CFF_PALETTE = [CFF_BLUE, CFF_GREEN, CFF_PURPLE, CFF_LIGHT_GREEN]

# Page configuration
st.set_page_config(
    page_title="C40 CFF - Phase 3 Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Clean and sophisticated
st.markdown(f"""
<style>
    /* Clean background */
    .stApp {{
        background-color: {CFF_WHITE};
    }}

    /* Header styling */
    .main-header {{
        font-size: 3.5rem;
        font-weight: 800;
        color: {CFF_BLUE};
        text-align: center;
        margin-bottom: 5px;
        padding: 20px 0 10px 0;
        letter-spacing: 2px;
    }}

    .sub-header {{
        font-size: 1.1rem;
        color: #666;
        text-align: center;
        margin-bottom: 30px;
        font-weight: 400;
        padding-bottom: 15px;
    }}

    /* Sidebar - subtle */
    [data-testid="stSidebar"] {{
        background-color: #f7f9fa;
        border-right: 2px solid {CFF_BLUE};
    }}

    [data-testid="stSidebar"] .stMarkdown h2 {{
        color: {CFF_BLUE} !important;
    }}

    /* Metric cards */
    [data-testid="stMetricValue"] {{
        font-size: 1.8rem;
        color: {CFF_BLUE};
        font-weight: 700;
    }}

    [data-testid="stMetricLabel"] {{
        font-size: 0.95rem;
        color: #555;
    }}

    /* Section headers */
    h3 {{
        color: {CFF_BLUE} !important;
        font-weight: 600;
        font-size: 1.1rem !important;
    }}

    /* Dividers */
    hr {{
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, {CFF_GREY}, transparent);
        margin: 25px 0;
    }}

    /* Download button */
    .stDownloadButton button {{
        background-color: {CFF_BLUE} !important;
        color: white !important;
        border: none;
        font-weight: 500;
        border-radius: 5px;
    }}

    .stDownloadButton button:hover {{
        background-color: {CFF_PURPLE} !important;
    }}

    /* Mobile responsive */
    @media (max-width: 768px) {{
        .main-header {{
            font-size: 1.8rem;
            padding: 10px 0;
        }}
        .sub-header {{
            font-size: 1rem;
        }}
        [data-testid="stMetricValue"] {{
            font-size: 1.3rem;
        }}
    }}

    /* Footer */
    .footer {{
        text-align: center;
        padding: 20px;
        color: #888;
        font-size: 0.85rem;
    }}

    .footer a {{
        color: {CFF_BLUE};
        text-decoration: none;
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
st.markdown(f'<h1 style="font-size: 3.5rem; font-weight: 800; color: {CFF_BLUE}; text-align: center; padding: 20px 0 10px 0;">C40 Cities Finance Facility</h1>', unsafe_allow_html=True)
st.markdown('<p style="font-size: 1.1rem; color: #666666; text-align: center; margin-bottom: 30px;">Phase 3 - Example</p>', unsafe_allow_html=True)

# Sidebar filters
st.sidebar.markdown("## Filters")

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
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_investment = filtered_df['Investment'].sum()
    st.metric(
        label="Total Investment",
        value=f"${total_investment:,.0f}"
    )

with col2:
    num_projects = len(filtered_df)
    st.metric(
        label="Projects",
        value=num_projects
    )

with col3:
    num_cities = filtered_df['City'].nunique()
    st.metric(
        label="Cities",
        value=num_cities
    )

with col4:
    avg_investment = filtered_df['Investment'].mean() if len(filtered_df) > 0 else 0
    st.metric(
        label="Avg. Investment",
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
        color_discrete_sequence=[CFF_BLUE, CFF_GREEN, CFF_PURPLE],
        hole=0.45
    )
    fig_region.update_traces(
        textposition='outside',
        textinfo='percent+label',
        textfont=dict(size=14, color='#333333')
    )
    fig_region.update_layout(
        margin=dict(t=40, b=40, l=40, r=40),
        font=dict(family="Arial", size=12, color="#333333"),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=True,
        legend=dict(font=dict(size=12, color='#333333'))
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
        color_discrete_sequence=[CFF_BLUE]
    )
    fig_sector.update_layout(
        margin=dict(t=20, b=20, l=20, r=20),
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis=dict(gridcolor='rgba(0,0,0,0)', tickfont=dict(color='#333333', size=12)),
        xaxis=dict(gridcolor='rgba(0,79,120,0.1)', tickfont=dict(color='#333333', size=11)),
        font=dict(color='#333333')
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
        color_discrete_sequence=[CFF_GREEN, CFF_BLUE, CFF_PURPLE]
    )
    fig_finance.update_layout(
        margin=dict(t=20, b=20, l=20, r=20),
        showlegend=False,
        xaxis_tickangle=-30,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis=dict(gridcolor='rgba(0,79,120,0.1)', tickfont=dict(color='#333333', size=11)),
        xaxis=dict(gridcolor='rgba(0,0,0,0)', tickfont=dict(color='#333333', size=11)),
        font=dict(color='#333333')
    )
    st.plotly_chart(fig_finance, use_container_width=True)

with col2:
    st.subheader("Top Projects by Investment")
    top_projects = filtered_df.nlargest(10, 'Investment')[['City', 'Project', 'Investment']]
    fig_top = px.bar(
        top_projects.sort_values('Investment', ascending=True),
        x='Investment',
        y='City',
        orientation='h',
        color_discrete_sequence=[CFF_GREEN],
        hover_data=['Project']
    )
    fig_top.update_layout(
        margin=dict(t=20, b=20, l=20, r=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis=dict(gridcolor='rgba(0,0,0,0)', tickfont=dict(color='#333333', size=12)),
        xaxis=dict(gridcolor='rgba(0,158,48,0.1)', tickfont=dict(color='#333333', size=11)),
        font=dict(color='#333333')
    )
    st.plotly_chart(fig_top, use_container_width=True)

# Treemap
st.markdown("---")
st.subheader("Investment Distribution")
fig_treemap = px.treemap(
    filtered_df,
    path=['Region', 'Sector', 'City'],
    values='Investment',
    color='Region',
    color_discrete_map={
        'Africa': CFF_BLUE,
        'Asia': CFF_GREEN,
        'LatAm': CFF_PURPLE
    }
)
fig_treemap.update_layout(
    margin=dict(t=20, b=20, l=20, r=20),
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#333333')
)
fig_treemap.update_traces(
    textfont=dict(color='white', size=14),
    textinfo='label+value'
)
st.plotly_chart(fig_treemap, use_container_width=True)

# Data table
st.markdown("---")
st.subheader("Project Details")

display_df = filtered_df.copy()
display_df['Investment'] = display_df['Investment'].apply(lambda x: f"${x:,.0f}")

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)

# Download button
st.download_button(
    label="Download Data (CSV)",
    data=filtered_df.to_csv(index=False).encode('utf-8'),
    file_name='cff_phase3_data.csv',
    mime='text/csv'
)

# Footer
st.markdown("---")
st.markdown(
    f'<p class="footer">C40 Cities Finance Facility | '
    f'<a href="https://c40cff.org" target="_blank">c40cff.org</a></p>',
    unsafe_allow_html=True
)
