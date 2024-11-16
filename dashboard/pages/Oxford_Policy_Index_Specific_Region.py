import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Load and prepare U.S. data
us_df = pd.read_csv("../data/OxCGRT_fullwithnotes_USA_v1.csv")

# Select required columns, including the indexes
us_df = us_df[['CountryName', 'RegionName', 'Date', 'ConfirmedCases', 'ConfirmedDeaths',
               'GovernmentResponseIndex_WeightedAverage']]
us_df = us_df.dropna()
us_df['Date'] = pd.to_datetime(us_df['Date'], format='%Y%m%d')
us_df['Country'] = 'US'

# Load and prepare Canada data
can_df = pd.read_csv("../data/OxCGRT_fullwithnotes_CAN_v1.csv")

# Select required columns, including the indexes
can_df = can_df[['CountryName', 'RegionName', 'Date', 'ConfirmedCases', 'ConfirmedDeaths',
                 'GovernmentResponseIndex_WeightedAverage']]
can_df = can_df.dropna()
can_df['Date'] = pd.to_datetime(can_df['Date'], format='%Y%m%d')
can_df['Country'] = 'Canada'

# Combine U.S. and Canada data
combined_df = pd.concat([us_df, can_df])

# Create a list of unique regions
combined_df['Region'] = combined_df['Country'] + ' - ' + combined_df['RegionName']
regions = combined_df['Region'].unique()

st.title("COVID-19 Daily Case and Death Rates Per 100K Population and Government Response Index Over Time")

# User selection for regions for case rate plot
st.header("Select Regions for Case Rate Plot")
selected_region_case1 = st.selectbox("Select the first State/Province for Case Rate:", sorted(regions), key="case1")
selected_region_case2 = st.selectbox("Select the second State/Province for Case Rate (optional):", ["None"] + sorted(regions), key="case2")

# Population data for U.S. states
us_state_populations = {
    'Alabama': 5024279, 'Alaska': 733391, 'Arizona': 7151502, 'Arkansas': 3011524, 'California': 39538223,
    'Colorado': 5773714, 'Connecticut': 3605944, 'Delaware': 989948, 'Florida': 21538187, 'Georgia': 10711908,
    'Hawaii': 1455271, 'Idaho': 1839106, 'Illinois': 12812508, 'Indiana': 6785528, 'Iowa': 3190369,
    'Kansas': 2937880, 'Kentucky': 4505836, 'Louisiana': 4657757, 'Maine': 1362359, 'Maryland': 6177224,
    'Massachusetts': 7029917, 'Michigan': 10077331, 'Minnesota': 5706494, 'Mississippi': 2961279, 'Missouri': 6154913,
    'Montana': 1084225, 'Nebraska': 1961504, 'Nevada': 3104614, 'New Hampshire': 1377529, 'New Jersey': 9288994,
    'New Mexico': 2117522, 'New York': 20201249, 'North Carolina': 10439388, 'North Dakota': 779094, 'Ohio': 11799448,
    'Oklahoma': 3959353, 'Oregon': 4237256, 'Pennsylvania': 13002700, 'Rhode Island': 1097379, 'South Carolina': 5118425,
    'South Dakota': 886667, 'Tennessee': 6910840, 'Texas': 29145505, 'Utah': 3271616, 'Vermont': 643077,
    'Virginia': 8631393, 'Washington': 7693612, 'West Virginia': 1793716, 'Wisconsin': 5893718, 'Wyoming': 576851
}

# Population data for Canadian provinces and territories
canada_province_populations = {
    'Alberta': 4413146, 'British Columbia': 5110917, 'Manitoba': 1377517, 'New Brunswick': 789225,
    'Newfoundland and Labrador': 521365, 'Nova Scotia': 979351, 'Northwest Territories': 45161,
    'Nunavut': 39097, 'Ontario': 14734014, 'Prince Edward Island': 164318,
    'Quebec': 8537674, 'Saskatchewan': 1177884, 'Yukon': 42176
}

# Combine population data
state_populations = {**us_state_populations, **canada_province_populations}

# Function to process data for a region
def process_region_data(selected_region):
    if selected_region == "None" or not selected_region:
        return None, None
    selected_country, selected_state = selected_region.split(' - ')
    region_data = combined_df[(combined_df['Country'] == selected_country) & (combined_df['RegionName'] == selected_state)]
    if region_data.empty:
        st.write(f"No data available for {selected_region}.")
        return None, None
    population = state_populations.get(selected_state, None)
    if population is None:
        st.write(f"Population data for {selected_state} is not available.")
        return None, None
    # Calculate daily rates
    region_data = region_data.sort_values('Date')
    region_data['DailyConfirmedCases'] = region_data['ConfirmedCases'].diff().fillna(0)
    region_data['DailyConfirmedDeaths'] = region_data['ConfirmedDeaths'].diff().fillna(0)
    region_data['DailyCaseRate'] = region_data['DailyConfirmedCases'].apply(lambda x: max(0, x) / population * 100_000)
    region_data['DailyDeathRate'] = region_data['DailyConfirmedDeaths'].apply(lambda x: max(0, x) / population * 100_000)
    return region_data, selected_region

# ------------------ Case Rate Plot ------------------
region_data_case1, label_case1 = process_region_data(selected_region_case1)
region_data_case2, label_case2 = process_region_data(selected_region_case2)

if region_data_case1 is not None:
    # Daily case rate with GovernmentResponseIndex_WeightedAverage
    fig_cases_gov = make_subplots(specs=[[{"secondary_y": True}]])

    # Add Daily Case Rate trace as scatter plot for first region
    fig_cases_gov.add_trace(
        go.Scatter(
            x=region_data_case1['Date'],
            y=region_data_case1['DailyCaseRate'],
            mode='markers',
            name=f"{label_case1} Daily Case Rate"
        ),
        secondary_y=False
    )
    # Add Government Response Index as line plot for first region
    fig_cases_gov.add_trace(
        go.Scatter(
            x=region_data_case1['Date'],
            y=region_data_case1['GovernmentResponseIndex_WeightedAverage'],
            mode='lines',
            name=f"{label_case1} Government Response Index"
        ),
        secondary_y=True
    )

    # If second region data is available, add its traces
    if region_data_case2 is not None:
        # Add Daily Case Rate trace as scatter plot for second region
        fig_cases_gov.add_trace(
            go.Scatter(
                x=region_data_case2['Date'],
                y=region_data_case2['DailyCaseRate'],
                mode='markers',
                name=f"{label_case2} Daily Case Rate"
            ),
            secondary_y=False
        )
        # Add Government Response Index as line plot for second region
        fig_cases_gov.add_trace(
            go.Scatter(
                x=region_data_case2['Date'],
                y=region_data_case2['GovernmentResponseIndex_WeightedAverage'],
                mode='lines',
                name=f"{label_case2} Government Response Index"
            ),
            secondary_y=True
        )

    # Update layout for case rate plot
    title_text = f"Daily COVID-19 Case Rate and Government Response Index Over Time in {label_case1}"
    if region_data_case2 is not None:
        title_text += f" and {label_case2}"

    fig_cases_gov.update_xaxes(title_text="Date")
    fig_cases_gov.update_yaxes(title_text="Daily Case Rate per 100K", secondary_y=False)
    fig_cases_gov.update_yaxes(title_text="Government Response Index", secondary_y=True)
    fig_cases_gov.update_layout(
        title_text=title_text,
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

# ------------------ Death Rate Plot ------------------
# User selection for regions for death rate plot
st.header("Select Regions for Death Rate Plot")
selected_region_death1 = st.selectbox("Select the first State/Province for Death Rate:", sorted(regions), key="death1")
selected_region_death2 = st.selectbox("Select the second State/Province for Death Rate (optional):", ["None"] + sorted(regions), key="death2")


region_data_death1, label_death1 = process_region_data(selected_region_death1)
region_data_death2, label_death2 = process_region_data(selected_region_death2)

if region_data_death1 is not None:
    # Daily death rate with GovernmentResponseIndex_WeightedAverage
    fig_deaths_gov = make_subplots(specs=[[{"secondary_y": True}]])

    # Add Daily Death Rate trace as scatter plot for first region
    fig_deaths_gov.add_trace(
        go.Scatter(
            x=region_data_death1['Date'],
            y=region_data_death1['DailyDeathRate'],
            mode='markers',
            name=f"{label_death1} Daily Death Rate"
        ),
        secondary_y=False
    )
    # Add Government Response Index as line plot for first region
    fig_deaths_gov.add_trace(
        go.Scatter(
            x=region_data_death1['Date'],
            y=region_data_death1['GovernmentResponseIndex_WeightedAverage'],
            mode='lines',
            name=f"{label_death1} Government Response Index"
        ),
        secondary_y=True
    )

    # If second region data is available, add its traces
    if region_data_death2 is not None:
        # Add Daily Death Rate trace as scatter plot for second region
        fig_deaths_gov.add_trace(
            go.Scatter(
                x=region_data_death2['Date'],
                y=region_data_death2['DailyDeathRate'],
                mode='markers',
                name=f"{label_death2} Daily Death Rate"
            ),
            secondary_y=False
        )
        # Add Government Response Index as line plot for second region
        fig_deaths_gov.add_trace(
            go.Scatter(
                x=region_data_death2['Date'],
                y=region_data_death2['GovernmentResponseIndex_WeightedAverage'],
                mode='lines',
                name=f"{label_death2} Government Response Index"
            ),
            secondary_y=True
        )

    # Update layout for death rate plot
    title_text = f"Daily COVID-19 Death Rate and Government Response Index Over Time in {label_death1}"
    if region_data_death2 is not None:
        title_text += f" and {label_death2}"

    fig_deaths_gov.update_xaxes(title_text="Date")
    fig_deaths_gov.update_yaxes(title_text="Daily Death Rate per 100K", secondary_y=False)
    fig_deaths_gov.update_yaxes(title_text="Government Response Index", secondary_y=True)
    fig_deaths_gov.update_layout(
        title_text=title_text,
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
