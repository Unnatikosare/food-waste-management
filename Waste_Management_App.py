import streamlit as st
import pandas as pd
import mysql.connector


st.markdown(
    """
    <style>
    .stApp {
        background-color: #fff9db;
    }
    </style>
    """,
    unsafe_allow_html=True
)
# page configuration
st.set_page_config(
    page_title="Food Wastage Management",
    page_icon="🍲",
    layout="wide"
)

# database connection
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Sahil@13",
    database="food_waste_management"
)

# load data
providers = pd.read_csv("clean_providers.csv")
receivers = pd.read_csv("clean_receivers.csv")
food = pd.read_csv("clean_food_listings.csv")
claims = pd.read_csv("clean_claims.csv")

# title
st.title("🍲 Local Food Wastage Management System")
st.caption("Reducing food waste and helping communities")

# sidebar menu
 
menu = st.sidebar.radio(
    "📌 Navigation",
    ["Dashboard", "Providers", "Receivers", "Food Listings", "Claims", "SQL Insights"]
)

# ---------------- DASHBOARD ----------------
if menu == "Dashboard":

    st.subheader("📊 Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Providers", len(providers))
    col2.metric("Receivers", len(receivers))
    col3.metric("Food Items", len(food))
    col4.metric("Total Claims", len(claims))

    st.divider()

    col5, col6 = st.columns(2)

    with col5:
        st.subheader("🥗 Food Type Distribution🥗")
        food_type_chart = food["Food_Type"].value_counts()
        st.bar_chart(food_type_chart)

    with col6:
        st.subheader("🍽 Meal Type Distribution")
        meal_chart = food["Meal_Type"].value_counts()
        st.bar_chart(meal_chart)

    st.divider()

    col7, col8 = st.columns(2)

    with col7:
        st.subheader("📦 Claim Status")
        claim_chart = claims["Status"].value_counts()
        st.bar_chart(claim_chart)

    with col8:
        st.subheader("🏙 Providers per City")
        provider_city_chart = providers["City"].value_counts()
        st.bar_chart(provider_city_chart)


# ---------------- PROVIDERS ----------------
elif menu == "Providers":

    st.subheader("🏢 Providers Data")

    city = st.selectbox(
        "Filter by City",
        providers["City"].unique()
    )

    filtered_providers = providers[
        providers["City"] == city
    ]

    st.dataframe(
        filtered_providers,
        use_container_width=True
    )

    st.download_button(
        "⬇ Download Providers Data",
        filtered_providers.to_csv(index=False),
        "providers.csv"
    )


# ---------------- RECEIVERS ----------------
elif menu == "Receivers":

    st.subheader("🙋 Receivers Data")

    city = st.selectbox(
        "Filter by City",
        receivers["City"].unique()
    )

    filtered_receivers = receivers[
        receivers["City"] == city
    ]

    st.dataframe(
        filtered_receivers,
        use_container_width=True
    )

    st.download_button(
        "⬇ Download Receivers Data",
        filtered_receivers.to_csv(index=False),
        "receivers.csv"
    )


# ---------------- FOOD ----------------
elif menu == "Food Listings":

    st.subheader("🍛 Food Listings")

    food_type = st.selectbox(
        "Filter by Food Type",
        food["Food_Type"].unique()
    )

    filtered_food = food[
        food["Food_Type"] == food_type
    ]

    st.dataframe(
        filtered_food,
        use_container_width=True
    )

    st.download_button(
        "⬇ Download Food Data",
        filtered_food.to_csv(index=False),
        "food.csv"
    )


# ---------------- CLAIMS ----------------
elif menu == "Claims":

    st.subheader("📦 Claims Data")

    st.dataframe(
        claims,
        use_container_width=True
    )

    st.subheader("Claim Status Distribution")

    claim_chart = claims["Status"].value_counts()

    st.bar_chart(claim_chart)

    st.download_button(
        "⬇ Download Claims Data",
        claims.to_csv(index=False),
        "claims.csv"
    )
    # ---------------- SQL INSIGHTS ----------------
elif menu == "SQL Insights":

    st.subheader("📊 SQL Query Results")

    # 1 providers per city
    q1 = pd.read_sql("""
    SELECT City, COUNT(*) as total_providers
    FROM providers
    GROUP BY City
    ORDER BY total_providers DESC
    """, connection)

    st.write("1. Providers count in each city")
    st.dataframe(q1)

    # 2 receivers per city
    q2 = pd.read_sql("""
    SELECT City, COUNT(*) as total_receivers
    FROM receivers
    GROUP BY City
    ORDER BY total_receivers DESC
    """, connection)

    st.write("2. Receivers count in each city")
    st.dataframe(q2)

    # 3 provider type
    q3 = pd.read_sql("""
    SELECT Type, COUNT(*) as provider_count
    FROM providers
    GROUP BY Type
    """, connection)

    st.write("3. Provider types contribution")
    st.dataframe(q3)

    # 4 total food quantity
    q4 = pd.read_sql("""
    SELECT SUM(Quantity) as total_food
    FROM food_listings
    """, connection)

    st.write("4. Total food quantity available")
    st.dataframe(q4)

    # 5 city with most food
    q5 = pd.read_sql("""
    SELECT Location, COUNT(*) as listings
    FROM food_listings
    GROUP BY Location
    ORDER BY listings DESC
    """, connection)

    st.write("5. City with highest food listings")
    st.dataframe(q5)

    # 6 food type distribution
    q6 = pd.read_sql("""
    SELECT Food_Type, COUNT(*) as total
    FROM food_listings
    GROUP BY Food_Type
    """, connection)

    st.write("6. Most common food types")
    st.dataframe(q6)

    # 7 claims per food item
    q7 = pd.read_sql("""
    SELECT Food_ID, COUNT(*) as claims
    FROM claims
    GROUP BY Food_ID
    """, connection)

    st.write("7. Claims per food item")
    st.dataframe(q7)

    # 8 successful claims per provider
    q8 = pd.read_sql("""
    SELECT f.Provider_ID, COUNT(*) as success_claims
    FROM claims c
    JOIN food_listings f ON c.Food_ID = f.Food_ID
    WHERE Status='Completed'
    GROUP BY f.Provider_ID
    """, connection)

    st.write("8. Successful claims by provider")
    st.dataframe(q8)

    # 9 claim status percentage
    st.subheader("📦 Claim Status (%)")

    claim_percent = (
    claims["Status"]
    .value_counts(normalize=True) * 100
    )

    claim_percent = claim_percent.round(2)

    st.bar_chart(claim_percent)

    st.write("9.Percentage distribution of claim status")
    st.dataframe(claim_percent)

    

    # 10 avg food per receiver
    q10 = pd.read_sql("""
    SELECT Receiver_ID, AVG(f.Quantity) as avg_food
    FROM claims c
    JOIN food_listings f ON c.Food_ID=f.Food_ID
    GROUP BY Receiver_ID
    """, connection)

    st.write("10. Average food claimed per receiver")
    st.dataframe(q10)

    # 11 meal type most claimed
    q11 = pd.read_sql("""
    SELECT f.Meal_Type, COUNT(*) as total
    FROM claims c
    JOIN food_listings f ON c.Food_ID=f.Food_ID
    GROUP BY f.Meal_Type
    """, connection)

    st.write("11. Most claimed meal type")
    st.dataframe(q11)

    # 12 total food by provider
    q12 = pd.read_sql("""
    SELECT Provider_ID, SUM(Quantity) as total_food
    FROM food_listings
    GROUP BY Provider_ID
    """, connection)

    st.write("12. Total food donated by each provider")
    st.dataframe(q12)

    q13 = pd.read_sql("""
    SELECT Location,
    COUNT(*) AS total_food_listings
    FROM food_listings
    GROUP BY Location
    ORDER BY total_food_listings DESC
    LIMIT 1
    """, connection)

    st.write("13. City with highest number of food listings")
    st.dataframe(q13)