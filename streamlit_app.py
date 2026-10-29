import numpy as np
import streamlit as st
import tensorflow as tf

# ---------------------------------------------------------
# 1. Page Header & Layout Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Project TerraSprout | Team Lemon Tea",
    page_icon="🌱",
    layout="wide",
)

st.title("🌱 Project TerraSprout — AI Dashboard")
st.caption("Team Lemon Tea | SDG 15: Life on Land")
st.divider()

SPECIES_CLASSES = [
    "Acacia mangium (Fast Growing)",
    "Dipterocarpus (Hardwood)",
    "Hopea odorata (Wetland)",
    "Shorea robusta (High Canopy)",
]


# ---------------------------------------------------------
# 2. Dynamic TensorFlow Engine (Calculates weights on feature vectors)
# ---------------------------------------------------------
def run_tf_inference(ph, moisture, npk, temp):
    """Passes normalized slider inputs through a custom TensorFlow tensor matrix

    to ensure realistic, dynamic class predictions.
    """
    # 1. Normalize sensor inputs into scale [0, 1] for neural net feature balance
    norm_ph = (ph - 4.0) / 5.0
    norm_moisture = moisture / 100.0
    norm_npk = (npk - 10) / 290.0
    norm_temp = (temp - 15.0) / 30.0

    # 2. Convert to TensorFlow Tensor (Shape: 1x4)
    input_tensor = tf.constant(
        [[norm_ph, norm_moisture, norm_npk, norm_temp]], dtype=tf.float32
    )

    # 3. Custom weight matrix mapped to eco-logical feature significance
    # Rows: [pH, Moisture, NPK, Temp] -> Columns: [Acacia, Dipterocarpus, Hopea, Shorea]
    weights = tf.constant(
        [
            [2.5, -1.0, -2.0, 0.5],  # Low/High pH bias
            [-1.0, -1.5, 3.5, 0.0],  # Moisture bias (High moisture favors Wetland Hopea)
            [1.0, 0.5, 0.0, 3.0],  # High NPK favors High Canopy Shorea
            [0.2, 1.8, 0.1, -0.5],  # Temp bias
        ],
        dtype=tf.float32,
    )

    # 4. Perform matrix multiplication (Dense Layer dot-product: X * W)
    logits = tf.matmul(input_tensor, weights)

    # 5. Apply Softmax Activation function to convert logits into percentages
    probabilities = tf.nn.softmax(logits).numpy()[0]

    predicted_idx = int(np.argmax(probabilities))
    confidence = float(probabilities[predicted_idx] * 100)

    return SPECIES_CLASSES[predicted_idx], confidence


# ---------------------------------------------------------
# 3. User Controls
# ---------------------------------------------------------
col_input, col_output = st.columns([1, 1])

with col_input:
    st.subheader("📊 Soil & Sensor Inputs")
    soil_ph = st.slider("Soil pH Level", 4.0, 9.0, 6.5, 0.1)
    moisture = st.slider("Soil Moisture Content (%)", 0, 100, 45)
    npk = st.slider("NPK Nutrient Index (PPM)", 10, 300, 150)
    temp = st.number_input("Ambient Temperature (°C)", 15.0, 45.0, 28.5)

    btn_predict = st.button(
        "🚀 Run AI Species Recommendation", use_container_width=True
    )

# ---------------------------------------------------------
# 4. Interactive Output Panel
# ---------------------------------------------------------
with col_output:
    st.subheader("🤖 TensorFlow Prediction Engine")

    if btn_predict:
        with st.spinner("Calculating Tensor activation maps..."):
            species, confidence = run_tf_inference(
                soil_ph, moisture, npk, temp
            )

            st.success(f"**Recommended Species:** {species}")
            st.progress(int(confidence))
            st.write(f"**TensorFlow Softmax Confidence:** {confidence:.1f}%")
            st.info(
                "**AI Rationale:** Dynamic Softmax probability generated from"
                " tensor matrix multiplication (`tf.matmul` + `tf.nn.softmax`)."
            )
    else:
        st.write(
            "Adjust sensor sliders on the left and click **Run AI Species"
            " Recommendation**."
        )
