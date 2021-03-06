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
    "table",
    # "tr",
    # style="height: 24px; font-size: 15px;"
    # style="height: 260px; width: 500px; border-collapse: collapse; border: thin solid #c8c8c8; margin-right: 15px;",
    # class_="tablepress tablepress-id-2 reportedcases"
)
html_h2 = soup.find_all("h2",)
html_thead = soup.find_all("thead")

# print(html_tb)

for h2 in html_h2:
    print("# h2: {}".format(h2.get_text()))

for thead in html_thead:
    print("# thead: {}".format(thead.tr.th.get_text()))

# %%
# print(html_tb[0])
str_strip = (
    str(html_tb[0])
    .replace("<strong>", "")
    .replace("</strong>", "")
    .replace("<thead>", "")
    .replace("</thead>", "")
    .replace("\xa0", " ")
    .replace(">", ">\n")
)
tb_header = ascii.read(str_strip, format="html", names=["case", "number"],)
tb_header.write(sys.stdout, format="ascii.fixed_width")  # , delimiter_pad=",")

# %%
for i in range(1, len(html_tb)):
    str_strip = (
        str(html_tb[i])
        .replace("<strong>", "")
        .replace("</strong>", "")
        .replace("<thead>", "")
        .replace("</thead>", "")
        .replace("\xa0", " ")
        .replace(">", ">\n")
    )
    try:
        tb_body_tmp = ascii.read(str_strip, format="html", names=["case", "number"])
        tb_body_tmp.write(sys.stdout, format="ascii.fixed_width_no_header")
    except:
        print(html_tb[i].get_text("   "))


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


# s = """
# <html>
#     <head>
#     </head>
#     <body>
#         <table>
#             <tr>
#                 <td>Total Cases</td>
#                 <td>574 (21 newly reported)</td>
#             </tr>
#             <tr>
#                 <td>Released from Isolation</td>
#                 <td>410</td>
#             </tr>
#             <tr>
#                 <td>Required Hospitalization</td>
#                 <td>51</td>
#             </tr>
#             <tr>
#                 <td>Deaths</td>
#                 <td>9</td>
#             </tr>
#         </table>
#     </body>
# </html>
# """
