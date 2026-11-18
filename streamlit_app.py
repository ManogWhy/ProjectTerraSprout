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
    bbox = '<rect x="0" y="0" width="140" height="160" fill="transparent"/>'
    if biome_type == "acacia":
        return (
            f'<g opacity="{opacity}">{bbox}'
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
            f'<g opacity="{opacity}">{bbox}'
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
            f'<g opacity="{opacity}">{bbox}'
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
            f'<g opacity="{opacity}">{bbox}'
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
# 4. Session State Initialization (Clean Highland Default)
# ---------------------------------------------------------
if "ph" not in st.session_state:
    st.session_state.ph = 6.4
if "moisture" not in st.session_state:
    st.session_state.moisture = 52
if "npk" not in st.session_state:
    st.session_state.npk = 240
if "temp" not in st.session_state:
    st.session_state.temp = 24.5
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
        # Col 0: Acacia | Col 1: Dipterocarpus | Col 2: Hopea | Col 3: Shorea
        [5.0, -2.0, -0.5, 1.5],   # norm_ph
        [-1.5, -1.5, 6.0, -1.5],  # norm_moisture
        [-1.0, 5.5, -1.5, 5.5],   # norm_npk
        [1.0, 1.5, 0.0, -1.5],    # norm_temp
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
# 6. Static CSS (Light/Mint Override + Dark Forest Typography)
# ---------------------------------------------------------
STATIC_CSS = """<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

html, body, [data-testid="stAppViewContainer"], [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    color: #123524 !important;
}

/* Force dark forest green on all headings, labels, and body copy across light & dark modes */
[data-testid="stAppViewContainer"] h1,
[data-testid="stAppViewContainer"] h2,
[data-testid="stAppViewContainer"] h3,
[data-testid="stAppViewContainer"] h4,
[data-testid="stAppViewContainer"] p,
[data-testid="stAppViewContainer"] label,
[data-testid="stAppViewContainer"] li,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] li {
    color: #123524 !important;
}

[data-testid="stCaptionContainer"] p {
    color: #2D6A4F !important;
    font-weight: 500 !important;
}

/* Top header bar & toolbar icons */
header[data-testid="stHeader"] {
    background: transparent !important;
}
header[data-testid="stHeader"] button,
header[data-testid="stHeader"] a,
header[data-testid="stHeader"] svg {
    color: #1B4332 !important;
    fill: #1B4332 !important;
}

.main .block-container,
[data-testid="stMainBlockContainer"] {
    position: relative;
    z-index: 2;
}

/* Background Animated Forest */
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
    width: 10
