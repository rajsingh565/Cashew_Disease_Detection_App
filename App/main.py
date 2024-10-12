import streamlit as st
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
from PIL import Image

# Load the MobileNet model
model = load_model('MobileNet.h5')

# Define class labels (ensure order matches the training labels)
class_names = ['Anthronoes','Healthy', 'Leaf Miner','Red Rust' ]
# Custom CSS to style the app
st.markdown(
    """
    <style>
    .main {
        background-color: #f5f5f5;
        padding: 20px;
        border-radius: 10px;
        max-width: 700px;
        margin: auto;
    }
    h1 {
        color: #4CAF50;
        text-align: center;
    }
    .uploaded-img {
        display: flex;
        justify-content: center;
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Function to preprocess uploaded image
def preprocess_image(img):
    img = img.resize((224, 224))  # Resize to input size
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img /= 255.0  # Normalize
    return img

# App header
st.title("🌿 Cashew Disease Detection App")
st.write("Upload an image of a cashew leaf to detect possible diseases.")

# Upload an image
uploaded_file = st.file_uploader("Upload Cashew Leaf Image:", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display uploaded image
    img = Image.open(uploaded_file)
    
    # Two-column layout for image and results
    col1, col2 = st.columns(2)
    
    with col1:
        st.image(img, caption='Uploaded Image', use_column_width=True)
    
    with col2:
        st.subheader("Prediction Results")

        # Preprocess and predict
        processed_img = preprocess_image(img)
        prediction = model.predict(processed_img)
        predicted_class_idx = np.argmax(prediction)
        predicted_class = class_names[predicted_class_idx]
        confidence = np.max(prediction) * 100
        
        # Display results with a confidence threshold
        if confidence > 80:  # Set confidence threshold
            st.write(f"**Prediction: {predicted_class}**")
            st.write(f"**Confidence: {confidence:.2f}%**")
            st.progress(int(confidence))
        else:
            st.write("⚠️ Prediction is uncertain. Please try another image.")
        
        # Provide information about each disease
        if predicted_class == 'Anthronoes':
            st.info("**Anthronoes:** This disease is caused by fungi, characterized by leaf spots and lesions.")
        elif predicted_class == 'Leaf Miner':
            st.info("**Leaf Miner:** These are small insects that cause tunnels or blotches in leaves.")
        elif predicted_class == 'Red Rust':
            st.info("**Red Rust:** A fungal disease, often resulting in reddish-brown pustules on leaves.")
        else:
            st.success("**Healthy:** No visible diseases detected.")

# App footer
st.markdown("""
    <div style="text-align:center; margin-top: 50px;">
        Made with ❤️ by [Raj Singh]
    </div>
""", unsafe_allow_html=True) 