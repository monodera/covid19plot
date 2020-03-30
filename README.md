# COVID-19 Plots
---

Plot COVID-19 cases based on publicly available data with some emphasis on the Hawaii cases.
The project is mainly for my own purpose.  I do not recommend to trust my plots too much for any of your decision making.
Please refer more reliable sources such [WHO](https://www.who.int), [CDC](https://www.cdc.gov/), and other local authorities if you are not sure what you are looking at.

## Getting Started

### Prerequisites

It is a Python script. You need following packages to run the script.

- [Python3](https://www.python.org/)
- [Pandas](https://pandas.pydata.org/)
- [Bokeh](https://docs.bokeh.org/en/latest/)
- [Colorcet](https://colorcet.holoviz.org/)

I'm currently using the following versions.

- Python 3.6.10
- Pandas 1.0.2
- Bokeh 2.0.0
- Colorcet 1.0.0

Also, currently,  I'm working in a directory with a structure like this.

```
.
├── covid19plot (This repository)
│  ├── csv/
│  ├── LICENSE
│  ├── make_covid19_plots.py
│  └── README.md
└── gist_covid19_plot
   └── index.html (Output file from the script)

```

The `csv` directory under this repository (`covid19plot`) contains CSV files for counties in State of Hawaii with the identical format to those of the JHU CSSE database.  I'm trying to keep update them, but make sure you are fine with them.  The update may suddenly stop.  At some point, I'm planning to use the CSV files from the NYT repository.

After the script is executed it writes `index.html` under `gist_covid19_plot` folder.

I should make the structure more flexible, but currently it works for my purpose.


### Installing

#### 1. Create the output directory

```
mkdir gist_covid19_plot  # sorry it's hard-coded
```

#### 2. Clone this repository

```
git clone https://github.com/monodera/covid19plot.git
```


### Run the script


It's very simple.  Just execute the script.

```
cd covid19plot
python ./make_covid19_plots.py
```

At the end, you should find `index.html` in the `gist_covid19_plot` directory you made in the step 1. Open it with a web browser.


## What's in the output

You can see the example of the output at https://bl.ocks.org/monodera/78ce91f69e3bf5da21302807f373b5b6 .

The script produces 4 plots with interactive legends and tooltips.  You can highlight or mute lines by clicking either legend entries and lines themselves.  You can also see numbers and regions at a given date by hovering the mouse cursor.

Here are some explations on what are plotted.

### 1st panel from the top

The cumulative number of confirmed cases at each day.


### 2nd panel from the top

The cumulative number of deaths at each day.


## Contributing

Please make any pull requests and put issues.


## Authors

- **Masato Onodera** - [monodera](https://github.com/monodera)

## License


This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Acknowledgments


- [JHU database](https://github.com/CSSEGISandData/COVID-19)
- [NYT database](https://github.com/nytimes/covid-19-data)
- [News Releases from Department of Health, State of Hawaii](https://health.hawaii.gov/news/category/corona-virus/)
- [Hawaii COVID-19 web site](https://hawaiicovid19.com/)
- [Mapping the Spread of Coronavirus COVID-19 with python and Plotly](https://medium.com/analytics-vidhya/mapping-the-spread-of-coronavirus-covid-19-d7830c4282e)
