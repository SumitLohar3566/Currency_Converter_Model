import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="ForexPro | Currency Converter",
    page_icon="💱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -------------------- ENHANCED CSS STYLING --------------------
st.markdown("""
<style>
    /* Base Styles - Improved Readability */
    .stApp {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }

    /* Better text contrast */
    h1, h2, h3, h4, h5, h6 {
        color: #1e293b !important;
        font-weight: 600 !important;
        letter-spacing: -0.025em !important;
    }

    p, span, div {
        color: #475569 !important;
    }

    /* Main Container */
    .main-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 20px;
    }

    /* Header - Enhanced */
    .app-header {
        text-align: center;
        padding: 40px 0;
        margin-bottom: 40px;
        background: white;
        border-radius: 20px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    }

    .app-title {
        font-size: 3.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 12px;
        line-height: 1.2;
    }

    .app-subtitle {
        font-size: 1.3rem;
        color: #64748b !important;
        margin-bottom: 25px;
        font-weight: 400;
        opacity: 0.9;
    }

    /* Cards - Better Contrast */
    .converter-card {
        background: white;
        border-radius: 18px;
        padding: 35px;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.08);
        margin-bottom: 35px;
        border: 1px solid #f1f5f9;
    }

    .section-card {
        background: white;
        border-radius: 16px;
        padding: 25px;
        margin: 20px 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
        border: 1px solid #f1f5f9;
    }

    /* Input Fields - Clearer */
    .stNumberInput > div > div > input,
    .stSelectbox > div > div,
    .stMultiSelect > div > div {
        border: 2px solid #e2e8f0 !important;
        border-radius: 12px !important;
        padding: 14px 18px !important;
        font-size: 16px !important;
        transition: all 0.3s !important;
        background: white !important;
        color: #1e293b !important;
    }

    .stNumberInput > div > div > input::placeholder,
    .stSelectbox > div > div::placeholder {
        color: #94a3b8 !important;
    }

    .stNumberInput > div > div > input:focus,
    .stSelectbox > div > div:focus-within,
    .stMultiSelect > div > div:focus-within {
        border-color: #4f46e5 !important;
        box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1) !important;
    }

    /* Labels */
    .stNumberInput label,
    .stSelectbox label,
    .stMultiSelect label {
        font-weight: 600 !important;
        color: #334155 !important;
        font-size: 1rem !important;
        margin-bottom: 8px !important;
    }

    /* Buttons - Clearer */
    .stButton > button {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 16px 32px !important;
        font-weight: 600 !important;
        font-size: 17px !important;
        transition: all 0.3s !important;
        width: 100%;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 12px 30px rgba(79, 70, 229, 0.25) !important;
    }

    .secondary-button {
        background: #f8fafc !important;
        color: #475569 !important;
        border: 2px solid #e2e8f0 !important;
    }

    /* Currency Cards - Better Readability */
    .currency-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border-radius: 14px;
        padding: 22px;
        margin: 12px 0;
        border: 1px solid #e2e8f0;
        transition: all 0.3s;
    }

    .currency-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
        border-color: #c7d2fe;
    }

    .currency-flag {
        font-size: 2.2rem;
        margin-bottom: 12px;
    }

    .currency-code {
        font-size: 1.4rem;
        font-weight: 700;
        color: #1e293b;
        margin: 8px 0;
    }

    .currency-name {
        font-size: 0.95rem;
        color: #64748b;
        margin-bottom: 12px;
    }

    .currency-rate {
        font-size: 1.6rem;
        font-weight: 800;
        color: #4f46e5;
        margin: 10px 0;
    }

    /* Stats Cards - Clearer */
    .stats-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border-radius: 16px;
        padding: 22px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
        border: 1px solid #f1f5f9;
    }

    .stats-flag {
        font-size: 1.8rem;
        margin-bottom: 12px;
    }

    .stats-rate {
        font-size: 1.9rem;
        font-weight: 800;
        color: #1e293b;
        margin: 12px 0;
    }

    .stats-label {
        color: #64748b;
        font-size: 0.95rem;
        font-weight: 500;
    }

    /* Custom Badge */
    .custom-badge {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
        color: white;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
    }

    /* Loading Animation */
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.6; }
        100% { opacity: 1; }
    }

    .loading {
        animation: pulse 1.5s infinite;
    }

    /* Section Headers */
    .section-header {
        display: flex;
        align-items: center;
        margin: 25px 0 15px 0;
        padding-bottom: 12px;
        border-bottom: 2px solid #f1f5f9;
    }

    .section-icon {
        font-size: 1.8rem;
        margin-right: 12px;
    }

    .section-title {
        font-size: 1.8rem;
        color: #1e293b;
        font-weight: 700;
        margin: 0;
    }

    /* Quick Select Buttons */
    .quick-select-btn {
        background: #f8fafc !important;
        color: #475569 !important;
        border: 2px solid #e2e8f0 !important;
        font-size: 0.9rem !important;
        padding: 10px 15px !important;
    }

    .quick-select-btn:hover {
        background: #f1f5f9 !important;
        border-color: #cbd5e1 !important;
    }

    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Data Table Styling */
    .dataframe {
        font-size: 0.95rem !important;
    }

    .dataframe th {
        background-color: #f8fafc !important;
        color: #334155 !important;
        font-weight: 600 !important;
    }

    /* Expandable Sections */
    .streamlit-expanderHeader {
        background: white !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        color: #1e293b !important;
    }

    /* Status Indicators */
    .status-indicator {
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        margin-right: 8px;
        background: #10b981;
    }

    /* Tooltip-like hover info */
    .info-tooltip {
        background: #f1f5f9;
        border-radius: 8px;
        padding: 8px 12px;
        font-size: 0.85rem;
        color: #64748b;
        margin-top: 5px;
        border-left: 3px solid #c7d2fe;
    }
</style>
""", unsafe_allow_html=True)


# -------------------- API FUNCTIONS (UNCHANGED) --------------------
@st.cache_data(ttl=300, show_spinner=False)
def get_exchange_rates(base_currency="USD"):
    """Get real-time exchange rates"""
    try:
        url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        return {
            "rates": data.get("rates", {}),
            "timestamp": datetime.now(),
            "base": base_currency
        }
    except requests.exceptions.RequestException:
        # Fallback to exchangerate.host API
        try:
            url = f"https://api.exchangerate.host/latest?base={base_currency}"
            response = requests.get(url, timeout=10)
            data = response.json()

            if data.get("success"):
                return {
                    "rates": data.get("rates", {}),
                    "timestamp": datetime.fromtimestamp(data.get("timestamp", time.time())),
                    "base": base_currency
                }
        except:
            pass

        # Return empty data with current timestamp
        return {
            "rates": {},
            "timestamp": datetime.now(),
            "base": base_currency
        }


@st.cache_data(ttl=3600, show_spinner=False)
def get_historical_data(base_currency, target_currency, days=30):
    """Get historical data for chart"""
    try:
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

        url = f"https://api.exchangerate.host/timeseries"
        params = {
            "start_date": start_date,
            "end_date": end_date,
            "base": base_currency,
            "symbols": target_currency
        }

        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        if data.get("success") and data.get("rates"):
            dates = []
            rates = []
            for date, rate_data in sorted(data["rates"].items()):
                dates.append(date)
                rate_value = list(rate_data.values())[0]
                rates.append(rate_value)
            return dates, rates
    except:
        pass

    return [], []


# -------------------- CONVERSION FUNCTION (UNCHANGED) --------------------
def convert_currency(amount, from_currency, to_currencies):
    """Convert currency with proper formatting"""
    try:
        if amount <= 0:
            return [], None

        data = get_exchange_rates(from_currency)
        rates = data.get("rates", {})
        results = []

        base_rate = rates.get(from_currency, 1.0)

        for curr in to_currencies:
            if curr == from_currency:
                results.append({
                    "currency": curr,
                    "rate": 1.0,
                    "amount": amount,
                    "formatted": f"{amount:,.2f}"
                })
            else:
                rate = rates.get(curr)
                if rate:
                    # Adjust rate based on base currency
                    adjusted_rate = rate / base_rate if base_rate != 0 else rate
                    converted = amount * adjusted_rate
                    results.append({
                        "currency": curr,
                        "rate": adjusted_rate,
                        "amount": converted,
                        "formatted": f"{converted:,.2f}"
                    })
                else:
                    results.append({
                        "currency": curr,
                        "rate": None,
                        "amount": None,
                        "formatted": "N/A"
                    })

        return results, data.get("timestamp")
    except Exception as e:
        st.error(f"Error during conversion: {str(e)}")
        return [], None


# -------------------- SESSION STATE (UNCHANGED) --------------------
if 'conversion_history' not in st.session_state:
    st.session_state.conversion_history = []
if 'favorites' not in st.session_state:
    st.session_state.favorites = ["EUR", "GBP", "JPY"]
if 'last_update' not in st.session_state:
    st.session_state.last_update = datetime.now()

# -------------------- CURRENCY DATA (UNCHANGED) --------------------
CURRENCY_DATA = {
    "USD": {"flag": "🇺🇸", "name": "US Dollar", "symbol": "$"},
    "EUR": {"flag": "🇪🇺", "name": "Euro", "symbol": "€"},
    "GBP": {"flag": "🇬🇧", "name": "British Pound", "symbol": "£"},
    "JPY": {"flag": "🇯🇵", "name": "Japanese Yen", "symbol": "¥"},
    "CAD": {"flag": "🇨🇦", "name": "Canadian Dollar", "symbol": "C$"},
    "AUD": {"flag": "🇦🇺", "name": "Australian Dollar", "symbol": "A$"},
    "CHF": {"flag": "🇨🇭", "name": "Swiss Franc", "symbol": "Fr"},
    "CNY": {"flag": "🇨🇳", "name": "Chinese Yuan", "symbol": "¥"},
    "INR": {"flag": "🇮🇳", "name": "Indian Rupee", "symbol": "₹"},
    "SGD": {"flag": "🇸🇬", "name": "Singapore Dollar", "symbol": "S$"},
    "AED": {"flag": "🇦🇪", "name": "UAE Dirham", "symbol": "د.إ"},
    "KRW": {"flag": "🇰🇷", "name": "South Korean Won", "symbol": "₩"},
    "BRL": {"flag": "🇧🇷", "name": "Brazilian Real", "symbol": "R$"},
    "MXN": {"flag": "🇲🇽", "name": "Mexican Peso", "symbol": "$"},
    "RUB": {"flag": "🇷🇺", "name": "Russian Ruble", "symbol": "₽"},
    "ZAR": {"flag": "🇿🇦", "name": "South African Rand", "symbol": "R"},
    "TRY": {"flag": "🇹🇷", "name": "Turkish Lira", "symbol": "₺"},
    "NZD": {"flag": "🇳🇿", "name": "New Zealand Dollar", "symbol": "NZ$"},
    "SEK": {"flag": "🇸🇪", "name": "Swedish Krona", "symbol": "kr"},
    "NOK": {"flag": "🇳🇴", "name": "Norwegian Krone", "symbol": "kr"},
}

# -------------------- MAIN LAYOUT WITH ENHANCED UI --------------------
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Header with better visibility
st.markdown("""
<div class="app-header">
    <h1 class="app-title">💱 ForexPro Currency Converter</h1>
    <p class="app-subtitle">Convert currencies in real-time with accurate exchange rates</p>
    <div style="display: inline-block; background: linear-gradient(135deg, rgba(79, 70, 229, 0.1) 0%, rgba(124, 58, 237, 0.1) 100%); padding: 8px 20px; border-radius: 20px; margin-top: 10px;">
        <span class="status-indicator"></span>
        <span style="color: #4f46e5; font-weight: 500;">Live Rates • 160+ Currencies • Updated Every 5 Minutes</span>
    </div>
</div>
""", unsafe_allow_html=True)

# -------------------- TOP STATS WITH BETTER VISIBILITY --------------------
st.markdown(
    '<div class="section-header"><span class="section-icon">📊</span><h2 class="section-title">Live Market Rates</h2></div>',
    unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

try:
    usd_rates = get_exchange_rates("USD")
    rates = usd_rates.get("rates", {})

    with col1:
        eur_rate = rates.get("EUR", 0)
        st.markdown(f"""
        <div class="stats-card">
            <div class="stats-flag">🇺🇸/🇪🇺</div>
            <div class="stats-rate">{eur_rate:.4f}</div>
            <div class="stats-label">USD to EUR</div>
            <div style="font-size: 0.8rem; color: #94a3b8; margin-top: 8px;">Major Currency Pair</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        gbp_rate = rates.get("GBP", 0)
        st.markdown(f"""
        <div class="stats-card">
            <div class="stats-flag">🇺🇸/🇬🇧</div>
            <div class="stats-rate">{gbp_rate:.4f}</div>
            <div class="stats-label">USD to GBP</div>
            <div style="font-size: 0.8rem; color: #94a3b8; margin-top: 8px;">Cable</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        jpy_rate = rates.get("JPY", 0)
        st.markdown(f"""
        <div class="stats-card">
            <div class="stats-flag">🇺🇸/🇯🇵</div>
            <div class="stats-rate">{jpy_rate:.2f}</div>
            <div class="stats-label">USD to JPY</div>
            <div style="font-size: 0.8rem; color: #94a3b8; margin-top: 8px;">Asian Session</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        cad_rate = rates.get("CAD", 0)
        st.markdown(f"""
        <div class="stats-card">
            <div class="stats-flag">🇺🇸/🇨🇦</div>
            <div class="stats-rate">{cad_rate:.4f}</div>
            <div class="stats-label">USD to CAD</div>
            <div style="font-size: 0.8rem; color: #94a3b8; margin-top: 8px;">North American</div>
        </div>
        """, unsafe_allow_html=True)
except:
    st.markdown('<div class="info-tooltip">⚠️ Unable to fetch live rates. Using cached data.</div>',
                unsafe_allow_html=True)

# -------------------- MAIN CONVERTER WITH BETTER VISIBILITY --------------------
st.markdown(
    '<div class="section-header"><span class="section-icon">💰</span><h2 class="section-title">Currency Converter</h2></div>',
    unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="converter-card">', unsafe_allow_html=True)

    st.markdown(
        '<div style="margin-bottom: 25px;"><span class="custom-badge">Enter Amount & Select Currencies</span></div>',
        unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 💵 Amount to Convert")
        amount = st.number_input(
            "Enter amount",
            min_value=0.01,
            value=100.0,
            step=10.0,
            label_visibility="collapsed",
            help="Enter the amount you want to convert"
        )

        st.markdown("#### 📤 From Currency")
        available_currencies = list(CURRENCY_DATA.keys())
        from_currency = st.selectbox(
            "Select source currency",
            available_currencies,
            index=available_currencies.index("USD"),
            label_visibility="collapsed",
            format_func=lambda x: f"{CURRENCY_DATA[x]['flag']} {x} - {CURRENCY_DATA[x]['name']}",
            help="Choose the currency you want to convert from"
        )

    with col2:
        st.markdown("#### 📥 To Currencies")
        to_currencies = st.multiselect(
            "Select target currencies",
            available_currencies,
            default=st.session_state.favorites,
            label_visibility="collapsed",
            format_func=lambda x: f"{CURRENCY_DATA[x]['flag']} {x} - {CURRENCY_DATA[x]['name']}",
            help="Select one or more currencies to convert to"
        )

        # Update favorites
        st.session_state.favorites = to_currencies

        # Quick select buttons with better visibility
        st.markdown("##### 🚀 Quick Selection")
        col_btns = st.columns(5)
        button_styles = {
            "💎 Major": ["EUR", "GBP", "JPY", "CAD", "AUD"],
            "🌏 Asian": ["JPY", "CNY", "INR", "SGD", "KRW"],
            "🇪🇺 EU": ["EUR", "GBP", "CHF", "SEK", "NOK"],
            "🌐 All": available_currencies[:8],
            "❌ Clear": []
        }

        for idx, (label, currencies) in enumerate(button_styles.items()):
            with col_btns[idx]:
                if st.button(label, use_container_width=True, key=f"btn_{label}"):
                    st.session_state.favorites = currencies
                    st.rerun()

    # Convert Button with better visibility
    st.markdown('<div style="margin-top: 30px;">', unsafe_allow_html=True)
    convert_button = st.button(
        "🚀 CONVERT NOW",
        type="primary",
        use_container_width=True,
        disabled=not to_currencies or amount <= 0,
        help="Click to convert with real-time exchange rates"
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# -------------------- CONVERSION RESULTS WITH BETTER VISIBILITY --------------------
if convert_button and to_currencies:
    with st.spinner("🔄 Fetching latest exchange rates..."):
        results, timestamp = convert_currency(amount, from_currency, to_currencies)

        if results:
            # Store in history
            st.session_state.conversion_history.insert(0, {
                "timestamp": datetime.now(),
                "from_currency": from_currency,
                "amount": amount,
                "results": results
            })
            st.session_state.last_update = datetime.now()

            # Display results section
            st.markdown(
                '<div class="section-header"><span class="section-icon">📈</span><h2 class="section-title">Conversion Results</h2></div>',
                unsafe_allow_html=True)
            st.markdown(
                f'<div class="info-tooltip">Converted {amount:,.2f} {from_currency} to {len(results)} currencies</div>',
                unsafe_allow_html=True)

            # Results in a grid
            cols = st.columns(2)
            for idx, result in enumerate(results):
                with cols[idx % 2]:
                    if result["rate"] is not None:
                        currency_info = CURRENCY_DATA.get(result["currency"], {})
                        st.markdown(f"""
                        <div class="currency-card">
                            <div class="currency-flag">{currency_info.get('flag', '🌐')}</div>
                            <div class="currency-code">{result['currency']}</div>
                            <div class="currency-name">{currency_info.get('name', '')}</div>
                            <div style="margin: 15px 0;">
                                <div style="font-size: 1.1rem; color: #64748b; margin-bottom: 5px;">Exchange Rate:</div>
                                <div style="font-size: 1.4rem; font-weight: 700; color: #4f46e5;">
                                    1 {from_currency} = {result['rate']:.6f} {result['currency']}
                                </div>
                            </div>
                            <div style="background: #f8fafc; padding: 15px; border-radius: 10px; margin-top: 15px;">
                                <div style="font-size: 1.1rem; color: #64748b; margin-bottom: 5px;">Converted Amount:</div>
                                <div style="font-size: 2rem; font-weight: 800; color: #1e293b;">
                                    {currency_info.get('symbol', '')}{result['formatted']}
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

            # Show chart for first currency if available
            if results and results[0]["rate"] is not None:
                st.markdown(
                    '<div class="section-header"><span class="section-icon">📊</span><h2 class="section-title">Exchange Rate Trend (30 Days)</h2></div>',
                    unsafe_allow_html=True)
                target_currency = results[0]['currency']
                dates, rates = get_historical_data(from_currency, target_currency, 30)

                if dates and rates:
                    fig = go.Figure()

                    fig.add_trace(go.Scatter(
                        x=dates,
                        y=rates,
                        mode='lines',
                        name=f'{from_currency}/{target_currency}',
                        line=dict(color='#4f46e5', width=3),
                        fill='tozeroy',
                        fillcolor='rgba(79, 70, 229, 0.1)'
                    ))

                    fig.update_layout(
                        plot_bgcolor='white',
                        paper_bgcolor='white',
                        xaxis=dict(
                            showgrid=True,
                            gridcolor='#f1f5f9',
                            title="Date",
                            title_font=dict(size=14, color="#475569")
                        ),
                        yaxis=dict(
                            showgrid=True,
                            gridcolor='#f1f5f9',
                            title=f"Exchange Rate ({target_currency})",
                            title_font=dict(size=14, color="#475569")
                        ),
                        height=450,
                        hovermode='x unified',
                        font=dict(family="Inter", color="#475569")
                    )

                    st.plotly_chart(fig, use_container_width=True)

# -------------------- POPULAR CURRENCIES WITH BETTER VISIBILITY --------------------
st.markdown(
    '<div class="section-header"><span class="section-icon">🌍</span><h2 class="section-title">Popular Currency Pairs</h2></div>',
    unsafe_allow_html=True)

popular_pairs = [
    ("USD", "EUR", "🇺🇸/🇪🇺", "USD/EUR", "Major Pair"),
    ("USD", "GBP", "🇺🇸/🇬🇧", "USD/GBP", "Cable"),
    ("USD", "JPY", "🇺🇸/🇯🇵", "USD/JPY", "Asian"),
    ("EUR", "GBP", "🇪🇺/🇬🇧", "EUR/GBP", "Euro Cable"),
    ("USD", "CAD", "🇺🇸/🇨🇦", "USD/CAD", "North America"),
    ("USD", "AUD", "🇺🇸/🇦🇺", "USD/AUD", "Commodity"),
]

cols = st.columns(3)
for idx, (from_curr, to_curr, flag, pair_name, pair_desc) in enumerate(popular_pairs):
    with cols[idx % 3]:
        try:
            rates = get_exchange_rates(from_curr)["rates"]
            rate = rates.get(to_curr, 0)
            st.markdown(f"""
            <div class="currency-card" style="text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 15px;">{flag}</div>
                <div style="font-size: 1.2rem; font-weight: 700; color: #1e293b; margin-bottom: 5px;">{pair_name}</div>
                <div style="font-size: 0.9rem; color: #64748b; margin-bottom: 15px;">{pair_desc}</div>
                <div style="font-size: 1.8rem; font-weight: 800; color: #4f46e5; margin: 15px 0;">{rate:.4f}</div>
                <div style="font-size: 0.85rem; color: #94a3b8; background: #f8fafc; padding: 8px; border-radius: 8px;">
                    1 {from_curr} = {rate:.4f} {to_curr}
                </div>
            </div>
            """, unsafe_allow_html=True)
        except:
            st.markdown(f"""
            <div class="currency-card" style="text-align: center; opacity: 0.7;">
                <div style="font-size: 2rem; margin-bottom: 15px;">{flag}</div>
                <div style="font-size: 1.2rem; font-weight: 700; color: #1e293b; margin-bottom: 5px;">{pair_name}</div>
                <div style="font-size: 0.9rem; color: #64748b; margin-bottom: 15px;">{pair_desc}</div>
                <div style="font-size: 1.8rem; font-weight: 800; color: #94a3b8; margin: 15px 0;">--.--</div>
                <div style="font-size: 0.85rem; color: #94a3b8;">Data unavailable</div>
            </div>
            """, unsafe_allow_html=True)

# -------------------- CONVERSION HISTORY WITH BETTER VISIBILITY --------------------
if st.session_state.conversion_history:
    st.markdown(
        '<div class="section-header"><span class="section-icon">📝</span><h2 class="section-title">Recent Conversions</h2></div>',
        unsafe_allow_html=True)

    with st.expander("View Conversion History", expanded=False):
        for idx, record in enumerate(st.session_state.conversion_history[:5]):
            bg_color = "#f8fafc" if idx % 2 == 0 else "#ffffff"
            st.markdown(f"""
            <div style="background: {bg_color}; padding: 20px; border-radius: 12px; margin-bottom: 12px; border-left: 4px solid #4f46e5;">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                    <div style="flex: 1;">
                        <div style="display: flex; align-items: center; margin-bottom: 10px;">
                            <div style="font-size: 1.5rem; margin-right: 12px;">💱</div>
                            <div>
                                <div style="font-size: 1.3rem; font-weight: 700; color: #1e293b;">
                                    {record['amount']:,.2f} {record['from_currency']}
                                </div>
                                <div style="font-size: 0.85rem; color: #64748b; margin-top: 4px;">
                                    {record['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}
                                </div>
                            </div>
                        </div>
                    </div>
                    <div style="flex: 1; text-align: right;">
                        <div style="font-size: 1.1rem; color: #475569; margin-bottom: 8px;">
                            Converted to:
                        </div>
                        <div style="font-size: 1rem; color: #4f46e5; font-weight: 600;">
                            {', '.join([f"{r['formatted']} {r['currency']}" for r in record['results'][:2]])}
                            {f" (+{len(record['results']) - 2} more)" if len(record['results']) > 2 else ''}
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        col1, col2 = st.columns([3, 1])
        with col2:
            if st.button("🗑️ Clear All History", use_container_width=True, type="secondary"):
                st.session_state.conversion_history = []
                st.rerun()

# -------------------- ALL CURRENCIES TABLE WITH BETTER VISIBILITY --------------------
st.markdown(
    '<div class="section-header"><span class="section-icon">📋</span><h2 class="section-title">Available Currencies</h2></div>',
    unsafe_allow_html=True)

with st.expander("Browse All Currencies", expanded=False):
    try:
        usd_rates = get_exchange_rates("USD")
        rates = usd_rates.get("rates", {})

        currencies_list = []
        for code, rate in rates.items():
            if code in CURRENCY_DATA:
                currencies_list.append({
                    "Flag": CURRENCY_DATA[code]["flag"],
                    "Code": code,
                    "Currency": CURRENCY_DATA[code]["name"],
                    "Rate (vs USD)": f"{rate:.4f}",
                    "Symbol": CURRENCY_DATA[code]["symbol"]
                })

        if currencies_list:
            df = pd.DataFrame(currencies_list)
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Flag": st.column_config.TextColumn("Flag", width="small"),
                    "Code": st.column_config.TextColumn("Code", width="small"),
                    "Currency": st.column_config.TextColumn("Currency", width="medium"),
                    "Rate (vs USD)": st.column_config.NumberColumn("Rate vs USD", width="small", format="%.4f"),
                    "Symbol": st.column_config.TextColumn("Symbol", width="small")
                }
            )
    except:
        st.markdown('<div class="info-tooltip">Unable to load complete currency list. Please try again later.</div>',
                    unsafe_allow_html=True)

# -------------------- SIMPLE FOOTER WITHOUT ERRORS --------------------
st.markdown("""
<div style="text-align: center; padding: 30px 0; color: #64748b; font-size: 0.9rem; margin-top: 50px;">
    <div style="margin-bottom: 10px;">
        <strong style="color: #4f46e5;">💱 ForexPro Currency Converter</strong> • Real-time Exchange Rates
    </div>
    <div style="margin-bottom: 15px;">
        Last updated: """ + st.session_state.last_update.strftime('%Y-%m-%d %H:%M:%S') + """ • Powered by ExchangeRate-API
    </div>
    <div style="font-size: 0.8rem; color: #94a3b8;">
        Exchange rates are for informational purposes only. Actual rates may vary.
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # Close main container
