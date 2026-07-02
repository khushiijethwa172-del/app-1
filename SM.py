import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

st.set_page_config(
    page_title="Global Stock Analyzer",
    page_icon="📈",
    layout="wide"
)

# ---------------------- CSS ---------------------

st.markdown("""
<style>

.main{
background-color:#0f172a;
}

h1,h2,h3{
color:white;
}

.metric-container{
padding:15px;
border-radius:15px;
background:#1e293b;
box-shadow:0px 4px 15px rgba(0,0,0,0.3);
}

.stock-card{
padding:12px;
border-radius:12px;
background:#1e293b;
color:white;
margin-bottom:8px;
}

</style>
""", unsafe_allow_html=True)

# ---------------------- Sidebar -----------------------

st.sidebar.title("📊 Global Stock Explorer")

popular = {
    "Apple":"AAPL",
    "Microsoft":"MSFT",
    "Tesla":"TSLA",
    "NVIDIA":"NVDA",
    "Amazon":"AMZN",
    "Google":"GOOGL",
    "Meta":"META",
    "Netflix":"NFLX",
    "Reliance":"RELIANCE.NS",
    "TCS":"TCS.NS",
    "Infosys":"INFY.NS"
}

st.sidebar.subheader("Popular Stocks")

selected = st.sidebar.selectbox(
    "Choose Stock",
    list(popular.keys())
)

symbol = popular[selected]

custom = st.sidebar.text_input(
    "Or Enter Symbol",
    placeholder="Example: AAPL"
)

if custom:
    symbol = custom.upper()

period = st.sidebar.selectbox(
    "Select Time Period",
    [
        "1d",
        "5d",
        "1mo",
        "3mo",
        "6mo",
        "1y",
        "2y",
        "5y",
        "max"
    ]
)

# ---------------------- Title -----------------------

st.title("📈 Global Stock Market Dashboard")

st.write(
    "Live Stock Market Data powered by Yahoo Finance"
)

# ---------------------- Fetch Data -----------------------

stock = yf.Ticker(symbol)

info = stock.info

hist = stock.history(period=period)

if hist.empty:
    st.error("No Data Found")
    st.stop()

current_price = hist["Close"].iloc[-1]

previous = hist["Close"].iloc[-2] if len(hist)>1 else current_price

change = current_price-previous

percent = (change/previous)*100 if previous else 0

# ---------------------- Metrics -----------------------

col1,col2,col3,col4 = st.columns(4)

col1.metric(
    "Current Price",
    f"${current_price:.2f}",
    f"{percent:.2f}%"
)

col2.metric(
    "Open",
    f"${hist['Open'].iloc[-1]:.2f}"
)

col3.metric(
    "High",
    f"${hist['High'].max():.2f}"
)

col4.metric(
    "Low",
    f"${hist['Low'].min():.2f}"
)

# ---------------------- Company Info -----------------------

st.subheader("Company Information")

left,right = st.columns([1,2])

with left:

    if "logo_url" in info:
        st.image(info["logo_url"], width=120)

with right:

    st.write("###", info.get("longName","Unknown"))

    st.write(info.get("longBusinessSummary","No description available."))

# ---------------------- Line Chart -----------------------

st.subheader("Stock Price Chart")

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=hist.index,
        y=hist["Close"],
        mode="lines",
        line=dict(width=3),
        name="Close Price"
    )
)

fig.update_layout(
    template="plotly_dark",
    height=550,
    xaxis_title="Date",
    yaxis_title="Price",
    margin=dict(l=20,r=20,t=40,b=20)
)

st.plotly_chart(fig, use_container_width=True)

# ---------------------- Extra Details -----------------------

st.subheader("Market Statistics")

c1,c2,c3 = st.columns(3)

c1.info(f"Market Cap : {info.get('marketCap','N/A')}")
c2.info(f"PE Ratio : {info.get('trailingPE','N/A')}")
c3.info(f"Dividend Yield : {info.get('dividendYield','N/A')}")

# ---------------------- Suggestions -----------------------

st.subheader("⭐ Suggested Global Stocks")

suggestions = [
    ("AAPL","Apple"),
    ("MSFT","Microsoft"),
    ("NVDA","NVIDIA"),
    ("AMZN","Amazon"),
    ("GOOGL","Alphabet"),
    ("META","Meta"),
    ("TSLA","Tesla"),
    ("NFLX","Netflix"),
    ("RELIANCE.NS","Reliance"),
    ("TCS.NS","TCS"),
    ("INFY.NS","Infosys")
]

cols = st.columns(3)

for i,(sym,name) in enumerate(suggestions):
    cols[i%3].success(f"{name}\n\n{sym}")

st.markdown("---")
st.caption("Powered by Yahoo Finance • Streamlit • Plotly")
