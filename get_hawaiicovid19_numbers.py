#!/usr/bin/env python

# %%
import os
import sys
from datetime import datetime
import pandas as pd
from bs4 import BeautifulSoup
from urllib import request
from astropy.table import Table, vstack
from astropy.io import ascii


# %%
# url = "https://hawaiicovid19.com/"
url = "https://health.hawaii.gov/coronavirusdisease2019/what-you-should-know/current-situation-in-hawaii/"
html = request.urlopen(url)
soup = BeautifulSoup(html, "lxml")
# mainNewsIndex = soup.find("ul", attrs={"class", "list-main-news"})
# headlines = mainNewsIndex.find_all("span", attrs={"class", "headline"})
# for headline in headlines:
#     print(headline.contents[0], headline.span.string)

# %%
html_tb = soup.find_all(
    "tr",
    # style="height: 24px; font-size: 15px;"
    # style="height: 260px; width: 500px; border-collapse: collapse; border: thin solid #c8c8c8; margin-right: 15px;",
    # class_="tablepress tablepress-id-2 reportedcases"
)
# print(html_tb)

# %%
# print(html_tb[0])
tb_header = ascii.read(
    "<table>" + str(html_tb[0]) + "</table>",
    format="html",
    # names=["county", "hawaii_residents", "nonhawaii_residents", "number"],
)
tb_header.write(sys.stdout, format="ascii.fixed_width_no_header", delimiter_pad=",")

# %%
for i in range(1, len(html_tb)):
    tb_body_tmp = ascii.read(
        "<table>" + str(html_tb[i]) + "</table>",
        format="html",
        # names=["county", "hawaii_residents", "nonhawaii_residents", "number"],
    )
    tb_body_tmp.write(
        sys.stdout, format="ascii.fixed_width_no_header", delimiter_pad=","
    )

# print(tb_body)

# # %%
# # print(tb.prettify())
# # print(type(tb.prettify()))
# tb = ascii.read(
#     str(html_tb),
#     format="html",
#     names=["county", "hawaii_residents", "nonhawaii_residents", "number"],
# )
# print(tb)
# # tb.find_all("td", class_="column-1")

# # %%
# # for county, number in zip(
# #     tb.find_all("td", class_="column-1"), tb.find_all("td", class_="column-2")
# # ):
# #     if not "TOTAL" in county.string:
# #         counties.append(county.string)
# #         numbers.append(int(number.string))
# #         print("{:20s} {:5d}".format(county.string, int(number.string)))

# # # %%
# # print("")


# # tb2 = soup.find(
# #     "span", class_="tablepress-table-description tablepress-table-description-id-1"
# # )
# # print(tb2.string)
# # print("")

# # # <span class=>*Cumulative totals as of 12:00pm on March 21, 2020, includes presumptive and confirmed</span>
# # %%
# # df = pd.DataFrame(data={"County": counties, "Counts": numbers})
# # df = tb.to_pandas()
# # print(df.head())

# # %%
# datestring = datetime.now().isoformat()
# # print(datestring)


# # %%
# outdir = "scraped"
# outfile = os.path.join(outdir, "hawaii_scraped-{:s}.csv".format(datestring))
# tb.write(outfile)
# # f = open(outfile, "w")
# # f.write("# " + tb2.string + "\n")
# # df.to_csv(f, index=False, header=True)
# # f.close()

# print("")
# print("{:s} is created.".format(outfile))
