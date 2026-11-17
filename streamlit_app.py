import numpy as np
import pandas as pd
import streamlit as st
import tensorflow as tf

# ---------------------------------------------------------
# 1. Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Project TerraSprout | Team Lemon Tea",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ---------------------------------------------------------
# 2. Shared Botanical SVG Generators (100% Unified Icon & BG)
# ---------------------------------------------------------
def get_species_botanical_art(
    biome_type,
    trunk_color="#1B4332",
    c1="#2D6A4F",
    c2="#52B788",
    c3="#95D5B2",
    opacity=1.0,
):
    """Returns a 140x160 botanical tree SVG group shared by both the card icon and background."""
    if biome_type == "acacia":
        return (
            f'<g opacity="{opacity}">'
            f'<path d="M58 148 C63 118, 65 95, 66 72 L74 72 C75 95, 77 118, 82 148 Z" fill="{trunk_color}"/>'
            f'<path d="M68 92 Q48 76 34 68" stroke="{trunk_color}" stroke-width="4" stroke-linecap="round" fill="none"/>'
            f'<path d="M72 88 Q92 72 106 66" stroke="{trunk_color}" stroke-width="4" stroke-linecap="round" fill="none"/>'
            f'<ellipse cx="70" cy="60" rx="54" ry="16" fill="{c1}"/>'
            f'<ellipse cx="46" cy="66" rx="32" ry="12" fill="{c2}"/>'
            f'<ellipse cx="94" cy="65" rx="34" ry="12" fill="{c2}"/>'
            f'<ellipse cx="70" cy="50" rx="38" ry="11" fill="{c3}"/>'
            f'</g>'
        )
    elif biome_type == "wetland":
        return (
            f'<g opacity="{opacity}">'
            f'<path d="M16 148 Q70 140 124 148" stroke="#48CAE4" stroke-width="3" stroke-linecap="round" fill="none"/>'
            f'<path d="M28 154 Q70 148 112 154" stroke="{c3}" stroke-width="2" stroke-linecap="round" fill="none"/>'
            f'<path d="M54 144 C62 134, 64 112, 65 44 L75 44 C76 112, 78 134, 86 144 L74 144 L70 132 L66 144 Z" fill="{trunk_color}"/>'
            f'<path d="M68 88 Q46 84 32 98" stroke="{trunk_color}" stroke-width="3.5" stroke-linecap="round" fill="none"/>'
            f'<path d="M72 88 Q94 84 108 98" stroke="{trunk_color}" stroke-width="3.5" stroke-linecap="round" fill="none"/>'
            f'<path d="M22 104 C26 78, 48 72, 70 72 C92 72, 114 78, 118 104 C112 112, 104 108, 98 100 C90 106, 80 104, 70 98 C60 104, 50 106, 42 100 C36 108, 28 112, 22 104 Z" fill="{c1}"/>'
            f'<path d="M30 80 C34 54, 52 46, 70 46 C88 46, 106 54, 110 80 C104 86, 96 82, 90 76 C82 82, 76 80, 70 75 C64 80, 58 82, 50 76 C44 82, 36 86, 30 80 Z" fill="{c2}"/>'
            f'<path d="M42 54 C46 30, 58 20, 70 18 C82 20, 94 30, 98 54 C92 60, 84 56, 78 50 C74 54, 66 54, 62 50 C56 56, 48 60, 42 54 Z" fill="{c3}"/>'
            f'</g>'
        )
    elif biome_type == "climax":
        return (
            f'<g opacity="{opacity}">'
            f'<path d="M56 148 C62 122, 64 96, 65 66 L75 66 C76 96, 78 122, 84 148 Z" fill="{trunk_color}"/>'
            f'<circle cx="70" cy="46" r="28" fill="{c1}"/>'
            f'<circle cx="44" cy="64" r="22" fill="{c1}"/>'
            f'<circle cx="96" cy="64" r="22" fill="{c1}"/>'
            f'<circle cx="56" cy="36" r="20" fill="{c2}"/>'
            f'<circle cx="84" cy="36" r="20" fill="{c2}"/>'
            f'<circle cx="70" cy="58" r="24" fill="{c3}"/>'
            f'</g>'
        )
    else:
        return (
            f'<g opacity="{opacity}">'
            f'<path d="M56 148 C62 122, 64 98, 65 70 L75 70 C76 98, 78 122, 84 148 Z" fill="{trunk_color}"/>'
            f'<path d="M68 92 Q50 78 38 70" stroke="{trunk_color}" stroke-width="4" stroke-linecap="round" fill="none"/>'
            f'<path d="M72 86 Q90 74 102 66" stroke="{trunk_color}" stroke-width="4" stroke-linecap="round" fill="none"/>'
            f'<circle cx="70" cy="52" r="26" fill="{c1}"/>'
            f'<circle cx="46" cy="68" r="20" fill="{c2}"/>'
            f'<circle cx="94" cy="66" r="21" fill="{c2}"/>'
            f'<circle cx="70" cy="38" r="19" fill="{c3}"/>'
            f'</g>'
        )


def build_card_icon_svg(biome_type, bg_fill):
    """Creates a 74x74 rounded card badge using the exact same botanical tree art."""
    art = get_species_botanical_art(
        biome_type=biome_type,
        trunk_color="#D8F3DC",
        c1="#40916C",
        c2="#74C69D",
        c3="#B7E4C7",
        opacity=1.0,
    )
    return (
        f'<svg width="74" height="74" viewBox="0 0 140 160" fill="none" xmlns="http://www.w3.org/2000/svg">'
        f'<rect x="4" y="4" width="132" height="152" rx="34" fill="{bg_fill}"/>'
        f'{art}</svg>'
    )


# ---------------------------------------------------------
# 3. Species Knowledge Base
# ---------------------------------------------------------
HERO_SVG = """<svg width="118" height="90" viewBox="0 0 120 90" fill="none" xmlns="http://www.w3.org/2000/svg"><circle cx="60" cy="45" r="42" fill="#40916C" fill-opacity="0.32"/><circle cx="60" cy="45" r="32" stroke="#95D5B2" stroke-opacity="0.45" stroke-dasharray="4 4"/><path d="M35 72C35 55 48 45 60 45C72 45 85 55 85 72H35Z" fill="#95D5B2"/><path d="M60 68V28" stroke="#D8F3DC" stroke-width="4" stroke-linecap="round"/><path d="M60 42C60 42 42 40 40 25C54 24 60 35 60 42Z" fill="#B7E4C7"/><path d="M60 34C60 34 78 32 80 17C66 16 60 27 60 34Z" fill="#FFFFFF"/><circle cx="94" cy="22" r="4" fill="#B7E4C7"/><circle cx="26" cy="34" r="3" fill="#95D5B2"/></svg>"""

SPECIES_DATA = [
    {
        "name": "Acacia mangium",
        "tag": "Fast-Growing Pioneer",
        "soil_pref": "Acidic to neutral soils (pH 4.5–6.5)",
        "benefit": "Rapid canopy closure & nitrogen fixation for degraded land.",
        "survival_rate": "94%",
        "co2_per_ha_yr": 18.5,
        "bg_tint": "#E4F5E9",
        "tree_color_1": "#2D6A4F",
        "tree_color_2": "#40916C",
        "tree_color_3": "#74C69D",
        "trunk_color": "#1B4332",
        "biome_type": "acacia",
        "svg": build_card_icon_svg("acacia", "#2D6A4F"),
    },
    {
        "name": "Dipterocarpus",
        "tag": "Tropical Hardwood",
        "soil_pref": "Well-drained loamy forest soils",
        "benefit": "High long-term carbon sequestration & structural biodiversity.",
        "survival_rate": "89%",
        "co2_per_ha_yr": 22.0,
        "bg_tint": "#E2F3ED",
        "tree_color_1": "#1B4332",
        "tree_color_2": "#2D6A4F",
        "tree_color_3": "#52B788",
        "trunk_color": "#123524",
        "biome_type": "hardwood",
        "svg": build_card_icon_svg("hardwood", "#1B4332"),
    },
    {
        "name": "Hopea odorata",
        "tag": "Riparian / Wetland Specialist",
        "soil_pref": "High moisture & alluvial clay soils",
        "benefit": "Prevents riverbank erosion and thrives in flood-prone zones.",
        "survival_rate": "96%",
        "co2_per_ha_yr": 19.8,
        "bg_tint": "#E0F2F4",
        "tree_color_1": "#164E52",
        "tree_color_2": "#1D6F72",
        "tree_color_3": "#2A9D8F",
        "trunk_color": "#0F383B",
        "biome_type": "wetland",
        "svg": build_card_icon_svg("wetland", "#164E52"),
    },
    {
        "name": "Shorea robusta",
        "tag": "High-Canopy Climax Species",
        "soil_pref": "Nutrient-rich deep soils (High NPK)",
        "benefit": "Supports multi-tier forest ecosystems and wildlife habitats.",
        "survival_rate": "91%",
        "co2_per_ha_yr": 24.2,
        "bg_tint": "#E6F5E6",
        "tree_color_1": "#23532F",
        "tree_color_2": "#386641",
        "tree_color_3": "#6A994E",
        "trunk_color": "#183A21",
        "biome_type": "climax",
        "svg": build_card_icon_svg("climax", "#1B4332"),
    },
]

# ---------------------------------------------------------
# 4. Session State Initialization
# ---------------------------------------------------------
if "ph" not in st.session_state:
    st.session_state.ph = 6.5
if "moisture" not in st.session_state:
    st.session_state.moisture = 45
if "npk" not in st.session_state:
    st.session_state.npk = 150
if "temp" not in st.session_state:
    st.session_state.temp = 28.5
if "hectares" not in st.session_state:
    st.session_state.hectares = 10


def set_preset(ph, moisture, npk, temp):
    st.session_state.ph = ph
    st.session_state.moisture = moisture
    st.session_state.npk = npk
    st.session_state.temp = temp


# ---------------------------------------------------------
# 5. Pre-Compiled TensorFlow Graph (< 1ms Inference)
# ---------------------------------------------------------
TF_WEIGHTS = tf.constant(
    [
        [4.5, -1.5, -2.5, 0.5],
        [-1.5, -2.0, 5.5, 0.0],
        [1.0, 0.5, -0.5, 5.0],
        [0.2, 3.8, 0.1, -0.5],
    ],
    dtype=tf.float32,
)


@tf.function(reduce_retracing=True)
def _tf_forward_pass(input_tensor):
    logits = tf.matmul(input_tensor, TF_WEIGHTS) * 2.2
    probs = tf.nn.softmax(logits)
    return logits, probs


def run_tf_inference(ph, moisture, npk, temp):
    norm_ph = (ph - 4.0) / 5.0
    norm_moisture = moisture / 100.0
    norm_npk = (npk - 10) / 290.0
    norm_temp = (temp - 15.0) / 30.0

    norm_values = [norm_ph, norm_moisture, norm_npk, norm_temp]
    input_tensor = tf.constant([norm_values], dtype=tf.float32)

    logits_tensor, probs_tensor = _tf_forward_pass(input_tensor)
    probabilities = probs_tensor.numpy()[0]
    raw_logits = logits_tensor.numpy()[0]

    predicted_idx = int(np.argmax(probabilities))
    confidence = float(probabilities[predicted_idx] * 100)

    return predicted_idx, confidence, probabilities, norm_values, raw_logits


# ---------------------------------------------------------
# 6. Static CSS (Injected Once — Zero Re-Parse Lag)
# ---------------------------------------------------------
STATIC_CSS = """<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}
header[data-testid="stHeader"] {
    background: transparent !important;
}
.main .block-container {
    position: relative;
    z-index: 2;
}
.forest-bg {
    position: fixed;
    bottom: 0px;
    left: 0px;
    width: 100vw;
    height: 450px;
    pointer-events: none;
    z-index: 1;
    overflow: hidden;
}
.forest-bg svg {
    width: 100%;
    height: 100%;
}
@keyframes swayTreeA {
    0%, 100% { transform: rotate(-2.4deg); }
    50% { transform: rotate(2.4deg); }
}
@keyframes swayTreeB {
    0%, 100% { transform: rotate(2.6deg); }
    50% { transform: rotate(-2.6deg); }
}
.hero-banner {
    background: linear-gradient(135deg, #123524 0%, #1B4332 50%, #2D6A4F 100%);
    padding: 1.8rem 2.5rem;
    border-radius: 34px;
    color: white;
    margin-bottom: 1.5rem;
    box-shadow: 0 12px 30px rgba(27, 67, 50, 0.22);
    border: 1px solid rgba(183, 228, 199, 0.25);
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1.5rem;
    position: relative;
    z-index: 3;
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
    margin-bottom: 0.6rem;
}
.hero-title {
    font-size: 2.1rem;
    font-weight: 800;
    margin: 0;
    letter-spacing: -0.6px;
    line-height: 1.15;
}
.hero-subtitle {
    font-size: 1rem;
    color: #D8F3DC;
    margin-top: 0.4rem;
    font-weight: 400;
}
div[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 30px !important;
    border: 1px solid #CBEAD6 !important;
    background-color: rgba(255, 255, 255, 0.82) !important;
    backdrop-filter: blur(8px);
    padding: 0.85rem !important;
    box-shadow: 0 10px 28px rgba(27, 67, 50, 0.06) !important;
    position: relative;
    z-index: 3;
}
div[data-testid="stMetric"] {
    background: linear-gradient(180deg, rgba(255,255,255,0.95) 0%, rgba(242,249,245,0.95) 100%);
    border: 1px solid #CBEAD6;
    padding: 16px 20px;
    border-radius: 24px !important;
    box-shadow: 0 4px 14px rgba(45, 106, 79, 0.06);
}
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
.prob-list {
    display: flex;
    flex-direction: column;
    gap: 0.65rem;
    margin-top: 0.5rem;
}
.prob-row {
    background: rgba(255, 255, 255, 0.85);
    border: 1px solid #D8F3DC;
    border-radius: 16px;
    padding: 0.55rem 0.9rem;
}
.prob-header {
    display: flex;
    justify-content: space-between;
    font-size: 0.88rem;
    font-weight: 700;
    color: #1B4332;
    margin-bottom: 0.32rem;
}
.prob-track {
    width: 100%;
    height: 10px;
    background: #E6F4EA;
    border-radius: 999px;
    overflow: hidden;
}
.prob-fill {
    height: 100%;
    border-radius: 999px;
    transition: width 0.25s ease, background-color 0.25s ease;
}
.stButton > button {
    border-radius: 999px !important;
    font-weight: 700 !important;
    transition: all 0.2s ease !important;
}
button[kind="primary"] {
    background: linear-gradient(90deg, #1B4332 0%, #2D6A4F 50%, #40916C 100%) !important;
    color: white !important;
    border: none !important;
    padding: 0.8rem 1.6rem !important;
}
button[kind="secondary"] {
    background-color: #EDF6F0 !important;
    color: #1B4332 !important;
    border: 1px solid #95D5B2 !important;
    font-size: 0.82rem !important;
}
div[data-baseweb="slider"] div[role="slider"] {
    background-color: #2D6A4F !important;
    border: 2px solid #FFFFFF !important;
}
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
section[data-testid="stSidebar"] > div {
    background-color: rgba(255, 255, 255, 0.96);
    border-top-right-radius: 34px;
    border-bottom-right-radius: 34px;
    border-right: 1px solid #CBEAD6;
    z-index: 4;
}
</style>"""

st.markdown(STATIC_CSS, unsafe_allow_html=True)

# ---------------------------------------------------------
# 7. Run Instant TensorFlow Inference & Build Synced Layer
# ---------------------------------------------------------
idx, confidence, probs, norm_vals, raw_logits = run_tf_inference(
    st.session_state.ph,
    st.session_state.moisture,
    st.session_state.npk,
    st.session_state.temp,
)
top_species = SPECIES_DATA[idx]
sway_duration = max(3.0, round(10.5 - (st.session_state.temp - 15.0) * 0.22, 1))


def build_dynamic_forest_html(species_cfg, confidence_val, hectares_val, sway_sec):
    c1 = species_cfg["tree_color_1"]
    c2 = species_cfg["tree_color_2"]
    c3 = species_cfg["tree_color_3"]
    trunk = species_cfg["trunk_color"]
    biome = species_cfg["biome_type"]

    op = round(0.20 + (confidence_val / 100.0) * 0.10, 2)

    tree_art = get_species_botanical_art(
        biome_type=biome,
        trunk_color=trunk,
        c1=c1,
        c2=c2,
        c3=c3,
        opacity=op,
    )

    trees_svg = (
        f'<g transform="translate(18, 120) scale(1.95)"><g style="transform-box:fill-box;transform-origin:70px 148px;animation:swayTreeA {sway_sec}s ease-in-out infinite;">{tree_art}</g></g>'
        f'<g transform="translate(245, 210) scale(1.38)"><g style="transform-box:fill-box;transform-origin:70px 148px;animation:swayTreeA {round(sway_sec * 1.15, 1)}s ease-in-out infinite;">{tree_art}</g></g>'
        f'<g transform="translate(1140, 110) scale(2.02)"><g style="transform-box:fill-box;transform-origin:70px 148px;animation:swayTreeB {round(sway_sec * 0.85, 1)}s ease-in-out infinite;">{tree_art}</g></g>'
    )

    if hectares_val >= 15:
        trees_svg += (
            f'<g transform="translate(460, 225) scale(1.28)"><g style="transform-box:fill-box;transform-origin:70px 148px;animation:swayTreeB {round(sway_sec * 0.9, 1)}s ease-in-out infinite;">{tree_art}</g></g>'
            f'<g transform="translate(860, 215) scale(1.34)"><g style="transform-box:fill-box;transform-origin:70px 148px;animation:swayTreeA {round(sway_sec * 1.1, 1)}s ease-in-out infinite;">{tree_art}</g></g>'
        )

    return (
        f'<style>.stApp{{background:radial-gradient(circle at top right,{species_cfg["bg_tint"]} 0%,#F4F9F6 55%,#EAF5EE 100%)!important;}}</style>'
        f'<div class="forest-bg">'
        f'<svg viewBox="0 0 1440 440" preserveAspectRatio="xMidYMax slice" fill="none" xmlns="http://www.w3.org/2000/svg">'
        f'<path d="M0 385 Q360 335 720 378 T1440 362 L1440 440 L0 440 Z" fill="{c1}" fill-opacity="{round(op * 0.45, 3)}"/>'
        f'<path d="M0 408 Q480 365 960 402 T1440 388 L1440 440 L0 440 Z" fill="{trunk}" fill-opacity="{round(op * 0.55, 3)}"/>'
        f'{trees_svg}'
        f'</svg></div>'
    )


# Render Background & Hero Banner in the same immediate flush
st.markdown(
    build_dynamic_forest_html(
        top_species, confidence, st.session_state.hectares, sway_duration
    ),
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("### 🍃 Team Lemon Tea")
    st.caption("2026 Han Chiang High School AI Vanguard Challenge")
    st.divider()
    st.markdown("**🎯 UN SDG Alignment**")
    st.success(
        "**SDG 15: Life on Land**\n\nAI-guided native species matching to maximize sapling survival and carbon capture."
    )
    st.markdown("**⚙️ System Stack**")
    st.markdown(
        """
        - **Frontend:** Streamlit
        - **AI Engine:** TensorFlow
        """
    )
    )
    st.divider()
    st.caption(f"🟢 Active Biome: **{top_species['name']}**")

st.markdown(
    f'<div class="hero-banner"><div><div class="hero-badge">● Live TensorFlow Inference • Active Biome: {top_species["name"]}</div><div class="hero-title">🌱 Project TerraSprout</div><div class="hero-subtitle">Intelligent Soil Telemetry, Carbon Modeling & Native Reforestation Matchmaker</div></div><div>{HERO_SVG}</div></div>',
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# 8. Main Interactive Columns (Synced Single-Frame Output)
# ---------------------------------------------------------
col_input, col_output = st.columns([1, 1.32], gap="large")

with col_input:
    with st.container(border=True):
        st.subheader("📊 Field Sensor Inputs")
        st.caption("Select a field preset or fine-tune IoT probe readings:")

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
        temp = st.number_input(
            "🌡️ Ambient Temperature (°C)", 15.0, 45.0, key="temp", step=0.5
        )

        st.divider()
        st.markdown("**🌍 Reforestation Plot Scale**")
        hectares = st.slider("Target Planting Area (Hectares)", 1, 50, key="hectares")

        st.write("")
        st.button(
            "🚀 Run TensorFlow Analysis",
            type="primary",
            use_container_width=True,
        )

with col_output:
    with st.container(border=True):
        trees_planted = hectares * 1100
        co2_10yr = round(top_species["co2_per_ha_yr"] * hectares * 10, 1)

        tab_overview, tab_xai = st.tabs(
            ["🌿 Species & Ecological Impact", "🔍 Explainable AI (Tensor Math)"]
        )

        with tab_overview:
            st.write("")
            m1, m2, m3 = st.columns(3)
            m1.metric("AI Confidence", f"{confidence:.1f}%", "Optimal Match")
            m2.metric(
                "Est. Survival",
                top_species["survival_rate"],
                f"{trees_planted:,} Trees",
            )
            m3.metric(
                "10-Yr CO₂ Offset", f"{co2_10yr:,.0f} t", f"{hectares} Hectares"
            )

            # Build instant GPU-accelerated probability bars synced with the background trees
            prob_bars_html = '<div class="prob-list">'
            for i, s in enumerate(SPECIES_DATA):
                pct = round(float(probs[i]) * 100, 1)
                bar_color = top_species["tree_color_1"] if i == idx else "#95D5B2"
                badge = " ★ Best Match" if i == idx else ""
                prob_bars_html += (
                    f'<div class="prob-row">'
                    f'<div class="prob-header"><span>{s["name"]}{badge}</span><span>{pct}%</span></div>'
                    f'<div class="prob-track"><div class="prob-fill" style="width:{pct}%;background-color:{bar_color};"></div></div>'
                    f'</div>'
                )
            prob_bars_html += "</div>"

            # Render Species Card + Ecological Impact + Probability Bars in ONE single DOM update
            st.markdown(
                f'<div class="species-card"><div>{top_species["svg"]}</div><div><h4>{top_species["name"]}</h4><p><strong>Classification:</strong> {top_species["tag"]}</p><p><strong>Ideal Soil:</strong> {top_species["soil_pref"]}</p></div></div>'
                f'<p style="margin:0.4rem 0 0.8rem 0;color:#1B4332;"><strong>🌍 Ecological Impact:</strong> {top_species["benefit"]}</p>'
                f'<p style="margin:0 0 0.35rem 0;font-weight:700;color:#123524;">📈 Species Probability Distribution (Softmax Output)</p>'
                f'{prob_bars_html}',
                unsafe_allow_html=True,
            )

        with tab_xai:
            st.write("")
            st.info(
                "**Transparent AI Architecture:** Every recommendation is computed live via pre-compiled tensor dot-products (`@tf.function` + `tf.matmul`) and calibrated Softmax."
            )
            st.markdown("**1. Normalized 4D Sensor Input Tensor `[0.0 – 1.0]`**")
            xai_df = pd.DataFrame(
                {
                    "Sensor Feature": [
                        "Soil pH",
                        "Soil Moisture (%)",
                        "NPK Index (PPM)",
                        "Temperature (°C)",
                    ],
                    "Raw Field Reading": [soil_ph, moisture, npk, temp],
                    "Normalized Tensor Value": [round(v, 3) for v in norm_vals],
                }
            )
            st.dataframe(xai_df, use_container_width=True, hide_index=True)

            st.markdown("**2. Layer Logits & Softmax Probability Calibration**")
            logits_df = pd.DataFrame(
                {
                    "Candidate Tree Species": [
                        s["name"] for s in SPECIES_DATA
                    ],
                    "Scaled Logit (X · W × 2.2)": [
                        round(float(l), 2) for l in raw_logits
                    ],
                    "Final Softmax Confidence": [
                        f"{round(float(p) * 100, 1)}%" for p in probs
                    ],
                }
            )
            st.dataframe(logits_df, use_container_width=True, hide_index=True)
