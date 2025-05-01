import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page title
st.set_page_config(page_title="Sri Lanka GDP Dashboard", layout="centered")
st.title("📊 Sri Lanka GDP Analysis (1960–2023)")
st.markdown("This dashboard explores the GDP (current US$) of Sri Lanka using World Bank data.")

# Load and clean data
@st.cache_data
def load_data():
    # Skip the metadata rows and read from the 5th row (0-indexed → header=4)
    df = pd.read_csv("GDP (current US$)_SL - 1960–2023.csv", header=4)
    
    # Extract only the year columns (from 1960 onward)
    year_columns = df.columns[4:]  # Skip Country Name, Country Code, Indicator, Indicator Code

    # Select Sri Lanka row only (if other countries are present)
    sri_lanka = df[df['Country Name'] == 'Sri Lanka']

    # Convert wide data to long format
    long_df = sri_lanka.melt(
        id_vars=['Country Name'],
        value_vars=year_columns,
        var_name='Year',
        value_name='GDP'
    )

    long_df['Year'] = long_df['Year'].astype(str)
    long_df['GDP'] = long_df['GDP'].astype(float)
    return long_df

data = load_data()

# Sidebar filter
st.sidebar.header("Filter by Year Range")
start_year, end_year = st.sidebar.select_slider(
    "Select range:",
    options=list(data['Year']),
    value=(data['Year'].min(), data['Year'].max())
)

# Filtered data
filtered_data = data[(data['Year'] >= start_year) & (data['Year'] <= end_year)]

# Show summary metrics
st.subheader(f"GDP Summary ({start_year}–{end_year})")
st.metric("Highest GDP", f"${filtered_data['GDP'].max():,.0f}")
st.metric("Lowest GDP", f"${filtered_data['GDP'].min():,.0f}")

# Line chart
st.subheader("📈 GDP Over Time")
fig, ax = plt.subplots()
ax.plot(filtered_data['Year'], filtered_data['GDP'], color='teal', marker='o')
ax.set_xlabel("Year")
ax.set_ylabel("GDP (US$)")
ax.set_title("Sri Lanka's GDP (Current US$)")
plt.xticks(rotation=45)
st.pyplot(fig)

# Show data table
with st.expander("🔎 View Data Table"):
    st.dataframe(filtered_data, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("**Data Source:** [World Bank Open Data](https://data.worldbank.org/country/sri-lanka)")
