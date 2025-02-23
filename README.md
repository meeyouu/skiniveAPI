# skiniveAPI
This application serves as an admin dashboard for Skinive, a platform that provides image-based skin disease analysis.

Introduction to Skinive:
Skinive is a cutting-edge solution for skin disease analysis through image processing. By leveraging advanced machine learning algorithms, Skinive assists dermatologists and users in early detection and analysis of various skin conditions. The dashboard provided in this demo enables a seamless workflow for interacting with Skinive's API services.

Skinive Admin Dashboard
------------------------

This application serves as an admin dashboard for Skinive, a platform that provides
image-based skin disease analysis. The dashboard allows users to:

1. **Upload and Validate an Image:** Users can upload a skin image and validate it using the 
   Skinive API's `/validate` endpoint. The validation checks if the image is of acceptable quality.
   
2. **Predict Skin Disease:** After validation, users can use the `/predict` endpoint to 
   receive a diagnosis that includes the predicted disease class, probability, risk factor, 
   atlas page link for more information, and a detailed description.
   
3. **Retrieve Disease Classes:** Users can also fetch a list of available disease classes 
   via the `/get_disease_classes` endpoint to better understand the range of diagnoses.

https://skinive.com/for-developers/

