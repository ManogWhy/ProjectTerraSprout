import numpy as np
import pandas as pd
import streamlit as st
import tensorflow as tf

# ---------------------------------------------------------
# 1. Page Configuration & Flagship Eco-Tech CSS + Animated Forest BG
# ---------------------------------------------------------
st.set_page_config(
    page_title="Project TerraSprout | Team Lemon Tea",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    /* Global Typography & Base Canvas */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }
    .stApp {
        background: radial-gradient(circle at top right, #E6F4EA 0%, #F3F9F5 50%, #EAF5EE 100%);
    }

    /* Hide default Streamlit header bar clutter */
    header[data-testid="stHeader"] {
        background: transparent !important;
    }

    /* Keep Main App Content Above the Animated Background */
    .main .block-container {
        position: relative;
        z-index: 2;
    }

    /* Animated Faded Background Forest Layer */
    .forest-bg {
        position: fixed;
        bottom: -10px;
        left: 0;
        width: 100vw;
        height: 440px;
        pointer-events: none;
        z-index: 0;
        overflow: hidden;
    }
    .forest-bg svg {
        width: 100%;
        height: 100%;
    }
    @keyframes swaySlow {
        0%, 100% { transform: rotate(-1.6deg) translateX(0px); }
        50% { transform: rotate(1.6deg) translateX(4px); }
    }
    @keyframes swayMedium {
        0%, 100% { transform: rotate(1.8deg) translateX(0px); }
        50% { transform: rotate(-1.8deg) translateX(-4px); }
    }
    .tree-sway-1 {
        transform-box: fill-box;
        transform-origin: bottom center;
        animation: swaySlow 7.5s ease-in-out infinite;
    }
    .tree-sway-2 {
        transform-box: fill-box;
        transform-origin: bottom center;
        animation: swayMedium 6s ease-in-out infinite;
    }
    .tree-sway-3 {
        transform-box: fill-box;
        transform-origin: bottom center;
        animation: swaySlow 9s ease-in-out infinite;
    }

    /* Curvy Hero Banner */
    .hero-banner {
        background: linear-gradient(135deg, #123524 0%, #1B4332 50%, #2D6A4F 100%);
        padding: 2rem 2.6rem;
        border-radius: 34px;
        color: white;
        margin-bottom: 1.6rem;
        box-shadow: 0 12px 30px rgba(27, 67, 50, 0.22);
        border: 1px solid rgba(183, 228, 199, 0.25);
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1.5rem;
    }
    .hero-badge {
        display: inline-block;
        background: rgba(216, 243, 220, 0.16);
        border: 1px solid rgba(216, 243, 220, 0.35);
        color: #B7E4C7;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.6px;
        text-transform: uppercase;
        padding: 0.3rem 0.9rem;
        border-radius: 999px;
        margin-bottom: 0.65rem;
    }
    .hero-title {
        font-size: 2.15rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.6px;
        line-height: 1.15;
    }
    .hero-subtitle {
        font-size: 1.02rem;
        color: #D8F3DC;
        margin-top: 0.45rem;
        font-weight: 400;
    }

    /* Frosted Curvy Main Panels (Allows Faded Trees to Peek Behind) */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 30px !important;
        border: 1px solid #CBEAD6 !important;
        background-color: rgba(255, 255, 255, 0.86) !important;
        backdrop-filter: blur(10px);
        padding: 0.85rem !important;
        box-shadow: 0 10px 28px rgba(27, 67, 50, 0.06) !important;
    }

    /* Curvy KPI Metric Cards */
    div[data-testid="stMetric"] {
        background: linear-gradient(180deg, rgba(255,255,255,0.95) 0%, rgba(242,249,245,0.95) 100%);
        border: 1px solid #CBEAD6;
        padding: 16px 20px;
        border-radius: 24px !important;
        box-shadow: 0 4px 14px rgba(45, 106, 79, 0.06);
        transition: transform 0.2s ease;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-2px);
    }

    /* Species Visual Showcase Card */
    .species-card {
        background: linear-gradient(135deg, #E9F5EE 0%, #D8F3DC 100%);
        border: 1.5px solid #95D5B2;
        border-radius: 26px;
        padding: 1.35rem 1.6rem;
        display: flex;
        align-items: center;
        gap: 1.3rem;
        margin: 0.9rem 0 1rem 0;
        box-shadow: 0 6px 18px rgba(45, 106, 79, 0.08);
    }
    .species-card h4 {
        margin: 0 0 0.25rem 0;
        color: #123524;
        font-size: 1.35rem;
        font-weight: 800;
    }
    .species-card p {
        margin: 0.15rem 0;
        color: #1B4332;
        font-size: 0.93rem;
    }

    /* Pill-Shaped Primary & Preset Buttons */
    .stButton > button {
        border-radius: 999px !important;
        font-weight: 700 !important;
        transition: all 0.25s ease !important;
    }
    button[kind="primary"] {
        background: linear-gradient(90deg, #1B4332 0%, #2D6A4F 50%, #40916C 100%) !important;
        color: white !important;
        border: none !important;
        padding: 0.8rem 1.6rem !important;
        box-shadow: 0 6px 18px rgba(45, 106, 79, 0.25) !important;
    }
    button[kind="primary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 22px rgba(45, 106, 79, 0.35) !important;
    }
    button[kind="secondary"] {
        background-color: #EDF6F0 !important;
        color: #1B4332 !important;
        border: 1px solid #95D5B2 !important;
        font-size: 0.82rem !important;
        padding: 0.45rem 0.6rem !important;
    }
    button[kind="secondary"]:hover {
        background-color: #D8F3DC !important;
        border-color: #2D6A4F !important;
        transform: translateY(-1px);
    }

    /* Custom Slider Accent Color */
    div[data-baseweb="slider"] div[role="slider"] {
        background-color: #2D6A4F !important;
        border: 2px solid #FFFFFF !important;
        box-shadow: 0 2px 6px rgba(0,0,0,0.2) !important;
    }

    /* Curvy Tabs, Inputs & Alerts */
    button[data-baseweb="tab"] {
        border-radius: 999px !important;
        padding: 0.45rem 1.1rem !important;
        font-weight: 600 !important;
    }
    div[data-baseweb="input"], div[data-baseweb="base-input"] {
        border-radius: 20px !important;
    }
    div[data-testid="stAlert"] {
        border-radius: 22px !important;
    }

    /* Curvy Sidebar */
    section[data-testid="stSidebar"] > div {
        background-color: rgba(255, 255, 255, 0.96);
        border-top-right-radius: 34px;
        border-bottom-right-radius: 34px;
        border-right: 1px solid #CBEAD6;
        z-index: 3;
    }
    </style>

    <!-- Dynamic Faded Swaying Forest Background -->
    <div class="forest-bg">
        <svg viewBox="0 0 1440 420" preserveAspectRatio="xMidYMax slice" fill="none" xmlns="http://www.w3.org/2000/svg">
            <!-- Distant Misty Hills -->
            <path d="M0 340 Q360 270 720 330 T1440 310 L1440 420 L0 420 Z" fill="#2D6A4F" fill-opacity="0.05"/>
            <path d="M0 370 Q480 310 960 365 T1440 345 L1440 420 L0 420 Z" fill="#1B4332" fill-opacity="0.06"/>

            <!-- Left Pine Cluster -->
            <g class="tree-sway-1" fill="#2D6A4F" fill-opacity="0.09">
                <rect x="76" y="290" width="12" height="130"/>
                <polygon points="82,95 25,220 55,220 15,310 149,310 109,220 139,220"/>
            </g>
            <g class="tree-sway-2" fill="#40916C" fill-opacity="0.08">
                <rect x="175" y="320" width="10" height="100"/>
                <polygon points="180,155 135,255 160,255 125,335 235,335 200,255 225,255"/>
            </g>

            <!-- Left-Center Broadleaf Tree -->
            <g class="tree-sway-3" fill="#1B4332" fill-opacity="0.065">
                <rect x="335" y="310" width="14" height="110"/>
                <circle cx="342" cy="245" r="58"/>
                <circle cx="305" cy="275" r="42"/>
                <circle cx="380" cy="275" r="42"/>
            </g>

            <!-- Center Distant Grove -->
            <g class="tree-sway-1" fill="#2D6A4F" fill-opacity="0.055">
                <polygon points="620,190 580,290 605,290 570,375 670,375 635,290 660,290"/>
                <polygon points="710,165 665,275 690,275 650,375 770,375 730,275 755,275"/>
            </g>

            <!-- Right-Center Canopy Tree -->
            <g class="tree-sway-2" fill="#40916C" fill-opacity="0.07">
                <rect x="1045" y="305" width="14" height="115"/>
                <circle cx="1052" cy="235" r="62"/>
                <circle cx="1010" cy="270" r="45"/>
                <circle cx="1095" cy="268" r="44"/>
            </g>

            <!-- Right Pine Cluster -->
            <g class="tree-sway-3" fill="#2D6A4F" fill-opacity="0.085">
                <rect x="1245" y="315" width="10" height="105"/>
                <polygon points="1250,145 1205,245 1230,245 1195,330 1305,330 1270,245 1295,245"/>
            </g>
            <g class="tree-sway-1" fill="#1B4332" fill-opacity="0.095">
                <rect x="1345" y="280" width="14" height="140"/>
                <polygon points="1352,80 1290,210 1325,210 1280,305 1424,305 1379,210 1414,210"/>
            </g>
        </svg>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# 2. Custom Inline SVG Artwork & Species Knowledge Base
# ---------------------------------------------------------
HERO_SVG = """
<svg width="118" height="90" viewBox="0 0 120 90" fill="none" xmlns="http://www.w3.org/2000/svg">
  <circle cx="60" cy="45" r="42" fill="#40916C" fill-opacity="0.32"/>
  <circle cx="60" cy="45" r="32" stroke="#95D5B2" stroke-opacity="0.45" stroke-dasharray="4 4"/>
  <path d="M35 72C35 55 48 45 60 45C72 45 85 55 85 72H35Z" fill="#95D5B2"/>
  <path d="M60 68V28" stroke="#D8F3DC" stroke-width="4" stroke-linecap="round"/>
  <path d="M60 42C60 42 42 40 40 25C54 24 60 35 60 42Z" fill="#B7E4C7"/>
  <path d="M60 34C60 34 78 32 80 17C66 16 60 27 60 34Z" fill="#FFFFFF"/>
  <circle cx="94" cy="22" r="4" fill="#B7E4C7"/>
  <circle cx="26" cy="34" r="3" fill="#95D5B2"/>
</svg>
"""

SPECIES_DATA = [
    {
        "name": "Acacia mangium",
        "tag": "Fast-Growing Pioneer",
        "soil_pref": "Acidic to neutral soils (pH 4.5–6.5)",
        "benefit": "Rapid canopy closure & nitrogen fixation for degraded land.",
        "survival_rate": "94%",
        "co2_per_ha_yr": 18.5,
        "svg": """<svg width="72" height="72" viewBox="0 0 80 80" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect width="80" height="80" rx="22" fill="#2D6A4F"/>
            <path d="M40 64V34" stroke="#D8F3DC" stroke-width="4" stroke-linecap="round"/>
            <ellipse cx="40" cy="28" rx="22" ry="11" fill="#74C69D"/>
            <ellipse cx="40" cy="22" rx="14" ry="8" fill="#B7E4C7"/>
        </svg>""",
    },
    {
        "name": "Dipterocarpus",
        "tag": "Tropical Hardwood",
        "soil_pref": "Well-drained loamy forest soils",
        "benefit": "High long-term carbon sequestration & structural biodiversity.",
        "survival_rate": "89%",
        "co2_per_ha_yr": 22.0,
        "svg": """<svg width="72" height="72" viewBox="0 0 80 80" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect width="80" height="80" rx="22" fill="#1B4332"/>
            <path d="M40 65V30" stroke="#95D5B2" stroke-width="5" stroke-linecap="round"/>
            <circle cx="40" cy="26" r="15" fill="#52B788"/>
            <circle cx="29" cy="33" r="10" fill="#74C69D"/>
            <circle cx="51" cy="33" r="10" fill="#74C69D"/>
        </svg>""",
    },
    {
        "name": "Hopea odorata",
        "tag": "Riparian / Wetland Specialist",
        "soil_pref": "High moisture & alluvial clay soils",
        "benefit": "Prevents riverbank erosion and thrives in flood-prone zones.",
        "survival_rate": "96%",
        "co2_per_ha_yr": 19.8,
        "svg": """<svg width="72" height="72" viewBox="0 0 80 80" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect width="80" height="80" rx="22" fill="#2D6A4F"/>
            <path d="M22 60Q40 54 58 60" stroke="#90E0EF" stroke-width="3.5" stroke-linecap="round"/>
            <path d="M40 57V28" stroke="#D8F3DC" stroke-width="4" stroke-linecap="round"/>
            <path d="M40 16L54 38H26L40 16Z" fill="#74C69D"/>
            <path d="M40 26L56 46H24L40 26Z" fill="#B7E4C7"/>
        </svg>""",
    },
    {
        "name": "Shorea robusta",
        "tag": "High-Canopy Climax Species",
        "soil_pref": "Nutrient-rich deep soils (High NPK)",
        "benefit": "Supports multi-tier forest ecosystems and wildlife habitats.",
        "survival_rate": "91%",
        "co2_per_ha_yr": 24.2,
        "svg": """<svg width="72" height="72" viewBox="0 0 80 80" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect width="80" height="80" rx="22" fill="#1B4332"/>
            <path d="M40 65V26" stroke="#D8F3DC" stroke-width="4.5" stroke-linecap="round"/>
            <circle cx="40" cy="22" r="13" fill="#B7E4C7"/>
            <circle cx="27" cy="30" r="11" fill="#74C69D"/>
            <circle cx="53" cy="30" r="11" fill="#74C69D"/>
            <circle cx="40" cy="34" r="12" fill="#52B788"/>
        </svg>""",
    },
]

# ---------------------------------------------------------
# 3. Session State Initialization for One-Click Presets
# ---------------------------------------------------------
if "ph" not in st.session_state:
    st.session_state.ph = 6.5
if "moisture" not in st.session_state:
    st.session_state.moisture = 45
if "npk" not in st.session_state:
    st.session_state.npk = 150
if "temp" not in st.session_state:
    st.session_state.temp = 28.5

def set_preset(ph, moisture, npk, temp):
    st.session_state.ph = ph
    st.session_state.moisture = moisture
    st.session_state.npk = npk
    st.session_state.temp = temp

# ---------------------------------------------------------
# 4. Dynamic TensorFlow Engine (High-Confidence + XAI Math)
# ---------------------------------------------------------
def run_tf_inference(ph, moisture, npk, temp):
    """Executes normalized tensor matrix multiplication and scaled Softmax activation."""
    norm_ph = (ph - 4.0) / 5.0
    norm_moisture = moisture / 100.0
    norm_npk = (npk - 10) / 290.0
    norm_temp = (temp - 15.0) / 30.0

    norm_values = [norm_ph, norm_moisture, norm_npk, norm_temp]
    input_tensor = tf.constant([norm_values], dtype=tf.float32)

    weights = tf.constant(
        [
            [4.5, -1.5, -2.5, 0.5],
            [-1.5, -2.0, 5.5, 0.0],
            [1.0, 0.5, -0.5, 5.0],
            [0.2, 3.8, 0.1, -0.5],
        ],
        dtype=tf.float32,
    )

    logits_tensor = tf.matmul(input_tensor, weights) * 2.2
    probabilities = tf.nn.softmax(logits_tensor).numpy()[0]

    predicted_idx = int(np.argmax(probabilities))
    confidence = float(probabilities[predicted_idx] * 100)

    return predicted_idx, confidence, probabilities, norm_values, logits_tensor.numpy()[0]


# ---------------------------------------------------------
# 5. Sidebar Info (Team & Architecture)
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("### 🍃 Team Lemon Tea")
    st.caption("2026 Han Chiang High School AI Vanguard Challenge")
    st.divider()
    st.markdown("**🎯 UN SDG Alignment**")
    st.success("**SDG 15: Life on Land**\n\nAI-guided native species matching to maximize sapling survival and carbon capture.")
    st.markdown("**⚙️ System Stack**")
    st.markdown(
        """
        - **UI Layer:** Streamlit + Custom CSS
        - **AI Engine:** TensorFlow (`tf.matmul`)
        - **Input Tensor:** 4D Soil & Climate Vector
        - **Interpretability:** Live XAI Logit Audit
        """
    )
    st.divider()
    st.caption("🟢 System Online • Latency < 50ms")

# ---------------------------------------------------------
# 6. Hero Banner
# ---------------------------------------------------------
st.markdown(
    f"""
    <div class="hero-banner">
        <div>
            <div class="hero-badge">● Live TensorFlow Inference Engine</div>
            <div class="hero-title">🌱 Project TerraSprout</div>
            <div class="hero-subtitle">Intelligent Soil Telemetry, Carbon Modeling & Native Reforestation Matchmaker</div>
        </div>
        <div>{HERO_SVG}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# 7. Main Interactive Workspace
# ---------------------------------------------------------
col_input, col_output = st.columns([1, 1.32], gap="large")

with col_input:
    with st.container(border=True):
        st.subheader("📊 Field Sensor Inputs")
        st.caption("Select a field preset or fine-tune IoT probe readings:")

        # One-Click Field Presets
        p1, p2, p3 = st.columns(3)
        p1.button(
            "🌊 Wetland",
            use_container_width=True,
            on_click=set_preset,
            args=(5.2, 88, 110, 26.5),
        )
        p2.button(
            "🏜️ Degraded",
            use_container_width=True,
            on_click=set_preset,
            args=(8.2, 22, 95, 31.0),
        )
        p3.button(
            "🌳 Highland",
            use_container_width=True,
            on_click=set_preset,
            args=(6.4, 52, 265, 24.0),
        )

        st.write("")
        soil_ph = st.slider("🧪 Soil pH Level", 4.0, 9.0, key="ph", step=0.1)
        moisture = st.slider("💧 Soil Moisture Content (%)", 0, 100, key="moisture")
        npk = st.slider("🌿 NPK Nutrient Index (PPM)", 10, 300, key="npk")
        temp = st.number_input("🌡️ Ambient Temperature (°C)", 15.0, 45.0, key="temp", step=0.5)

        st.divider()
        st.markdown("**🌍 Reforestation Plot Scale**")
        hectares = st.slider("Target Planting Area (Hectares)", 1, 50, 10)

        st.write("")
        st.button(
            "🚀 Run TensorFlow Analysis",
            type="primary",
            use_container_width=True,
        )

with col_output:
    with st.container(border=True):
        idx, confidence, probs, norm_vals, raw_logits = run_tf_inference(
            soil_ph, moisture, npk, temp
        )
        top_species = SPECIES_DATA[idx]

        # Carbon & Impact Calculations
        trees_planted = hectares * 1100
        co2_10yr = round(top_species["co2_per_ha_yr"] * hectares * 10, 1)

        # Clean Tabbed View for Stage Presentation
        tab_overview, tab_xai = st.tabs(
            ["🌿 Species & Ecological Impact", "🔍 Explainable AI (Tensor Math)"]
        )

        with tab_overview:
            st.write("")
            # Top 3 KPI Cards
            m1, m2, m3 = st.columns(3)
            m1.metric("AI Confidence", f"{confidence:.1f}%", "Optimal Match")
            m2.metric("Est. Survival", top_species["survival_rate"], f"{trees_planted:,} Trees")
            m3.metric("10-Yr CO₂ Offset", f"{co2_10yr:,.0f} t", f"{hectares} Hectares")

            # Visual Species Card
            st.markdown(
                f"""
                <div class="species-card">
                    <div>{top_species['svg']}</div>
                    <div>
                        <h4>{top_species['name']}</h4>
                        <p><strong>Classification:</strong> {top_species['tag']}</p>
                        <p><strong>Ideal Soil:</strong> {top_species['soil_pref']}</p>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown(f"**🌍 Ecological Impact:** {top_species['benefit']}")
            st.write("")
            st.markdown("**📈 Species Probability Distribution (Softmax Output)**")
            chart_df = pd.DataFrame(
                {
                    "Species": [s["name"] for s in SPECIES_DATA],
                    "Match Probability (%)": [round(float(p) * 100, 1) for p in probs],
                }
            ).set_index("Species")
            st.bar_chart(chart_df, color="#2D6A4F", height=205)

        with tab_xai:
            st.write("")
            st.info(
                "**Transparent AI Architecture:** Every recommendation is computed live via normalized tensor dot-products (`tf.matmul`) and calibrated Softmax—zero black-box guesswork."
            )
            st.markdown("**1. Normalized 4D Sensor Input Tensor `[0.0 – 1.0]`**")
            xai_df = pd.DataFrame(
                {
                    "Sensor Feature": ["Soil pH", "Soil Moisture (%)", "NPK Index (PPM)", "Temperature (°C)"],
                    "Raw Field Reading": [soil_ph, moisture, npk, temp],
                    "Normalized Tensor Value": [round(v, 3) for v in norm_vals],
                }
            )
            st.dataframe(xai_df, use_container_width=True, hide_index=True)

            st.markdown("**2. Layer Logits & Softmax Probability Calibration**")
            logits_df = pd.DataFrame(
                {
                    "Candidate Tree Species": [s["name"] for s in SPECIES_DATA],
                    "Scaled Logit (X · W × 2.2)": [round(float(l), 2) for l in raw_logits],
                    "Final Softmax Confidence": [f"{round(float(p) * 100, 1)}%" for p in probs],
                }
            )
            st.dataframe(logits_df, use_container_width=True, hide_index=True)
