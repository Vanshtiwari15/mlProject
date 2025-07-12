## End to End Machine Learning Project

# 🚀 End-to-End Machine Learning Regression Project

Hi! I’m Vansh Tiwari, and this is my end-to-end ML regression project where I take raw data from ingestion to deployment-ready pipelines.

---

## 📌 **Project Overview**

This project demonstrates:
- Automated **data ingestion** from source files
- Clean **data transformation** (handling missing values, encoding, scaling)
- A **training pipeline** for multiple regression models (Random Forest, XGBoost, CatBoost)
- Model evaluation using **R² Score**
- A **FastAPI backend** to serve predictions as an API
- An interactive **Streamlit frontend** for user-friendly predictions

---

## 🗂️ **Project Structure**

```plaintext
mlProject/
│
├── application.py         # FastAPI backend
├── frontend.py            # Streamlit app
├── src/                   # Source code
│   ├── components/        # Data ingestion, transformation, model trainer
│   ├── pipeline/          # Training & prediction pipelines
│   ├── exception.py       # Custom exception class
│   ├── logger.py          # Logging setup
│   └── utils.py           # Utility functions
├── artifacts/             # Saved datasets & models
├── notebooks/             # EDA and experiments
├── requirements.txt       # Python dependencies
├── README.md              # Project overview (this file!)
