import streamlit as st
import pandas as pd
import plotly.express as px

rolling_window = 7

# --- Load and Prepare U.S. Data ---
us_population = 331_000_000
us_df = pd.read_csv("../data/OxCGRT_fullwithnotes_USA_v1.csv")

# Filter for national data and select relevant columns
us_nat_df = us_df[us_df["Jurisdiction"] == "NAT_TOTAL"][[
    "Date", "GovernmentResponseIndex_WeightedAverage", "ContainmentHealthIndex_WeightedAverage",
    "EconomicSupportIndex", "StringencyIndex_WeightedAverage", "ConfirmedCases", "ConfirmedDeaths"
]]

us_nat_df["Date"] = pd.to_datetime(us_nat_df['Date'], format='%Y%m%d')
us_nat_df = us_nat_df.sort_values(by="Date", ascending=True)

# Calculate rates per 100,000 population
us_nat_df["ConfirmedCases"] = us_nat_df["ConfirmedCases"] / us_population * 100_000
us_nat_df["ConfirmedDeaths"] = us_nat_df["ConfirmedDeaths"] / us_population * 100_000

# Calculate daily rates
us_nat_df["DailyCaseRate"] = us_nat_df["ConfirmedCases"].diff().fillna(0)
us_nat_df["DailyDeathRate"] = us_nat_df["ConfirmedDeaths"].diff().fillna(0)

# Select relevant columns
us_nat_df = us_nat_df[[
    "GovernmentResponseIndex_WeightedAverage", "ContainmentHealthIndex_WeightedAverage",
    "EconomicSupportIndex", "StringencyIndex_WeightedAverage", "DailyCaseRate", "DailyDeathRate"
]].rolling(window=rolling_window).mean()

# --- Load and Prepare Canada Data ---
can_population = 38_000_000
can_df = pd.read_csv("../data/OxCGRT_fullwithnotes_CAN_v1.csv")

# Filter for national data and select relevant columns
can_nat_df = can_df[can_df["Jurisdiction"] == "NAT_TOTAL"][[
    "Date", "GovernmentResponseIndex_WeightedAverage", "ContainmentHealthIndex_WeightedAverage",
    "EconomicSupportIndex", "StringencyIndex_WeightedAverage", "ConfirmedCases", "ConfirmedDeaths"
]]

can_nat_df["Date"] = pd.to_datetime(can_nat_df['Date'], format='%Y%m%d')
can_nat_df = can_nat_df.sort_values(by="Date", ascending=True)

# Calculate rates per 100,000 population
can_nat_df["ConfirmedCases"] = can_nat_df["ConfirmedCases"] / can_population * 100_000
can_nat_df["ConfirmedDeaths"] = can_nat_df["ConfirmedDeaths"] / can_population * 100_000

# Calculate daily rates
can_nat_df["DailyCaseRate"] = can_nat_df["ConfirmedCases"].diff().fillna(0)
can_nat_df["DailyDeathRate"] = can_nat_df["ConfirmedDeaths"].diff().fillna(0)

# Select relevant columns
can_nat_df = can_nat_df[[
    "GovernmentResponseIndex_WeightedAverage", "ContainmentHealthIndex_WeightedAverage",
    "EconomicSupportIndex", "StringencyIndex_WeightedAverage", "DailyCaseRate", "DailyDeathRate"
]].rolling(window=rolling_window).mean()

# rolling_indexes = ["GovernmentResponseIndex_WeightedAverage", "ContainmentHealthIndex_WeightedAverage", "EconomicSupportIndex", "StringencyIndex_WeightedAverage", "DailyCaseRate", "DailyDeathRate"]
# us_nat_df[rolling_indexes] = us_nat_df[rolling_indexes].rolling(window=7).mean()

# --- Function to Compute Lagged Correlations ---
def compute_lagged_correlations(data, max_lag=720):
    indices = [
        'GovernmentResponseIndex_WeightedAverage',
        'ContainmentHealthIndex_WeightedAverage',
        'EconomicSupportIndex',
        'StringencyIndex_WeightedAverage'
    ]
    rates = ['DailyCaseRate', 'DailyDeathRate']
    lagged_correlations_cases = {}
    lagged_correlations_deaths = {}
    
    for lag in range(max_lag + 1):
        lagged_data = data.copy()
        for rate in rates:
            lagged_data[f'{rate}_lag{lag}'] = lagged_data[rate].shift(-lag)  # Shift negative for future values
        
        # Drop rows with NaN values introduced by lagging
        lagged_data = lagged_data.dropna()
        
        # Calculate correlations
        for index in indices:
            for rate in rates:
                lagged_corr = lagged_data[index].corr(lagged_data[f'{rate}_lag{lag}'])
                if rate == 'DailyCaseRate':
                    lagged_correlations_cases.setdefault(index, []).append(lagged_corr)
                else:
                    lagged_correlations_deaths.setdefault(index, []).append(lagged_corr)
    return lagged_correlations_cases, lagged_correlations_deaths

# --- Compute Lagged Correlations for U.S. ---
us_lagged_correlations_cases, us_lagged_correlations_deaths = compute_lagged_correlations(us_nat_df)

# --- Compute Lagged Correlations for Canada ---
can_lagged_correlations_cases, can_lagged_correlations_deaths = compute_lagged_correlations(can_nat_df)

# --- Create DataFrames for Plotting ---
us_case_df = pd.DataFrame(us_lagged_correlations_cases)
us_death_df = pd.DataFrame(us_lagged_correlations_deaths)
can_case_df = pd.DataFrame(can_lagged_correlations_cases)
can_death_df = pd.DataFrame(can_lagged_correlations_deaths)

# --- Plot Correlations for U.S. ---
st.header("U.S. Correlation of Policy Indexes with Lagged Daily Case Rates")

# Prepare data for plotting
us_case_df['Lag'] = range(len(us_case_df))
us_case_melted = us_case_df.melt(id_vars='Lag', var_name='Index', value_name='Correlation')

# Plot using Plotly Express
fig_us_cases = px.line(
    us_case_melted,
    x='Lag',
    y='Correlation',
    color='Index',
    title='U.S. - Correlation between Policy Indexes and Lagged Daily Case Rates',
    labels={'Lag': 'Lag (Days)', 'Correlation': 'Correlation Coefficient'}
)
st.plotly_chart(fig_us_cases)

# --- Plot Correlations for Canada ---
st.header("Canada Correlation of Policy Indexes with Lagged Daily Case Rates")

can_case_df['Lag'] = range(len(can_case_df))
can_case_melted = can_case_df.melt(id_vars='Lag', var_name='Index', value_name='Correlation')

fig_can_cases = px.line(
    can_case_melted,
    x='Lag',
    y='Correlation',
    color='Index',
    title='Canada - Correlation between Policy Indexes and Lagged Daily Case Rates',
    labels={'Lag': 'Lag (Days)', 'Correlation': 'Correlation Coefficient'}
)
st.plotly_chart(fig_can_cases)


st.header("U.S. Correlation of Policy Indexes with Lagged Daily Death Rates")

us_death_df['Lag'] = range(len(us_death_df))
us_death_melted = us_death_df.melt(id_vars='Lag', var_name='Index', value_name='Correlation')

fig_us_deaths = px.line(
    us_death_melted,
    x='Lag',
    y='Correlation',
    color='Index',
    title='U.S. - Correlation between Policy Indexes and Lagged Daily Death Rates',
    labels={'Lag': 'Lag (Days)', 'Correlation': 'Correlation Coefficient'}
)
st.plotly_chart(fig_us_deaths)

st.header("Canada Correlation of Policy Indexes with Lagged Daily Death Rates")

can_death_df['Lag'] = range(len(can_death_df))
can_death_melted = can_death_df.melt(id_vars='Lag', var_name='Index', value_name='Correlation')

fig_can_deaths = px.line(
    can_death_melted,
    x='Lag',
    y='Correlation',
    color='Index',
    title='Canada - Correlation between Policy Indexes and Lagged Daily Death Rates',
    labels={'Lag': 'Lag (Days)', 'Correlation': 'Correlation Coefficient'}
)
st.plotly_chart(fig_can_deaths)