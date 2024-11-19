import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

original_index_columns = [
    'C1E_School closing', 
    'C2E_Workplace closing',  
    'C3E_Cancel public events', 
    'C4E_Restrictions on gatherings', 
    'C5E_Close public transport', 
    'C6E_Stay at home requirements', 
    'C7E_Restrictions on internal movement', 
    'C8E_International travel controls', 
    'E1_Income support', 
    'E2_Debt/contract relief', 
    'E3_Fiscal measures', 
    'E4_International support', 
    'H1_Public information campaigns', 
    'H2_Testing policy', 
    'H3_Contact tracing', 
    'H4_Emergency investment in healthcare', 
    'H5_Investment in vaccines',
    'H6E_Facial Coverings', 
    'H7_Vaccination policy', 
    'H8E_Protection of elderly people', 
    'V1_Vaccine Prioritisation (summary)', 
    'V2A_Vaccine Availability (summary)', 
    'V3_Vaccine Financial Support (summary)', 
    'V4_Mandatory Vaccination (summary)', 
    'GovernmentResponseIndex_WeightedAverage', 
    'StringencyIndex_WeightedAverage',
    'ContainmentHealthIndex_WeightedAverage', 
    'EconomicSupportIndex',
]


# Define the new specific indexes
index_columns = [
    'C1E_School closing', 
    'C2E_Workplace closing',  
    'C3E_Cancel public events', 
    'C4E_Restrictions on gatherings', 
    'C5E_Close public transport', 
    'C6E_Stay at home requirements', 
    'C7E_Restrictions on internal movement', 
    'C8E_International travel controls', 
    'E1_Income support', 
    'E2_Debt/contract relief', 
    'E3_Fiscal measures Per 100K Population', 
    'E4_International support Per 100K Population', 
    'H1_Public information campaigns', 
    'H2_Testing policy', 
    'H3_Contact tracing', 
    'H4_Emergency investment in healthcare Per 100K Population', 
    'H5_Investment in vaccines Per 100K Population',
    'H6E_Facial Coverings', 
    'H7_Vaccination policy', 
    'H8E_Protection of elderly people', 
    'V1_Vaccine Prioritisation (summary)', 
    'V2A_Vaccine Availability (summary)', 
    'V3_Vaccine Financial Support (summary)', 
    'V4_Mandatory Vaccination (summary)', 
    'GovernmentResponseIndex_WeightedAverage', 
    'StringencyIndex_WeightedAverage',
    'ContainmentHealthIndex_WeightedAverage', 
    'EconomicSupportIndex',
]

# Create a dictionary for detailed index explanations
index_explanations = {
    'C1E_School closing': 'Records closings of schools and universities (0-3): 0 - no measures; 1 - recommend closing; 2 - require closing some levels or categories; 3 - require closing all levels.',
    'C2E_Workplace closing': 'Records closings of workplaces (0-3): 0 - no measures; 1 - recommend closing; 2 - require closing some sectors or categories; 3 - require closing all-but-essential workplaces.',
    'C3E_Cancel public events': 'Records cancelling public events (0-2): 0 - no measures; 1 - recommend cancelling; 2 - require cancelling.',
    'C4E_Restrictions on gatherings': 'Limits on private gatherings (0-4): 0 - no restrictions; 1 - restrictions on very large gatherings (above 1000 people); 2 - gatherings between 101-1000 people; 3 - gatherings between 11-100 people; 4 - gatherings of 10 people or less.',
    'C5E_Close public transport': 'Records closing of public transport (0-2): 0 - no measures; 1 - recommend closing; 2 - require closing or prohibit most citizens from using it.',
    'C6E_Stay at home requirements': 'Records orders to "shelter-in-place" and otherwise confine to home (0-3): 0 - no measures; 1 - recommend not leaving house; 2 - require not leaving house with exceptions for essential trips; 3 - require not leaving house with minimal exceptions.',
    'C7E_Restrictions on internal movement': 'Restrictions on internal movement between cities/regions (0-2): 0 - no measures; 1 - recommend not to travel between regions/cities; 2 - internal movement restrictions in place.',
    'C8E_International travel controls': 'Restrictions on international travel (0-4): 0 - no restrictions; 1 - screening; 2 - quarantine arrivals from high-risk regions; 3 - ban on high-risk regions; 4 - total border closure.',
    'E1_Income support': 'Government providing direct cash payments to people who lose their jobs or cannot work (0-2): 0 - no income support; 1 - government is replacing less than 50% of lost salary; 2 - government is replacing 50% or more of lost salary.',
    'E2_Debt/contract relief': 'Government freezing financial obligations for households (0-2): 0 - no relief; 1 - narrow relief; 2 - broad relief.',
    'E3_Fiscal measures Per 100K Population': 'Announced economic stimulus spending (excluding income support and debt relief) in response to COVID-19. Scaled to Per 100K Population.',
    'E4_International support Per 100K Population': 'Announced offers of COVID-19 related aid spending to other countries. Scaled to Per 100K Population.',
    'H1_Public information campaigns': 'Public awareness campaigns (0-2): 0 - no COVID-19 public information campaign; 1 - public officials urging caution; 2 - coordinated public information campaign.',
    'H2_Testing policy': 'Government policy on who has access to testing (0-3): 0 - no testing policy; 1 - only those who both (a) have symptoms AND (b) meet specific criteria; 2 - testing of anyone showing COVID-19 symptoms; 3 - open public testing (e.g., "drive-through" testing available to asymptomatic people).',
    'H3_Contact tracing': 'Government policy on contact tracing after a positive diagnosis (0-2): 0 - no contact tracing; 1 - limited contact tracing; 2 - comprehensive contact tracing.',
    'H4_Emergency investment in healthcare Per 100K Population': 'Announced short-term spending on healthcare system, e.g., hospitals, masks, etc. Scaled to Per 100K Population.',
    'H5_Investment in vaccines Per 100K Population': 'Announced public spending on vaccine development. Scaled to Per 100K Population.',
    'H6E_Facial Coverings': 'Policies on the use of face coverings outside the home (0-4): 0 - no policy; 1 - recommended; 2 - required in some specified shared/public spaces; 3 - required in all shared/public spaces; 4 - required outside the home at all times.',
    'H7_Vaccination policy': 'Policy on vaccine availability for different groups (0-5): 0 - no availability; 1 - availability for ONE of the following: key workers, clinically vulnerable groups, elderly groups; 2 - availability for TWO of these groups; 3 - availability for ALL of these groups; 4 - availability for select broad groups/ages; 5 - universal availability.',
    'H8E_Protection of elderly people': 'Policies for protecting elderly people (0-3): 0 - no measures; 1 - recommended isolation; 2 - required isolation in some circumstances; 3 - required isolation for all elderly people.',
    'V1_Vaccine Prioritisation (summary)': 'Summary of vaccine prioritization plans, detailing which groups are prioritized.',
    'V2A_Vaccine Availability (summary)': 'Summary of vaccine availability, indicating which groups can access vaccines.',
    'V3_Vaccine Financial Support (summary)': 'Government financial support for vaccine procurement and distribution.',
    'V4_Mandatory Vaccination (summary)': 'Policies mandating vaccination for certain groups or the entire population.',
    'GovernmentResponseIndex_WeightedAverage': '...', 
    'StringencyIndex_WeightedAverage': '...', 
    'ContainmentHealthIndex_WeightedAverage': '...', 
    'EconomicSupportIndex': '...', 
}

# Load and prepare U.S. data
us_population = 331_000_000  # U.S. population
us_df = pd.read_csv("./data/OxCGRT_fullwithnotes_USA_v1.csv")
us_raw = pd.read_csv("./data/OxCGRT_fullwithnotes_USA_v1.csv")
us_df = us_df[us_df['Jurisdiction'] == "NAT_TOTAL"]
us_df = us_df[['Date', 'ConfirmedCases', 'ConfirmedDeaths', 'GovernmentResponseIndex_WeightedAverage', 'StringencyIndex_WeightedAverage',
               'ContainmentHealthIndex_WeightedAverage', 'EconomicSupportIndex']]
us_df = us_df.dropna()
for index in original_index_columns:
    us_df[index] = us_raw[index]
us_df['Date'] = pd.to_datetime(us_df['Date'], format='%Y%m%d')

us_df_grouped = us_df

us_df_grouped['Country'] = 'US'

# Calculate daily case and death rates for U.S.
us_df_grouped['DailyCaseRate'] = us_df_grouped['ConfirmedCases'].diff().fillna(0)
us_df_grouped['DailyDeathRate'] = us_df_grouped['ConfirmedDeaths'].diff().fillna(0)
us_df_grouped['DailyCaseRate'] = us_df_grouped['DailyCaseRate'].apply(lambda x: max(0, x) / us_population * 100_000)
us_df_grouped['DailyDeathRate'] = us_df_grouped['DailyDeathRate'].apply(lambda x: max(0, x) / us_population * 100_000)

# Load and prepare Canada data
can_population = 38_000_000  #CAN population
can_df = pd.read_csv("./data/OxCGRT_fullwithnotes_CAN_v1.csv")
can_raw = pd.read_csv("./data/OxCGRT_fullwithnotes_CAN_v1.csv")
can_df = can_df[can_df['Jurisdiction'] == "NAT_TOTAL"]
can_df = can_df[['Date', 'ConfirmedCases', 'ConfirmedDeaths', 'GovernmentResponseIndex_WeightedAverage', 'StringencyIndex_WeightedAverage',
               'ContainmentHealthIndex_WeightedAverage', 'EconomicSupportIndex']]
can_df = can_df.dropna()
for index in original_index_columns:
    can_df[index] = can_raw[index]
can_df['Date'] = pd.to_datetime(can_df['Date'], format='%Y%m%d')

can_df_grouped = can_df
can_df_grouped['Country'] = 'Canada'

# Calculate daily case and death rates for Canada
can_df_grouped['DailyCaseRate'] = can_df_grouped['ConfirmedCases'].diff().fillna(0)
can_df_grouped['DailyDeathRate'] = can_df_grouped['ConfirmedDeaths'].diff().fillna(0)
can_df_grouped['DailyCaseRate'] = can_df_grouped['DailyCaseRate'].apply(lambda x: max(0, x) / can_population * 100_000)
can_df_grouped['DailyDeathRate'] = can_df_grouped['DailyDeathRate'].apply(lambda x: max(0, x) / can_population * 100_000)

# Scale to 100 k POP
index_to_scale = [
    "E3_Fiscal measures",
    "E4_International support",
    "H4_Emergency investment in healthcare",
    "H5_Investment in vaccines"
]
for idx in index_to_scale:
    us_df_grouped[idx + " Per 100K Population"] = us_df_grouped[idx] / us_population * 100_000
    can_df_grouped[idx + " Per 100K Population"] = can_df_grouped[idx] / can_population * 100_000

# Combine U.S. and Canada data
combined_df = pd.concat([us_df_grouped, can_df_grouped])

st.header("COVID-19 Daily Case and Death Counts Per 100K Population and Policy Index Over Time: U.S. vs Canada")

# ------------------ First Plot ------------------
# Daily case rate with selectable index using selectbox
st.text("Select an Index to Display with Daily Case Count")

# Create selectbox for selecting one index
selected_index = st.selectbox("Select an Index", index_columns)

if selected_index:
    # Display the detailed explanation for the selected index
    st.write(f"**Explanation:** {index_explanations[selected_index]}")

    fig_cases_indexes = make_subplots(specs=[[{"secondary_y": True}]])
    for country in ['US', 'Canada']:
        country_data = combined_df[combined_df['Country'] == country]
        # Add Daily Case Rate trace as scatter plot
        fig_cases_indexes.add_trace(
            go.Scatter(
                x=country_data['Date'],
                y=country_data['DailyCaseRate'],
                mode='markers',
                name=f"{country} Daily Case Count"
            ),
            secondary_y=False
        )
        # Add selected index as line plot
        fig_cases_indexes.add_trace(
            go.Scatter(
                x=country_data['Date'],
                y=country_data[selected_index],
                mode='lines',
                name=f"{country} {selected_index}"
            ),
            secondary_y=True
        )

    # Update layout for first plot
    fig_cases_indexes.update_xaxes(title_text="Date")
    fig_cases_indexes.update_yaxes(title_text="Daily Case Count per 100K", secondary_y=False)
    fig_cases_indexes.update_yaxes(title_text="Index Value", secondary_y=True)
    fig_cases_indexes.update_layout(
        title_text="Daily COVID-19 Case Count and Selected Index Over Time",
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
    st.write("Please select an index to display.")

# ------------------ Second Plot ------------------
# Daily death rate with selectable index using selectbox
# st.text("Select an Index to Display with Daily Death Rate")

# Create selectbox for selecting one index
selected_index_death = selected_index
# selected_index_death = st.selectbox("Select an Index", index_columns, key='death_index')

if selected_index_death:
    # Display the detailed explanation for the selected index
    # st.write(f"**Explanation:** {index_explanations[selected_index_death]}")

    fig_deaths_indexes = make_subplots(specs=[[{"secondary_y": True}]])
    for country in ['US', 'Canada']:
        country_data = combined_df[combined_df['Country'] == country]
        # Add Daily Death Rate trace as scatter plot
        fig_deaths_indexes.add_trace(
            go.Scatter(
                x=country_data['Date'],
                y=country_data['DailyDeathRate'],
                mode='markers',
                name=f"{country} Daily Death Count"
            ),
            secondary_y=False
        )
        # Add selected index as line plot
        fig_deaths_indexes.add_trace(
            go.Scatter(
                x=country_data['Date'],
                y=country_data[selected_index_death],
                mode='lines',
                name=f"{country} {selected_index_death}"
            ),
            secondary_y=True
        )

    # Update layout for second plot
    fig_deaths_indexes.update_xaxes(title_text="Date")
    fig_deaths_indexes.update_yaxes(title_text="Daily Death Count per 100K", secondary_y=False)
    fig_deaths_indexes.update_yaxes(title_text="Index Value", secondary_y=True)
    fig_deaths_indexes.update_layout(
        title_text="Daily COVID-19 Death Count and Selected Index Over Time",
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
    st.write("Please select an index to display.")

