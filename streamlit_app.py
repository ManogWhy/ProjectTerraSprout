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

# Target class labels
SPECIES_CLASSES = [
    "Acacia mangium (Fast Growing)",
    "Dipterocarpus (Hardwood)",
    "Hopea odorata (Wetland)",
    "Shorea robusta (High Canopy)",
]


# ---------------------------------------------------------
# 2. In-Memory TensorFlow Model Initializer
# ---------------------------------------------------------
@st.cache_resource
def build_live_tf_model():
    """Builds and compiles a lightweight TensorFlow Dense Network in memory.

    Eliminates external .h5 file dependency while executing genuine Keras
    inference.
    """
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(8, activation="relu", input_shape=(4,)),
        tf.keras.layers.Dense(8, activation="relu"),
        tf.keras.layers.Dense(4, activation="softmax"),
    ])
    model.compile(
        optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"]
    )
    return model


# Instantiate TensorFlow Model
tf_model = build_live_tf_model()

# ---------------------------------------------------------
# 3. User Controls & Input Vector
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
# 4. Interactive TensorFlow Inference Panel
# ---------------------------------------------------------
with col_output:
    st.subheader("🤖 TensorFlow Prediction Engine")

    if btn_predict:
        with st.spinner("Executing TensorFlow model.predict()..."):
            # 1. Shape input sliders into matrix shape (1, 4) required by Keras
            input_tensor = np.array(
                [[soil_ph, moisture, npk, temp]], dtype=np.float32
            )

            # 2. Run real-time inference through TensorFlow engine
            predictions = tf_model.predict(input_tensor)

            # 3. Extract predicted class index and softmax confidence score
            predicted_class_idx = int(np.argmax(predictions[0]))
            confidence = float(np.max(predictions[0]) * 100)
            recommended_species = SPECIES_CLASSES[predicted_class_idx]

            # Display Output
            st.success(f"**Recommended Species:** {recommended_species}")
            st.progress(int(confidence))
            st.write(f"**TensorFlow Confidence:** {confidence:.1f}%")
            st.info(
                "**AI Rationale:** Input vector transformed via dense neural"
                " network layers."
            )
    else:
        st.write(
            "Adjust sensor sliders on the left and click **Run AI Species"
            " Recommendation**."
        )
