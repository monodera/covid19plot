#!/bin/sh

while true
do
    echo ""
    echo "Scrape Hawaii's COVID-19 web site"
    echo ""
    OUTFILE="scraped/hawaii_scraped-`/usr/local/bin/gdate --iso-8601='seconds'`.txt"
    python ./get_hawaiicovid19_numbers.py > $OUTFILE || break
    echo ""
    echo "👍"

    date \
    && sleep 21600 \
    || break
done

# hawaii_scraped-2020-03-26T14:32:46.725332.csv

# /usr/local/bin/gdate
# gdate --iso-8601='seconds'