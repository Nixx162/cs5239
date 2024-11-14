import streamlit as st
import pandas as pd
import plotly.express as px

# Load and prepare U.S. data
us_df = pd.read_csv("../data/OxCGRT_fullwithnotes_USA_v1.csv")
us_df = us_df[['CountryName', 'Date', 'ConfirmedCases', 'ConfirmedDeaths']]
us_df = us_df.dropna()
us_df['Date'] = pd.to_datetime(us_df['Date'], format='%Y%m%d')
us_df_grouped = us_df.groupby('Date')[['ConfirmedCases', 'ConfirmedDeaths']].sum().reset_index()
us_population = 331_000_000  # U.S. population
us_df_grouped['CasesPerCapita'] = us_df_grouped['ConfirmedCases'] / us_population * 100_000
us_df_grouped['DeathsPerCapita'] = us_df_grouped['ConfirmedDeaths'] / us_population * 100_000
us_df_grouped['Country'] = 'US'

# Calculate daily case and death rates for U.S.
us_df_grouped['DailyCaseRate'] = us_df_grouped['ConfirmedCases'] - us_df_grouped['ConfirmedCases'].shift(1)
us_df_grouped['DailyDeathRate'] = us_df_grouped['ConfirmedDeaths'] - us_df_grouped['ConfirmedDeaths'].shift(1)
us_df_grouped['DailyCaseRate'] = us_df_grouped['DailyCaseRate'].apply(lambda x: max(0, x) / us_population * 100_000)
us_df_grouped['DailyDeathRate'] = us_df_grouped['DailyDeathRate'].apply(lambda x: max(0, x) / us_population * 100_000)

# Load and prepare Canada data
can_df = pd.read_csv("../data/OxCGRT_fullwithnotes_CAN_v1.csv")
can_df = can_df[['CountryName', 'Date', 'ConfirmedCases', 'ConfirmedDeaths']]
can_df = can_df.dropna()
can_df['Date'] = pd.to_datetime(can_df['Date'], format='%Y%m%d')
can_df_grouped = can_df.groupby('Date')[['ConfirmedCases', 'ConfirmedDeaths']].sum().reset_index()
can_population = 38_000_000  # Canada population
can_df_grouped['CasesPerCapita'] = can_df_grouped['ConfirmedCases'] / can_population * 100_000
can_df_grouped['DeathsPerCapita'] = can_df_grouped['ConfirmedDeaths'] / can_population * 100_000
can_df_grouped['Country'] = 'Canada'

# Calculate daily case and death rates for Canada
can_df_grouped['DailyCaseRate'] = can_df_grouped['ConfirmedCases'] - can_df_grouped['ConfirmedCases'].shift(1)
can_df_grouped['DailyDeathRate'] = can_df_grouped['ConfirmedDeaths'] - can_df_grouped['ConfirmedDeaths'].shift(1)
can_df_grouped['DailyCaseRate'] = can_df_grouped['DailyCaseRate'].apply(lambda x: max(0, x) / can_population * 100_000)
can_df_grouped['DailyDeathRate'] = can_df_grouped['DailyDeathRate'].apply(lambda x: max(0, x) / can_population * 100_000)


# Combine U.S. and Canada data
combined_df = pd.concat([us_df_grouped, can_df_grouped])

# Streamlit title and description
st.title("COVID-19 Cumulative Case and Death Counts Per 100K Over Time: U.S. vs Canada")

# Plot CasesPerCapita for both countries
fig_cases = px.line(combined_df, x='Date', y='CasesPerCapita', color='Country', 
                    title='Confirmed COVID-19 Cases Per 100K Population Over Time: U.S. vs Canada', 
                    labels={'CasesPerCapita': 'Cases Per 100K Population'})
st.plotly_chart(fig_cases)

# Plot DeathsPerCapita for both countries
fig_deaths = px.line(combined_df, x='Date', y='DeathsPerCapita', color='Country', 
                     title='COVID-19 Deaths Per 100K Population Over Time: U.S. vs Canada', 
                     labels={'DeathsPerCapita': 'Deaths Per 100K Population'})
st.plotly_chart(fig_deaths)

st.title("COVID-19 Daily Case and Death Rates Per 100K Over Time: U.S. vs Canada")

# Plot DailyCaseRate for both countries (scatter plot)
fig_daily_cases = px.scatter(combined_df, x='Date', y='DailyCaseRate', color='Country', 
                             title='Daily COVID-19 Case Rate Per 100K Population: U.S. vs Canada', 
                             labels={'DailyCaseRate': 'Daily Case Rate Per 100K Population'})
st.plotly_chart(fig_daily_cases)

# Plot DailyDeathRate for both countries (scatter plot)
fig_daily_deaths = px.scatter(combined_df, x='Date', y='DailyDeathRate', color='Country', 
                              title='Daily COVID-19 Death Rate Per 100K Population: U.S. vs Canada', 
                              labels={'DailyDeathRate': 'Daily Death Rate Per 100K Population'})
st.plotly_chart(fig_daily_deaths)
