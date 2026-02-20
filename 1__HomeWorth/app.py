import streamlit as st

st.set_page_config(
    page_title="HomeWorth AI",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 HomeWorth AI")
st.markdown("### Smart Property & Loan Intelligence System")

st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to",
    ["Home", "House Price Prediction", "Future Forecast", "Credit Eligibility"]
)

if page == "Home":
    st.header("Welcome")
    st.write("This application predicts house prices and evaluates loan eligibility.")

elif page == "House Price Prediction":
    st.header("House Price Prediction Module (Coming Soon)")

elif page == "Future Forecast":
    st.header("Future Price Forecast Module (Coming Soon)")

elif page == "Credit Eligibility":
    st.header("Credit & Loan Eligibility Module (Coming Soon)")