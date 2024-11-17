import streamlit as st
import pandas as pd
import plotly.express as px

# Load and prepare U.S. data
us_df = pd.read_csv("../data/OxCGRT_fullwithnotes_USA_v1.csv")
us_df = us_df[us_df['Jurisdiction'] == "NAT_TOTAL"]
us_df = us_df[['Date', 'ConfirmedCases', 'ConfirmedDeaths']]
us_df = us_df.dropna()
us_df['Date'] = pd.to_datetime(us_df['Date'], format='%Y%m%d')
us_population = 331_000_000  # U.S. population
us_df['CasesPerCapita'] = us_df['ConfirmedCases'] / us_population * 100_000
us_df['DeathsPerCapita'] = us_df['ConfirmedDeaths'] / us_population * 100_000
us_df['Country'] = 'US'

# Calculate daily case and death rates for U.S.
us_df['DailyCaseRate'] = us_df['ConfirmedCases'].diff().fillna(0)
us_df['DailyDeathRate'] = us_df['ConfirmedDeaths'].diff().fillna(0)
us_df['DailyCaseRate'] = us_df['DailyCaseRate'].apply(lambda x: max(0, x) / us_population * 100_000)
us_df['DailyDeathRate'] = us_df['DailyDeathRate'].apply(lambda x: max(0, x) / us_population * 100_000)

# Load and prepare Canada data
can_df = pd.read_csv("../data/OxCGRT_fullwithnotes_CAN_v1.csv")
can_df = can_df[can_df['Jurisdiction'] == "NAT_TOTAL"]
can_df = can_df[['Date', 'ConfirmedCases', 'ConfirmedDeaths']]
can_df = can_df.dropna()
can_df['Date'] = pd.to_datetime(can_df['Date'], format='%Y%m%d')
can_population = 38_000_000  # U.S. population
can_df['CasesPerCapita'] = can_df['ConfirmedCases'] / can_population * 100_000
can_df['DeathsPerCapita'] = can_df['ConfirmedDeaths'] / can_population * 100_000
can_df['Country'] = 'CAN'

# Calculate daily case and death rates for U.S.
can_df['DailyCaseRate'] = can_df['ConfirmedCases'].diff().fillna(0)
can_df['DailyDeathRate'] = can_df['ConfirmedDeaths'].diff().fillna(0)
can_df['DailyCaseRate'] = can_df['DailyCaseRate'].apply(lambda x: max(0, x) / can_population * 100_000)
can_df['DailyDeathRate'] = can_df['DailyDeathRate'].apply(lambda x: max(0, x) / can_population * 100_000)

# Combine U.S. and Canada data
combined_df = pd.concat([us_df, can_df])

# Streamlit title and description
st.header("COVID-19 Cumulative Case and Death Counts Per 100K Over Time: U.S. vs Canada")

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

st.header("COVID-19 Daily Case and Death Counts Per 100K Population Over Time: U.S. vs Canada")

# Plot DailyCaseRate for both countries (scatter plot)
fig_daily_cases = px.scatter(combined_df, x='Date', y='DailyCaseRate', color='Country', 
                             title='Daily COVID-19 Case Count Per 100K Population: U.S. vs Canada', 
                             labels={'DailyCaseRate': 'Daily Case Count Per 100K Population'})
st.plotly_chart(fig_daily_cases)

# Plot DailyDeathRate for both countries (scatter plot)
fig_daily_deaths = px.scatter(combined_df, x='Date', y='DailyDeathRate', color='Country', 
                              title='Daily COVID-19 Death Count Per 100K Population: U.S. vs Canada', 
                              labels={'DailyDeathRate': 'Daily Death Count Per 100K Population'})
st.plotly_chart(fig_daily_deaths)

st.header("Distribution of Daily Case and Death Count per 100K Population: U.S. vs Canada")

# Plot boxplot of DailyCaseRate
fig_box_cases = px.box(combined_df, x='Country', y='DailyCaseRate',
                       title='Boxplot of Daily COVID-19 Case Count Per 100K Population: U.S. vs Canada',
                       labels={'DailyCaseRate': 'Daily Case Count Per 100K Population'})
st.plotly_chart(fig_box_cases)

# Plot boxplot of DailyDeathRate
fig_box_deaths = px.box(combined_df, x='Country', y='DailyDeathRate',
                        title='Boxplot of Daily COVID-19 Death Count Per 100K Population: U.S. vs Canada',
                        labels={'DailyDeathRate': 'Daily Death Count Per 100K Population'})
st.plotly_chart(fig_box_deaths)


