from streamlit.runtime.scriptrunner import add_script_run_ctx
import streamlit as st
st.set_page_config(
    page_title="💰 Smart Budget Tracker | AF3005",
    page_icon="💸",
    layout="wide",
    initial_sidebar_state="expanded"
)
import pandas as pd
import plotly.express as px
from datetime import datetime

# Custom CSS
st.markdown("""
<style>
    /* === Base Styles === */
    * {
        font-family: 'Inter', sans-serif;
    }

    /* === Main Container === */
    .main {
        background: #0f0f1a;
        background: linear-gradient(155deg, #0f0f1a 0%, #1a1a2f 100%);
    }

    /* === Glassmorphism Sidebar === */
    [data-testid=stSidebar] {
        background: rgba(25, 25, 50, 0.9) !important;
        backdrop-filter: blur(15px) !important;
        border-right: 1px solid rgba(255,255,255,0.1);
        box-shadow: 5px 0 25px rgba(0,0,0,0.3);
    }

    /* === Neon Accent Elements === */
    .stButton>button {
        background: linear-gradient(45deg, #00f2fe, #4facfe) !important;
        border: none !important;
        color: white !important;
        border-radius: 12px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(79,172,254,0.3) !important;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(79,172,254,0.5) !important;
    }

    /* === Holographic Metric Cards === */
    [data-testid="metric-container"] {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 20px !important;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }

    [data-testid="metric-container"]::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(79,172,254,0.1), transparent);
        transform: rotate(45deg);
        animation: hologram 6s linear infinite;
    }

    [data-testid="metric-container"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 30px rgba(0,0,0,0.3) !important;
    }

    /* === Animated Input Fields === */
    .stTextInput input, .stNumberInput input, .stDateInput input, .stSelectbox select {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        color: white !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
        transition: all 0.3s ease !important;
    }

    .stTextInput input:focus, .stNumberInput input:focus, .stDateInput input:focus {
        border-color: #4facfe !important;
        box-shadow: 0 0 0 3px rgba(79,172,254,0.2) !important;
        background: rgba(79,172,254,0.05) !important;
    }

    /* === Cyberpunk Progress Bar === */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #ff61d7 0%, #7c4dff 100%) !important;
        border-radius: 8px;
        box-shadow: 0 0 15px rgba(124,77,255,0.3);
    }

    /* === Animated Title === */
    h1 {
        font-family: 'Poppins', sans-serif;
        font-weight: 700 !important;
        background: linear-gradient(45deg, #00f2fe, #4facfe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 30px rgba(79,172,254,0.3);
        animation: titleGlow 2s ease-in-out infinite alternate;
    }

    /* === Custom Scrollbar === */
    ::-webkit-scrollbar {
        width: 8px;
        background: rgba(0,0,0,0.2);
    }

    ::-webkit-scrollbar-thumb {
        background: linear-gradient(45deg, #4facfe, #00f2fe);
        border-radius: 4px;
    }

    /* === Keyframe Animations === */
    @keyframes hologram {
        0% { transform: rotate(45deg) translate(-30%, -30%); }
        100% { transform: rotate(45deg) translate(30%, 30%); }
    }

    @keyframes titleGlow {
        0% { text-shadow: 0 0 20px rgba(79,172,254,0.3); }
        100% { text-shadow: 0 0 40px rgba(79,172,254,0.6); }
    }

    /* === Chart Containers === */
    .stPlotlyChart {
        border-radius: 20px !important;
        overflow: hidden;
        border: 1px solid rgba(255,255,255,0.1);
        background: rgba(255,255,255,0.05) !important;
    }

    /* === Success Message Styling === */
    .stAlert {
        border-radius: 15px !important;
        background: rgba(76,175,80,0.15) !important;
        border: 1px solid #4CAF50 !important;
    }
</style>
""", unsafe_allow_html=True)
# Initialize Session State
if 'transactions' not in st.session_state:
    st.session_state.transactions = []

if 'budget' not in st.session_state:
    st.session_state.budget = 0

# Helper Functions
def add_transaction(type, category, amount, date, notes):
    st.session_state.transactions.append({
        "Date": date,
        "Type": type,
        "Category": category,
        "Amount": amount,
        "Notes": notes
    })

def calculate_metrics():
    df = pd.DataFrame(st.session_state.transactions)
    if df.empty:
        return 0, 0, 0
    
    income = df[df['Type'] == 'Income']['Amount'].sum()
    expenses = df[df['Type'] == 'Expense']['Amount'].sum()
    balance = income - expenses
    return income, expenses, balance

# Sidebar Inputs
with st.sidebar:
    st.header("➕ Add Transaction")
    transaction_type = st.selectbox("Type", ["Income", "Expense"])
    category = st.selectbox("Category", ["Salary", "Investment", "Freelance"] if transaction_type == "Income" 
                          else ["Food", "Transport", "Housing", "Entertainment", "Utilities"])
    amount = st.number_input("Amount ($)", min_value=0.0, step=10.0)
    date = st.date_input("Date", datetime.today())
    notes = st.text_input("Notes")
    
    if st.button("Add Transaction", use_container_width=True):
        add_transaction(transaction_type, category, amount, date, notes)
        st.success("Transaction Added!")

    st.header("🎯 Set Monthly Budget")
    st.session_state.budget = st.number_input("Monthly Budget ($)", min_value=0, step=100)

# Main Interface
st.title("💰 Smart Budget Tracker")
st.markdown("Track your finances with interactive visualizations and real-time insights")

# Metrics
income, expenses, balance = calculate_metrics()
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Income", f"${income:,.2f}")
with col2:
    st.metric("Total Expenses", f"${expenses:,.2f}", delta=f"-${expenses:,.2f}")
with col3:
    st.metric("Current Balance", f"${balance:,.2f}", 
             delta="Over Budget" if balance < 0 else "Under Budget")
with col4:
    if st.session_state.budget > 0:
        budget_usage = (expenses / st.session_state.budget) * 100
        st.metric("Budget Used", f"{budget_usage:.1f}%")
        st.progress(budget_usage/100)

# Visualizations
if not pd.DataFrame(st.session_state.transactions).empty:
    df = pd.DataFrame(st.session_state.transactions)
    df['Month'] = pd.to_datetime(df['Date']).dt.strftime('%B %Y')
    
    tab1, tab2, tab3 = st.tabs(["📈 Spending Analysis", "📅 Monthly Trends", "📋 Transaction History"])
    
    with tab1:
        fig = px.pie(df[df['Type'] == 'Expense'], 
                     values='Amount', 
                     names='Category',
                     title="Expense Distribution by Category")
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        monthly_data = df.groupby(['Month', 'Type'])['Amount'].sum().reset_index()
        fig = px.bar(monthly_data, 
                     x='Month', 
                     y='Amount',
                     color='Type',
                     title="Monthly Income vs Expenses")
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.dataframe(df.sort_values('Date', ascending=False),
                     use_container_width=True,
                     hide_index=True)
else:
    st.info("No transactions recorded yet. Start adding transactions from the sidebar!")
