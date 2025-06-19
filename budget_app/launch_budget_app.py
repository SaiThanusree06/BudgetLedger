import os

# ✅ Tell Streamlit to skip asking for email
os.environ["STREAMLIT_SUPPRESS_EMAIL_PROMPT"] = "1"

# ✅ Now launch the app normally
os.system("streamlit run budget_app_streamlit.py")
