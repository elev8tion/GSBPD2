import streamlit as st
import pandas as pd
import requests
import json
import plotly.express as px

# Page Config
st.set_page_config(
    page_title="Grok's Memvid Visualizer",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Neon/Dark Theme
st.markdown("""
    <style>
    .stApp {
        background-color: #0f172a;
        color: #f8fafc;
    }
    .stMarkdown, .stHeader, .stMetricLabel {
        color: #f8fafc !important;
    }
    div[data-testid="stMetricValue"] {
        color: #8b5cf6 !important;
    }
    .css-1d391kg {
        background-color: #1e293b;
    }
    div.stButton > button {
        background: linear-gradient(to right, #8b5cf6, #06b6d4);
        color: white;
        border: none;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.title("🧠 Grok's Memvid Visual DB")
st.markdown("Visualizing the **Memvid** video storage for your betting portfolio.")

# Fetch Data
API_URL = "http://localhost:8000/portfolio"

@st.cache_data(ttl=5)
def fetch_data():
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            return response.json()
        else:
            st.error("Failed to fetch data from backend.")
            return []
    except Exception as e:
        st.error(f"Connection Error: {e}")
        return []

data = fetch_data()

if not data:
    st.warning("No bets found in Memvid storage yet.")
else:
    # Metrics
    df = pd.DataFrame(data)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Bets Stored", len(df))
    with col2:
        total_wagered = df['wager_amount'].sum() if 'wager_amount' in df.columns else 0
        st.metric("Total Volume", f"${total_wagered:,.2f}")
    with col3:
        # Mock win rate calculation
        win_rate = 50 # Placeholder
        st.metric("Est. Win Rate", f"{win_rate}%")

    # Visuals
    st.subheader("💾 Memory Chunks (Video Frames)")
    
    for i, bet in enumerate(data):
        status_color = "orange"
        if bet.get('status') == 'WIN':
            status_color = "green"
        elif bet.get('status') == 'LOSS':
            status_color = "red"
            
        with st.expander(f"Frame #{i+1}: {bet.get('home_team')} vs {bet.get('away_team')} [{bet.get('status')}]", expanded=False):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Status:** :{status_color}[{bet.get('status')}]")
                st.markdown(f"**Wager:** ${bet.get('wager_amount')}")
                st.markdown(f"**Odds:** {bet.get('odds')}")
                st.code(json.dumps(bet, indent=2), language='json')
            
            with col2:
                if 'shap_values' in bet and bet['shap_values']:
                    st.markdown("**🧠 AI Reasoning (SHAP):**")
                    shap_df = pd.DataFrame(list(bet['shap_values'].items()), columns=['Feature', 'Impact'])
                    shap_df['Color'] = shap_df['Impact'].apply(lambda x: 'Positive' if x > 0 else 'Negative')
                    
                    fig = px.bar(shap_df, x='Impact', y='Feature', orientation='h', 
                                 color='Color', color_discrete_map={'Positive': '#10b981', 'Negative': '#ef4444'},
                                 title="Why did Grok make this bet?",
                                 template="plotly_dark")
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No AI reasoning data stored for this bet.")

    st.subheader("📈 Analytics")
    if 'wager_amount' in df.columns:
        fig = px.bar(df, x=df.index, y='wager_amount', title="Wager History", 
                     labels={'index': 'Bet Sequence', 'wager_amount': 'Amount ($)'},
                     template="plotly_dark")
        fig.update_traces(marker_color='#8b5cf6')
        st.plotly_chart(fig, use_container_width=True)

# Sidebar
st.sidebar.header("Control Panel")
if st.sidebar.button("Refresh Data"):
    st.cache_data.clear()
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.info("This dashboard connects to the FastAPI backend to visualize the contents of the `portfolio.mp4` Memvid file.")
