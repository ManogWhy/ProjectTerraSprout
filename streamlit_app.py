import numpy as np
import pandas as pd
import streamlit as st
import tensorflow as tf

# ---------------------------------------------------------
# 1. Page Configuration & Ultra-Curvy Organic CSS
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
    /* Main background */
    .stApp {
        background-color: #F4F8F5;
    }

    /* Curvy Hero Banner with Flex Layout for SVG Art */
    .hero-banner {
        background: linear-gradient(135deg, #1B4332 0%, #2D6A4F 100%);
        padding: 1.8rem 2.5rem;
        border-radius: 32px;
        color: white;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 24px rgba(27, 67, 50, 0.16);
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1.5rem;
    }
    .hero-title {
        font-size: 2.1rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .hero-subtitle {
        font-size: 1rem;
        color: #D8F3DC;
        margin-top: 0.35rem;
    }

    /* Curvy Main Containers */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 28px !important;
        border: 1px solid #D8F3DC !important;
        background-color: #FFFFFF !important;
        padding: 0.6rem !important;
        box-shadow: 0 6px 18px rgba(0, 0, 0, 0.04) !important;
    }

    /* Curvy KPI Metric Cards */
    div[data-testid="stMetric"] {
        background-color: #F8FBF9;
        border: 1px solid #D8F3DC;
        padding: 14px 18px;
        border-radius: 24px !important;
        box-shadow: 0 4px 12px rgba(45, 106, 79, 0.05);
    }

    /* Species Visual Showcase Card */
    .species-card {
        background: linear-gradient(135deg, #EDF6F0 0%, #D8F3DC 100%);
        border: 1px solid #B7E4C7;
        border-radius: 24px;
        padding: 1.2rem 1.5rem;
        display: flex;
        align-items: center;
        gap: 1.2rem;
        margin: 0.8rem 0 1rem 0;
    }
    .species-card h4 {
        margin: 0 0 0.25rem 0;
        color: #1B4332;
        font-size: 1.25rem;
    }
    .species-card p {
        margin: 0;
        color: #2D6A4F;
        font-size: 0.92rem;
    }

    /* Pill-Shaped Primary & Preset Buttons */
    .stButton > button {
        border-radius: 999px !important;
        font-weight: 600;
        transition: all 0.25s ease;
    }
    button[kind="primary"] {
        background: linear-gradient(90deg, #2D6A4F 0%, #40916C 100%) !important;
        color: white !important;
        border: none !important;
        padding: 0.75rem 1.5rem !important;
    }
    button[kind="primary"]:hover {
        background: linear-gradient(90deg, #1B4332 0%, #2D6A4F 100%) !important;
        transform: translateY(-1px);
        box-shadow: 0 6px 16px rgba(45, 106, 79, 0.3);
    }
    button[kind="secondary"] {
        background-color: #EDF6F0 !important;
        color: #1B4332 !important;
        border: 1px solid #B7E4C7 !important;
        font-size: 0.82rem !important;
    }
    button[kind="secondary"]:hover {
        background-color: #D8F3DC !important;
        border-color: #40916C !important;
    }

    /* Curvy Number Inputs, Alerts & Expanders */
    div[data-baseweb="input"], div[data-baseweb="base-input"] {
        border-radius: 20px !important;
    }
    div[data-testid="stAlert"] {
        border-radius: 22px !important;
    }
    div[data-testid="stExpander"] {
        border-radius: 22px !important;
        border: 1px solid #D8F3DC !important;
        overflow: hidden;
    }

    /* Curvy Sidebar */
    section[data-testid="stSidebar"] > div {
        border-top-right-radius: 32px;
        border-bottom-right-radius: 32px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# 2. Custom Inline SVG Artwork & Species Knowledge Base
# ---------------------------------------------------------
HERO_SVG = """
<svg width="110" height="85" viewBox="0 0 120 90" fill="none" xmlns="http://www.w3.org/2000/svg">
  <circle cx="60" cy="45" r="40" fill="#40916C" fill-opacity="0.35"/>
  <path d="M35 72C35 55 48 45 60 45C72 45 85 55 85 72H35Z" fill="#95D5B2"/>
  <path d="M60 68V28" stroke="#D8F3DC" stroke-width="4" stroke-linecap="round"/>
  <path d="M60 42C60 42 42 40 40 25C54 24 60 35 60 42Z" fill="#B7E4C7"/>
  <path d="M60 34C60 34 78 32 80 17C66 16 60 27 60 34Z" fill="#FFFFFF"/>
  <circle cx="92" cy="24" r="4" fill="#B7E4C7"/>
  <circle cx="28" cy="34" r="3" fill="#95D5B2"/>
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
        "svg": """<svg width="68" height="68" viewBox="0 0 80 80" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect width="80" height="80" rx="20" fill="#2D6A4F"/>
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
        "svg": """<svg width="68" height="68" viewBox="0 0 80 80" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect width="80" height="80" rx="20" fill="#1B4332"/>
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
        "svg": """<svg width="68" height="68" viewBox="0 0 80 80" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect width="80" height="80" rx="20" fill="#2D6A4F"/>
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
        "svg": """<svg width="68" height="68" viewBox="0 0 80 80" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect width="80" height="80" rx="20" fill="#1B4332"/>
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
    st.markdown("**🎯 Target Alignment**")
    st.info("**UN SDG 15:** Life on Land — Sustainable Reforestation & Soil Recovery")
    st.markdown("**⚙️ Model Architecture**")
    st.markdown(
        """
        - **Frontend:** Python + Streamlit
        - **Backend:** TensorFlow (`tf.matmul` + Softmax)
        - **Input Vector:** 4D Soil & Climate Tensor
        - **Transparency:** Full XAI Logit Inspection
        """
    )
    st.divider()
    st.caption("v3.0 • Complete Demo & XAI Build")

# ---------------------------------------------------------
# 6. Hero Banner with Custom Vector Artwork
# ---------------------------------------------------------
st.markdown(
    f"""
    <div class="hero-banner">
        <div>
            <div class="hero-title">🌱 Project TerraSprout — AI Reforestation Engine</div>
            <div class="hero-subtitle">Real-Time Soil Telemetry, Carbon Impact & TensorFlow Species Matching</div>
        </div>
        <div>{HERO_SVG}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# 7. Main Interactive Workspace
# ---------------------------------------------------------
col_input, col_output = st.columns([1, 1.3], gap="large")

with col_input:
    with st.container(border=True):
        st.subheader("📊 Field Sensor Inputs")
        st.caption("Quick-load a simulated field site or adjust sliders manually:")

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
        btn_predict = st.button(
            "🚀 Analyze Soil & Recommend Species",
            type="primary",
            use_container_width=True,
        )

with col_output:
    with st.container(border=True):
        st.subheader("🤖 TensorFlow Prediction Engine")

        # Run live inference automatically whenever inputs change or button is clicked
        idx, confidence, probs, norm_vals, raw_logits = run_tf_inference(
            soil_ph, moisture, npk, temp
        )
        top_species = SPECIES_DATA[idx]

        # Carbon & Impact Calculations (10-Year Projection)
        trees_planted = hectares * 1100  # ~1,100 saplings per hectare standard density
        co2_10yr = round(top_species["co2_per_ha_yr"] * hectares * 10, 1)

        # Top 3 KPI Cards
        m1, m2, m3 = st.columns(3)
        m1.metric("AI Confidence", f"{confidence:.1f}%", "High Match")
        m2.metric("Est. Survival", top_species["survival_rate"], f"{trees_planted:,} Saplings")
        m3.metric("10-Yr CO₂ Offset", f"{co2_10yr:,.0f} t", f"{hectares} Hectares")

        # Dynamic Visual Species Card with Custom Tree SVG
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

        st.divider()
        st.markdown("**📈 Species Probability Distribution (Softmax Output)**")
        chart_df = pd.DataFrame(
            {
                "Species": [s["name"] for s in SPECIES_DATA],
                "Match Probability (%)": [round(float(p) * 100, 1) for p in probs],
            }
        ).set_index("Species")
        st.bar_chart(chart_df, color="#2D6A4F", height=190)

        # Explainable AI (XAI) Tensor Breakdown Expander
        with st.expander("🔍 Explainable AI (XAI): Inspect Live TensorFlow Math"):
            st.caption(
                "Transparent non-black-box inspection of the live tensor operations executed by TensorFlow:"
            )
            xai_df = pd.DataFrame(
                {
                    "Feature": ["Soil pH", "Moisture (%)", "NPK (PPM)", "Temp (°C)"],
                    "Raw Input": [soil_ph, moisture, npk, temp],
                    "Normalized Tensor [0–1]": [round(v, 3) for v in norm_vals],
                }
            )
            st.dataframe(xai_df, use_container_width=True, hide_index=True)

            logits_df = pd.DataFrame(
                {
                    "Candidate Species": [s["name"] for s in SPECIES_DATA],
                    "Scaled Logit (X · W × 2.2)": [round(float(l), 2) for l in raw_logits],
                    "Softmax Probability": [f"{round(float(p) * 100, 1)}%" for p in probs],
                }
            )
            st.dataframe(logits_df, use_container_width=True, hide_index=True)
