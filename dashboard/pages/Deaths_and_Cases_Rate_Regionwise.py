import streamlit as st
import pandas as pd
import plotly.express as px

us_df = pd.read_csv("../data/OxCGRT_fullwithnotes_USA_v1.csv")
us_df = us_df[['CountryName', 'RegionName', 'RegionCode', 'Date', 'ConfirmedCases', 'ConfirmedDeaths']]
us_df = us_df.dropna()
us_df['Date'] = pd.to_datetime(us_df['Date'], format='%Y%m%d')
us_df["RegionCode"] = us_df['RegionCode'].str[3:]

chosen_date = pd.to_datetime("2021-01-01", format='%Y-%m-%d')
us_df = us_df[us_df["Date"] == chosen_date]
us_df_plot = us_df[["RegionCode", "ConfirmedCases"]]
us_df_plot

# Sample data (replace with your actual DataFrame)
data = pd.DataFrame({
    'RegionCode': ['AK', 'WY', 'FL', 'CA', 'NY'],
    'Count': [10, 20, 30, 40, 50]
})

# Plotly Choropleth Map
fig = px.choropleth(
    data_frame=us_df_plot,
    locations='RegionCode',
    locationmode="USA-states",  # This specifies that the location mode is U.S. states
    color='ConfirmedCases',
    color_continuous_scale="Viridis",  # Choose any color scale you like
    scope="usa",  # Focus on the USA
    labels={'ConfirmedCases': 'Count'},
    range_color=(0, max_value),
)

# Display the Plotly chart in Streamlit
st.plotly_chart(fig)


# import streamlit as st
# import pandas as pd

# us_deaths = pd.read_csv("../data/OxCGRT_fullwithnotes_USA_v1.csv")

# print(len(us_deaths))