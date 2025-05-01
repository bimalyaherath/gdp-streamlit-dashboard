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
    df = pd.read_csv("GDP (current US$)_SL - 1960–2023.csv", header=None)
    df = df.T
    df.columns = df.iloc[0]
    df = df[1:]
    df = df.reset_index()
    df.columns = ['Year', 'GDP']
    df['Year'] = df['Year'].astype(str)
    df['GDP'] = df['GDP'].astype(float)
    return df

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
