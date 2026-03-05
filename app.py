import streamlit as st
import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns

# ─── Page Config ───────────────────────────────────────────────
st.set_page_config(
    page_title="ChurnLens | E-Commerce Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── Custom CSS ────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');

/* ── Animated Icons Keyframes ── */
@keyframes pulse-ring {
    0% { transform: scale(0.95); opacity: 1; }
    50% { transform: scale(1.08); opacity: 0.7; }
    100% { transform: scale(0.95); opacity: 1; }
}
@keyframes spin-slow {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}
@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-4px); }
}
@keyframes blink-dot {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.2; }
}
@keyframes warn-shake {
    0%, 100% { transform: translateX(0); }
    20% { transform: translateX(-3px) rotate(-5deg); }
    40% { transform: translateX(3px) rotate(5deg); }
    60% { transform: translateX(-2px) rotate(-3deg); }
    80% { transform: translateX(2px) rotate(3deg); }
}
@keyframes tick-pop {
    0% { transform: scale(0.5); opacity: 0; }
    60% { transform: scale(1.2); opacity: 1; }
    100% { transform: scale(1); opacity: 1; }
}
@keyframes orbit {
    from { transform: rotate(0deg) translateX(6px) rotate(0deg); }
    to   { transform: rotate(360deg) translateX(6px) rotate(-360deg); }
}
@keyframes dash {
    to { stroke-dashoffset: 0; }
}
@keyframes glow-pulse {
    0%, 100% { filter: drop-shadow(0 0 2px #63b3ed); }
    50% { filter: drop-shadow(0 0 8px #63b3ed); }
}
@keyframes bounce-in {
    0% { transform: scale(0); opacity: 0; }
    60% { transform: scale(1.15); opacity: 1; }
    100% { transform: scale(1); }
}
@keyframes spin-gear {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}
@keyframes wave {
    0%, 100% { transform: rotate(0deg); }
    25% { transform: rotate(20deg); }
    75% { transform: rotate(-10deg); }
}
@keyframes radar-ping {
    0% { transform: scale(1); opacity: 0.8; }
    100% { transform: scale(2.2); opacity: 0; }
}

/* Animated icon base styles */
.anim-icon { display: inline-flex; align-items: center; justify-content: center; vertical-align: middle; }
.anim-float { animation: float 2.5s ease-in-out infinite; }
.anim-pulse { animation: pulse-ring 2s ease-in-out infinite; }
.anim-spin { animation: spin-slow 4s linear infinite; }
.anim-shake { animation: warn-shake 1.2s ease-in-out infinite; }
.anim-tick { animation: tick-pop 0.5s cubic-bezier(0.175,0.885,0.32,1.275) forwards; }
.anim-glow { animation: glow-pulse 2s ease-in-out infinite; }
.anim-bounce { animation: bounce-in 0.6s cubic-bezier(0.175,0.885,0.32,1.275) forwards; }
.anim-gear { animation: spin-gear 3s linear infinite; }
.anim-wave { animation: wave 1.5s ease-in-out infinite; }

/* ── Global Reset ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #080c14 !important;
    color: #e8eaf0 !important;
    font-family: 'DM Mono', monospace !important;
}

[data-testid="stAppViewContainer"] {
    background: radial-gradient(ellipse at 20% 0%, #0d1f3c 0%, #080c14 50%),
                radial-gradient(ellipse at 80% 100%, #0a1628 0%, transparent 60%) !important;
}

/* Hide streamlit default elements */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stSidebar"] { display: none; }
.block-container { padding: 2rem 3rem !important; max-width: 1400px !important; }

/* ── Hero Header ── */
.hero {
    position: relative;
    padding: 3rem 0 2rem 0;
    margin-bottom: 2rem;
    border-bottom: 1px solid rgba(99, 179, 237, 0.15);
}
.hero-tag {
    display: inline-block;
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.2em;
    color: #63b3ed;
    background: rgba(99, 179, 237, 0.08);
    border: 1px solid rgba(99, 179, 237, 0.2);
    padding: 0.3rem 0.8rem;
    border-radius: 2px;
    margin-bottom: 1rem;
    text-transform: uppercase;
}
.hero-title {
    font-family: 'Syne', sans-serif !important;
    font-size: 3.2rem !important;
    font-weight: 800 !important;
    line-height: 1.1 !important;
    color: #ffffff !important;
    letter-spacing: -0.02em !important;
    margin-bottom: 0.5rem !important;
}
.hero-title span { color: #63b3ed; }
.hero-subtitle {
    font-family: 'DM Mono', monospace;
    font-size: 0.85rem;
    color: #6b7a99;
    letter-spacing: 0.05em;
}
.hero-stats {
    display: flex;
    gap: 2rem;
    margin-top: 1.5rem;
}
.hero-stat {
    display: flex;
    flex-direction: column;
}
.hero-stat-val {
    font-family: 'Syne', sans-serif;
    font-size: 1.4rem;
    font-weight: 700;
    color: #63b3ed;
}
.hero-stat-label {
    font-size: 0.65rem;
    color: #4a5568;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}

/* ── Tabs ── */
[data-testid="stTabs"] [role="tablist"] {
    background: rgba(255,255,255,0.02) !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    border-radius: 4px !important;
    padding: 4px !important;
    gap: 4px !important;
}
[data-testid="stTabs"] [role="tab"] {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    color: #4a5568 !important;
    border-radius: 2px !important;
    padding: 0.5rem 1.2rem !important;
    border: none !important;
    transition: all 0.2s !important;
}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    background: rgba(99, 179, 237, 0.12) !important;
    color: #63b3ed !important;
    border: 1px solid rgba(99, 179, 237, 0.25) !important;
}

/* ── Section Headers ── */
.section-header {
    font-family: 'Syne', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: #ffffff;
    letter-spacing: -0.01em;
    margin-bottom: 1.5rem;
    padding-bottom: 0.75rem;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.section-header::before {
    content: '';
    display: inline-block;
    width: 3px;
    height: 16px;
    background: #63b3ed;
    border-radius: 2px;
}

/* ── Input Cards ── */
.input-card {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 6px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    transition: border-color 0.2s;
}
.input-card:hover { border-color: rgba(99, 179, 237, 0.2); }
.input-card-title {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    font-weight: 500;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #63b3ed;
    margin-bottom: 1rem;
    opacity: 0.8;
}

/* ── Inputs styling ── */
[data-testid="stNumberInput"] input,
[data-testid="stSelectbox"] select,
[data-testid="stTextInput"] input {
    background: #ffffff !important;
    border: 1px solid #d0d0d0 !important;
    border-radius: 4px !important;
    color: #111111 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.85rem !important;
}
[data-testid="stNumberInput"] button p {
    color: #111111 !important;
}
[data-testid="stNumberInput"] input:focus,
[data-testid="stSelectbox"] select:focus {
    border-color: rgba(99, 179, 237, 0.4) !important;
    box-shadow: 0 0 0 2px rgba(99, 179, 237, 0.1) !important;
}

/* Labels */
label, [data-testid="stWidgetLabel"] p {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.72rem !important;
    color: #6b7a99 !important;
    letter-spacing: 0.05em !important;
    text-transform: uppercase !important;
    font-weight: 400 !important;
}

/* ── Predict Button ── */
[data-testid="stButton"] button {
    background: linear-gradient(135deg, #1a3a5c 0%, #0d2240 100%) !important;
    color: #63b3ed !important;
    border: 1px solid rgba(99, 179, 237, 0.3) !important;
    border-radius: 4px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    padding: 0.75rem 2rem !important;
    transition: all 0.2s !important;
    width: 100% !important;
}
[data-testid="stButton"] button:hover {
    background: linear-gradient(135deg, #1e4a73 0%, #0f2d52 100%) !important;
    border-color: rgba(99, 179, 237, 0.6) !important;
    box-shadow: 0 0 20px rgba(99, 179, 237, 0.15) !important;
    transform: translateY(-1px) !important;
}

/* ── Result Cards ── */
.result-high {
    background: linear-gradient(135deg, rgba(197, 48, 48, 0.12) 0%, rgba(197, 48, 48, 0.05) 100%);
    border: 1px solid rgba(197, 48, 48, 0.3);
    border-radius: 8px;
    padding: 2rem;
}
.result-low {
    background: linear-gradient(135deg, rgba(39, 103, 73, 0.15) 0%, rgba(39, 103, 73, 0.05) 100%);
    border: 1px solid rgba(72, 187, 120, 0.3);
    border-radius: 8px;
    padding: 2rem;
}
.result-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}
.result-label-high { color: #fc8181; }
.result-label-low { color: #68d391; }
.result-probability {
    font-family: 'Syne', sans-serif;
    font-size: 4rem;
    font-weight: 800;
    line-height: 1;
    margin-bottom: 0.25rem;
}
.result-probability-high { color: #fc8181; }
.result-probability-low { color: #68d391; }
.result-verdict {
    font-family: 'Syne', sans-serif;
    font-size: 1.1rem;
    font-weight: 600;
    color: #ffffff;
    margin-bottom: 1.5rem;
}
.action-item {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.6rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.04);
    font-size: 0.8rem;
    color: #a0aec0;
}
.action-icon {
    font-size: 1rem;
    width: 24px;
    text-align: center;
}

/* ── Metrics ── */
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.025) !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    border-radius: 6px !important;
    padding: 1rem 1.25rem !important;
}
[data-testid="stMetricLabel"] {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.65rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    color: #4a5568 !important;
}
[data-testid="stMetricValue"] {
    font-family: 'Syne', sans-serif !important;
    font-size: 1.8rem !important;
    font-weight: 700 !important;
    color: #63b3ed !important;
}

/* ── Info/Warning boxes ── */
[data-testid="stInfo"] {
    background: rgba(99, 179, 237, 0.06) !important;
    border: 1px solid rgba(99, 179, 237, 0.2) !important;
    border-radius: 4px !important;
    color: #a0c4e8 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.78rem !important;
}
[data-testid="stSuccess"] {
    background: rgba(72, 187, 120, 0.06) !important;
    border: 1px solid rgba(72, 187, 120, 0.2) !important;
    border-radius: 4px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.78rem !important;
}
[data-testid="stError"] {
    background: rgba(252, 129, 129, 0.06) !important;
    border: 1px solid rgba(252, 129, 129, 0.2) !important;
    border-radius: 4px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.78rem !important;
}

/* ── Dataframe ── */
[data-testid="stDataFrame"] {
    border: 1px solid rgba(255,255,255,0.06) !important;
    border-radius: 6px !important;
}

/* ── File Uploader ── */
[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.02) !important;
    border: 1px dashed rgba(99, 179, 237, 0.2) !important;
    border-radius: 6px !important;
    padding: 1rem !important;
}

/* ── Slider ── */
[data-testid="stSlider"] [role="slider"] {
    background: #63b3ed !important;
    border-color: #63b3ed !important;
}
[data-testid="stSlider"] [data-baseweb="slider"] div[role="progressbar"] {
    background: #63b3ed !important;
}

/* ── Divider ── */
hr {
    border: none !important;
    border-top: 1px solid rgba(255,255,255,0.06) !important;
    margin: 2rem 0 !important;
}

/* ── Footer ── */
.footer {
    margin-top: 3rem;
    padding-top: 1.5rem;
    border-top: 1px solid rgba(255,255,255,0.06);
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.footer-left {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    color: #2d3748;
}
.footer-right {
    display: flex;
    gap: 1.5rem;
}
.footer-badge {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    color: #4a5568;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.06);
    padding: 0.25rem 0.6rem;
    border-radius: 2px;
    letter-spacing: 0.05em;
}
</style>
""", unsafe_allow_html=True)

# ─── Load Model ────────────────────────────────────────────────
@st.cache_resource
def load_model():
    with open('ecom_churn_model.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('ecom_feature_names.pkl', 'rb') as f:
        features = pickle.load(f)
    return model, features

model, feature_names = load_model()

# ─── Hero Header ───────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-tag"><span class="anim-icon anim-glow"><svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="#63b3ed" stroke-width="2.5"><circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M4.22 4.22l2.12 2.12M17.66 17.66l2.12 2.12M2 12h3M19 12h3M4.22 19.78l2.12-2.12M17.66 6.34l2.12-2.12"/></svg></span> ML-Powered Analytics</div>
    <div class="hero-title">Churn<span>Lens</span></div>
    <div class="hero-subtitle">E-Commerce Customer Intelligence Platform</div>
    <div class="hero-stats">
        <div class="hero-stat">
            <div class="hero-stat-val">94.23%</div>
            <div class="hero-stat-label">Accuracy</div>
        </div>
        <div class="hero-stat">
            <div class="hero-stat-val">0.97</div>
            <div class="hero-stat-label">AUC Score</div>
        </div>
        <div class="hero-stat">
            <div class="hero-stat-val">0.81</div>
            <div class="hero-stat-label">F1 Score</div>
        </div>
        <div class="hero-stat">
            <div class="hero-stat-val">5,630</div>
            <div class="hero-stat-label">Training Records</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Tabs ──────────────────────────────────────────────────────
tab1, tab2 = st.tabs(["  Single Prediction", "  Bulk Analysis"])


# ══════════════════════════════════════════════════════════════
# TAB 1 — Single Customer Prediction
# ══════════════════════════════════════════════════════════════
with tab1:
    st.markdown('<div class="section-header"><span class="anim-icon anim-float"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#63b3ed" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg></span> Customer Profile Input</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('<div class="input-card"><div class="input-card-title"><span class="anim-icon anim-float"><svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="#63b3ed" stroke-width="2"><rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 7V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v2"/></svg></span> Account &amp; Activity</div>', unsafe_allow_html=True)
        tenure = st.number_input("Tenure (months)", 0, 61, 10)
        city_tier = st.selectbox("City Tier", [1, 2, 3])
        warehouse_to_home = st.number_input("Warehouse Distance (km)", 5, 130, 20)
        hour_spend_on_app = st.number_input("Hours on App / Day", 0, 5, 3)
        num_devices = st.number_input("Devices Registered", 1, 6, 3)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="input-card"><div class="input-card-title"><span class="anim-icon anim-pulse"><svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="#63b3ed" stroke-width="2"><rect x="2" y="5" width="20" height="14" rx="2"/><path d="M2 10h20"/></svg></span> Purchase Behaviour</div>', unsafe_allow_html=True)
        satisfaction_score = st.slider("Satisfaction Score", 1, 5, 3)
        num_address = st.number_input("Saved Addresses", 1, 22, 3)
        complain = st.selectbox("Filed Complaint?", [0, 1],
                                format_func=lambda x: "Yes" if x == 1 else "No")
        order_hike = st.number_input("Order Value Hike YoY (%)", 11, 26, 15)
        coupon_used = st.number_input("Coupons Used", 0, 16, 2)
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="input-card"><div class="input-card-title"><span class="anim-icon anim-spin"><svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="#63b3ed" stroke-width="2"><circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/></svg></span> Order &amp; Payment</div>', unsafe_allow_html=True)
        order_count = st.number_input("Orders Last Month", 1, 16, 3)
        day_since_last_order = st.number_input("Days Since Last Order", 0, 46, 5)
        cashback_amount = st.number_input("Cashback Earned (₹)", 0, 325, 150)
        preferred_login = st.selectbox("Login Device", ["Mobile Phone", "Computer"])
        gender = st.selectbox("Gender", ["Male", "Female"])
        st.markdown('</div>', unsafe_allow_html=True)

    col4, col5, col6 = st.columns(3)
    with col4:
        payment_mode = st.selectbox("Payment Method",
                                    ["Debit Card", "Credit Card", "E wallet", "COD", "UPI"])
    with col5:
        preferred_order_cat = st.selectbox("Favourite Category",
                                           ["Mobile Phone", "Laptop & Accessory",
                                            "Fashion", "Grocery", "Others"])
    with col6:
        marital_status = st.selectbox("Marital Status", ["Married", "Single", "Divorced"])

    # ── Encode inputs ──
    def encode_input():
        login_map = {'Mobile Phone': 0, 'Computer': 1}
        gender_map = {'Male': 0, 'Female': 1}

        data = {
            'Tenure': tenure,
            'PreferredLoginDevice': login_map[preferred_login],
            'CityTier': city_tier,
            'WarehouseToHome': warehouse_to_home,
            'Gender': gender_map[gender],
            'HourSpendOnApp': hour_spend_on_app,
            'NumberOfDeviceRegistered': num_devices,
            'SatisfactionScore': satisfaction_score,
            'NumberOfAddress': num_address,
            'Complain': complain,
            'OrderAmountHikeFromlastYear': order_hike,
            'CouponUsed': coupon_used,
            'OrderCount': order_count,
            'DaySinceLastOrder': day_since_last_order,
            'CashbackAmount': cashback_amount,
            'PreferredPaymentMode_COD': 1 if payment_mode == 'COD' else 0,
            'PreferredPaymentMode_Credit Card': 1 if payment_mode == 'Credit Card' else 0,
            'PreferredPaymentMode_Debit Card': 1 if payment_mode == 'Debit Card' else 0,
            'PreferredPaymentMode_E wallet': 1 if payment_mode == 'E wallet' else 0,
            'PreferredPaymentMode_UPI': 1 if payment_mode == 'UPI' else 0,
            'PreferedOrderCat_Fashion': 1 if preferred_order_cat == 'Fashion' else 0,
            'PreferedOrderCat_Grocery': 1 if preferred_order_cat == 'Grocery' else 0,
            'PreferedOrderCat_Laptop & Accessory': 1 if preferred_order_cat == 'Laptop & Accessory' else 0,
            'PreferedOrderCat_Mobile Phone': 1 if preferred_order_cat == 'Mobile Phone' else 0,
            'PreferedOrderCat_Others': 1 if preferred_order_cat == 'Others' else 0,
            'MaritalStatus_Divorced': 1 if marital_status == 'Divorced' else 0,
            'MaritalStatus_Married': 1 if marital_status == 'Married' else 0,
            'MaritalStatus_Single': 1 if marital_status == 'Single' else 0,
        }
        return pd.DataFrame([data])[feature_names]

    st.markdown("<br>", unsafe_allow_html=True)
    predict_btn = st.button("[ → ] RUN CHURN ANALYSIS", use_container_width=True)

    if predict_btn:
        try:
            input_df = encode_input()
            prediction = model.predict(input_df)[0]
            probability = model.predict_proba(input_df)[0][1]
            retain_prob = 1 - probability

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="section-header"><span class="anim-icon anim-bounce"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#63b3ed" stroke-width="2"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg></span> Prediction Result</div>', unsafe_allow_html=True)

            res_col1, res_col2 = st.columns([1, 1])

            with res_col1:
                if prediction == 1:
                    st.markdown(f"""
                    <div class="result-high">
                        <div class="result-label result-label-high">
                            <span class="anim-icon anim-shake"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#fc8181" stroke-width="2.5"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg></span>
                            CHURN RISK DETECTED
                        </div>
                        <div class="result-probability result-probability-high">{probability*100:.1f}%</div>
                        <div class="result-verdict">This customer is likely to churn</div>
                        <div class="action-item">
                            <span class="action-icon anim-icon anim-float"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#fc8181" stroke-width="2"><path d="M20 12V22H4V12"/><path d="M22 7H2v5h20V7z"/><path d="M12 22V7"/><path d="M12 7H7.5a2.5 2.5 0 0 1 0-5C11 2 12 7 12 7z"/><path d="M12 7h4.5a2.5 2.5 0 0 0 0-5C13 2 12 7 12 7z"/></svg></span>
                            Send personalized discount or cashback offer
                        </div>
                        <div class="action-item">
                            <span class="action-icon anim-icon anim-pulse"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#fc8181" stroke-width="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07A19.5 19.5 0 0 1 4.99 12a19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 3.9 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg></span>
                            Proactive retention call from support team
                        </div>
                        <div class="action-item">
                            <span class="action-icon anim-icon anim-wave"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#fc8181" stroke-width="2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg></span>
                            Re-engagement email campaign
                        </div>
                        <div class="action-item">
                            <span class="action-icon anim-icon anim-glow"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#fc8181" stroke-width="2"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg></span>
                            Offer loyalty tier upgrade
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="result-low">
                        <div class="result-label result-label-low">
                            <span class="anim-icon anim-tick"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#68d391" stroke-width="2.5"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg></span>
                            LOW CHURN RISK
                        </div>
                        <div class="result-probability result-probability-low">{probability*100:.1f}%</div>
                        <div class="result-verdict">This customer is likely to stay</div>
                        <div class="action-item">
                            <span class="action-icon anim-icon anim-glow"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#68d391" stroke-width="2"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg></span>
                            Enroll in premium loyalty rewards program
                        </div>
                        <div class="action-item">
                            <span class="action-icon anim-icon anim-wave"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#68d391" stroke-width="2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg></span>
                            Send curated product recommendations
                        </div>
                        <div class="action-item">
                            <span class="action-icon anim-icon anim-pulse"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#68d391" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg></span>
                            Request product review or NPS feedback
                        </div>
                        <div class="action-item">
                            <span class="action-icon anim-icon anim-float"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#68d391" stroke-width="2"><path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/><path d="M16 10a4 4 0 0 1-8 0"/></svg></span>
                            Upsell with exclusive member offers
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

            with res_col2:
                # ── Donut chart ──
                # churn_pct  = probability * 100  (e.g. 7.6%)
                # retain_pct = retain_prob * 100  (e.g. 92.4%)
                # Slice order: [Retain (big), Churn (small)]
                # Colors:       green           red
                churn_pct  = probability * 100
                retain_pct = retain_prob * 100

                fig, ax = plt.subplots(figsize=(5, 5), subplot_kw=dict(aspect='equal'))
                fig.patch.set_facecolor('#0d1117')
                ax.set_facecolor('#0d1117')

                # Always: first slice = Retain (green), second slice = Churn (red)
                slice_vals   = [retain_pct, churn_pct]
                slice_colors = ['#9ae6b4', '#fc8181']
                slice_labels = ['Retain', 'Churn']

                wedges, _ = ax.pie(
                    slice_vals,
                    colors=slice_colors,
                    startangle=90,
                    wedgeprops=dict(width=0.55, edgecolor='#0d1117', linewidth=3),
                    counterclock=False
                )

                # Centre text always shows the CHURN probability
                centre_color = '#fc8181' if prediction == 1 else '#48bb78'

                ax.text(0, 0, f"{churn_pct:.1f}%",
                        ha='center', va='center',
                        fontsize=26, fontweight='bold',
                        color=centre_color, fontfamily='monospace')

                # Legend — always Retain then Churn
                from matplotlib.patches import Patch
                legend_elements = [
                    Patch(facecolor='#9ae6b4', label=f'Retain   {retain_pct:.1f}%'),
                    Patch(facecolor='#fc8181', label=f'Churn    {churn_pct:.1f}%'),
                ]
                legend = ax.legend(
                    handles=legend_elements,
                    loc='lower center',
                    bbox_to_anchor=(0, -0.08),
                    ncol=2,
                    frameon=False,
                    fontsize=8,
                    labelcolor='#a0aec0',
                )
                for text in legend.get_texts():
                    text.set_fontfamily('monospace')

                ax.set_title('Risk Probability',
                             color='#6b7a99', fontsize=9,
                             fontfamily='monospace', pad=10, loc='left')
                plt.tight_layout()
                st.pyplot(fig)
                plt.close()

        except KeyError as e:
            st.error(f"Column mismatch: {e}")
        except Exception as e:
            st.error(f"Error: {e}")


# ══════════════════════════════════════════════════════════════
# TAB 2 — Bulk CSV Prediction
# ══════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-header"><span class="anim-icon anim-spin"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#63b3ed" stroke-width="2"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/></svg></span> Batch Customer Analysis</div>', unsafe_allow_html=True)

    with st.expander("[ i ] Required CSV column format"):
        st.code(str(list(feature_names)))
        st.caption("PreferredLoginDevice: 0=Mobile Phone, 1=Computer | Gender: 0=Male, 1=Female | Payment/Category/Marital columns are one-hot encoded (0 or 1)")

    uploaded_file = st.file_uploader("Drop your CSV file here", type=['csv'])

    if uploaded_file is not None:
        try:
            bulk_df = pd.read_csv(uploaded_file)

            st.markdown('<div class="section-header"><span class="anim-icon anim-float"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#63b3ed" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M3 15h18M9 3v18"/></svg></span> Data Preview</div>', unsafe_allow_html=True)
            st.dataframe(bulk_df.head(), use_container_width=True)

            missing_cols = set(feature_names) - set(bulk_df.columns)
            if missing_cols:
                st.error(f"Missing columns: {missing_cols}")
            else:
                input_bulk = bulk_df[feature_names]
                predictions = model.predict(input_bulk)
                probabilities = model.predict_proba(input_bulk)[:, 1]

                bulk_df['Churn_Prediction'] = predictions
                bulk_df['Churn_Probability_%'] = (probabilities * 100).round(1)
                bulk_df['Risk_Level'] = pd.cut(
                    probabilities,
                    bins=[0, 0.3, 0.6, 1.0],
                    labels=['Low', 'Medium', 'High']
                )

                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown('<div class="section-header"><span class="anim-icon anim-pulse"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#63b3ed" stroke-width="2"><rect x="2" y="3" width="20" height="14" rx="2"/><path d="M8 21h8M12 17v4"/></svg></span> Summary Dashboard</div>', unsafe_allow_html=True)

                total = len(bulk_df)
                churned = int(predictions.sum())
                retained = total - churned
                churn_rate = churned / total * 100

                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Total Customers", f"{total:,}")
                m2.metric("Predicted Churn", f"{churned:,}")
                m3.metric("Retained", f"{retained:,}")
                m4.metric("Churn Rate", f"{churn_rate:.1f}%")

                st.markdown("<br>", unsafe_allow_html=True)

                chart_col1, chart_col2 = st.columns(2)

                with chart_col1:
                    fig1, ax1 = plt.subplots(figsize=(5, 4))
                    fig1.patch.set_facecolor('#0d1117')
                    ax1.set_facecolor('#0d1117')

                    wedge_props = {'linewidth': 2, 'edgecolor': '#0d1117'}
                    wedges, texts, autotexts = ax1.pie(
                        [retained, churned],
                        labels=['Retained', 'Churned'],
                        colors=['#48bb78', '#fc8181'],
                        autopct='%1.1f%%',
                        startangle=90,
                        wedgeprops=wedge_props,
                        pctdistance=0.75
                    )
                    for text in texts:
                        text.set_color('#6b7a99')
                        text.set_fontsize(9)
                        text.set_fontfamily('monospace')
                    for autotext in autotexts:
                        autotext.set_color('#ffffff')
                        autotext.set_fontsize(9)
                        autotext.set_fontweight('bold')
                        autotext.set_fontfamily('monospace')

                    ax1.set_title('Churn vs Retention Split',
                                  color='#6b7a99', fontsize=9,
                                  fontfamily='monospace', pad=15, loc='left')
                    plt.tight_layout()
                    st.pyplot(fig1)
                    plt.close()

                with chart_col2:
                    fig2, ax2 = plt.subplots(figsize=(5, 4))
                    fig2.patch.set_facecolor('#0d1117')
                    ax2.set_facecolor('#0d1117')

                    risk_counts = bulk_df['Risk_Level'].value_counts()
                    risk_order = ['Low', 'Medium', 'High']
                    risk_vals = [risk_counts.get(r, 0) for r in risk_order]
                    risk_colors = ['#48bb78', '#f6ad55', '#fc8181']

                    bars = ax2.bar(risk_order, risk_vals,
                                   color=risk_colors, width=0.5,
                                   edgecolor='none')
                    for bar, val in zip(bars, risk_vals):
                        ax2.text(bar.get_x() + bar.get_width()/2,
                                 bar.get_height() + 0.3,
                                 str(val), ha='center', va='bottom',
                                 color='#e8eaf0', fontsize=10,
                                 fontfamily='monospace', fontweight='bold')

                    ax2.set_ylabel('Customers', color='#4a5568',
                                   fontsize=8, fontfamily='monospace')
                    ax2.set_title('Risk Level Distribution',
                                  color='#6b7a99', fontsize=9,
                                  fontfamily='monospace', pad=15, loc='left')
                    ax2.tick_params(colors='#6b7a99', labelsize=9)
                    for spine in ax2.spines.values():
                        spine.set_visible(False)
                    ax2.set_ylim(0, max(risk_vals) * 1.2 if max(risk_vals) > 0 else 10)
                    ax2.grid(axis='y', color='#1a2235', linewidth=0.5)
                    plt.tight_layout()
                    st.pyplot(fig2)
                    plt.close()

                st.markdown('<div class="section-header"><span class="anim-icon anim-glow"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#63b3ed" stroke-width="2"><line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><line x1="3" y1="6" x2="3.01" y2="6"/><line x1="3" y1="12" x2="3.01" y2="12"/><line x1="3" y1="18" x2="3.01" y2="18"/></svg></span> Detailed Results</div>', unsafe_allow_html=True)
                result_cols = ['Churn_Prediction', 'Churn_Probability_%', 'Risk_Level'] + list(feature_names)
                result_cols = [c for c in result_cols if c in bulk_df.columns]
                st.dataframe(
                    bulk_df[result_cols].sort_values('Churn_Probability_%', ascending=False),
                    use_container_width=True
                )

                csv_out = bulk_df.to_csv(index=False)
                st.download_button(
                    label="↓ EXPORT RESULTS AS CSV",
                    data=csv_out,
                    file_name='churn_predictions.csv',
                    mime='text/csv',
                    use_container_width=True
                )

        except Exception as e:
            st.error(f"Error processing file: {e}")

# ─── Footer ────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    <div class="footer-left">
        <span class="anim-icon anim-pulse" style="margin-right:6px;">
            <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="#2d3748" stroke-width="2">
                <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>
            </svg>
        </span>
        2025 ChurnLens · Built with Streamlit &amp; scikit-learn
    </div>
    <div class="footer-right">
        <span class="footer-badge">
            <span class="anim-icon anim-gear" style="display:inline-block;margin-right:4px;">
                <svg width="9" height="9" viewBox="0 0 24 24" fill="none" stroke="#4a5568" stroke-width="2">
                    <circle cx="12" cy="12" r="3"/>
                    <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/>
                </svg>
            </span>
            Random Forest
        </span>
        <span class="footer-badge">AUC 0.97</span>
        <span class="footer-badge">ACC 94.23%</span>
        <span class="footer-badge">F1 0.81</span>
    </div>
</div>
""", unsafe_allow_html=True)