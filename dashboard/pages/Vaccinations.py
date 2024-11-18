import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

all_vaccinations_data_df = pd.read_csv("../data/vaccinations.csv")
us_policy_df = pd.read_csv("../data/OxCGRT_fullwithnotes_USA_v1.csv")
canada_policy_df = pd.read_csv("../data/OxCGRT_fullwithnotes_CAN_v1.csv")

us_policy_df = us_policy_df[us_policy_df["Jurisdiction"] == "NAT_TOTAL"]
us_policy_df["date"] = pd.to_datetime(us_policy_df["Date"], format="%Y%m%d")
us_policy_df.reset_index(drop=True, inplace=True)
us_gr_df = pd.melt(
    us_policy_df,
    id_vars=["date"],
    value_vars=["GovernmentResponseIndex_NonVaccinated", "GovernmentResponseIndex_Vaccinated"],
    var_name="vaccination_status",
    value_name="government_response_index",
)
us_gr_df["vaccination_status"] = us_gr_df["vaccination_status"].replace(
    {"GovernmentResponseIndex_NonVaccinated": "Not Vaccinated", "GovernmentResponseIndex_Vaccinated": "Vaccinated"}
)
us_ch_df = pd.melt(
    us_policy_df,
    id_vars=["date"],
    value_vars=["ContainmentHealthIndex_NonVaccinated", "ContainmentHealthIndex_Vaccinated"],
    var_name="vaccination_status",
    value_name="containment_health_index",
)
us_ch_df["vaccination_status"] = us_ch_df["vaccination_status"].replace(
    {"ContainmentHealthIndex_NonVaccinated": "Not Vaccinated", "ContainmentHealthIndex_Vaccinated": "Vaccinated"}
)

canada_policy_df = canada_policy_df[canada_policy_df["Jurisdiction"] == "NAT_TOTAL"]
canada_policy_df["date"] = pd.to_datetime(canada_policy_df["Date"], format="%Y%m%d")
canada_policy_df.reset_index(drop=True, inplace=True)
canada_gr_df = pd.melt(
    canada_policy_df,
    id_vars=["date"],
    value_vars=["GovernmentResponseIndex_NonVaccinated", "GovernmentResponseIndex_Vaccinated"],
    var_name="vaccination_status",
    value_name="government_response_index",
)
canada_gr_df["vaccination_status"] = canada_gr_df["vaccination_status"].replace(
    {"GovernmentResponseIndex_NonVaccinated": "Not Vaccinated", "GovernmentResponseIndex_Vaccinated": "Vaccinated"}
)
canada_ch_df = pd.melt(
    canada_policy_df,
    id_vars=["date"],
    value_vars=["ContainmentHealthIndex_NonVaccinated", "ContainmentHealthIndex_Vaccinated"],
    var_name="vaccination_status",
    value_name="containment_health_index",
)
canada_ch_df["vaccination_status"] = canada_ch_df["vaccination_status"].replace(
    {"ContainmentHealthIndex_NonVaccinated": "Not Vaccinated", "ContainmentHealthIndex_Vaccinated": "Vaccinated"}
)


def replace_trailing_zeros_with_last_nonzero(df, column):
    last_nonzero = df[column].replace(0, pd.NA).ffill().iloc[-1]
    df[column] = df[column].replace(0, pd.NA).ffill().fillna(last_nonzero)
    return df


cutoff_date = pd.to_datetime("2023-05-09 00:00:00")


US_POPULATION = 346000000
us_vac_data_df = all_vaccinations_data_df[all_vaccinations_data_df["iso_code"] == "USA"]
us_vac_data_df.reset_index(inplace=True, drop=True)
us_vac_data_df.fillna(0, inplace=True)
us_vac_data_df["date"] = pd.to_datetime(us_vac_data_df["date"], format="%Y-%m-%d")
us_vac_data_df = us_vac_data_df.loc[us_vac_data_df["date"] < cutoff_date]
us_vac_data_df = replace_trailing_zeros_with_last_nonzero(us_vac_data_df, "people_fully_vaccinated")
us_vac_data_df = replace_trailing_zeros_with_last_nonzero(us_vac_data_df, "total_vaccinations")
us_vac_data_df["cumulative_people_vaccinated"] = us_vac_data_df["daily_people_vaccinated"].cumsum()
us_vac_data_df["percent_people_vaccinated"] = us_vac_data_df["cumulative_people_vaccinated"] / US_POPULATION * 100
us_vac_data_df["percent_people_fully_vaccinated"] = us_vac_data_df["people_fully_vaccinated"] / US_POPULATION * 100
us_vac_data_df["vaccine_administered_per_people"] = (
    us_vac_data_df["total_vaccinations"] / us_vac_data_df["cumulative_people_vaccinated"]
)


CANADA_POPULATION = 41000000
canada_vac_data_df = all_vaccinations_data_df[all_vaccinations_data_df["iso_code"] == "CAN"]
canada_vac_data_df.reset_index(inplace=True, drop=True)
canada_vac_data_df.fillna(0, inplace=True)
canada_vac_data_df["date"] = pd.to_datetime(canada_vac_data_df["date"], format="%Y-%m-%d")
canada_vac_data_df = canada_vac_data_df.loc[canada_vac_data_df["date"] < cutoff_date]
canada_vac_data_df = replace_trailing_zeros_with_last_nonzero(canada_vac_data_df, "people_fully_vaccinated")
canada_vac_data_df = replace_trailing_zeros_with_last_nonzero(canada_vac_data_df, "total_vaccinations")
canada_vac_data_df["cumulative_people_vaccinated"] = canada_vac_data_df["daily_people_vaccinated"].cumsum()
canada_vac_data_df["percent_people_vaccinated"] = (
    canada_vac_data_df["cumulative_people_vaccinated"] / CANADA_POPULATION * 100
)
canada_vac_data_df["percent_people_fully_vaccinated"] = (
    canada_vac_data_df["people_fully_vaccinated"] / CANADA_POPULATION * 100
)
canada_vac_data_df["vaccine_administered_per_people"] = (
    canada_vac_data_df["total_vaccinations"] / canada_vac_data_df["cumulative_people_vaccinated"]
)

combined_vac_df = pd.concat([us_vac_data_df, canada_vac_data_df])
combined_vac_df_filtered = combined_vac_df.groupby("iso_code", as_index=False).apply(lambda x: x.iloc[15:])

# Percentage of people vaccinated

st.header("Percentage of the Population Vaccinated Over Time in the US and Canada")

fig_percent_vaccinated = px.line(
    combined_vac_df_filtered,
    x="date",
    y="percent_people_vaccinated",
    color="iso_code",
    title="Percentage of the Population Vaccinated Over Time in the US and Canada",
    labels={"iso_code": "Country", "date": "Date", "percent_people_vaccinated": "Percentage of Population Vaccinated"},
)
st.plotly_chart(fig_percent_vaccinated)

# Percentage of people fully vaccinated

st.header("Percentage of the Population Fully Vaccinated Over Time in the US and Canada")

fig_percent_fully_vaccinated = px.line(
    combined_vac_df_filtered,
    x="date",
    y="percent_people_fully_vaccinated",
    color="iso_code",
    title="Percentage of the Population Fully Vaccinated Over Time in the US and Canada",
    labels={
        "iso_code": "Country",
        "date": "Date",
        "percent_people_fully_vaccinated": "Percentage of Populations Fully Vaccinated",
    },
)
st.plotly_chart(fig_percent_fully_vaccinated)

# Vaccine administered per people

st.header("Vaccine Administered per Person in the US and Canada")

fig_vaccine_administered_per_people = px.line(
    combined_vac_df_filtered,
    x="date",
    y="vaccine_administered_per_people",
    color="iso_code",
    title="Vaccine Administered per Person in the US and Canada",
    labels={
        "iso_code": "Country",
        "date": "Date",
        "vaccine_administered_per_people": "Vaccine Administered per Person",
    },
)
st.plotly_chart(fig_vaccine_administered_per_people)

# Daily number of vaccine administered

st.header("Daily Number of People Vaccinated Over Time in the US and Canada per 1M Population")

fig_daily_vaccine = px.line(
    combined_vac_df_filtered,
    x="date",
    y="daily_vaccinations_per_million",
    color="iso_code",
    title="Daily Number of People Vaccinated Over Time in the US and Canada per 1M Population",
    labels={
        "iso_code": "Country",
        "date": "Date",
        "daily_vaccinations_per_million": "Daily People Vaccinated (per 1M pops)",
    },
)
st.plotly_chart(fig_daily_vaccine)

# Difference in treatment of NV and V

st.header("Government Response Index for Vaccinated vs. Non-Vaccinated, Canada")

fig_gr_canada = px.line(
    canada_gr_df,
    x="date",
    y="government_response_index",
    color="vaccination_status",
    title="Government Response Index for Vaccinated vs. Non-Vaccinated, Canada",
    labels={
        "vaccination_status": "Vaccination Status",
        "date": "Date",
        "government_response_index": "Government Response Index Value",
    },
)
st.plotly_chart(fig_gr_canada)

st.header("Government Response Index for Vaccinated vs. Non-Vaccinated, USA")

fig_gr_us = px.line(
    us_gr_df,
    x="date",
    y="government_response_index",
    color="vaccination_status",
    title="Government Response Index for Vaccinated vs. Non-Vaccinated, USA",
    labels={
        "vaccination_status": "Vaccination Status",
        "date": "Date",
        "government_response_index": "Government Response Index Value",
    },
)
st.plotly_chart(fig_gr_us)

st.header("Containment and Health Index for Vaccinated vs. Non-Vaccinated, Canada")

fig_ch_canada = px.line(
    canada_ch_df,
    x="date",
    y="containment_health_index",
    color="vaccination_status",
    title="Containment and Health Index for Vaccinated vs. Non-Vaccinated, Canada",
    labels={
        "vaccination_status": "Vaccination Status",
        "date": "Date",
        "containment_health_index": "Containment and Health Index Value",
    },
)
st.plotly_chart(fig_ch_canada)

st.header("Containment and Health Index for Vaccinated vs. Non-Vaccinated, USA")

fig_ch_us = px.line(
    us_ch_df,
    x="date",
    y="containment_health_index",
    color="vaccination_status",
    title="Containment and Health Index for Vaccinated vs. Non-Vaccinated, USA",
    labels={
        "vaccination_status": "Vaccination Status",
        "date": "Date",
        "containment_health_index": "Containment and Health Index Value",
    },
)
st.plotly_chart(fig_ch_us)
