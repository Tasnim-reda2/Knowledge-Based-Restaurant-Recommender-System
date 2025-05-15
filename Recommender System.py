import pandas as pd
import numpy as np
import streamlit as st

# Step 1: Data Loading & Preprocessing

@st.cache_data
def load_and_clean_data():
    # Load datasets
    zomato_df = pd.read_csv("C:/Users/Acer/Desktop/zomato.csv", encoding='latin-1')
    country_df = pd.read_excel("C:/Users/Acer/Desktop/Country-Code.xlsx")

    # Merge country info into zomato dataset
    zomato_df = zomato_df.merge(country_df, on='Country Code', how='left')

    # Drop duplicates
    zomato_df.drop_duplicates(inplace=True)

    # Drop irrelevant columns
    columns_to_drop = ['Restaurant ID', 'Switch to order menu', 'Address', 'Locality Verbose',
                       'Currency', 'Rating color', 'Rating text', 'Menu Page', 'Phone']
    zomato_df.drop(columns=columns_to_drop, inplace=True, errors='ignore')

    # Drop rows with missing cuisines or ratings
    zomato_df.dropna(subset=['Cuisines', 'Aggregate rating'], inplace=True)

    # Normalize cuisine text to lowercase and strip spaces
    zomato_df['Cuisines'] = zomato_df['Cuisines'].str.lower().str.strip()

    # Extract primary cuisine if multiple
    zomato_df['Primary Cuisine'] = zomato_df['Cuisines'].apply(lambda x: x.split(',')[0])

    # Convert cost for two to numeric and handle errors
    zomato_df['Average Cost for two'] = pd.to_numeric(zomato_df['Average Cost for two'], errors='coerce')

    # Drop rows with missing cost
    zomato_df.dropna(subset=['Average Cost for two'], inplace=True)

    # Create price buckets: Low, Medium, High
    def categorize_price(price):
        if price < 300:
            return 'Low'
        elif price <= 700:
            return 'Medium'
        else:
            return 'High'

    zomato_df['Price Range'] = zomato_df['Average Cost for two'].apply(categorize_price)

    # Convert aggregate rating to float (already mostly float)
    zomato_df['Aggregate rating'] = zomato_df['Aggregate rating'].astype(float)

    # Fill missing 'Country' values with 'Unknown'
    zomato_df['Country'].fillna('Unknown', inplace=True)

    return zomato_df

# Step 2: Recommendation Engine


def filter_and_rank(df, cuisine_list, price_range, country, top_n=10):
    # Filter by cuisine (match any cuisine in the list)
    filtered = df[df['Primary Cuisine'].isin(cuisine_list)]

    # Filter by price range
    filtered = filtered[filtered['Price Range'].isin(price_range)]

    # Filter by country
    filtered = filtered[filtered['Country'].str.contains(country, case=False, na=False)]

    # Score calculation: weighted score by rating and votes
    # Normalize votes and ratings between 0 and 1 for fair weighting
    if filtered.empty:
        return filtered

    max_votes = filtered['Votes'].max()
    max_rating = 5.0  # max rating scale

    filtered['Normalized Votes'] = filtered['Votes'] / max_votes if max_votes > 0 else 0
    filtered['Normalized Rating'] = filtered['Aggregate rating'] / max_rating

    # Weighted score: 70% rating, 30% votes
    filtered['Score'] = 0.7 * filtered['Normalized Rating'] + 0.3 * filtered['Normalized Votes']

    # Sort by score descending
    filtered = filtered.sort_values(by='Score', ascending=False)

    # Return top N results
    return filtered.head(top_n)

# Step 3: Streamlit User Interface


def main():
    st.title("Knowledge-Based Restaurant Recommender System")

    # Load data
    zomato_df = load_and_clean_data()

    st.sidebar.header("User Preferences")

    # Cuisine options
    cuisine_options = sorted(zomato_df['Primary Cuisine'].unique())
    selected_cuisines = st.sidebar.multiselect("Select Cuisine(s)", cuisine_options, default=["italian"])

    # Price range options
    price_options = ['Low', 'Medium', 'High']
    selected_prices = st.sidebar.multiselect("Select Price Range(s)", price_options, default=price_options)

    # Country options
    country_options = sorted(zomato_df['Country'].dropna().unique())
    selected_country = st.sidebar.selectbox("Select Country", country_options,
                                            index=country_options.index('India') if 'India' in country_options else 0)

    # Number of results
    top_n = st.sidebar.slider("Number of recommendations", 5, 20, 10)

    # Button to get recommendations
    if st.sidebar.button("Recommend"):
        results = filter_and_rank(zomato_df, selected_cuisines, selected_prices, selected_country, top_n)

        if results.empty:
            st.write("No restaurants found with the given preferences. Please try different filters.")
        else:
            for idx, row in results.iterrows():
                st.subheader(row['Restaurant Name'])
                st.write(f"Cuisine: {row['Primary Cuisine'].title()}")
                st.write(f"Cost for two: ₹{int(row['Average Cost for two'])} ({row['Price Range']})")
                st.write(f"Rating: {row['Aggregate rating']} ({row['Votes']} votes)")
                st.write(f"Country: {row['Country']}")
                st.write(f"Location: {row['City'] if 'City' in row else 'Unknown'}")
                st.markdown("---")

                # Explanation
                explanation = (f"Matched on cuisine(s): {', '.join(selected_cuisines)} | "
                               f"Price range(s): {', '.join(selected_prices)} | "
                               f"Country: {selected_country} | "
                               f"Rating: {row['Aggregate rating']} | "
                               f"Votes: {row['Votes']}")
                st.info(explanation)


if __name__ == '__main__':
    main()
