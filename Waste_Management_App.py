import streamlit as st
import pandas as pd



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
# ---------------- SQL INSIGHTS ----------------
elif menu == "SQL Insights":

    st.subheader("📊 SQL Query Results (Using CSV Data)")

    # 1 providers per city
    q1 = providers.groupby("City").size().reset_index(name="total_providers")

    st.write("1. Providers count in each city")
    st.dataframe(q1)

    # 2 receivers per city
    q2 = receivers.groupby("City").size().reset_index(name="total_receivers")

    st.write("2. Receivers count in each city")
    st.dataframe(q2)

    # 3 provider type contribution
    q3 = food.groupby("Provider_Type")["Quantity"].sum().reset_index()

    st.write("3. Provider type contributing most food")
    st.dataframe(q3.sort_values(by="Quantity", ascending=False))

    # 4 total food available
    total_food = food["Quantity"].sum()

    st.write("4. Total quantity of food available")
    st.write(total_food)

    # 5 city with highest food listings
    q5 = food["Location"].value_counts().reset_index()
    q5.columns = ["City", "Listings"]

    st.write("5. City with highest number of food listings")
    st.dataframe(q5.head(1))

    # 6 most common food types
    q6 = food["Food_Type"].value_counts().reset_index()
    q6.columns = ["Food Type", "Count"]

    st.write("6. Most commonly available food types")
    st.dataframe(q6)

    # 7 claims per food item
    q7 = claims["Food_ID"].value_counts().reset_index()
    q7.columns = ["Food_ID", "Total Claims"]

    st.write("7. Claims made for each food item")
    st.dataframe(q7)

    # 8 provider with highest successful claims
    merged = claims.merge(food, on="Food_ID")

    q8 = merged[merged["Status"]=="Completed"] \
        .groupby("Provider_ID") \
        .size() \
        .reset_index(name="Successful Claims")

    st.write("8. Provider with highest successful claims")
    st.dataframe(q8.sort_values(by="Successful Claims", ascending=False))

    # 9 claim status percentage
    st.subheader("9. Claim Status Percentage")

    claim_percent = claims["Status"].value_counts(normalize=True)*100
    claim_percent = claim_percent.round(2)

    st.bar_chart(claim_percent)
    st.dataframe(claim_percent)

    # 10 avg quantity per receiver
    q10 = merged.groupby("Receiver_ID")["Quantity"].mean().reset_index()

    st.write("10. Average quantity claimed per receiver")
    st.dataframe(q10)

    # 11 most claimed meal type
    q11 = merged["Meal_Type"].value_counts().reset_index()
    q11.columns = ["Meal Type", "Total Claims"]

    st.write("11. Most claimed meal type")
    st.dataframe(q11)

    # 12 total food donated by provider
    q12 = food.groupby("Provider_ID")["Quantity"].sum().reset_index()

    st.write("12. Total food donated by each provider")
    st.dataframe(q12.sort_values(by="Quantity", ascending=False))

    # 13 receiver claiming most food
    q13 = merged.groupby("Receiver_ID")["Quantity"].sum().reset_index()

    st.write("13. Receivers who claimed the most food")
    st.dataframe(q13.sort_values(by="Quantity", ascending=False))