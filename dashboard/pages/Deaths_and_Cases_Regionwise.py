import pandas as pd
import plotly.express as px
import streamlit as st
import requests
from datetime import datetime

# Load U.S. data
us_df = pd.read_csv("../data/OxCGRT_fullwithnotes_USA_v1.csv")
us_df = us_df[['RegionCode', 'Date', 'ConfirmedCases', 'ConfirmedDeaths']].dropna()
us_df['Date'] = pd.to_datetime(us_df['Date'], format='%Y%m%d')
us_df['RegionCode'] = us_df['RegionCode'].str[3:]  # Remove 'US_' prefix

# Population data for each U.S. state
state_population = {
    'AL': 5024279, 'AK': 733391, 'AZ': 7151502, 'AR': 3011524, 'CA': 39538223,
    'CO': 5773714, 'CT': 3605944, 'DE': 989948, 'FL': 21538187, 'GA': 10711908,
    'HI': 1455271, 'ID': 1839106, 'IL': 12812508, 'IN': 6785528, 'IA': 3190369,
    'KS': 2937880, 'KY': 4505836, 'LA': 4657757, 'ME': 1362359, 'MD': 6177224,
    'MA': 7029917, 'MI': 10077331, 'MN': 5706494, 'MS': 2961279, 'MO': 6154913,
    'MT': 1084225, 'NE': 1961504, 'NV': 3104614, 'NH': 1377529, 'NJ': 9288994,
    'NM': 2117522, 'NY': 20201249, 'NC': 10439388, 'ND': 779094, 'OH': 11799448,
    'OK': 3959353, 'OR': 4237256, 'PA': 13002700, 'RI': 1097379, 'SC': 5118425,
    'SD': 886667, 'TN': 6910840, 'TX': 29145505, 'UT': 3271616, 'VT': 643077,
    'VA': 8631393, 'WA': 7693612, 'WV': 1793716, 'WI': 5893718, 'WY': 576851
}

# Normalize U.S. data
us_df['CasesPer100K'] = us_df.apply(
    lambda row: (row['ConfirmedCases'] / state_population.get(row['RegionCode'], 1)) * 100000, axis=1
)
us_df['DeathsPer100K'] = us_df.apply(
    lambda row: (row['ConfirmedDeaths'] / state_population.get(row['RegionCode'], 1)) * 100000, axis=1
)

# Map state codes to state names
state_codes = {
    'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas', 'CA': 'California',
    'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware', 'FL': 'Florida', 'GA': 'Georgia',
    'HI': 'Hawaii', 'ID': 'Idaho', 'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa',
    'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MD': 'Maryland',
    'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi', 'MO': 'Missouri',
    'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada', 'NH': 'New Hampshire', 'NJ': 'New Jersey',
    'NM': 'New Mexico', 'NY': 'New York', 'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio',
    'OK': 'Oklahoma', 'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island', 'SC': 'South Carolina',
    'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah', 'VT': 'Vermont',
    'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia', 'WI': 'Wisconsin', 'WY': 'Wyoming'
}
us_df['StateName'] = us_df['RegionCode'].map(state_codes)

# Load GeoJSON for U.S. states
us_geojson_url = 'https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json'
response_us = requests.get(us_geojson_url)
us_geojson = response_us.json()

# Adjust GeoJSON properties for U.S. states
for feature in us_geojson['features']:
    feature['properties']['StateName'] = feature['properties']['name']

# Load Canada data
can_df = pd.read_csv("../data/OxCGRT_fullwithnotes_CAN_v1.csv")
can_df = can_df[['RegionCode', 'Date', 'ConfirmedCases', 'ConfirmedDeaths']].dropna()
can_df['Date'] = pd.to_datetime(can_df['Date'], format='%Y%m%d')
can_df['RegionCode'] = can_df['RegionCode'].str[4:]  # Remove 'CAN_' prefix

# Population data for Canadian provinces (estimates)
province_population = {
    'AB': 4413146, 'BC': 5110917, 'MB': 1377517, 'NB': 789225, 'NL': 521365,
    'NS': 979351, 'NT': 45161, 'NU': 39097, 'ON': 14734014, 'PE': 164318,
    'QC': 8537674, 'SK': 1177884, 'YT': 42176
}

# Normalize Canada data
can_df['CasesPer100K'] = can_df.apply(
    lambda row: (row['ConfirmedCases'] / province_population.get(row['RegionCode'], 1)) * 100000, axis=1
)
can_df['DeathsPer100K'] = can_df.apply(
    lambda row: (row['ConfirmedDeaths'] / province_population.get(row['RegionCode'], 1)) * 100000, axis=1
)

# Map province codes to province names
province_codes = {
    'AB': 'Alberta',
    'BC': 'British Columbia',
    'MB': 'Manitoba',
    'NB': 'New Brunswick',
    'NL': 'Newfoundland and Labrador',
    'NS': 'Nova Scotia',
    'NT': 'Northwest Territories',
    'NU': 'Nunavut',
    'ON': 'Ontario',
    'PE': 'Prince Edward Island',
    'QC': 'Quebec',
    'SK': 'Saskatchewan',
    'YT': 'Yukon'
}
can_df['ProvinceName'] = can_df['RegionCode'].map(province_codes)

# Load GeoJSON for Canadian provinces
canada_geojson_url = 'https://raw.githubusercontent.com/codeforgermany/click_that_hood/main/public/data/canada.geojson'
response_canada = requests.get(canada_geojson_url)
canada_geojson = response_canada.json()

# Adjust GeoJSON properties for Canadian provinces
for feature in canada_geojson['features']:
    province_name = feature['properties']['name']
    # Ensure names match between DataFrame and GeoJSON
    feature['properties']['ProvinceName'] = province_name

# Adjust Province Names in can_df to match GeoJSON if necessary
can_df['ProvinceName'] = can_df['ProvinceName'].replace({
    'NL': 'Newfoundland and Labrador',
    'PE': 'Prince Edward Island',
    'NT': 'Northwest Territories',
    'YT': 'Yukon',
    # Add any other adjustments if needed
})

st.title("Regionwise COVID-19 Cumulative Case Counts Per 100K Over Time: U.S. vs Canada")

# Define the date range for the slider
min_date = pd.to_datetime("2020-01-01")
max_date = pd.to_datetime("2022-12-31")

# Create a date slider
chosen_date_case = st.slider(
    "Date",
    min_value=datetime(2020, 1, 1),
    max_value=datetime(2022, 12, 31),
    value=datetime(2021, 1, 1),
    format="MM/DD/YYYY",
    key="slider_for_chosen_date_case",
)

# Choose a specific date for the maps
# chosen_date = pd.to_datetime("2021-01-01")
us_df_case = us_df[us_df['Date'] == chosen_date_case]
can_df_case = can_df[can_df['Date'] == chosen_date_case]

# Plotly Choropleth Mapbox for U.S. Cases Per 100K
fig_us_case = px.choropleth_mapbox(
    us_df_case,
    geojson=us_geojson,
    locations='StateName',
    featureidkey='properties.StateName',
    color='CasesPer100K',
    color_continuous_scale='Viridis',
    mapbox_style='carto-positron',
    zoom=2.5,
    center={'lat': 37.0902, 'lon': -95.7129},
    opacity=0.5,
    labels={'CasesPer100K': 'Cases Per 100K'},
    range_color=(0, 40000),
)
fig_us_case.update_layout(margin={'r':0, 't':0, 'l':0, 'b':0})
st.plotly_chart(fig_us_case)

# Plotly Choropleth Mapbox for Canada Cases Per 100K
fig_can_case = px.choropleth_mapbox(
    can_df_case,
    geojson=canada_geojson,
    locations='ProvinceName',
    featureidkey='properties.ProvinceName',
    color='CasesPer100K',
    color_continuous_scale='Viridis',
    mapbox_style='carto-positron',
    zoom=1.25,
    center={'lat': 72, 'lon': -97},
    opacity=0.5,
    labels={'CasesPer100K': 'Cases Per 100K'},
    range_color=(0, 40000),
)
fig_can_case.update_layout(margin={'r':0, 't':0, 'l':0, 'b':0})
st.plotly_chart(fig_can_case)

st.title("Regionwise COVID-19 Cumulative Death Counts Per 100K Over Time: U.S. vs Canada")

# Create a date slider
chosen_date_death = st.slider(
    "Date",
    min_value=datetime(2020, 1, 1),
    max_value=datetime(2022, 12, 31),
    value=datetime(2021, 1, 1),
    format="MM/DD/YYYY",
    key="slider_for_chosen_date_death",
)

# Choose a specific date for the maps
# chosen_date = pd.to_datetime("2021-01-01")
us_df_death = us_df[us_df['Date'] == chosen_date_death]
can_df_death = can_df[can_df['Date'] == chosen_date_death]

# Plotly Choropleth Mapbox for U.S. Deaths Per 100K
fig_us_death = px.choropleth_mapbox(
    us_df_death,
    geojson=us_geojson,
    locations='StateName',
    featureidkey='properties.StateName',
    color='DeathsPer100K',
    color_continuous_scale='Viridis',
    mapbox_style='carto-positron',
    zoom=2.5,
    center={'lat': 37.0902, 'lon': -95.7129},
    opacity=0.5,
    labels={'DeathsPer100K': 'Deaths Per 100K'},
    range_color=(0, 500),
)
fig_us_death.update_layout(margin={'r':0, 't':0, 'l':0, 'b':0})
st.plotly_chart(fig_us_death)



# Plotly Choropleth Mapbox for Canada Deaths Per 100K
fig_can_death = px.choropleth_mapbox(
    can_df_death,
    geojson=canada_geojson,
    locations='ProvinceName',
    featureidkey='properties.ProvinceName',
    color='DeathsPer100K',
    color_continuous_scale='Viridis',
    mapbox_style='carto-positron',
    zoom=1.25,
    center={'lat': 72, 'lon': -97},
    opacity=0.5,
    labels={'DeathsPer100K': 'Deaths Per 100K'},
    range_color=(0, 500),
)
fig_can_death.update_layout(margin={'r':0, 't':0, 'l':0, 'b':0})
st.plotly_chart(fig_can_death)
