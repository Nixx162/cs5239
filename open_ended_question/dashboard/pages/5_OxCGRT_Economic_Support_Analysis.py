import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.stats import spearmanr
import dcor

us_df = pd.read_csv("../data/OxCGRT_fullwithnotes_USA_v1.csv")
us_df = us_df[us_df["Jurisdiction"] == "NAT_TOTAL"]
us_population = 331_000_000 
us_df['DailyCaseRate'] = us_df['ConfirmedCases'].diff().fillna(0)
us_df['DailyDeathRate'] = us_df['ConfirmedDeaths'].diff().fillna(0)
us_df['DailyCaseRate'] = us_df['DailyCaseRate'].apply(lambda x: max(0, x) / us_population * 100_000)
us_df['DailyDeathRate'] = us_df['DailyDeathRate'].apply(lambda x: max(0, x) / us_population * 100_000)

can_df = pd.read_csv("../data/OxCGRT_fullwithnotes_CAN_v1.csv")
can_df = can_df[can_df["Jurisdiction"] == "NAT_TOTAL"]
can_population = 331_000_000 
can_df['DailyCaseRate'] = can_df['ConfirmedCases'].diff().fillna(0)
can_df['DailyDeathRate'] = can_df['ConfirmedDeaths'].diff().fillna(0)
can_df['DailyCaseRate'] = can_df['DailyCaseRate'].apply(lambda x: max(0, x) / can_population * 100_000)
can_df['DailyDeathRate'] = can_df['DailyDeathRate'].apply(lambda x: max(0, x) / can_population * 100_000)

index_to_scale = [
    "E3_Fiscal measures",
    "E4_International support",
]
for idx in index_to_scale:
    us_df[idx + " Per 100K Population"] = us_df[idx] / us_population * 100_000
    can_df[idx + " Per 100K Population"] = can_df[idx] / can_population * 100_000

def spearmanr_correlation(df1, df2, lags):
    corrs = []
    for lag in lags:
        # Shift df2 without modifying it in place
        shifted_df2 = df2.shift(-lag)
        
        # Combine df1 and shifted_df2 into a single DataFrame
        combined = pd.concat([df1, shifted_df2], axis=1)
        combined.columns = ['df1', 'df2']
        
        # Drop rows with NaN values
        combined = combined.dropna()
        
        corr, _ = spearmanr(combined['df1'], combined['df2'])
        corrs.append(corr)

    return corrs

def spearmanr_plot(selected_index, lags):
    df1 = us_df[selected_index]
    df2 = us_df['DailyCaseRate']
    df3 = us_df['DailyDeathRate']
    lagged_correlations_cases = spearmanr_correlation(df1, df2, lags)
    lagged_correlations_deaths = spearmanr_correlation(df1, df3, lags)

    us_df_cases = pd.DataFrame({"Lag": lags, "Correlation": lagged_correlations_cases})
    us_df_deaths = pd.DataFrame({"Lag": lags, "Correlation": lagged_correlations_deaths})

    df1 = can_df[selected_index]
    df2 = can_df['DailyCaseRate']
    df3 = can_df['DailyDeathRate']
    lagged_correlations_cases = spearmanr_correlation(df1, df2, lags)
    lagged_correlations_deaths = spearmanr_correlation(df1, df3, lags)

    can_df_cases = pd.DataFrame({"Lag": lags, "Correlation": lagged_correlations_cases})
    can_df_deaths = pd.DataFrame({"Lag": lags, "Correlation": lagged_correlations_deaths})

    # Plotly visualization for DailyCaseRate
    fig_cases = go.Figure()
    fig_cases.add_trace(go.Scatter(x=us_df_cases["Lag"], y=us_df_cases["Correlation"], name="US"))
    fig_cases.add_trace(go.Scatter(x=can_df_cases["Lag"], y=can_df_cases["Correlation"], name="Canada"))
    fig_cases.update_layout(title=f"Spearman Correlation of {selected_index} and Lagged Daily Case Count",
                            xaxis_title="Lag (days)",
                            yaxis_title="Spearman Correlation",
                            )
    st.plotly_chart(fig_cases)

    # Plotly visualization for DailyDeathRate
    fig_deaths = go.Figure()
    fig_deaths.add_trace(go.Scatter(x=us_df_deaths["Lag"], y=us_df_deaths["Correlation"], name="US"))
    fig_deaths.add_trace(go.Scatter(x=can_df_deaths["Lag"], y=can_df_deaths["Correlation"], name="Canada"))
    fig_deaths.update_layout(title=f"Spearman Correlation of {selected_index} and Lagged Daily Death Count",
                            xaxis_title="Lag (days)",
                            yaxis_title="Spearman Correlation",
                            )
    st.plotly_chart(fig_deaths)

st.header("Analysis of the Effects of E1 Income Support and E2 Debt or Contract Relief for Households")

spearmanr_plot("E1_Income support", list(range(0, 481, 60)))

spearmanr_plot("E2_Debt/contract relief", list(range(0, 481, 60)))

def dcor_correlation(df1, df2, lags):
    corrs = []
    for lag in lags:
        # Shift df2 without modifying it in place
        shifted_df2 = df2.shift(-lag)
        
        # Combine df1 and shifted_df2 into a single DataFrame
        combined = pd.concat([df1, shifted_df2], axis=1)
        combined.columns = ['df1', 'df2']
        
        # Drop rows with NaN values
        combined = combined.dropna()
        
        corr = dcor.distance_correlation(combined['df1'], combined['df2'])
        corrs.append(corr)

    return corrs

def dcor_plot(selected_index, lags):
    df1 = us_df[selected_index]
    df2 = us_df['DailyCaseRate']
    df3 = us_df['DailyDeathRate']
    lagged_correlations_cases = dcor_correlation(df1, df2, lags)
    lagged_correlations_deaths = dcor_correlation(df1, df3, lags)

    us_df_cases = pd.DataFrame({"Lag": lags, "Correlation": lagged_correlations_cases})
    us_df_deaths = pd.DataFrame({"Lag": lags, "Correlation": lagged_correlations_deaths})

    df1 = can_df[selected_index]
    df2 = can_df['DailyCaseRate']
    df3 = can_df['DailyDeathRate']
    lagged_correlations_cases = dcor_correlation(df1, df2, lags)
    lagged_correlations_deaths = dcor_correlation(df1, df3, lags)

    can_df_cases = pd.DataFrame({"Lag": lags, "Correlation": lagged_correlations_cases})
    can_df_deaths = pd.DataFrame({"Lag": lags, "Correlation": lagged_correlations_deaths})

    # Plotly visualization for DailyCaseRate
    fig_cases = go.Figure()
    fig_cases.add_trace(go.Scatter(x=us_df_cases["Lag"], y=us_df_cases["Correlation"], name="US"))
    fig_cases.add_trace(go.Scatter(x=can_df_cases["Lag"], y=can_df_cases["Correlation"], name="Canada"))
    fig_cases.update_layout(title=f"Distance Correlation of {selected_index} and Lagged Daily Case Count",
                            xaxis_title="Lag (days)",
                            yaxis_title="Distance Correlation",
                            )
    st.plotly_chart(fig_cases)

    # Plotly visualization for DailyDeathRate
    fig_deaths = go.Figure()
    fig_deaths.add_trace(go.Scatter(x=us_df_deaths["Lag"], y=us_df_deaths["Correlation"], name="US"))
    fig_deaths.add_trace(go.Scatter(x=can_df_deaths["Lag"], y=can_df_deaths["Correlation"], name="Canada"))
    fig_deaths.update_layout(title=f"Distance Correlation of {selected_index} and Lagged Daily Death Count",
                            xaxis_title="Lag (days)",
                            yaxis_title="Distance Correlation",
                            )
    st.plotly_chart(fig_deaths)

st.header("Analysis of the Effects of E3 Fiscal Measures Per 100K Population and E4 Providing Support to Other Countries Per 100K Population")

dcor_plot("E3_Fiscal measures Per 100K Population", list(range(0, 481, 60)))

dcor_plot("E4_International support Per 100K Population", list(range(0, 481, 60)))