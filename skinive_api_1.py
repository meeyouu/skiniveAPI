import streamlit as st
import requests
import json
from PIL import Image
from io import BytesIO

# ==========================
# 1. Streamlit Page Layout
# ==========================
st.set_page_config(page_title="Skinive Admin Dashboard", layout="centered")
st.title("Skinive Admin Dashboard")

# ==========================
# 2. Configuration Inputs
# ==========================
st.sidebar.header("API Configuration")

# -- Authorization token
auth_token = st.sidebar.text_input("Authorization Token", type="password")

# -- Endpoints
validate_endpoint = st.sidebar.text_input(
    "Validate Endpoint",
    value="https://api.skiniver.com/validate"
)
predict_endpoint = st.sidebar.text_input(
    "Predict Endpoint",
    value="https://api.skiniver.com/predict"
)
disease_classes_endpoint = st.sidebar.text_input(
    "Disease Classes Endpoint",
    value="https://api.skiniver.com/get_disease_classes"
)

locale = st.sidebar.selectbox("Locale", ["en", "ru"], index=0)

st.write("Provide your API credentials and endpoints in the sidebar to begin.")

# ==========================
# 3. Helper Functions
# ==========================
def call_validate(img_file):
    """Calls the /validate endpoint."""
    headers = {
        "Authorization": auth_token
    }
    files = {
        "img": img_file
    }
    try:
        response = requests.post(validate_endpoint, headers=headers, files=files, timeout=30)
        return response.json()
    except Exception as e:
        return {"error": str(e), "status": False}

def call_predict(img_file, lang=None):
    """Calls the /predict endpoint."""
    headers = {
        "Authorization": auth_token,
        "Locale": locale  # or "ru"
    }
    files = {
        "img": img_file
    }
    data = {}
    if lang:
        data["lang"] = lang

    try:
        response = requests.post(predict_endpoint, headers=headers, files=files, data=data, timeout=30)
        return response.json()
    except Exception as e:
        return {"error": str(e), "status": False}

def call_get_disease_classes():
    """Calls the /get_disease_classes endpoint."""
    headers = {
        "Authorization": auth_token,
        "Locale": locale
    }
    try:
        response = requests.get(disease_classes_endpoint, headers=headers, timeout=30)
        return response.json()
    except Exception as e:
        return {"error": str(e), "status": False}

# ==========================
# 4. Main Interface
# ==========================
st.header("Step 1: Upload and Validate Image")

uploaded_file = st.file_uploader("Upload an image (JPG/PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display preview
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image Preview", use_column_width=True)

# Button to Validate
if st.button("Validate"):
    if not auth_token:
        st.warning("Please provide an authorization token in the sidebar.")
    elif not uploaded_file:
        st.warning("Please upload an image first.")
    else:
        with st.spinner("Validating..."):
            response_data = call_validate(uploaded_file)
        st.subheader("Validation Response")
        st.json(response_data)

        # If there's an error in the response, display it
        if "error" in response_data and response_data["error"]:
            st.error(f"Error: {response_data['error']}")
        else:
            # Show result
            is_good = response_data.get("isgood", "false")
            probability = response_data.get("prob", "N/A")
            st.write(f"**isgood**: {is_good}, **prob**: {probability}")

# ==========================
# 5. Prediction
# ==========================
st.header("Step 2: Predict Skin Disease")

# Button to Predict
if st.button("Predict"):
    if not auth_token:
        st.warning("Please provide an authorization token in the sidebar.")
    elif not uploaded_file:
        st.warning("Please upload an image first.")
    else:
        with st.spinner("Predicting..."):
            response_data = call_predict(uploaded_file)
        st.subheader("Prediction Response")
        st.json(response_data)

        # Check for error
        if "error" in response_data and response_data["error"]:
            st.error(f"Error: {response_data['error']}")
        else:
            # Show important fields
            disease_class = response_data.get("class", "N/A")
            disease_class_raw = response_data.get("class_raw", "N/A")
            probability = response_data.get("prob", "N/A")
            risk = response_data.get("risk", "N/A")
            atlas_link = response_data.get("atlas_page_link", "#")
            description = response_data.get("description", "")

            st.write(f"**Class**: {disease_class}")
            st.write(f"**Class Raw**: {disease_class_raw}")
            st.write(f"**Probability**: {probability}%")
            st.write(f"**Risk**: {risk}")
            st.write(f"**Atlas Page**: [Link]({atlas_link})")
            st.write("**Description**:")
            st.write(description)

# ==========================
# 6. Get Disease Classes
# ==========================
st.header("Step 3: Retrieve Disease Classes")

if st.button("Get Disease Classes"):
    if not auth_token:
        st.warning("Please provide an authorization token in the sidebar.")
    else:
        with st.spinner("Fetching disease classes..."):
            response_data = call_get_disease_classes()
        st.subheader("Disease Classes Response")
        st.json(response_data)

        if "error" in response_data and response_data["error"]:
            st.error(f"Error: {response_data['error']}")
        else:
            # Display in a more readable format
            categories = response_data.get("categories", [])
            for category in categories:
                title_name = category.get("title_name", "N/A")
                st.markdown(f"### {title_name}")
                diseases = category.get("diseases", [])
                for dis in diseases:
                    st.write(f"- **ID**: {dis['id']}, **Label**: {dis['label']}, **Name**: {dis['name']}")

# ==========================
# 7. Final Notes
# ==========================
st.info("Use this demo to explore the Validate → Predict → Get Disease Classes workflow. Make sure you have a valid token and correct endpoints.")
