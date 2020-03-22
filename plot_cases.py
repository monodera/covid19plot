#!/usr/bin/env python

# %%
from datetime import datetime, timedelta, date
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from functools import reduce
import colorcet as cc
from bokeh.plotting import figure, output_file, show, save, ColumnDataSource
from bokeh.models import ColumnDataSource, Range1d, HoverTool
from bokeh.palettes import viridis, cividis, all_palettes
from bokeh.layouts import column, row, gridplot


#     (click on legend entries to highlight the corresponding lines)""",
def plot_cases(
    corona_sums_hawaii,
    corona_sums_states,
    corona_sums_countries,
    colors,
    counties_to_plot,
    states_to_plot,
    countries_to_plot,
    case="Confirmed",
    ymin=1,
    ymax=1e5,
    thresh_confirmed=1000,
):
    n_counties = len(counties_to_plot)
    n_states = len(states_to_plot)
    n_countries = len(countries_to_plot)

    pp = figure(
        plot_width=850,
        plot_height=700,
        x_axis_type="datetime",
        y_axis_type="log",
        x_axis_label="Date",
        y_axis_label="Number of cases",
        tools="box_zoom,pan,save,hover,reset,tap,wheel_zoom",
    )
    pp.title.text_font_size = "16pt"
    pp.xaxis.axis_label_text_font_size = "16pt"
    pp.yaxis.axis_label_text_font_size = "16pt"

    for i, county in enumerate(counties_to_plot, start=0):
        df_hawaii = corona_sums_hawaii[
            (corona_sums_hawaii["Province/State"] == county)
            & (corona_sums_hawaii["type"] == case)
        ]
        c = colors[i]
        pp.line(
            x="Date",
            y="Count",
            source=df_hawaii,
            line_width=3,
            color=c,
            alpha=0.8,
            muted_color=c,
            muted_alpha=0.4,
            muted_line_width=2,
            muted=True,
            legend_group="Province/State",
        )

    for i, state in enumerate(states_to_plot, start=n_counties):
        df_state = corona_sums_states[
            (corona_sums_states["Province/State"] == state)
            & (corona_sums_states["type"] == case)
        ]
        c = colors[i]
        pp.line(
            x="Date",
            y="Count",
            source=df_state,
            line_width=3,
            color=c,
            alpha=0.8,
            muted_color=c,
            muted_alpha=0.4,
            muted_line_width=2,
            muted=True,
            legend_group="Province/State",
        )

    for i, country in enumerate(countries_to_plot, start=(n_counties + n_states)):
        df_country = corona_sums_countries[
            (corona_sums_countries["Country/Region"] == country)
            & (corona_sums_countries["type"] == case)
        ]
        c = colors[i]
        pp.line(
            x="Date",
            y="Count",
            source=df_country,
            line_width=3,
            color=c,
            alpha=0.8,
            muted_color=c,
            muted_alpha=0.4,
            muted_line_width=2,
            muted=True,
            legend_group="Country/Region",
        )

    for country in corona_sums_countries["Country/Region"].unique():
        df_country = corona_sums_countries[
            (corona_sums_countries["Country/Region"] == country)
        ]
        if (country not in countries_to_plot) and (
            df_country[df_country["type"] == "Confirmed"]["Count"].max()
            > thresh_confirmed
        ):
            print(country, df_country[df_country["type"] == case]["Count"].max())
            df_country = df_country[df_country["type"] == case]
            pp.line(
                x="Date",
                y="Count",
                source=df_country,
                line_width=1.0,
                color="gray",
                alpha=0.8,
                muted_color="gray",
                muted_alpha=0.5,
                muted_line_width=0.5,
                muted=True,
                legend_group="Country/Region",
            )

    pp.legend.location = "top_left"
    pp.legend.click_policy = "mute"
    pp.legend.title = "Click to highlight"
    pp.legend.label_text_font_size = "8pt"
    pp.x_range = Range1d(datetime(2020, 1, 1), datetime.now())
    pp.y_range = Range1d(ymin, ymax)

    hover = pp.select(dict(type=HoverTool))
    hover.tooltips = [
        ("Province/State", "@{Province/State}"),
        ("Country/Region", "@{Country/Region}"),
        ("Date", "$x{%Y-%m-%d}"),
        ("Value", "$y{0,0}"),
        # ("Confirmed", "@Confirmed"),
        # ("Deaths", "@Deaths"),
        # ("Recovered", "@Recovered"),
        # ("Active", "@Active"),
    ]
    # hover.formatters={"$y": ''}
    hover.formatters = {"$x": "datetime"}
    hover.mode = "mouse"

    return pp


# reference : https://medium.com/analytics-vidhya/mapping-the-spread-of-coronavirus-covid-19-d7830c4282e
# %%
df_confirmed = pd.read_csv(
    "../COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv"
)
df_deaths = pd.read_csv(
    "../COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv"
)
df_recovered = pd.read_csv(
    "../COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv"
)

df_confirmed_hawaii = pd.read_csv("csv/time_series_19-covid-Confirmed_Hawaii.csv")
df_deaths_hawaii = pd.read_csv("csv/time_series_19-covid-Deaths_Hawaii.csv")
df_recovered_hawaii = pd.read_csv("csv/time_series_19-covid-Recovered_Hawaii.csv")

countries = sorted(df_confirmed["Country/Region"].unique())

# %%
# 1.2 Tidying the data
# Using melt() command in pandas (similar to gather() in R's tidyr)

id_list = df_confirmed.columns.to_list()[:4]
vars_list = df_confirmed.columns.to_list()[4:]
confirmed_tidy = pd.melt(
    df_confirmed,
    id_vars=id_list,
    value_vars=vars_list,
    var_name="Date",
    value_name="Confirmed",
)
deaths_tidy = pd.melt(
    df_deaths,
    id_vars=id_list,
    value_vars=vars_list,
    var_name="Date",
    value_name="Deaths",
)
recovered_tidy = pd.melt(
    df_recovered,
    id_vars=id_list,
    value_vars=vars_list,
    var_name="Date",
    value_name="Recovered",
)
active = (
    confirmed_tidy["Confirmed"] - deaths_tidy["Deaths"] - recovered_tidy["Recovered"]
)
active_tidy = recovered_tidy.copy()
active_tidy.rename(columns={"Recovered": "Active"}, inplace=True)
active_tidy["Active"] = active

# for Hawaii
id_list_hawaii = df_confirmed_hawaii.columns.to_list()[:4]
vars_list_hawaii = df_confirmed_hawaii.columns.to_list()[4:]
confirmed_hawaii_tidy = pd.melt(
    df_confirmed_hawaii,
    id_vars=id_list_hawaii,
    value_vars=vars_list_hawaii,
    var_name="Date",
    value_name="Confirmed",
)
deaths_hawaii_tidy = pd.melt(
    df_deaths_hawaii,
    id_vars=id_list_hawaii,
    value_vars=vars_list_hawaii,
    var_name="Date",
    value_name="Deaths",
)
recovered_hawaii_tidy = pd.melt(
    df_recovered_hawaii,
    id_vars=id_list_hawaii,
    value_vars=vars_list_hawaii,
    var_name="Date",
    value_name="Recovered",
)
active_hawaii = (
    confirmed_hawaii_tidy["Confirmed"]
    - deaths_hawaii_tidy["Deaths"]
    - recovered_hawaii_tidy["Recovered"]
)
active_hawaii_tidy = recovered_hawaii_tidy.copy()
active_hawaii_tidy.rename(columns={"Recovered": "Active"}, inplace=True)
active_hawaii_tidy["Active"] = active_hawaii

# %%
# 1.3 Merging the three dataframes into one
data_frames = [confirmed_tidy, deaths_tidy, recovered_tidy, active_tidy]
df_corona = reduce(
    lambda left, right: pd.merge(left, right, on=id_list + ["Date"], how="outer"),
    data_frames,
)

data_frames_hawaii = [
    confirmed_hawaii_tidy,
    deaths_hawaii_tidy,
    recovered_hawaii_tidy,
    active_hawaii_tidy,
]
df_corona_hawaii = reduce(
    lambda left, right: pd.merge(
        left, right, on=id_list_hawaii + ["Date"], how="outer"
    ),
    data_frames_hawaii,
)

# 1.4 Each row should only represent one observation
id_vars = df_corona.columns[:5]
data_type = ["Confirmed", "Deaths", "Recovered", "Active"]
df_corona = pd.melt(
    df_corona,
    id_vars=id_vars,
    value_vars=data_type,
    var_name="type",
    value_name="Count",
)
df_corona["Date"] = pd.to_datetime(df_corona["Date"], format="%m/%d/%y", errors="raise")

id_vars_hawaii = df_corona_hawaii.columns[:5]
df_corona_hawaii = pd.melt(
    df_corona_hawaii,
    id_vars=id_vars_hawaii,
    value_vars=data_type,
    var_name="type",
    value_name="Count",
)
df_corona_hawaii["Date"] = pd.to_datetime(
    df_corona_hawaii["Date"], format="%m/%d/%y", errors="raise"
)

corona_sums_states = df_corona.groupby(
    ["type", "Date", "Province/State"], as_index=False
).agg({"Count": "sum"})
corona_sums_countries = df_corona.groupby(
    ["type", "Date", "Country/Region"], as_index=False
).agg({"Count": "sum"})
corona_sums_hawaii = df_corona_hawaii

print(corona_sums_hawaii)

# %%

# source = ColumnDataSource(data=df_corona)

counties_to_plot = [
    "Hawaii County, HI",
    "Honolulu County, HI",
    # "Maui County, HI",
    # "Kauai County, HI",
]
states_to_plot = ["California", "Hawaii"]
countries_to_plot = [
    "China",
    "Iran",
    "Italy",
    "Germany",
    "France",
    "Japan",
    "Korea, South",
    "Spain",
    "Switzerland",
    "United Kingdom",
    "US",
]

n_plot = len(counties_to_plot) + len(states_to_plot) + len(countries_to_plot)
colors_interval = int(256 / (n_plot + 1))
colors = cc.glasbey_dark[: n_plot + 1]

p1 = plot_cases(
    corona_sums_hawaii,
    corona_sums_states,
    corona_sums_countries,
    colors,
    counties_to_plot,
    states_to_plot,
    countries_to_plot,
    case="Confirmed",
    ymin=1,
    ymax=1e5,
    thresh_confirmed=2000,
)
p1.title.text = 'Number of "confirmed" COVID-19 cases'

p2 = plot_cases(
    corona_sums_hawaii,
    corona_sums_states,
    corona_sums_countries,
    colors,
    counties_to_plot,
    states_to_plot,
    countries_to_plot,
    case="Deaths",
    ymin=1,
    ymax=1e5,
    thresh_confirmed=2000,
)
p2.title.text = 'Number of "death" COVID-19 cases'

p3 = plot_cases(
    corona_sums_hawaii,
    corona_sums_states,
    corona_sums_countries,
    colors,
    counties_to_plot,
    states_to_plot,
    countries_to_plot,
    case="Recovered",
    ymin=1,
    ymax=1e5,
    thresh_confirmed=2000,
)
p3.title.text = 'Number of "recovered" COVID-19 cases'

p4 = plot_cases(
    corona_sums_hawaii,
    corona_sums_states,
    corona_sums_countries,
    colors,
    counties_to_plot,
    states_to_plot,
    countries_to_plot,
    case="Active",
    ymin=1,
    ymax=1e5,
    thresh_confirmed=2000,
)
p4.title.text = 'Number of "currently active" COVID-19 cases'

output_file("../gist/index.html", title="COVID-19 Cases")

p = column(p1, p2, p3, p4)
# p = column(p1)
save(p)


# %%
