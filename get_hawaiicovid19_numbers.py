#!/usr/bin/env python

# %%
import os
from datetime import datetime
import pandas as pd
from bs4 import BeautifulSoup
from urllib import request


# %%
url = "https://hawaiicovid19.com/"
html = request.urlopen(url)
soup = BeautifulSoup(html, "lxml")
# mainNewsIndex = soup.find("ul", attrs={"class", "list-main-news"})
# headlines = mainNewsIndex.find_all("span", attrs={"class", "headline"})
# for headline in headlines:
#     print(headline.contents[0], headline.span.string)

# %%
tb = soup.find("table", class_="tablepress tablepress-id-1")
print(tb)

counties = []
numbers = []

print("")
print("")
print("")

# %%
for county, number in zip(
    tb.find_all("td", class_="column-1"), tb.find_all("td", class_="column-2")
):
    if not "TOTAL" in county.string:
        counties.append(county.string)
        numbers.append(int(number.string))
        print("{:20s} {:5d}".format(county.string, int(number.string)))

# %%
print("")


tb2 = soup.find(
    "span", class_="tablepress-table-description tablepress-table-description-id-1"
)
print(tb2.string)
print("")

# <span class=>*Cumulative totals as of 12:00pm on March 21, 2020, includes presumptive and confirmed</span>
# %%
df = pd.DataFrame(data={"County": counties, "Counts": numbers})
print(df.head())

# %%
datestring = datetime.now().isoformat()
# print(datestring)


# %%
outdir = "scraped"
outfile = os.path.join(outdir, "hawaii_scraped-{:s}.csv".format(datestring))
f = open(outfile, "w")
f.write("# " + tb2.string + "\n")
df.to_csv(f, index=False, header=True)
f.close()

print("")
print("{:s} is created.".format(outfile))
