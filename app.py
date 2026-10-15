
import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime

# =========================================================
# PAGE CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="MarketView | Stock Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================
# PROFESSIONAL UI DESIGN
# =========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

:root {
    --bg: #0b1020;
    --panel: #111a2d;
    --panel-light: #16223a;
    --border: rgba(148, 163, 184, 0.15);
    --text: #edf4ff;
    --muted: #8fa3bf;
    --cyan: #55e6d0;
    --blue: #6d9cff;
    --purple: #a78bfa;
    --green: #4ade80;
    --red: #fb7185;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background:
        radial-gradient(ellipse at 8% 0%, rgba(63, 115, 220, .14), transparent 35%),
        radial-gradient(ellipse at 92% 12%, rgba(126, 87, 194, .11), transparent 32%),
        linear-gradient(145deg, #0b1020 0%, #0c1425 55%, #0a1020 100%);
    color: var(--text);
}

[data-testid="stHeader"] {
    background: rgba(11, 16, 32, .7);
}

.main .block-container {
    max-width: 1500px;
    padding-top: 2.1rem;
    padding-bottom: 3rem;
}

h1, h2, h3 {
    font-family: 'Space Grotesk', sans-serif !important;
    color: var(--text) !important;
    letter-spacing: -0.7px;
}

p, label, .stMarkdown {
    color: var(--text);
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #101a2d 0%, #0c1425 100%);
    border-right: 1px solid var(--border);
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: var(--text) !important;
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    color: #b5c4da;
}

[data-testid="stMetric"] {
    background: linear-gradient(145deg, rgba(23, 36, 59, .97), rgba(15, 25, 43, .97));
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 18px 18px 15px;
    min-height: 125px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, .12);
    transition: transform .22s ease, border-color .22s ease,
                box-shadow .22s ease;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-5px);
    border-color: rgba(85, 230, 208, .5);
    box-shadow: 0 14px 30px rgba(0, 0, 0, .25),
                0 0 18px rgba(85, 230, 208, .06);
}

[data-testid="stMetricLabel"] {
    color: #9db0ca !important;
    font-size: .82rem !important;
    font-weight: 600 !important;
}

[data-testid="stMetricValue"] {
    color: #f3f7ff !important;
    font-family: 'Space Grotesk', sans-serif;
    font-size: clamp(1.25rem, 2vw, 1.9rem) !important;
    font-weight: 700 !important;
}

[data-testid="stMetricDelta"] {
    font-size: .82rem !important;
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    background: linear-gradient(145deg, rgba(19, 31, 52, .86), rgba(13, 23, 40, .86));
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 16px;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    border-bottom: 1px solid var(--border);
}

.stTabs [data-baseweb="tab"] {
    background: transparent;
    color: #9db0ca;
    border-radius: 9px 9px 0 0;
    padding: 10px 18px;
}

.stTabs [aria-selected="true"] {
    color: var(--cyan) !important;
    border-bottom-color: var(--cyan) !important;
}

.stButton button, .stDownloadButton button {
    background: linear-gradient(100deg, #42d9c5, #71a3ff);
    color: #081322;
    border: 0;
    border-radius: 10px;
    font-weight: 700;
    transition: transform .2s ease, filter .2s ease;
}

.stButton button:hover, .stDownloadButton button:hover {
    transform: translateY(-2px);
    filter: brightness(1.08);
    border: 0;
}

.stSelectbox > div > div,
.stTextInput > div > div,
.stNumberInput > div > div {
    background: #111c30;
    border-color: var(--border);
    border-radius: 10px;
}

hr {
    border-color: var(--border);
}

.hero {
    padding: 28px 30px 24px;
    margin-bottom: 25px;
    border-radius: 22px;
    border: 1px solid rgba(125, 163, 220, .2);
    background:
        radial-gradient(ellipse at 85% 0%, rgba(109, 156, 255, .16), transparent 38%),
        linear-gradient(120deg, rgba(20, 34, 57, .97), rgba(14, 24, 43, .97));
    box-shadow: 0 20px 50px rgba(0, 0, 0, .16);
    position: relative;
    overflow: hidden;
}

.hero-eyebrow {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 12px;
    color: #a9bdd7;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 2px;
    margin-bottom: 16px;
}

.live-badge {
    border: 1px solid rgba(74, 222, 128, .28);
    background: rgba(74, 222, 128, .09);
    color: #7cf2a3;
    padding: 5px 9px;
    border-radius: 20px;
    font-size: 10px;
    letter-spacing: 1px;
}

.hero-title {
    font-family: 'Space Grotesk', sans-serif;
    color: #f5f8ff;
    font-size: clamp(32px, 4vw, 54px);
    line-height: 1.1;
    font-weight: 700;
    letter-spacing: -2px;
    margin-bottom: 14px;
}

.hero-title .accent {
    background: linear-gradient(95deg, #55e6d0, #83b2ff 75%, #b49bff);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-title .period {
    -webkit-text-fill-color: #55e6d0;
}

.hero-description {
    color: #a7b8d0;
    font-size: 14px;
    line-height: 1.8;
    max-width: 680px;
    margin-bottom: 20px;
}

.hero-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 9px;
}

.hero-tags span {
    color: #bdcde2;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: .7px;
    padding: 8px 11px;
    border-radius: 8px;
    background: rgba(120, 155, 205, .08);
    border: 1px solid rgba(148, 163, 184, .13);
}

.section-heading {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 20px;
    font-weight: 700;
    color: #edf4ff;
    margin: 22px 0 5px;
}

.section-subtitle {
    font-size: 12px;
    color: #8fa3bf;
    margin-bottom: 18px;
}

.company-panel {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 15px;
    flex-wrap: wrap;
    padding: 20px 22px;
    margin: 8px 0 22px;
    border-radius: 16px;
    background: linear-gradient(110deg, rgba(26, 43, 69, .9), rgba(17, 29, 49, .92));
    border: 1px solid var(--border);
}

.company-name {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 23px;
    font-weight: 700;
    color: #f3f7ff;
}

.company-caption {
    color: #8fa3bf;
    font-size: 12px;
    margin-top: 4px;
}

.ticker-pill {
    background: rgba(85, 230, 208, .09);
    border: 1px solid rgba(85, 230, 208, .3);
    color: #72f0dd;
    border-radius: 10px;
    padding: 10px 16px;
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
    letter-spacing: 1px;
}

.small-note {
    color: #8195b2;
    font-size: 11px;
}

.footer {
    border-top: 1px solid var(--border);
    margin-top: 35px;
    padding-top: 18px;
    color: #7185a1;
    font-size: 11px;
}

.stAlert {
    border-radius: 12px;
}

@media (max-width: 700px) {
    .main .block-container {
        padding: 1rem 1rem 2rem;
    }
    .hero {
        padding: 22px 18px;
    }
    .hero-title {
        letter-spacing: -1px;
    }
    .company-name {
        font-size: 19px;
    }
}
</style>
""", unsafe_allow_html=True)


# =========================================================
# HELPER FUNCTIONS
# =========================================================
def safe_float(value):
    try:
        number = float(value)
        if pd.isna(number):
            return None
        return number
    except (TypeError, ValueError):
        return None


def format_price(value, currency="USD"):
    value = safe_float(value)
    if value is None:
        return "N/A"
    if currency == "INR":
        return f"₹{value:,.2f}"
    return f"${value:,.2f}"


def format_large_number(value, currency="USD"):
    value = safe_float(value)
    if value is None:
        return "N/A"

    prefix = "₹" if currency == "INR" else "$"

    if abs(value) >= 1_000_000_000_000:
        return f"{prefix}{value / 1_000_000_000_000:.2f}T"
    if abs(value) >= 1_000_000_000:
        return f"{prefix}{value / 1_000_000_000:.2f}B"
    if abs(value) >= 1_000_000:
        return f"{prefix}{value / 1_000_000:.2f}M"
    if abs(value) >= 1_000:
        return f"{prefix}{value / 1_000:.2f}K"
    return f"{prefix}{value:,.0f}"


def format_volume(value):
    value = safe_float(value)
    if value is None:
        return "N/A"
    if value >= 1_000_000_000:
        return f"{value / 1_000_000_000:.2f}B"
    if value >= 1_000_000:
        return f"{value / 1_000_000:.2f}M"
    if value >= 1_000:
        return f"{value / 1_000:.2f}K"
    return f"{value:,.0f}"


def calculate_rsi(series, period=14):
    delta = series.diff()
    gains = delta.clip(lower=0)
    losses = -delta.clip(upper=0)

    average_gain = gains.ewm(
        alpha=1 / period, min_periods=period, adjust=False
    ).mean()
    average_loss = losses.ewm(
        alpha=1 / period, min_periods=period, adjust=False
    ).mean()

    rs = average_gain / average_loss.replace(0, float("nan"))
    rsi = 100 - (100 / (1 + rs))
    rsi = rsi.where(average_loss != 0, 100)
    return rsi


@st.cache_data(ttl=300, show_spinner=False)
def load_history(symbol, period):
    ticker = yf.Ticker(symbol)
    history = ticker.history(
        period=period,
        interval="1d",
        auto_adjust=True
    )
    if history is None or history.empty:
        return pd.DataFrame()
    history = history.dropna(subset=["Close"])
    history.index = pd.to_datetime(history.index)
    return history


@st.cache_data(ttl=900, show_spinner=False)
def load_company_info(symbol):
    try:
        info = yf.Ticker(symbol).info
        return info if isinstance(info, dict) else {}
    except Exception:
        return {}


def chart_layout(fig, height=390, show_legend=True):
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            family="DM Sans, sans-serif",
            color="#a9bbd3",
            size=11
        ),
        margin=dict(l=12, r=12, t=25, b=12),
        hovermode="x unified",
        showlegend=show_legend,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=False,
            tickfont=dict(color="#8296b3"),
        ),
        yaxis=dict(
            gridcolor="rgba(148,163,184,.10)",
            zeroline=False,
            showline=False,
            tickfont=dict(color="#8296b3"),
        ),
    )
    return fig


# =========================================================
# SIDEBAR CONTROLS
# =========================================================
with st.sidebar:
    st.markdown(
        "<div style='font-family:Space Grotesk;font-size:23px;"
        "font-weight:700;color:#edf4ff;'>◈ MarketView</div>",
        unsafe_allow_html=True,
    )
    st.caption("STOCK ANALYTICS WORKSPACE")
    st.divider()

    st.markdown("### Market settings")

    ticker = st.text_input(
        "Stock ticker",
        value="AAPL",
        max_chars=15,
        help="Examples: AAPL, MSFT, NVDA, RELIANCE.NS, TCS.NS",
    ).strip().upper()

    period_labels = {
        "1 Month": "1mo",
        "3 Months": "3mo",
        "6 Months": "6mo",
        "1 Year": "1y",
        "2 Years": "2y",
        "5 Years": "5y",
    }

    selected_period = st.selectbox(
        "Historical period",
        options=list(period_labels.keys()),
        index=3,
    )
    period = period_labels[selected_period]

    chart_type = st.selectbox(
        "Price chart",
        ["Candlestick", "Line"],
        index=0,
    )

    st.divider()
    st.markdown("### Chart indicators")

    show_ma20 = st.checkbox("20-day moving average", value=True)
    show_ma50 = st.checkbox("50-day moving average", value=True)
    show_volume = st.checkbox("Volume bars", value=True)
    show_rsi = st.checkbox("RSI indicator", value=True)
    show_macd = st.checkbox("MACD indicator", value=True)

    st.divider()
    st.markdown("### Compare stocks")

    compare_symbol = st.text_input(
        "Comparison ticker",
        value="MSFT",
        max_chars=15,
        help="Used to compare percentage performance.",
    ).strip().upper()

    st.caption("Data source: Yahoo Finance")
    st.caption("Data may be delayed and is not investment advice.")


# =========================================================
# HERO
# =========================================================
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">
        MARKET INTELLIGENCE PLATFORM
        <span class="live-badge">● LIVE DATA ACCESS</span>
    </div>
    <div class="hero-title">
        Stock Market <span class="accent">Dashboard<span class="period">.</span></span>
    </div>
    <div class="hero-description">
        Explore price action, discover market trends, and analyze
        technical indicators through one unified workspace.
    </div>
    <div class="hero-tags">
        <span>↗ PRICE ACTION</span>
        <span>◈ TECHNICAL ANALYSIS</span>
        <span>⌁ MARKET DATA</span>
    </div>
</div>
""", unsafe_allow_html=True)


# =========================================================
# VALIDATION AND DATA LOADING
# =========================================================
if not ticker:
    st.warning("Enter a stock ticker in the sidebar to continue.")
    st.stop()

if any(char.isspace() for char in ticker):
    st.error("Please enter a valid ticker symbol without spaces.")
    st.stop()

try:
    with st.spinner(f"Loading market data for {ticker}..."):
        data = load_history(ticker, period)
        company_info = load_company_info(ticker)
except Exception as error:
    st.error("Unable to retrieve market data. Please try again.")
    st.caption(f"Technical details: {error}")
    st.stop()

if data.empty:
    st.error(
        f"No price history was returned for **{ticker}**. "
        "Check the symbol and try again."
    )
    st.info(
        "Examples: AAPL, MSFT, NVDA for US stocks; "
        "RELIANCE.NS or TCS.NS for Indian NSE listings."
    )
    st.stop()

# Prepare data
data = data.copy()
data["MA20"] = data["Close"].rolling(20).mean()
data["MA50"] = data["Close"].rolling(50).mean()
data["RSI"] = calculate_rsi(data["Close"])
data["EMA12"] = data["Close"].ewm(span=12, adjust=False).mean()
data["EMA26"] = data["Close"].ewm(span=26, adjust=False).mean()
data["MACD"] = data["EMA12"] - data["EMA26"]
data["MACD_Signal"] = data["MACD"].ewm(span=9, adjust=False).mean()
data["MACD_Hist"] = data["MACD"] - data["MACD_Signal"]

latest = data.iloc[-1]
previous = data.iloc[-2] if len(data) > 1 else latest

current_price = safe_float(latest["Close"])
previous_price = safe_float(previous["Close"])
daily_change = (
    current_price - previous_price
    if current_price is not None and previous_price is not None
    else None
)
daily_change_pct = (
    daily_change / previous_price * 100
    if daily_change is not None and previous_price
    else None
)

period_high = safe_float(data["High"].max())
period_low = safe_float(data["Low"].min())
average_volume = safe_float(data["Volume"].tail(20).mean())
latest_volume = safe_float(latest.get("Volume"))
currency = company_info.get("currency", "USD")
company_name = (
    company_info.get("longName")
    or company_info.get("shortName")
    or ticker
)
sector = company_info.get("sector", "Not available")
industry = company_info.get("industry", "Not available")
exchange = company_info.get("exchange", "Not available")


# =========================================================
# COMPANY OVERVIEW
# =========================================================
st.markdown('<div class="section-heading">Company overview</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-subtitle">A quick snapshot of your selected company</div>',
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <div class="company-panel">
        <div>
            <div class="company-name">{company_name}</div>
            <div class="company-caption">
                {sector} &nbsp;·&nbsp; {industry}
            </div>
        </div>
        <div class="ticker-pill">{ticker}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# MARKET METRICS
# =========================================================
st.markdown('<div class="section-heading">Market snapshot</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-subtitle">Key metrics for the selected historical period</div>',
    unsafe_allow_html=True,
)

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.metric(
        "Last closing price",
        format_price(current_price, currency),
        (
            f"{daily_change_pct:+.2f}%"
            if daily_change_pct is not None
            else None
        ),
    )

with m2:
    st.metric(
        "Period high",
        format_price(period_high, currency),
    )

with m3:
    st.metric(
        "Period low",
        format_price(period_low, currency),
    )

with m4:
    st.metric(
        "Latest volume",
        format_volume(latest_volume),
    )

m5, m6, m7, m8 = st.columns(4)

period_return = (
    (data["Close"].iloc[-1] / data["Close"].iloc[0] - 1) * 100
    if len(data) > 1 and data["Close"].iloc[0] != 0
    else None
)

with m5:
    st.metric(
        "Period return",
        f"{period_return:+.2f}%" if period_return is not None else "N/A",
    )

with m6:
    st.metric(
        "20-day average volume",
        format_volume(average_volume),
    )

with m7:
    current_rsi = safe_float(latest.get("RSI"))
    st.metric(
        "RSI (14)",
        f"{current_rsi:.1f}" if current_rsi is not None else "N/A",
    )

with m8:
    market_cap = company_info.get("marketCap")
    st.metric(
        "Market capitalization",
        format_large_number(market_cap, currency),
    )


# =========================================================
# PRICE CHART
# =========================================================
st.markdown('<div class="section-heading">Price performance</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-subtitle">Historical price movement and selected indicators</div>',
    unsafe_allow_html=True,
)

price_fig = make_subplots(
    rows=2 if show_volume else 1,
    cols=1,
    shared_xaxes=True,
    vertical_spacing=0.04,
    row_heights=[0.75, 0.25] if show_volume else [1],
)

if chart_type == "Candlestick":
    price_fig.add_trace(
        go.Candlestick(
            x=data.index,
            open=data["Open"],
            high=data["High"],
            low=data["Low"],
            close=data["Close"],
            name=ticker,
            increasing_line_color="#4ade80",
            decreasing_line_color="#fb7185",
            increasing_fillcolor="#4ade80",
            decreasing_fillcolor="#fb7185",
        ),
        row=1,
        col=1,
    )
else:
    price_fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data["Close"],
            name="Closing price",
            mode="lines",
            line=dict(color="#55e6d0", width=2.5),
            fill="tozeroy",
            fillcolor="rgba(85,230,208,0.06)",
        ),
        row=1,
        col=1,
    )

if show_ma20:
    price_fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data["MA20"],
            name="20-day MA",
            mode="lines",
            line=dict(color="#6d9cff", width=1.6),
        ),
        row=1,
        col=1,
    )

if show_ma50:
    price_fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data["MA50"],
            name="50-day MA",
            mode="lines",
            line=dict(color="#b49bff", width=1.6),
        ),
        row=1,
        col=1,
    )

if show_volume:
    volume_colors = [
        "#4ade80" if close >= open_ else "#fb7185"
        for close, open_ in zip(data["Close"], data["Open"])
    ]
    price_fig.add_trace(
        go.Bar(
            x=data.index,
            y=data["Volume"],
            name="Volume",
            marker_color=volume_colors,
            opacity=0.65,
        ),
        row=2,
        col=1,
    )
    price_fig.update_yaxes(title_text="Volume", row=2, col=1)

price_fig.update_yaxes(title_text=f"Price ({currency})", row=1, col=1)
price_fig.update_layout(
    xaxis_rangeslider_visible=False,
    bargap=0.15,
)
chart_layout(price_fig, height=500)
st.plotly_chart(price_fig, use_container_width=True, config={"displaylogo": False})


# =========================================================
# TECHNICAL ANALYSIS
# =========================================================
st.markdown('<div class="section-heading">Technical analysis</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-subtitle">Momentum and trend indicators calculated from historical prices</div>',
    unsafe_allow_html=True,
)

technical_tabs = st.tabs(["RSI", "MACD", "Daily returns"])

with technical_tabs[0]:
    if show_rsi:
        rsi_fig = go.Figure()
        rsi_fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data["RSI"],
                name="RSI",
                mode="lines",
                line=dict(color="#55e6d0", width=2),
                fill="tozeroy",
                fillcolor="rgba(85,230,208,0.05)",
            )
        )
        rsi_fig.add_hline(
            y=70,
            line_dash="dash",
            line_color="#fb7185",
            annotation_text="70",
        )
        rsi_fig.add_hline(
            y=30,
            line_dash="dash",
            line_color="#4ade80",
            annotation_text="30",
        )
        rsi_fig.update_yaxes(range=[0, 100], title_text="RSI")
        chart_layout(rsi_fig, height=300, show_legend=False)
        st.plotly_chart(rsi_fig, use_container_width=True, config={"displaylogo": False})

        if current_rsi is not None:
            if current_rsi >= 70:
                st.info("RSI is in the traditionally overbought zone (70 or above).")
            elif current_rsi <= 30:
                st.info("RSI is in the traditionally oversold zone (30 or below).")
            else:
                st.caption("RSI is between 30 and 70. These levels are reference signals, not predictions.")
    else:
        st.info("Enable RSI indicator in the sidebar to display this chart.")

with technical_tabs[1]:
    if show_macd:
        macd_fig = go.Figure()
        macd_fig.add_trace(
            go.Bar(
                x=data.index,
                y=data["MACD_Hist"],
                name="MACD histogram",
                marker_color=[
                    "#4ade80" if val >= 0 else "#fb7185"
                    for val in data["MACD_Hist"].fillna(0)
                ],
                opacity=0.7,
            )
        )
        macd_fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data["MACD"],
                name="MACD",
                line=dict(color="#6d9cff", width=2),
            )
        )
        macd_fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data["MACD_Signal"],
                name="Signal",
                line=dict(color="#b49bff", width=2),
            )
        )
        chart_layout(macd_fig, height=320)
        st.plotly_chart(macd_fig, use_container_width=True, config={"displaylogo": False})
        st.caption("MACD compares two exponential moving averages to illustrate trend momentum.")
    else:
        st.info("Enable MACD indicator in the sidebar to display this chart.")

with technical_tabs[2]:
    daily_returns = data["Close"].pct_change() * 100
    returns_fig = go.Figure()
    returns_fig.add_trace(
        go.Bar(
            x=data.index,
            y=daily_returns,
            name="Daily return",
            marker_color=[
                "#4ade80" if val >= 0 else "#fb7185"
                for val in daily_returns.fillna(0)
            ],
        )
    )
    returns_fig.add_hline(y=0, line_color="rgba(200,210,225,.4)")
    returns_fig.update_yaxes(title_text="Return (%)")
    chart_layout(returns_fig, height=300, show_legend=False)
    st.plotly_chart(returns_fig, use_container_width=True, config={"displaylogo": False})


# =========================================================
# STOCK COMPARISON
# =========================================================
st.markdown('<div class="section-heading">Stock comparison</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-subtitle">Compare indexed price performance over the same period</div>',
    unsafe_allow_html=True,
)

if compare_symbol and compare_symbol != ticker:
    try:
        with st.spinner(f"Loading comparison data for {compare_symbol}..."):
            compare_data = load_history(compare_symbol, period)

        if not compare_data.empty:
            comparison_fig = go.Figure()

            primary_indexed = data["Close"] / data["Close"].iloc[0] * 100
            comparison_fig.add_trace(
                go.Scatter(
                    x=data.index,
                    y=primary_indexed,
                    name=ticker,
                    mode="lines",
                    line=dict(color="#55e6d0", width=2.5),
                )
            )

            comparison_indexed = (
                compare_data["Close"] / compare_data["Close"].iloc[0] * 100
            )
            comparison_fig.add_trace(
                go.Scatter(
                    x=compare_data.index,
                    y=comparison_indexed,
                    name=compare_symbol,
                    mode="lines",
                    line=dict(color="#a78bfa", width=2.5),
                )
            )

            comparison_fig.add_hline(
                y=100,
                line_dash="dot",
                line_color="rgba(200,210,225,.35)",
            )
            comparison_fig.update_yaxes(title_text="Indexed value (start = 100)")
            chart_layout(comparison_fig, height=370)
            st.plotly_chart(
                comparison_fig,
                use_container_width=True,
                config={"displaylogo": False},
            )
            st.caption(
                "Both series start at 100 so relative percentage performance "
                "can be compared despite different share prices."
            )
        else:
            st.warning(f"No comparison data found for {compare_symbol}.")
    except Exception:
        st.warning("Could not load the comparison stock. Check the ticker and try again.")
elif compare_symbol == ticker:
    st.info("Enter a different comparison ticker in the sidebar.")
else:
    st.info("Add a comparison ticker in the sidebar to compare performance.")


# =========================================================
# COMPANY FUNDAMENTALS
# =========================================================
st.markdown('<div class="section-heading">Company fundamentals</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-subtitle">Company information supplied by Yahoo Finance, when available</div>',
    unsafe_allow_html=True,
)

f1, f2, f3, f4 = st.columns(4)

with f1:
    st.metric("Sector", sector if sector else "N/A")

with f2:
    st.metric("Exchange", exchange if exchange else "N/A")

with f3:
    pe_ratio = safe_float(company_info.get("trailingPE"))
    st.metric("Trailing P/E", f"{pe_ratio:.2f}" if pe_ratio is not None else "N/A")

with f4:
    dividend_yield = safe_float(company_info.get("dividendYield"))
    st.metric(
        "Dividend yield",
        f"{dividend_yield * 100:.2f}%"
        if dividend_yield is not None
        else "N/A",
    )

with st.expander("More company information"):
    info_left, info_right = st.columns(2)

    with info_left:
        st.write("**Company**", company_name)
        st.write("**Industry**", industry)
        st.write("**Country**", company_info.get("country", "N/A"))
        st.write("**Website**", company_info.get("website", "N/A"))

    with info_right:
        st.write("**Employees**", company_info.get("fullTimeEmployees", "N/A"))
        st.write(
            "**52-week high**",
            format_price(company_info.get("fiftyTwoWeekHigh"), currency),
        )
        st.write(
            "**52-week low**",
            format_price(company_info.get("fiftyTwoWeekLow"), currency),
        )
        st.write(
            "**Forward P/E**",
            (
                f"{safe_float(company_info.get('forwardPE')):.2f}"
                if safe_float(company_info.get("forwardPE")) is not None
                else "N/A"
            ),
        )

    business_summary = company_info.get("longBusinessSummary")
    if business_summary:
        st.markdown("**Business summary**")
        st.write(business_summary)


# =========================================================
# DATA TABLE AND DOWNLOAD
# =========================================================
st.markdown('<div class="section-heading">Historical data</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-subtitle">Review and export the underlying price history</div>',
    unsafe_allow_html=True,
)

with st.expander("View historical price table"):
    display_columns = [
        col for col in
        ["Open", "High", "Low", "Close", "Volume", "MA20", "MA50", "RSI"]
        if col in data.columns
    ]

    table = data[display_columns].sort_index(ascending=False).copy()
    table.index = table.index.strftime("%Y-%m-%d")
    st.dataframe(
        table,
        use_container_width=True,
        height=350,
    )

download_data = data.copy()
download_data.index.name = "Date"
csv_bytes = download_data.to_csv().encode("utf-8")

st.download_button(
    label="↓  Download historical data (CSV)",
    data=csv_bytes,
    file_name=f"{ticker}_{period}_historical_data.csv",
    mime="text/csv",
)

# =========================================================
# FOOTER
# =========================================================
st.markdown(
    f"""
    <div class="footer">
        <strong style="color:#a9bbd3;">MARKETVIEW</strong>
        &nbsp; · &nbsp; Stock Market Analytics Dashboard
        <span style="float:right;">
            {ticker} &nbsp; · &nbsp; Updated {datetime.now().strftime("%d %b %Y, %H:%M")}
        </span>
        <br><br>
        Market data is provided by Yahoo Finance and may be delayed, incomplete,
        or unavailable. This dashboard is an educational analytics project,
        not financial advice.
    </div>
    """,
    unsafe_allow_html=True,
)
