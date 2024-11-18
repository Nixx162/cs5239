import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px  # Added for boxplots

us_df = pd.read_csv("../data/OxCGRT_fullwithnotes_USA_v1.csv")
us_df = us_df[us_df['Jurisdiction'] == "NAT_TOTAL"]
us_df = us_df[['Date', 'ConfirmedCases', 'ConfirmedDeaths', 'GovernmentResponseIndex_WeightedAverage', 'StringencyIndex_WeightedAverage',
               'ContainmentHealthIndex_WeightedAverage', 'EconomicSupportIndex']]
us_df = us_df.dropna()
us_df['Date'] = pd.to_datetime(us_df['Date'], format='%Y%m%d')
us_population = 331_000_000  # U.S. population
us_df['CasesPerCapita'] = us_df['ConfirmedCases'] / us_population * 100_000
us_df['DeathsPerCapita'] = us_df['ConfirmedDeaths'] / us_population * 100_000
us_df['Country'] = 'US'

us_df['DailyCaseRate'] = us_df['ConfirmedCases'].diff().fillna(0)
us_df['DailyDeathRate'] = us_df['ConfirmedDeaths'].diff().fillna(0)
us_df['DailyCaseRate'] = us_df['DailyCaseRate'].apply(lambda x: max(0, x) / us_population * 100_000)
us_df['DailyDeathRate'] = us_df['DailyDeathRate'].apply(lambda x: max(0, x) / us_population * 100_000)

us_df_grouped = us_df

can_df = pd.read_csv("../data/OxCGRT_fullwithnotes_CAN_v1.csv")
can_df = can_df[can_df['Jurisdiction'] == "NAT_TOTAL"]
can_df = can_df[['Date', 'ConfirmedCases', 'ConfirmedDeaths', 'GovernmentResponseIndex_WeightedAverage', 'StringencyIndex_WeightedAverage',
               'ContainmentHealthIndex_WeightedAverage', 'EconomicSupportIndex']]
can_df = can_df.dropna()
can_df['Date'] = pd.to_datetime(can_df['Date'], format='%Y%m%d')
can_population = 38_000_000  #CAN population
can_df['CasesPerCapita'] = can_df['ConfirmedCases'] / can_population * 100_000
can_df['DeathsPerCapita'] = can_df['ConfirmedDeaths'] / can_population * 100_000
can_df['Country'] = 'Canada'

# Calculate daily case and death rates for U.S.
can_df['DailyCaseRate'] = can_df['ConfirmedCases'].diff().fillna(0)
can_df['DailyDeathRate'] = can_df['ConfirmedDeaths'].diff().fillna(0)
can_df['DailyCaseRate'] = can_df['DailyCaseRate'].apply(lambda x: max(0, x) / can_population * 100_000)
can_df['DailyDeathRate'] = can_df['DailyDeathRate'].apply(lambda x: max(0, x) / can_population * 100_000)

can_df_grouped = can_df

# Combine U.S. and Canada data
combined_df = pd.concat([us_df_grouped, can_df_grouped])

st.header("Government Response Index")

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
            name=f"{country} Daily Case Count"
        ),
        secondary_y=False
    )
    # Add Government Response Index as line plot
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
fig_cases_gov.update_yaxes(title_text="Daily Case Count per 100K", secondary_y=False)
fig_cases_gov.update_yaxes(title_text="Government Response Index", secondary_y=True)
fig_cases_gov.update_layout(
    title_text="Daily COVID-19 Case Count and Government Response Index Over Time",
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
            name=f"{country} Daily Death Count"
        ),
        secondary_y=False
    )
    # Add Government Response Index as line plot
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
fig_deaths_gov.update_yaxes(title_text="Daily Death Count per 100K", secondary_y=False)
fig_deaths_gov.update_yaxes(title_text="Government Response Index", secondary_y=True)
fig_deaths_gov.update_layout(
    title_text="Daily COVID-19 Death Count and Government Response Index Over Time",
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

# --- Added Boxplot of Government Response Index ---
st.subheader("Distribution of Government Response Index Values")

# Prepare data for boxplot
boxplot_data = pd.concat([
    us_df_grouped[['Date', 'GovernmentResponseIndex_WeightedAverage']].assign(Country='US'),
    can_df_grouped[['Date', 'GovernmentResponseIndex_WeightedAverage']].assign(Country='Canada')
])

# Create boxplot
fig_box_gov = px.box(
    boxplot_data,
    x='Country',
    y='GovernmentResponseIndex_WeightedAverage',
    title='Boxplot of Government Response Index: U.S. vs Canada',
    labels={'GovernmentResponseIndex_WeightedAverage': 'Government Response Index'}
)
st.plotly_chart(fig_box_gov)

# --- Added Selectbox and Boxplot for Other Indexes ---
st.header("Stringency, Containment Health, Economic Support Indexes")

# ------------------ Third Plot ------------------
# Daily case rate with selectable indexes using checkboxes
st.text("Select Indexes to Display with Daily Case Rate")

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

# Before third plot: Add selectbox to choose an index for boxplot
st.subheader("Distribution of Selected Index Values")

# Define index options for selectbox
index_options = {
    'Stringency Index': 'StringencyIndex_WeightedAverage',
    'Containment Health Index': 'ContainmentHealthIndex_WeightedAverage',
    'Economic Support Index': 'EconomicSupportIndex'
}

# Create selectbox
selected_index_name = st.selectbox(
    'Select an Index to Display Boxplot:',
    options=list(index_options.keys()),
    index=0  # Default to 'Stringency Index'
)

selected_index = index_options[selected_index_name]

# Prepare data for boxplot
boxplot_index_data = pd.concat([
    us_df_grouped[['Date', selected_index]].assign(Country='US'),
    can_df_grouped[['Date', selected_index]].assign(Country='Canada')
])

# Create boxplot for selected index
fig_box_index = px.box(
    boxplot_index_data,
    x='Country',
    y=selected_index,
    title=f'Boxplot of {selected_index_name}: U.S. vs Canada',
    labels={selected_index: selected_index_name}
)
st.plotly_chart(fig_box_index)