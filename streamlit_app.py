import numpy as np
import pandas as pd
import streamlit as st
import tensorflow as tf

# ---------------------------------------------------------
# 1. Page Configuration & Base Layout
# ---------------------------------------------------------
st.set_page_config(
    page_title="Project TerraSprout | Team Lemon Tea",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------
# 2. Species Knowledge Base & Botanical SVG Artwork
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
        "bg_tint": "#EAF6EE",
        "tree_color_1": "#2D6A4F",
        "tree_color_2": "#52B788",
        "trunk_color": "#1B4332",
        "biome_type": "acacia",  # Wide umbrella savanna/pioneer canopy
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
        "bg_tint": "#E8F4F0",
        "tree_color_1": "#1B4332",
        "tree_color_2": "#40916C",
        "trunk_color": "#123524",
        "biome_type": "hardwood",  # Tall multi-layered rainforest giant
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
        "bg_tint": "#E6F4F5",
        "tree_color_1": "#1D6F72",
        "tree_color_2": "#48CAE4",
        "trunk_color": "#134E52",
        "biome_type": "wetland",  # Weeping riparian branches + water ripples
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
        "bg_tint": "#ECF6EC",
        "tree_color_1": "#23532F",
        "tree_color_2": "#6A994E",
        "trunk_color": "#183A21",
        "biome_type": "climax",  # Dense towering crown with thick organic foliage clusters
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
# 5. Dynamic Botanical Tree SVG Builder (Reacts to TF Output)
# ---------------------------------------------------------
def build_dynamic_forest_svg(species_cfg, confidence, hectares):
    """Generates realistic, organic tree silhouettes tailored to the predicted species."""
    c1 = species_cfg["tree_color_1"]
    c2 = species_cfg["tree_color_2"]
    trunk = species_cfg["trunk_color"]
    biome = species_cfg["biome_type"]

    # Canopy opacity scales subtly with AI confidence (0.08 to 0.15)
    base_opacity = round(0.08 + (confidence / 100.0) * 0.07, 3)

    # Extra grove trees appear when Target Planting Area (Hectares) >= 15
    extra_grove = ""
    if hectares >= 15:
        extra_grove = f"""
        <g class="tree-sway-2" opacity="{base_opacity}">
            <path d="M510 430 C512 370, 514 320, 516 260 L526 260 C528 320, 530 370, 534 430 Z" fill="{trunk}"/>
            <path d="M521 310 Q495 285 478 272" stroke="{trunk}" stroke-width="5" stroke-linecap="round"/>
            <path d="M522 295 Q548 270 568 258" stroke="{trunk}" stroke-width="5" stroke-linecap="round"/>
            <circle cx="521" cy="235" r="46" fill="{c1}"/>
            <circle cx="482" cy="260" r="34" fill="{c2}"/>
            <circle cx="562" cy="255" r="36" fill="{c1}"/>
            <circle cx="521" cy="205" r="32" fill="{c2}"/>
        </g>
        <g class="tree-sway-3" opacity="{base_opacity}">
            <path d="M895 430 C898 365, 900 315, 902 250 L912 250 C914 315, 916 365, 920 430 Z" fill="{trunk}"/>
            <path d="M906 300 Q880 275 862 262" stroke="{trunk}" stroke-width="5" stroke-linecap="round"/>
            <path d="M908 285 Q935 260 952 248" stroke="{trunk}" stroke-width="5" stroke-linecap="round"/>
            <circle cx="907" cy="225" r="48" fill="{c2}"/>
            <circle cx="866" cy="252" r="36" fill="{c1}"/>
            <circle cx="948" cy="248" r="35" fill="{c1}"/>
        </g>
        """

    # Species-specific realistic tree architecture
    if biome == "acacia":
        # Wide, flat-topped umbrella crowns with forked limbs
        hero_trees = f"""
        <!-- Left Acacia Umbrella Tree -->
        <g class="tree-sway-1" opacity="{base_opacity + 0.02}">
            <path d="M115 430 C122 365, 128 310, 132 245 L146 245 C148 310, 155 365, 165 430 Z" fill="{trunk}"/>
            <path d="M136 285 Q95 245 65 225" stroke="{trunk}" stroke-width="7" stroke-linecap="round"/>
            <path d="M142 275 Q185 235 220 218" stroke="{trunk}" stroke-width="7" stroke-linecap="round"/>
            <path d="M139 260 L139 215" stroke="{trunk}" stroke-width="6" stroke-linecap="round"/>
            <ellipse cx="140" cy="205" rx="115" ry="34" fill="{c1}"/>
            <ellipse cx="95" cy="218" rx="68" ry="24" fill="{c2}"/>
            <ellipse cx="188" cy="215" rx="72" ry="25" fill="{c2}"/>
            <ellipse cx="140" cy="188" rx="78" ry="22" fill="{c1}"/>
        </g>
        <!-- Right Acacia Umbrella Tree -->
        <g class="tree-sway-2" opacity="{base_opacity + 0.02}">
            <path d="M1265 430 C1272 360, 1278 300, 1282 230 L1296 230 C1300 300, 1306 360, 1316 430 Z" fill="{trunk}"/>
            <path d="M1286 270 Q1240 230 1205 210" stroke="{trunk}" stroke-width="7" stroke-linecap="round"/>
            <path d="M1292 260 Q1335 220 1370 205" stroke="{trunk}" stroke-width="7" stroke-linecap="round"/>
            <ellipse cx="1288" cy="192" rx="122" ry="36" fill="{c1}"/>
            <ellipse cx="1235" cy="206" rx="72" ry="25" fill="{c2}"/>
            <ellipse cx="1340" cy="204" rx="74" ry="25" fill="{c2}"/>
        </g>
        """
    elif biome == "wetland":
        # Graceful weeping riparian trees + flowing water ripples
        hero_trees = f"""
        <!-- Flowing River Ripple Lines -->
        <path d="M0 395 Q360 375 720 395 T1440 390" stroke="{c2}" stroke-width="3" stroke-opacity="{base_opacity}"/>
        <path d="M0 412 Q360 392 720 412 T1440 408" stroke="{c1}" stroke-width="3" stroke-opacity="{base_opacity}"/>

        <!-- Left Riparian Weeping Tree -->
        <g class="tree-sway-1" opacity="{base_opacity + 0.02}">
            <path d="M118 430 C125 360, 122 295, 134 225 L148 225 C144 295, 152 360, 162 430 Z" fill="{trunk}"/>
            <path d="M138 255 Q95 235 72 265" stroke="{trunk}" stroke-width="6" stroke-linecap="round"/>
            <path d="M144 245 Q185 225 210 258" stroke="{trunk}" stroke-width="6" stroke-linecap="round"/>
            <path d="M55 265 Q65 180 140 175 Q215 180 225 265 Q205 325 195 345 Q185 290 172 275 Q162 335 152 355 Q142 295 130 278 Q118 335 108 350 Q98 290 85 275 Q72 325 55 265 Z" fill="{c1}"/>
            <path d="M78 245 Q90 190 140 186 Q190 190 202 245 Q180 300 170 315 Q155 265 140 265 Q125 265 110 315 Q100 300 78 245 Z" fill="{c2}"/>
        </g>

        <!-- Right Riparian Weeping Tree -->
        <g class="tree-sway-2" opacity="{base_opacity + 0.02}">
            <path d="M1275 430 C1282 355, 1280 285, 1292 215 L1306 215 C1302 285, 1310 355, 1320 430 Z" fill="{trunk}"/>
            <path d="M1210 255 Q1222 165 1298 160 Q1375 165 1388 255 Q1368 320 1358 340 Q1346 280 1332 265 Q1320 330 1310 350 Q1298 285 1285 268 Q1272 330 1262 345 Q1250 280 1236 265 Q1222 320 1210 255 Z" fill="{c1}"/>
            <path d="M1235 235 Q1248 178 1298 174 Q1348 178 1362 235 Q1340 295 1330 310 Q1314 255 1298 255 Q1282 255 1266 310 Q1256 295 1235 235 Z" fill="{c2}"/>
        </g>
        """
    else:
        # Realistic Multi-Branching Hardwood / Climax Broadleaf Trees
        hero_trees = f"""
        <!-- Left Organic Broadleaf Tree with Roots & Branches -->
        <g class="tree-sway-1" opacity="{base_opacity + 0.025}">
            <path d="M108 430 C124 385, 128 325, 132 245 L148 245 C152 325, 156 385, 174 430 Z" fill="{trunk}"/>
            <path d="M135 295 Q102 268 78 248" stroke="{trunk}" stroke-width="8" stroke-linecap="round"/>
            <path d="M145 280 Q178 252 204 235" stroke="{trunk}" stroke-width="8" stroke-linecap="round"/>
            <path d="M140 265 L140 205" stroke="{trunk}" stroke-width="7" stroke-linecap="round"/>
            <!-- Layered Organic Foliage Clusters -->
            <circle cx="140" cy="185" r="64" fill="{c1}"/>
            <circle cx="88" cy="222" r="48" fill="{c1}"/>
            <circle cx="192" cy="220" r="50" fill="{c1}"/>
            <circle cx="115" cy="162" r="44" fill="{c2}"/>
            <circle cx="168" cy="165" r="42" fill="{c2}"/>
            <circle cx="140" cy="212" r="52" fill="{c2}"/>
        </g>

        <!-- Secondary Left Sapling -->
        <g class="tree-sway-3" opacity="{base_opacity}">
            <path d="M275 430 C280 385, 282 340, 284 295 L294 295 C296 340, 298 385, 304 430 Z" fill="{trunk}"/>
            <path d="M288 330 Q268 310 254 298" stroke="{trunk}" stroke-width="5" stroke-linecap="round"/>
            <path d="M290 320 Q312 300 326 290" stroke="{trunk}" stroke-width="5" stroke-linecap="round"/>
            <circle cx="289" cy="268" r="42" fill="{c2}"/>
            <circle cx="258" cy="288" r="30" fill="{c1}"/>
            <circle cx="320" cy="286" r="32" fill="{c1}"/>
        </g>

        <!-- Right Organic Broadleaf Tree with Roots & Branches -->
        <g class="tree-sway-2" opacity="{base_opacity + 0.025}">
            <path d="M1265 430 C1282 380, 1286 315, 1290 230 L1308 230 C1312 315, 1316 380, 1335 430 Z" fill="{trunk}"/>
            <path d="M1294 285 Q1258 255 1230 235" stroke="{trunk}" stroke-width="8" stroke-linecap="round"/>
            <path d="M1304 270 Q1340 242 1368 222" stroke="{trunk}" stroke-width="8" stroke-linecap="round"/>
            <path d="M1299 250 L1299 190" stroke="{trunk}" stroke-width="7" stroke-linecap="round"/>
            <!-- Layered Organic Foliage Clusters -->
            <circle cx="1299" cy="170" r="68" fill="{c1}"/>
            <circle cx="1242" cy="210" r="52" fill="{c1}"/>
            <circle cx="1355" cy="208" r="54" fill="{c1}"/>
            <circle cx="1272" cy="148" r="46" fill="{c2}"/>
            <circle cx="1328" cy="150" r="45" fill="{c2}"/>
            <circle cx="1299" cy="198" r="55" fill="{c2}"/>
        </g>
        """

    return f"""
    <div class="forest-bg">
        <svg viewBox="0 0 1440 430" preserveAspectRatio="xMidYMax slice" fill="none" xmlns="http://www.w3.org/2000/svg">
            <!-- Rolling Forest Terrain Hills -->
            <path d="M0 365 Q360 310 720 355 T1440 340 L1440 430 L0 430 Z" fill="{c1}" fill-opacity="0.055"/>
            <path d="M0 390 Q480 345 960 385 T1440 370 L1440 430 L0 430 Z" fill="{trunk}" fill-opacity="0.065"/>
            {hero_trees}
            {extra_grove}
        </svg>
    </div>
    """


# ---------------------------------------------------------
# 6. Run Live TensorFlow Inference First (So UI & BG React)
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

# Execute TensorFlow inference using live slider states
idx, confidence, probs, norm_vals, raw_logits = run_tf_inference(
    soil_ph, moisture, npk, temp
)
top_species = SPECIES_DATA[idx]

# Sway speed reacts dynamically to Ambient Temperature (warmer breeze = faster sway)
sway_duration = max(3.5, round(11.0 - (temp - 15.0) * 0.22, 1))

# ---------------------------------------------------------
# 7. Inject Dynamic Theme CSS & Reactive Tree Background
# ---------------------------------------------------------
st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }}
    .stApp {{
        background: radial-gradient(circle at top right, {top_species['bg_tint']} 0%, #F4F9F6 50%, #EAF5EE 100%);
        transition: background 0.6s ease;
    }}
    header[data-testid="stHeader"] {{
        background: transparent !important;
    }}
    .main .block-container {{
        position: relative;
        z-index: 2;
    }}

    /* Reactive Faded Background Forest Layer */
    .forest-bg {{
        position: fixed;
        bottom: -8px;
        left: 0;
        width: 100vw;
        height: 430px;
        pointer-events: none;
        z-index: 0;
        overflow: hidden;
    }}
    .forest-bg svg {{
        width: 100%;
        height: 100%;
    }}
    @keyframes swayTreeA {{
        0%, 100% {{ transform: rotate(-1.8deg) translateX(0px); }}
        50% {{ transform: rotate(1.8deg) translateX(4px); }}
    }}
    @keyframes swayTreeB {{
        0%, 100% {{ transform: rotate(2.0deg) translateX(0px); }}
        50% {{ transform: rotate(-2.0deg) translateX(-4px); }}
    }}
    .tree-sway-1 {{
        transform-box: fill-box;
        transform-origin: bottom center;
        animation: swayTreeA {sway_duration}s ease-in-out infinite;
    }}
    .tree-sway-2 {{
        transform-box: fill-box;
        transform-origin: bottom center;
        animation: swayTreeB {round(sway_duration * 0.85, 1)}s ease-in-out infinite;
    }}
    .tree-sway-3 {{
        transform-box: fill-box;
        transform-origin: bottom center;
        animation: swayTreeA {round(sway_duration * 1.15, 1)}s ease-in-out infinite;
    }}

    /* Curvy Hero Banner */
    .hero-banner {{
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
    }}
    .hero-badge {{
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
    }}
    .hero-title {{
        font-size: 2.1rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.6px;
        line-height: 1.15;
    }}
    .hero-subtitle {{
        font-size: 1rem;
        color: #D8F3DC;
        margin-top: 0.4rem;
        font-weight: 400;
    }}

    /* Frosted Curvy Main Panels */
    div[data-testid="stVerticalBlockBorderWrapper"] {{
        border-radius: 30px !important;
        border: 1px solid #CBEAD6 !important;
        background-color: rgba(255, 255, 255, 0.85) !important;
        backdrop-filter: blur(10px);
        padding: 0.85rem !important;
        box-shadow: 0 10px 28px rgba(27, 67, 50, 0.06) !important;
    }}

    /* Curvy KPI Metric Cards */
    div[data-testid="stMetric"] {{
        background: linear-gradient(180deg, rgba(255,255,255,0.95) 0%, rgba(242,249,245,0.95) 100%);
        border: 1px solid #CBEAD6;
        padding: 16px 20px;
        border-radius: 24px !important;
        box-shadow: 0 4px 14px rgba(45, 106, 79, 0.06);
        transition: transform 0.2s ease;
    }}
    div[data-testid="stMetric"]:hover {{
        transform: translateY(-2px);
    }}

    /* Species Visual Showcase Card */
    .species-card {{
        background: linear-gradient(135deg, #E9F5EE 0%, #D8F3DC 100%);
        border: 1.5px solid #95D5B2;
        border-radius: 26px;
        padding: 1.35rem 1.6rem;
        display: flex;
        align-items: center;
        gap: 1.3rem;
        margin: 0.9rem 0 1rem 0;
        box-shadow: 0 6px 18px rgba(45, 106, 79, 0.08);
    }}
    .species-card h4 {{
        margin: 0 0 0.25rem 0;
        color: #123524;
        font-size: 1.35rem;
        font-weight: 800;
    }}
    .species-card p {{
        margin: 0.15rem 0;
        color: #1B4332;
        font-size: 0.93rem;
    }}

    /* Pill-Shaped Primary & Preset Buttons */
    .stButton > button {{
        border-radius: 999px !important;
        font-weight: 700 !important;
        transition: all 0.25s ease !important;
    }}
    button[kind="primary"] {{
        background: linear-gradient(90deg, #1B4332 0%, #2D6A4F 50%, #40916C 100%) !important;
        color: white !important;
        border: none !important;
        padding: 0.8rem 1.6rem !important;
        box-shadow: 0 6px 18px rgba(45, 106, 79, 0.25) !important;
    }}
    button[kind="primary"]:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 22px rgba(45, 106, 79, 0.35) !important;
    }}
    button[kind="secondary"] {{
        background-color: #EDF6F0 !important;
        color: #1B4332 !important;
        border: 1px solid #95D5B2 !important;
        font-size: 0.82rem !important;
        padding: 0.45rem 0.6rem !important;
    }}
    button[kind="secondary"]:hover {{
        background-color: #D8F3DC !important;
        border-color: #2D6A4F !important;
        transform: translateY(-1px);
    }}

    /* Custom Slider Accent Color */
    div[data-baseweb="slider"] div[role="slider"] {{
        background-color: #2D6A4F !important;
        border: 2px solid #FFFFFF !important;
        box-shadow: 0 2px 6px rgba(0,0,0,0.2) !important;
    }}

    /* Curvy Tabs, Inputs & Alerts */
    button[data-baseweb="tab"] {{
        border-radius: 999px !important;
        padding: 0.45rem 1.1rem !important;
        font-weight: 600 !important;
    }}
    div[data-baseweb="input"], div[data-baseweb="base-input"] {{
        border-radius: 20px !important;
    }}
    div[data-testid="stAlert"] {{
        border-radius: 22px !important;
    }}

    /* Curvy Sidebar */
    section[data-testid="stSidebar"] > div {{
        background-color: rgba(255, 255, 255, 0.96);
        border-top-right-radius: 34px;
        border-bottom-right-radius: 34px;
        border-right: 1px solid #CBEAD6;
        z-index: 3;
    }}
    </style>
    {build_dynamic_forest_svg(top_species, confidence, hectares)}
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# 8. Sidebar & Hero Banner Render
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
        - **Visual Sync:** Biome-Reactive Forest SVG
        """
    )
    st.divider()
    st.caption(f"🟢 Active Biome: **{top_species['name']}**")

st.markdown(
    f"""
    <div class="hero-banner">
        <div>
            <div class="hero-badge">● Live TensorFlow Inference • Active Biome: {top_species['name']}</div>
            <div class="hero-title">🌱 Project TerraSprout</div>
            <div class="hero-subtitle">Intelligent Soil Telemetry, Carbon Modeling & Native Reforestation Matchmaker</div>
        </div>
        <div>{HERO_SVG}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# 9. Output Panel Render
# ---------------------------------------------------------
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
            m2.metric("Est. Survival", top_species["survival_rate"], f"{trees_planted:,} Trees")
            m3.metric("10-Yr CO₂ Offset", f"{co2_10yr:,.0f} t", f"{hectares} Hectares")

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
