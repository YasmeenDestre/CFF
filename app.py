import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="CFF Investment Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better mobile experience
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
    }
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 30px;
    }
    @media (max-width: 768px) {
        .main-header {
            font-size: 1.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    df = pd.read_excel('data.xlsx')
    # Clean column names
    df.columns = df.columns.str.strip()
    # Rename for easier use
    df = df.rename(columns={'Investment volume': 'Investment'})
    if 'Investment volume ' in df.columns:
        df = df.rename(columns={'Investment volume ': 'Investment'})
    return df

df = load_data()

# Header
st.markdown('<p class="main-header">🌍 CFF Investment Dashboard</p>', unsafe_allow_html=True)

# Sidebar filters
st.sidebar.header("🔍 Filters")

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
        color_discrete_sequence=px.colors.qualitative.Set2,
        hole=0.4
    )
    fig_region.update_traces(textposition='inside', textinfo='percent+label')
    fig_region.update_layout(margin=dict(t=20, b=20, l=20, r=20))
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
        color_continuous_scale='Blues'
    )
    fig_sector.update_layout(
        margin=dict(t=20, b=20, l=20, r=20),
        showlegend=False,
        coloraxis_showscale=False
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
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig_finance.update_layout(
        margin=dict(t=20, b=20, l=20, r=20),
        showlegend=False,
        xaxis_tickangle=-45
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
        color_continuous_scale='Viridis',
        hover_data=['Project']
    )
    fig_top.update_layout(
        margin=dict(t=20, b=20, l=20, r=20),
        coloraxis_showscale=False
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
    color_continuous_scale='RdYlGn'
)
fig_treemap.update_layout(margin=dict(t=20, b=20, l=20, r=20))
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
    "<p style='text-align: center; color: gray;'>CFF Investment Dashboard | Built with Streamlit</p>",
    unsafe_allow_html=True
)
