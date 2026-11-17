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
# 2. Shared Botanical SVG Helper for Hopea odorata
# ---------------------------------------------------------
def get_hopea_svg_art(
    trunk_color="#134E52",
    foliage_dark="#1D6F72",
    foliage_mid="#2A9D8F",
    foliage_light="#74C69D",
    water_color="#48CAE4",
    opacity=1.0,
):
    """Returns authentic Hopea odorata SVG elements (buttress roots, straight bole, layered conical-drooping crown)."""
    return (
        f'<g opacity="{opacity}">'
        # Riparian water ripples at base
        f'<path d="M16 146 Q70 138 124 146" stroke="{water_color}" stroke-width="3" stroke-linecap="round" fill="none"/>'
        f'<path d="M28 153 Q70 147 112 153" stroke="{foliage_light}" stroke-width="2" stroke-linecap="round" fill="none"/>'
        # Straight dipterocarp trunk with flared buttress roots
        f'<path d="M54 142 C62 132, 64 112, 65 44 L75 44 C76 112, 78 132, 86 142 L74 142 L70 130 L66 142 Z" fill="{trunk_color}"/>'
        # Upper ascending & outer drooping limbs
        f'<path d="M68 88 Q46 84 32 98" stroke="{trunk_color}" stroke-width="3.5" stroke-linecap="round" fill="none"/>'
        f'<path d="M72 88 Q94 84 108 98" stroke="{trunk_color}" stroke-width="3.5" stroke-linecap="round" fill="none"/>'
        f'<path d="M68 64 Q50 60 40 72" stroke="{trunk_color}" stroke-width="3" stroke-linecap="round" fill="none"/>'
        f'<path d="M72 64 Q90 60 100 72" stroke="{trunk_color}" stroke-width="3" stroke-linecap="round" fill="none"/>'
        # Tier 1 (Lower wide skirt with drooping branch tips)
        f'<path d="M22 104 C26 78, 48 72, 70 72 C92 72, 114 78, 118 104 C112 112, 104 108, 98 100 C90 106, 80 104, 70 98 C60 104, 50 106, 42 100 C36 108, 28 112, 22 104 Z" fill="{foliage_dark}"/>'
        # Tier 2 (Middle conical-layered foliage)
        f'<path d="M30 80 C34 54, 52 46, 70 46 C88 46, 106 54, 110 80 C104 86, 96 82, 90 76 C82 82, 76 80, 70 75 C64 80, 58 82, 50 76 C44 82, 36 86, 30 80 Z" fill="{foliage_mid}"/>'
        # Tier 3 (Upper emergent crown)
        f'<path d="M42 54 C46 30, 58 20, 70 18 C82 20, 94 30, 98 54 C92 60, 84 56, 78 50 C74 54, 66 54, 62 50 C56 56, 48 60, 42 54 Z" fill="{foliage_light}"/>'
        f'</g>'
    )


# ---------------------------------------------------------
# 3. Species Knowledge Base & Botanical SVG Artwork
# ---------------------------------------------------------
HERO_SVG = """<svg width="118" height="90" viewBox="0 0 120 90" fill="none" xmlns="http://www.w3.org/2000/svg"><circle cx="60" cy="45" r="42" fill="#40916C" fill-opacity="0.32"/><circle cx="60" cy="45" r="32" stroke="#95D5B2" stroke-opacity="0.45" stroke-dasharray="4 4"/><path d="M35 72C35 55 48 45 60 45C72 45 85 55 85 72H35Z" fill="#95D5B2"/><path d="M60 68V28" stroke="#D8F3DC" stroke-width="4" stroke-linecap="round"/><path d="M60 42C60 42 42 40 40 25C54 24 60 35 60 42Z" fill="#B7E4C7"/><path d="M60 34C60 34 78 32 80 17C66 16 60 27 60 34Z" fill="#FFFFFF"/><circle cx="94" cy="22" r="4" fill="#B7E4C7"/><circle cx="26" cy="34" r="3" fill="#95D5B2"/></svg>"""

# Matching Hopea odorata Card Icon using the exact same botanical tree function
HOPEA_ICON_SVG = (
    '<svg width="74" height="74" viewBox="0 0 140 160" fill="none" xmlns="http://www.w3.org/2000/svg">'
    '<rect x="4" y="4" width="132" height="152" rx="34" fill="#164E52"/>'
    + get_hopea_svg_art(
        trunk_color="#D8F3DC",
        foliage_dark="#40916C",
        foliage_mid="#74C69D",
        foliage_light="#B7E4C7",
        water_color="#90E0EF",
        opacity=1.0,
    )
    + "</svg>"
)

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
        "tree_color_2": "#52B788",
        "trunk_color": "#1B4332",
        "biome_type": "acacia",
        "svg": """<svg width="74" height="74" viewBox="0 0 80 80" fill="none" xmlns="http://www.w3.org/2000/svg"><rect width="80" height="80" rx="22" fill="#2D6A4F"/><path d="M40 64V34" stroke="#D8F3DC" stroke-width="4" stroke-linecap="round"/><ellipse cx="40" cy="28" rx="22" ry="11" fill="#74C69D"/><ellipse cx="40" cy="22" rx="14" ry="8" fill="#B7E4C7"/></svg>""",
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
        "tree_color_2": "#40916C",
        "trunk_color": "#123524",
        "biome_type": "hardwood",
        "svg": """<svg width="74" height="74" viewBox="0 0 80 80" fill="none" xmlns="http://www.w3.org/2000/svg"><rect width="80" height="80" rx="22" fill="#1B4332"/><path d="M40 65V30" stroke="#95D5B2" stroke-width="5" stroke-linecap="round"/><circle cx="40" cy="26" r="15" fill="#52B788"/><circle cx="29" cy="33" r="10" fill="#74C69D"/><circle cx="51" cy="33" r="10" fill="#74C69D"/></svg>""",
    },
    {
        "name": "Hopea odorata",
        "tag": "Riparian / Wetland Specialist",
        "soil_pref": "High moisture & alluvial clay soils",
        "benefit": "Prevents riverbank erosion and thrives in flood-prone zones.",
        "survival_rate": "96%",
        "co2_per_ha_yr": 19.8,
        "bg_tint": "#E0F2F4",
        "tree_color_1": "#1D6F72",
        "tree_color_2": "#2A9D8F",
        "trunk_color": "#134E52",
        "biome_type": "wetland",
        "svg": HOPEA_ICON_SVG,
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
        "tree_color_2": "#6A994E",
        "trunk_color": "#183A21",
        "biome_type": "climax",
        "svg": """<svg width="74" height="74" viewBox="0 0 80 80" fill="none" xmlns="http://www.w3.org/2000/svg"><rect width="80" height="80" rx="22" fill="#1B4332"/><path d="M40 65V26" stroke="#D8F3DC" stroke-width="4.5" stroke-linecap="round"/><circle cx="40" cy="22" r="13" fill="#B7E4C7"/><circle cx="27" cy="30" r="11" fill="#74C69D"/><circle cx="53" cy="30" r="11" fill="#74C69D"/><circle cx="40" cy="34" r="12" fill="#52B788"/></svg>""",
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


def set_preset(ph, moisture, npk, temp):
    st.session_state.ph = ph
    st.session_state.moisture = moisture
    st.session_state.npk = npk
    st.session_state.temp = temp


# ---------------------------------------------------------
# 5. Dynamic TensorFlow Engine
# ---------------------------------------------------------
def run_tf_inference(ph, moisture, npk, temp):
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

    return (
        predicted_idx,
        confidence,
        probabilities,
        norm_values,
        logits_tensor.numpy()[0],
    )


# ---------------------------------------------------------
# 6. Reactive Botanical Tree SVG Generator
# ---------------------------------------------------------
def build_dynamic_forest_html(species_cfg, confidence, hectares):
    c1 = species_cfg["tree_color_1"]
    c2 = species_cfg["tree_color_2"]
    trunk = species_cfg["trunk_color"]
    biome = species_cfg["biome_type"]

    op = round(0.15 + (confidence / 100.0) * 0.10, 2)

    extra_grove = ""
    if hectares >= 15:
        if biome == "wetland":
            hopea_mid = get_hopea_svg_art(
                trunk_color=trunk,
                foliage_dark=c1,
                foliage_mid=c2,
                foliage_light="#74C69D",
                water_color="#48CAE4",
                opacity=op,
            )
            extra_grove = (
                f'<g class="tree-sway-2" transform="translate(430, 185) scale(1.45)">{hopea_mid}</g>'
                f'<g class="tree-sway-3" transform="translate(860, 175) scale(1.5)">{hopea_mid}</g>'
            )
        else:
            extra_grove = (
                f'<g class="tree-sway-2" opacity="{op}">'
                f'<path d="M475 430 C478 370, 480 320, 482 260 L494 260 C496 320, 498 370, 502 430 Z" fill="{trunk}"/>'
                f'<circle cx="488" cy="232" r="52" fill="{c1}"/>'
                f'<circle cx="445" cy="258" r="38" fill="{c2}"/>'
                f'<circle cx="532" cy="254" r="40" fill="{c1}"/>'
                f'</g>'
                f'<g class="tree-sway-3" opacity="{op}">'
                f'<path d="M930 430 C933 365, 935 315, 937 250 L949 250 C951 315, 953 365, 957 430 Z" fill="{trunk}"/>'
                f'<circle cx="943" cy="222" r="54" fill="{c2}"/>'
                f'<circle cx="898" cy="250" r="40" fill="{c1}"/>'
                f'<circle cx="988" cy="246" r="38" fill="{c1}"/>'
                f'</g>'
            )

    if biome == "acacia":
        hero_trees = (
            f'<g class="tree-sway-1" opacity="{op + 0.04}">'
            f'<path d="M105 430 C112 365, 118 310, 122 240 L138 240 C140 310, 148 365, 158 430 Z" fill="{trunk}"/>'
            f'<path d="M126 282 Q82 240 50 218" stroke="{trunk}" stroke-width="8" stroke-linecap="round"/>'
            f'<path d="M134 272 Q180 230 215 212" stroke="{trunk}" stroke-width="8" stroke-linecap="round"/>'
            f'<ellipse cx="130" cy="198" rx="125" ry="38" fill="{c1}"/>'
            f'<ellipse cx="82" cy="212" rx="75" ry="26" fill="{c2}"/>'
            f'<ellipse cx="182" cy="210" rx="78" ry="28" fill="{c2}"/>'
            f'<ellipse cx="130" cy="180" rx="85" ry="24" fill="{c1}"/>'
            f'</g>'
            f'<g class="tree-sway-2" opacity="{op + 0.04}">'
            f'<path d="M1275 430 C1282 360, 1288 300, 1292 225 L1308 225 C1312 300, 1318 360, 1328 430 Z" fill="{trunk}"/>'
            f'<path d="M1296 268 Q1248 225 1210 205" stroke="{trunk}" stroke-width="8" stroke-linecap="round"/>'
            f'<path d="M1304 258 Q1350 215 1385 198" stroke="{trunk}" stroke-width="8" stroke-linecap="round"/>'
            f'<ellipse cx="1300" cy="185" rx="130" ry="40" fill="{c1}"/>'
            f'<ellipse cx="1245" cy="200" rx="78" ry="28" fill="{c2}"/>'
            f'<ellipse cx="1355" cy="198" rx="80" ry="28" fill="{c2}"/>'
            f'</g>'
        )
    elif biome == "wetland":
        # Uses the EXACT same Hopea odorata SVG art as the species card icon!
        hopea_unit = get_hopea_svg_art(
            trunk_color=trunk,
            foliage_dark=c1,
            foliage_mid=c2,
            foliage_light="#74C69D",
            water_color="#48CAE4",
            opacity=min(0.32, op + 0.06),
        )
        hero_trees = (
            f'<path d="M0 398 Q360 374 720 398 T1440 392" stroke="#48CAE4" stroke-width="3.5" stroke-opacity="{op}"/>'
            f'<path d="M0 416 Q360 392 720 416 T1440 410" stroke="{c1}" stroke-width="3.5" stroke-opacity="{op}"/>'
            # Left Primary Hopea odorata
            f'<g class="tree-sway-1" transform="translate(15, 110) scale(2.05)">{hopea_unit}</g>'
            # Secondary Left Young Hopea odorata
            f'<g class="tree-sway-3" transform="translate(230, 200) scale(1.42)">{hopea_unit}</g>'
            # Right Primary Hopea odorata
            f'<g class="tree-sway-2" transform="translate(1150, 95) scale(2.15)">{hopea_unit}</g>'
        )
    else:
        hero_trees = (
            f'<g class="tree-sway-1" opacity="{op + 0.04}">'
            f'<path d="M98 430 C115 385, 120 325, 124 240 L142 240 C146 325, 150 385, 170 430 Z" fill="{trunk}"/>'
            f'<path d="M128 292 Q92 264 66 244" stroke="{trunk}" stroke-width="9" stroke-linecap="round"/>'
            f'<path d="M138 278 Q174 248 202 230" stroke="{trunk}" stroke-width="9" stroke-linecap="round"/>'
            f'<path d="M133 262 L133 198" stroke="{trunk}" stroke-width="8" stroke-linecap="round"/>'
            f'<circle cx="133" cy="178" r="68" fill="{c1}"/>'
            f'<circle cx="78" cy="218" r="52" fill="{c1}"/>'
            f'<circle cx="188" cy="215" r="54" fill="{c1}"/>'
            f'<circle cx="106" cy="154" r="48" fill="{c2}"/>'
            f'<circle cx="162" cy="156" r="46" fill="{c2}"/>'
            f'<circle cx="133" cy="206" r="56" fill="{c2}"/>'
            f'</g>'
            f'<g class="tree-sway-3" opacity="{op}">'
            f'<path d="M275 430 C280 385, 282 340, 284 290 L296 290 C298 340, 300 385, 306 430 Z" fill="{trunk}"/>'
            f'<circle cx="290" cy="264" r="46" fill="{c2}"/>'
            f'<circle cx="256" cy="285" r="34" fill="{c1}"/>'
            f'<circle cx="324" cy="282" r="35" fill="{c1}"/>'
            f'</g>'
            f'<g class="tree-sway-2" opacity="{op + 0.04}">'
            f'<path d="M1268 430 C1286 380, 1290 315, 1294 225 L1314 225 C1318 315, 1322 380, 1342 430 Z" fill="{trunk}"/>'
            f'<path d="M1298 282 Q1260 250 1230 230" stroke="{trunk}" stroke-width="9" stroke-linecap="round"/>'
            f'<path d="M1308 268 Q1346 238 1376 218" stroke="{trunk}" stroke-width="9" stroke-linecap="round"/>'
            f'<path d="M1304 248 L1304 185" stroke="{trunk}" stroke-width="8" stroke-linecap="round"/>'
            f'<circle cx="1304" cy="164" r="72" fill="{c1}"/>'
            f'<circle cx="1244" cy="206" r="56" fill="{c1}"/>'
            f'<circle cx="1362" cy="204" r="58" fill="{c1}"/>'
            f'<circle cx="1276" cy="142" r="50" fill="{c2}"/>'
            f'<circle cx="1334" cy="144" r="48" fill="{c2}"/>'
            f'<circle cx="1304" cy="194" r="58" fill="{c2}"/>'
            f'</g>'
        )

    return (
        f'<div class="forest-bg">'
        f'<svg viewBox="0 0 1440 430" preserveAspectRatio="xMidYMax slice" fill="none" xmlns="http://www.w3.org/2000/svg">'
        f'<path d="M0 365 Q360 305 720 355 T1440 338 L1440 430 L0 430 Z" fill="{c1}" fill-opacity="{round(op * 0.45, 3)}"/>'
        f'<path d="M0 392 Q480 342 960 385 T1440 368 L1440 430 L0 430 Z" fill="{trunk}" fill-opacity="{round(op * 0.55, 3)}"/>'
        f'{hero_trees}{extra_grove}'
        f'</svg></div>'
    )


# ---------------------------------------------------------
# 7. Main Interactive Columns & TensorFlow Execution
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
        hectares = st.slider("Target Planting Area (Hectares)", 1, 50, 10)

        st.write("")
        st.button(
            "🚀 Run TensorFlow Analysis",
            type="primary",
            use_container_width=True,
        )

# Run live TensorFlow inference
idx, confidence, probs, norm_vals, raw_logits = run_tf_inference(
    soil_ph, moisture, npk, temp
)
top_species = SPECIES_DATA[idx]
sway_duration = max(3.0, round(10.5 - (temp - 15.0) * 0.22, 1))

# ---------------------------------------------------------
# 8. Inject CSS & Dynamic Tree Layer (Zero Indentation)
# ---------------------------------------------------------
css_and_bg = f"""<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"] {{
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}}
.stApp {{
    background: radial-gradient(circle at top right, {top_species['bg_tint']} 0%, #F4F9F6 55%, #EAF5EE 100%) !important;
}}
header[data-testid="stHeader"] {{
    background: transparent !important;
}}
.main .block-container {{
    position: relative;
    z-index: 2;
}}
.forest-bg {{
    position: fixed;
    bottom: 0px;
    left: 0px;
    width: 100vw;
    height: 440px;
    pointer-events: none;
    z-index: 1;
    overflow: hidden;
}}
.forest-bg svg {{
    width: 100%;
    height: 100%;
}}
@keyframes swayTreeA {{
    0%, 100% {{ transform: rotate(-2.2deg) translateX(0px); }}
    50% {{ transform: rotate(2.2deg) translateX(5px); }}
}}
@keyframes swayTreeB {{
    0%, 100% {{ transform: rotate(2.4deg) translateX(0px); }}
    50% {{ transform: rotate(-2.4deg) translateX(-5px); }}
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
    position: relative;
    z-index: 3;
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
div[data-testid="stVerticalBlockBorderWrapper"] {{
    border-radius: 30px !important;
    border: 1px solid #CBEAD6 !important;
    background-color: rgba(255, 255, 255, 0.84) !important;
    backdrop-filter: blur(8px);
    padding: 0.85rem !important;
    box-shadow: 0 10px 28px rgba(27, 67, 50, 0.06) !important;
    position: relative;
    z-index: 3;
}}
div[data-testid="stMetric"] {{
    background: linear-gradient(180deg, rgba(255,255,255,0.95) 0%, rgba(242,249,245,0.95) 100%);
    border: 1px solid #CBEAD6;
    padding: 16px 20px;
    border-radius: 24px !important;
    box-shadow: 0 4px 14px rgba(45, 106, 79, 0.06);
}}
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
}}
button[kind="secondary"] {{
    background-color: #EDF6F0 !important;
    color: #1B4332 !important;
    border: 1px solid #95D5B2 !important;
    font-size: 0.82rem !important;
}}
div[data-baseweb="slider"] div[role="slider"] {{
    background-color: #2D6A4F !important;
    border: 2px solid #FFFFFF !important;
}}
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
section[data-testid="stSidebar"] > div {{
    background-color: rgba(255, 255, 255, 0.96);
    border-top-right-radius: 34px;
    border-bottom-right-radius: 34px;
    border-right: 1px solid #CBEAD6;
    z-index: 4;
}}
</style>
{build_dynamic_forest_html(top_species, confidence, hectares)}"""

st.markdown(css_and_bg, unsafe_allow_html=True)

# ---------------------------------------------------------
# 9. Sidebar & Hero Banner Render
# ---------------------------------------------------------
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
        - **UI Layer:** Streamlit + Custom CSS
        - **AI Engine:** TensorFlow (`tf.matmul`)
        - **Input Tensor:** 4D Soil & Climate Vector
        - **Visual Sync:** Biome-Reactive Forest SVG
        """
    )
    st.divider()
    st.caption(f"🟢 Active Biome: **{top_species['name']}**")

st.markdown(
    f'<div class="hero-banner"><div><div class="hero-badge">● Live TensorFlow Inference • Active Biome: {top_species["name"]}</div><div class="hero-title">🌱 Project TerraSprout</div><div class="hero-subtitle">Intelligent Soil Telemetry, Carbon Modeling & Native Reforestation Matchmaker</div></div><div>{HERO_SVG}</div></div>',
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# 10. Output Panel Render
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
            m2.metric(
                "Est. Survival",
                top_species["survival_rate"],
                f"{trees_planted:,} Trees",
            )
            m3.metric(
                "10-Yr CO₂ Offset", f"{co2_10yr:,.0f} t", f"{hectares} Hectares"
            )

            st.markdown(
                f'<div class="species-card"><div>{top_species["svg"]}</div><div><h4>{top_species["name"]}</h4><p><strong>Classification:</strong> {top_species["tag"]}</p><p><strong>Ideal Soil:</strong> {top_species["soil_pref"]}</p></div></div>',
                unsafe_allow_html=True,
            )

            st.markdown(f"**🌍 Ecological Impact:** {top_species['benefit']}")
            st.write("")
            st.markdown(
                "**📈 Species Probability Distribution (Softmax Output)**"
            )
            chart_df = pd.DataFrame(
                {
                    "Species": [s["name"] for s in SPECIES_DATA],
                    "Match Probability (%)": [
                        round(float(p) * 100, 1) for p in probs
                    ],
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
            
