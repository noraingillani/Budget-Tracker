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
    /* Main container styling */
    .main {
        background: linear-gradient(145deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    /* Sidebar with glassmorphism effect */
    [data-testid=stSidebar] {
        background: rgba(40, 70, 110, 0.85) !important;
        backdrop-filter: blur(12px) !important;
        box-shadow: 5px 0 15px rgba(0,0,0,0.1);
        border-right: 1px solid rgba(255,255,255,0.1);
    }
    
    /* Sidebar hover effects */
    [data-testid=stSidebar] .stButton button {
        transition: all 0.3s ease;
        border: 2px solid rgba(255,255,255,0.2) !important;
    }
    
    [data-testid=stSidebar] .stButton button:hover {
        transform: translateY(-2px);
        background: rgba(255,255,255,0.1) !important;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    /* Metric cards with neumorphic design */
    [data-testid="metric-container"] {
        background: linear-gradient(145deg, #ffffff, #f8f9fa) !important;
        border-radius: 15px !important;
        box-shadow: 8px 8px 16px #d9d9d9, 
                   -8px -8px 16px #ffffff !important;
        padding: 20px !important;
        margin: 10px 0;
        border: none !important;
        transition: all 0.3s ease;
    }
    
    [data-testid="metric-container"]:hover {
        transform: translateY(-5px);
        box-shadow: 12px 12px 24px #d1d1d1, 
                   -12px -12px 24px #ffffff !important;
    }
    
    /* Progress bar styling */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%) !important;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(0,0,0,0.05);
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(45deg, #4facfe, #00f2fe);
        border-radius: 4px;
    }
    
    /* Data table styling */
    [data-testid="stDataFrame"] {
        border-radius: 15px !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05) !important;
        border: 1px solid rgba(0,0,0,0.05) !important;
    }
    
    /* Input field styling */
    .stTextInput input, .stNumberInput input, .stDateInput input {
        border: 2px solid rgba(0,0,0,0.1) !important;
        border-radius: 8px !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput input:focus, .stNumberInput input:focus, .stDateInput input:focus {
        border-color: #4facfe !important;
        box-shadow: 0 0 0 3px rgba(79,172,254,0.2) !important;
    }
    
    /* Custom header styling */
    h1 {
        font-family: 'Segoe UI', sans-serif;
        font-weight: 700 !important;
        color: #2c3e50 !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.05);
        letter-spacing: -0.5px !important;
    }
    
    /* Floating animation for main title */
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-5px); }
        100% { transform: translateY(0px); }
    }
    
    h1 {
        animation: float 3s ease-in-out infinite;
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