#!/bin/sh

while true
do
    echo ""
    echo "Scrape Hawaii's COVID-19 web site"
    echo ""
    python ./get_hawaiicovid19_numbers.py || break
    echo ""
    echo "👍"

    date \
    && sleep 21600 \
    || break
done
