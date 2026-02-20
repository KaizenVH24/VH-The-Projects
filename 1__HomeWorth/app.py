import streamlit as st
import pandas as pd
import joblib

# ---------------------------------------------------
# Page Config
# ---------------------------------------------------
st.set_page_config(page_title="HomeWorth AI", layout="wide")

# ---------------------------------------------------
# Custom Styling
# ---------------------------------------------------
st.markdown("""
<style>

body {
    background-color: #f5f7fa;
}

.navbar {
    background-color: #111827;
    padding: 1rem 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    color: white;
}

.nav-links a {
    color: white;
    margin-left: 25px;
    text-decoration: none;
    font-weight: 500;
}

.nav-links a:hover {
    color: #60a5fa;
}

.footer {
    position: fixed;
    bottom: 0;
    width: 100%;
    background-color: #111827;
    color: white;
    text-align: center;
    padding: 0.7rem;
    font-size: 14px;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 5rem;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# Top Navigation Bar
# ---------------------------------------------------
st.markdown("""
<div class="navbar">
    <div><strong>HomeWorth AI</strong></div>
    <div class="nav-links">
        <a href="?page=home">Home</a>
        <a href="?page=price">Price Prediction</a>
        <a href="?page=credit">Credit Eligibility</a>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# Page Routing
# ---------------------------------------------------
query_params = st.query_params
page = query_params.get("page", "home")

# ---------------------------------------------------
# Load Model & Data
# ---------------------------------------------------
model = joblib.load("models/house_price_model.pkl")
data = pd.read_csv("data/housing_data.csv")

growth_rates = {
    "Mumbai": 0.07,
    "Delhi": 0.065,
    "Bengaluru": 0.09,
    "Pune": 0.08,
    "Hyderabad": 0.085,
    "Chennai": 0.07,
    "Kolkata": 0.06,
    "Ahmedabad": 0.065,
    "Jaipur": 0.06,
    "Lucknow": 0.055
}

# ---------------------------------------------------
# HOME PAGE
# ---------------------------------------------------
if page == "home":

    st.markdown("<h1 style='text-align: center;'>HomeWorth AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>Smart Property & Loan Intelligence System</p>", unsafe_allow_html=True)

    st.markdown("---")

    st.write("""
    This platform helps you:

    - Predict property prices across major Indian cities  
    - Understand city-level market ranges  
    - Forecast investment value over time  
    - Evaluate credit eligibility and loan affordability  
    """)

# ---------------------------------------------------
# PRICE PREDICTION PAGE
# ---------------------------------------------------
elif page == "price":

    st.title("House Price Prediction")

    col1, col2 = st.columns(2)

    with col1:
        city = st.selectbox("City", list(growth_rates.keys()))
        area = st.number_input("Area (sq ft)", 300, 5000, 1000)
        bhk = st.slider("BHK", 1, 5, 2)
        bathrooms = st.slider("Bathrooms", 1, 4, 2)

    with col2:
        parking = st.selectbox("Parking Available", [0, 1])
        location = st.selectbox("Location Type", ["Premium", "Standard", "Developing"])
        age = st.slider("Property Age (years)", 0, 30, 5)
        furnishing = st.selectbox("Furnishing", ["Furnished", "Semi-Furnished", "Unfurnished"])

    if st.button("Predict Price"):

        input_data = pd.DataFrame([{
            "city": city,
            "area_sqft": area,
            "bhk": bhk,
            "bathrooms": bathrooms,
            "parking": parking,
            "location_type": location,
            "property_age": age,
            "furnishing": furnishing
        }])

        prediction = model.predict(input_data)[0]

        st.success(f"Estimated Property Price: ₹ {round(prediction, 2):,}")

        st.markdown("---")
        st.subheader(f"{city} Market Overview")

        city_data = data[data["city"] == city]

        min_price = city_data["price"].min()
        avg_price = city_data["price"].mean()
        max_price = city_data["price"].max()

        c1, c2, c3 = st.columns(3)
        c1.metric("Lowest Price", f"₹ {round(min_price, 0):,}")
        c2.metric("Average Price", f"₹ {round(avg_price, 0):,}")
        c3.metric("Highest Price", f"₹ {round(max_price, 0):,}")

        st.markdown("---")
        st.subheader("Future Price Forecast")

        rate = growth_rates[city]

        price_3 = prediction * ((1 + rate) ** 3)
        price_5 = prediction * ((1 + rate) ** 5)
        price_7 = prediction * ((1 + rate) ** 7)

        f1, f2, f3 = st.columns(3)
        f1.metric("After 3 Years", f"₹ {round(price_3, 0):,}")
        f2.metric("After 5 Years", f"₹ {round(price_5, 0):,}")
        f3.metric("After 7 Years", f"₹ {round(price_7, 0):,}")

# ---------------------------------------------------
# CREDIT ELIGIBILITY PAGE
# ---------------------------------------------------
elif page == "credit":

    st.title("Credit & Loan Eligibility")

    col1, col2 = st.columns(2)

    with col1:
        age = st.slider("Age", 21, 60, 30)
        income = st.number_input("Monthly Income (₹)", 10000, 1000000, 50000)
        employment = st.selectbox("Employment Type", ["Salaried", "Self-Employed"])
        existing_emi = st.number_input("Existing Monthly EMI (₹)", 0, 500000, 10000)

    with col2:
        loan_amount = st.number_input("Desired Loan Amount (₹)", 500000, 50000000, 2000000)
        tenure = st.slider("Loan Tenure (Years)", 5, 30, 20)

    if st.button("Evaluate Credit Profile"):

        dti = existing_emi / income

        if dti < 0.30:
            category = "Excellent"
            rate_range = (8.2, 8.8)
        elif dti < 0.45:
            category = "Good"
            rate_range = (8.8, 9.4)
        elif dti < 0.55:
            category = "Moderate"
            rate_range = (9.4, 10.2)
        else:
            category = "High Risk"
            rate_range = (10.2, 11.5)

        avg_rate = sum(rate_range) / 2 / 100 / 12
        months = tenure * 12

        emi = (loan_amount * avg_rate * (1 + avg_rate)**months) / ((1 + avg_rate)**months - 1)

        st.success(f"Credit Category: {category}")

        c1, c2, c3 = st.columns(3)
        c1.metric("Lowest Interest", f"{rate_range[0]}%")
        c2.metric("Average Interest", f"{round(sum(rate_range)/2,2)}%")
        c3.metric("Highest Interest", f"{rate_range[1]}%")

        st.markdown("---")
        st.subheader("Estimated Monthly EMI")
        st.info(f"₹ {round(emi, 2):,}")

        st.markdown("---")
        st.subheader("Loan Affordability Analysis")

        emi_ratio = emi / income

        if emi_ratio < 0.30:
            st.success("This loan is comfortably affordable.")
        elif emi_ratio < 0.45:
            st.warning("This loan is manageable but slightly stretched.")
        else:
            st.error("This loan may be financially risky based on your income.")

# ---------------------------------------------------
# FIXED FOOTER
# ---------------------------------------------------
st.markdown("""
<div class="footer">
    Built by Vinay |
    <a href="https://github.com/KaizenVH24" target="_blank" style="color:white;">GitHub</a> |
    <a href="https://linkedin.com/in/vinayhulsurkar" target="_blank" style="color:white;">LinkedIn</a> |
    <a href="https://leetcode.com/vinayhulsurkar24" target="_blank" style="color:white;">LeetCode</a>
</div>
""", unsafe_allow_html=True)