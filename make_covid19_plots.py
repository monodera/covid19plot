#!/usr/bin/env python

# %%
import os
from datetime import datetime, timedelta, date
import pandas as pd
import numpy as np
from functools import reduce
import colorcet as cc
from bokeh.plotting import figure, output_file, show, save, ColumnDataSource
from bokeh.models import ColumnDataSource, Range1d, HoverTool, Div
from bokeh.palettes import viridis, cividis, all_palettes
from bokeh.layouts import column, row, gridplot

# %%
def read_jhu_data():

    df_confirmed = pd.read_csv(
        "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
    )
    df_deaths = pd.read_csv(
        "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"
    )
    df_recovered = pd.read_csv(
        "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"
    )

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

    # 1.3 Merging the three dataframes into one
    data_frames = [confirmed_tidy, deaths_tidy, recovered_tidy]
    df_corona = reduce(
        lambda left, right: pd.merge(left, right, on=id_list + ["Date"], how="outer"),
        data_frames,
    )

    # 1.4 Each row should only represent one observation
    id_vars = df_corona.columns[:5]
    data_type = ["Confirmed", "Deaths"]
    df_corona = pd.melt(
        df_corona,
        id_vars=id_vars,
        value_vars=data_type,
        var_name="type",
        value_name="Count",
    )

    df_corona["Date"] = pd.to_datetime(
        df_corona["Date"], format="%m/%d/%y", errors="raise"
    )
    corona_sums_countries = df_corona.groupby(
        ["type", "Date", "Country/Region"], as_index=False
    ).agg({"Count": "sum"})

    corona_sums_countries = corona_sums_countries.rename(
        columns={"Date": "date", "Province/State": "state", "Country/Region": "place",},
    )
    corona_sums_countries["type"] = corona_sums_countries["type"].str.replace(
        "Confirmed", "cases"
    )
    corona_sums_countries["type"] = corona_sums_countries["type"].str.replace(
        "Deaths", "deaths"
    )
    corona_sums_countries["type"] = corona_sums_countries["type"].str.replace(
        "Recovered", "recovered"
    )

    return corona_sums_countries


# %%
def read_hawaii_data():
    df_confirmed_hawaii = pd.read_csv("csv/time_series_19-covid-Confirmed_Hawaii.csv")
    df_deaths_hawaii = pd.read_csv("csv/time_series_19-covid-Deaths_Hawaii.csv")

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

    data_frames_hawaii = [
        confirmed_hawaii_tidy,
        deaths_hawaii_tidy,
    ]
    df_corona_hawaii = reduce(
        lambda left, right: pd.merge(
            left, right, on=id_list_hawaii + ["Date"], how="outer"
        ),
        data_frames_hawaii,
    )

    id_vars_hawaii = df_corona_hawaii.columns[:5]
    data_type = ["Confirmed", "Deaths"]
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

    corona_sums_hawaii = df_corona_hawaii
    corona_sums_hawaii = corona_sums_hawaii.rename(
        columns={
            "Date": "date",
            "Province/State": "place",
            "Country/Region": "country",
        },
    )
    corona_sums_hawaii["type"] = corona_sums_hawaii["type"].str.replace(
        "Confirmed", "cases"
    )
    corona_sums_hawaii["type"] = corona_sums_hawaii["type"].str.replace(
        "Deaths", "deaths"
    )
    corona_sums_hawaii["type"] = corona_sums_hawaii["type"].str.replace(
        "Recovered", "recovered"
    )

    return corona_sums_hawaii


# %%
def read_nyt_data():
    # NYT data
    df_states = pd.read_csv(
        "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv"
    )
    df_states["date"] = pd.to_datetime(
        df_states["date"], format="%Y/%m/%d", errors="raise"
    )
    df_states = df_states.rename(columns={"state": "place"})

    df_counties = pd.read_csv(
        "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv"
    )
    df_counties["date"] = pd.to_datetime(
        df_counties["date"], format="%Y/%m/%d", errors="raise"
    )
    df_counties = df_counties.rename(columns={"county": "place"})

    return df_counties, df_states


def read_tokyo_data():
    df = pd.read_json(
        "https://raw.githubusercontent.com/tokyo-metropolitan-gov/covid19/development/data/data.json"
    )

    dates = []
    numbers = []
    total = []
    for i, entry in enumerate(df["patients_summary"]["data"]):
        # print(i, entry)
        dates.append(entry["日付"])
        numbers.append(entry["小計"])
        if i == 0:
            total.append(entry["小計"])
        else:
            total.append(total[i - 1] + entry["小計"])
    # print(dates, numbers, total)

    dfout = pd.DataFrame(
        data={"date": dates, "cases": total, "deaths": np.array(total) * 0 + np.nan}
    )
    # dfout["date"] = pd.to_datetime(dfout["date"], format="%Y-%m-%dT%H:%M:%SZ")
    dfout["date"] = pd.to_datetime(dfout["date"])
    print(dfout.head(10))

    return dfout


# def read_toyokeizai_data():
#     df_japan = pd.read_csv(
#         "https://raw.githubusercontent.com/kaz-ogiwara/covid19/master/data/individuals.csv"
#     )


# %%
def plot_cases(
    df_hawaii,
    df_japan,
    df_counties,
    df_states,
    df_global,
    df_places_to_plot,
    colors,
    case="cases",
    ymin=0.9,
    ymax=5e5,
    thresh_confirmed=3000,
):

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

    for icolor, (place, category) in enumerate(
        zip(df_places_to_plot["place"], df_places_to_plot["category"])
    ):
        if category == "hawaii":
            df_plot = df_hawaii[
                (df_hawaii["place"] == place) & (df_hawaii["type"] == case)
            ]
            legend = "{} (County)".format(place)
            ystr = "Count"
        elif category == "japan":
            df_plot = df_japan
            legend = "{}".format(place)
            ystr = case
        elif category == "county":
            df_plot = df_counties[df_counties["place"] == place]
            legend = "{} (County)".format(place)
            ystr = case
        elif category == "state":
            df_plot = df_states[df_states["place"] == place]
            legend = "{} (State)".format(place)
            ystr = case
        elif category == "global":
            df_plot = df_global[
                (df_global["place"] == place) & (df_global["type"] == case)
            ]
            legend = df_plot["place"].values[0]
            ystr = "Count"

        df_plot.loc[:, "legend"] = legend

        pp.line(
            x="date",
            y=ystr,
            source=df_plot,
            line_width=3,
            color=colors[icolor],
            alpha=0.8,
            muted_color=colors[icolor],
            muted_alpha=0.4,
            muted_line_width=2,
            muted=True,
            legend_group="legend",
        )

    # for country in corona_sums_countries["Country/Region"].unique():
    #     df_country = corona_sums_countries[
    #         (corona_sums_countries["Country/Region"] == country)
    #     ]
    #     if (country not in countries_to_plot) and (
    #         df_country[df_country["type"] == "Confirmed"]["Count"].max()
    #         > thresh_confirmed
    #     ):
    #         # print(country, df_country[df_country["type"] == "Confirmed"]["Count"].max())
    #         df_country = df_country[df_country["type"] == case]
    #         pp.line(
    #             x="Date",
    #             y="Count",
    #             source=df_country,
    #             line_width=1.0,
    #             color="gray",
    #             alpha=0.8,
    #             muted_color="gray",
    #             muted_alpha=0.5,
    #             muted_line_width=0.5,
    #             muted=True,
    #             legend_group="Country/Region",
    #         )

    pp.legend.location = "top_left"
    pp.legend.click_policy = "mute"
    pp.legend.title = "Click to highlight"
    pp.legend.label_text_font_size = "8pt"
    pp.x_range = Range1d(datetime(2020, 1, 1), datetime.now())
    pp.y_range = Range1d(ymin, ymax)

    hover = pp.select(dict(type=HoverTool))
    hover.tooltips = [
        ("Place", "@{legend}"),
        ("Date", "$x{%Y-%m-%d}"),
        ("Value", "$y{0,0}"),
    ]
    hover.formatters = {"$x": "datetime"}
    hover.mode = "mouse"

    return pp


# %%
def plot_covid19_timeseries(outdir, df_places_to_plot):

    df_global = read_jhu_data()
    df_hawaii = read_hawaii_data()
    df_counties, df_states = read_nyt_data()
    df_japan = read_tokyo_data()

    n_lines = df_places_to_plot["place"].size
    colors = cc.glasbey_dark[:n_lines]

    p1 = plot_cases(
        df_hawaii,
        df_japan,
        df_counties,
        df_states,
        df_global,
        df_places_to_plot,
        colors,
        case="cases",
        ymin=0.9,
        ymax=5e5,
        thresh_confirmed=3000,
    )
    p1.title.text = 'Number of "confirmed" cases'

    p2 = plot_cases(
        df_hawaii,
        df_japan,
        df_counties,
        df_states,
        df_global,
        df_places_to_plot,
        colors,
        case="deaths",
        ymin=0.9,
        ymax=5e5,
        thresh_confirmed=3000,
    )
    p2.title.text = 'Number of "deaths"'

    div_disclaimer_en = Div(
        text="""The plots here are mainly for my own purpose. I do not recommend to trust my plots too much for any of your decision making. Please refer more reliable sources such WHO, CDC, and other local authorities if you are not sure what you are looking at.""",
        width=850,
    )
    div_disclaimer_ja = Div(
        text="""以下の図は自分用に作成したものです。そのため、図を過剰に信用して何かの判断の根拠にすることは避けてください。もしなにが描かれているかわからないようでしたら、WHOやCDC、各種国や自治体等の一次情報にあたることをおすすめします。""",
        width=850,
    )

    div_lastupdate = Div(
        text="""Last Update: {:s} (UTC)""".format(datetime.utcnow().isoformat()),
        width=850,
    )

    output_file(os.path.join(outdir, "index.html"), title="COVID-19 Cases")

    # p = column(div_disclaimer_en, div_disclaimer_ja, div_lastupdate, p1)
    p = column(div_disclaimer_en, div_disclaimer_ja, div_lastupdate, p1, p2)
    # p = column(p1)
    save(p)


# %%
if __name__ == "__main__":
    outdir = "../gist_covid19_plot/"

    df_places_to_plot = pd.DataFrame(
        data={
            "place": [
                "Hawaii",
                "Honolulu",
                "Tokyo",
                "Santa Clara",
                "California",
                "Hawaii",
                "China",
                "India",
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
            ],
            "category": [
                "hawaii",
                "hawaii",
                "japan",
                "county",
                "state",
                "state",
                "global",
                "global",
                "global",
                "global",
                "global",
                "global",
                "global",
                "global",
                "global",
                "global",
                "global",
                "global",
            ],
        }
    )

    plot_covid19_timeseries(outdir, df_places_to_plot)
