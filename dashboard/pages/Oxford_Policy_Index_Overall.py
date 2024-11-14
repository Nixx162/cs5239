import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Load and prepare U.S. data
us_df = pd.read_csv("../data/OxCGRT_fullwithnotes_USA_v1.csv")

# Select required columns, including the indexes
us_df = us_df[['CountryName', 'Date', 'ConfirmedCases', 'ConfirmedDeaths',
               'GovernmentResponseIndex_WeightedAverage', 'StringencyIndex_WeightedAverage',
               'ContainmentHealthIndex_WeightedAverage', 'EconomicSupportIndex']]
us_df = us_df.dropna()
us_df['Date'] = pd.to_datetime(us_df['Date'], format='%Y%m%d')

# Group by Date and calculate mean for indexes, sum for cases and deaths
us_df_grouped = us_df.groupby('Date').agg({
    'ConfirmedCases': 'sum',
    'ConfirmedDeaths': 'sum',
    'GovernmentResponseIndex_WeightedAverage': 'mean',
    'StringencyIndex_WeightedAverage': 'mean',
    'ContainmentHealthIndex_WeightedAverage': 'mean',
    'EconomicSupportIndex': 'mean'
}).reset_index()
us_population = 331_000_000  # U.S. population
us_df_grouped['Country'] = 'US'

# Calculate daily case and death rates for U.S.
us_df_grouped['DailyCaseRate'] = us_df_grouped['ConfirmedCases'].diff().fillna(0)
us_df_grouped['DailyDeathRate'] = us_df_grouped['ConfirmedDeaths'].diff().fillna(0)
us_df_grouped['DailyCaseRate'] = us_df_grouped['DailyCaseRate'].apply(lambda x: max(0, x) / us_population * 100_000)
us_df_grouped['DailyDeathRate'] = us_df_grouped['DailyDeathRate'].apply(lambda x: max(0, x) / us_population * 100_000)

# Load and prepare Canada data
can_df = pd.read_csv("../data/OxCGRT_fullwithnotes_CAN_v1.csv")

# Select required columns, including the indexes
can_df = can_df[['CountryName', 'Date', 'ConfirmedCases', 'ConfirmedDeaths',
                 'GovernmentResponseIndex_WeightedAverage', 'StringencyIndex_WeightedAverage',
                 'ContainmentHealthIndex_WeightedAverage', 'EconomicSupportIndex']]
can_df = can_df.dropna()
can_df['Date'] = pd.to_datetime(can_df['Date'], format='%Y%m%d')

# Group by Date and calculate mean for indexes, sum for cases and deaths
can_df_grouped = can_df.groupby('Date').agg({
    'ConfirmedCases': 'sum',
    'ConfirmedDeaths': 'sum',
    'GovernmentResponseIndex_WeightedAverage': 'mean',
    'StringencyIndex_WeightedAverage': 'mean',
    'ContainmentHealthIndex_WeightedAverage': 'mean',
    'EconomicSupportIndex': 'mean'
}).reset_index()
can_population = 38_000_000  # Canada population
can_df_grouped['Country'] = 'Canada'

# Calculate daily case and death rates for Canada
can_df_grouped['DailyCaseRate'] = can_df_grouped['ConfirmedCases'].diff().fillna(0)
can_df_grouped['DailyDeathRate'] = can_df_grouped['ConfirmedDeaths'].diff().fillna(0)
can_df_grouped['DailyCaseRate'] = can_df_grouped['DailyCaseRate'].apply(lambda x: max(0, x) / can_population * 100_000)
can_df_grouped['DailyDeathRate'] = can_df_grouped['DailyDeathRate'].apply(lambda x: max(0, x) / can_population * 100_000)

# Combine U.S. and Canada data
combined_df = pd.concat([us_df_grouped, can_df_grouped])

st.title("COVID-19 Daily Case and Death Rates Per 100K Population and Policy Index Over Time: U.S. vs Canada")

st.header("Government Response Index (Overall Index)")

# ------------------ First Plot ------------------
# Daily case rate with GovernmentResponseIndex_WeightedAverage
fig_cases_gov = make_subplots(specs=[[{"secondary_y": True}]])
for country in ['US', 'Canada']:
    country_data = combined_df[combined_df['Country'] == country]
    # Add Daily Case Rate trace as scatter plot
    fig_cases_gov.add_trace(
        go.Scatter(
            x=country_data['Date'],
            y=country_data['DailyCaseRate'],
            mode='markers',
            name=f"{country} Daily Case Rate"
        ),
        secondary_y=False
    )
    # Add GovernmentResponseIndex_WeightedAverage as line plot
    fig_cases_gov.add_trace(
        go.Scatter(
            x=country_data['Date'],
            y=country_data['GovernmentResponseIndex_WeightedAverage'],
            mode='lines',
            name=f"{country} Government Response Index"
        ),
        secondary_y=True
    )

# Update layout for first plot
fig_cases_gov.update_xaxes(title_text="Date")
fig_cases_gov.update_yaxes(title_text="Daily Case Rate per 100K", secondary_y=False)
fig_cases_gov.update_yaxes(title_text="Government Response Index", secondary_y=True)
fig_cases_gov.update_layout(
    title_text="Daily COVID-19 Case Rate and Government Response Index Over Time",
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.3,
        xanchor="center",
        x=0.5
    ),
    margin=dict(b=150),
    height=600
)

st.plotly_chart(fig_cases_gov)

# ------------------ Second Plot ------------------
# Daily death rate with GovernmentResponseIndex_WeightedAverage
fig_deaths_gov = make_subplots(specs=[[{"secondary_y": True}]])
for country in ['US', 'Canada']:
    country_data = combined_df[combined_df['Country'] == country]
    # Add Daily Death Rate trace as scatter plot
    fig_deaths_gov.add_trace(
        go.Scatter(
            x=country_data['Date'],
            y=country_data['DailyDeathRate'],
            mode='markers',
            name=f"{country} Daily Death Rate"
        ),
        secondary_y=False
    )
    # Add GovernmentResponseIndex_WeightedAverage as line plot
    fig_deaths_gov.add_trace(
        go.Scatter(
            x=country_data['Date'],
            y=country_data['GovernmentResponseIndex_WeightedAverage'],
            mode='lines',
            name=f"{country} Government Response Index"
        ),
        secondary_y=True
    )

# Update layout for second plot
fig_deaths_gov.update_xaxes(title_text="Date")
fig_deaths_gov.update_yaxes(title_text="Daily Death Rate per 100K", secondary_y=False)
fig_deaths_gov.update_yaxes(title_text="Government Response Index", secondary_y=True)
fig_deaths_gov.update_layout(
    title_text="Daily COVID-19 Death Rate and Government Response Index Over Time",
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.3,
        xanchor="center",
        x=0.5
    ),
    margin=dict(b=150),
    height=600
)

st.plotly_chart(fig_deaths_gov)

st.header("Stringency, Containment Health, Economic Support Indexes")
# ------------------ Third Plot ------------------
# Daily case rate with selectable indexes using checkboxes
st.text("Select Indexes to Display with Daily Case Rate")

# Define index options
index_options = {
    'Stringency Index': 'StringencyIndex_WeightedAverage',
    'Containment Health Index': 'ContainmentHealthIndex_WeightedAverage',
    'Economic Support Index': 'EconomicSupportIndex'
}

# Create checkboxes for each index
display_stringency = st.checkbox('Stringency Index', value=True)
display_containment = st.checkbox('Containment Health Index', value=False)
display_economic = st.checkbox('Economic Support Index', value=False)

# Build selected_indexes list based on checkboxes
selected_indexes = []
if display_stringency:
    selected_indexes.append('StringencyIndex_WeightedAverage')
if display_containment:
    selected_indexes.append('ContainmentHealthIndex_WeightedAverage')
if display_economic:
    selected_indexes.append('EconomicSupportIndex')

index_names = {
    'StringencyIndex_WeightedAverage': 'Stringency Index',
    'ContainmentHealthIndex_WeightedAverage': 'Containment Health Index',
    'EconomicSupportIndex': 'Economic Support Index'
}

if selected_indexes:
    fig_cases_indexes = make_subplots(specs=[[{"secondary_y": True}]])
    for country in ['US', 'Canada']:
        country_data = combined_df[combined_df['Country'] == country]
        # Add Daily Case Rate trace as scatter plot
        fig_cases_indexes.add_trace(
            go.Scatter(
                x=country_data['Date'],
                y=country_data['DailyCaseRate'],
                mode='markers',
                name=f"{country} Daily Case Rate"
            ),
            secondary_y=False
        )
        # Add selected indexes as line plots
        for index in selected_indexes:
            fig_cases_indexes.add_trace(
                go.Scatter(
                    x=country_data['Date'],
                    y=country_data[index],
                    mode='lines',
                    name=f"{country} {index_names[index]}"
                ),
                secondary_y=True
            )

    # Update layout for third plot
    fig_cases_indexes.update_xaxes(title_text="Date")
    fig_cases_indexes.update_yaxes(title_text="Daily Case Rate per 100K", secondary_y=False)
    fig_cases_indexes.update_yaxes(title_text="Index Value", secondary_y=True)
    fig_cases_indexes.update_layout(
        title_text="Daily COVID-19 Case Rate and Selected Indexes Over Time",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.4,
            xanchor="center",
            x=0.5
        ),
        margin=dict(b=150),
        height=600
    )

    st.plotly_chart(fig_cases_indexes)
else:
    st.write("Please select at least one index to display.")

# ------------------ Fourth Plot ------------------
# Daily death rate with selectable indexes using checkboxes
st.text("Select Indexes to Display with Daily Death Rate")

# Create checkboxes for each index
display_stringency_death = st.checkbox('Stringency Index', value=True, key='stringency_death')
display_containment_death = st.checkbox('Containment Health Index', value=False, key='containment_death')
display_economic_death = st.checkbox('Economic Support Index', value=False, key='economic_death')

# Build selected_indexes_death list based on checkboxes
selected_indexes_death = []
if display_stringency_death:
    selected_indexes_death.append('StringencyIndex_WeightedAverage')
if display_containment_death:
    selected_indexes_death.append('ContainmentHealthIndex_WeightedAverage')
if display_economic_death:
    selected_indexes_death.append('EconomicSupportIndex')

if selected_indexes_death:
    fig_deaths_indexes = make_subplots(specs=[[{"secondary_y": True}]])
    for country in ['US', 'Canada']:
        country_data = combined_df[combined_df['Country'] == country]
        # Add Daily Death Rate trace as scatter plot
        fig_deaths_indexes.add_trace(
            go.Scatter(
                x=country_data['Date'],
                y=country_data['DailyDeathRate'],
                mode='markers',
                name=f"{country} Daily Death Rate"
            ),
            secondary_y=False
        )
        # Add selected indexes as line plots
        for index in selected_indexes_death:
            fig_deaths_indexes.add_trace(
                go.Scatter(
                    x=country_data['Date'],
                    y=country_data[index],
                    mode='lines',
                    name=f"{country} {index_names[index]}"
                ),
                secondary_y=True
            )

    # Update layout for fourth plot
    fig_deaths_indexes.update_xaxes(title_text="Date")
    fig_deaths_indexes.update_yaxes(title_text="Daily Death Rate per 100K", secondary_y=False)
    fig_deaths_indexes.update_yaxes(title_text="Index Value", secondary_y=True)
    fig_deaths_indexes.update_layout(
        title_text="Daily COVID-19 Death Rate and Selected Indexes Over Time",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.4,
            xanchor="center",
            x=0.5
        ),
        margin=dict(b=150),
        height=600
    )

    st.plotly_chart(fig_deaths_indexes)
else:
    st.write("Please select at least one index to display.")