# COVID-19 Plots

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
├── COVID-19
├── covid19plot (This repository)
│  ├── csv/
│  ├── LICENSE
│  ├── plot_cases.py
│  └── README.md
└── gist
   └── index.html (Output file from the script)

```
The `COVID-19` folder is a cloned repository of [the JHT CSSE database](https://github.com/CSSEGISandData/COVID-19) for international data and US state data.

After the script is executed it writes `index.html` under `gist` folder.

I should make the structure more flexible, but currently it works for my purpose.


### Installing

#### 1. Make a parent directory and go there

```
mkdir covid19_plots
cd covid19_plots
```

#### 2. Clone the JHU CSSE repository

```
git clone https://github.com/CSSEGISandData/COVID-19.git
```

#### 3. Create the output directory

```
mkdir gist  # sorry it's hard-coded
```

#### 4. Clone this repository

```
git clone https://github.com/monodera/covid19plot.git
```


## Run the script

It's very simple.  Just execute the script.

```
cd covid19plot
python ./plot_cases.py
```

At the end, you should find `index.html` in the `gist` directory you made in the step 3. Open it with a web browser.


## What's in the output

The script produces 4 plots with interactive legends and tooltips.  You can highlight or mute lines by clicking either legend entries and lines themselves.  You can also see numbers and regions at a given date by hovering the mouse cursor.

Here are some explations on what are plotted.

### 1st panel from the top

The cumulative number of confirmed cases at each day.


### 2nd panel from the top

The cumulative number of deaths at each day.


### 3rd panel from the top

The cumulative number of recovered cases at each day.


### 4th panel from the top

The cumulative number of active (confirmed - deaths - recovered) cases at each day.



## Contributing

Please make any pull requests and put issues.


## Authors

* **Masato Onodera** - [monodera](https://github.com/monodera)


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

- [JHU database](https://github.com/CSSEGISandData/COVID-19)
- [News Releasesfrom Department of Health, State of Hawaii](https://health.hawaii.gov/news/category/corona-virus/)
- [Mapping the Spread of Coronavirus COVID-19 with python and Plotly](https://medium.com/analytics-vidhya/mapping-the-spread-of-coronavirus-covid-19-d7830c4282e)
