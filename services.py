import requests
import json
import logging
from datetime import date
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import models


def get_flights():
    # file = open("index.html", 'r')
    # file.close()
    URL = "https://www.airfarewatchdog.com/cheap-flights/from-Seattle-Washington/SEA/?filter_type=INTERNATIONAL&sortedBy=price%2CASC"
    source = visit_page(URL)
    soup = BeautifulSoup(source, 'html.parser')

    # for i, el in enumerate(all_fares):
    #     flight_div = el.select('.fare_group_location')[0]
    #     city, country, airport_code = parse_destination(flight_div)
    #     print(f"{i}, {city}, {airport_code}")

    destinations = []
    all_fares = soup.findAll("div", {"class": "fares"})
    for el in all_fares:
        flight, destination = get_flight_and_destination(el)
        flight.save()
        destinations.append(flight)

    return destinations


def visit_page(url):
    driver = webdriver.Firefox()
    driver.get(url)
    driver.implicitly_wait(5)
    driver.find_element_by_class_name('close_btn').click()
    driver.find_element_by_class_name('do_load_more_fares_row').click()
    driver.implicitly_wait(3)
    driver.find_element_by_class_name('do_load_more_fares_row').click()
    text = driver.page_source
    driver.quit()
    return text


def get_flight_and_destination(el):
    flight_div = el.select('.fare_group_location')[0]
    city, country, code = parse_destination(flight_div)
    cheapest = scrape_cheapest(el.find_all("div", {"class": "fare_row"}))
    print(", ".join([city, country, code, str(cheapest)]))
    destination = models.Destination.find_or_create_by(
        {'city': city, 'country': country, 'code': code})

    flight = models.Flight(beginning=cheapest['beginning'],
                           end=cheapest['end'],
                           cost=cheapest['cost'],
                           url=cheapest['url'])
    destination.flights.append(flight)

    return flight, destination


def parse_destination(el):
    d, code = el.text.split("to\n\n")[1].strip().split(" (")
    code = code[:-1]
    city, country = d.split(", ")
    return city, country, code


def scrape_cheapest(el_arr):
    cheapest = {}
    for el in el_arr:
        price = int(el.select('.fare_price')[0].text.strip('$'))
        if 'cost' not in cheapest or cheapest['cost'] > price:
            b, e = parse_dates_from_flight(el)
            u = el.find('a').get('href')

            cheapest = {
                "beginning": b,
                "end": e,
                "cost": price,
                "url": u
            }

    return cheapest


def parse_dates_from_flight(el):
    if len(el.select('.fare_travel_dates')) > 0:
        dates_str = el.select('.fare_travel_dates')[0].text
        b, e = dates_str.split(" - ")
        return make_date(b), make_date(e)
    return make_date("1/1/1990"), make_date("1/1/1990")


def make_date(date_str):
    m, d, y = map(lambda x: int(x), date_str.split("/"))
    y = y + 2000
    return date(y, m, d)


def post_to_slack(flights):
    url = "https://hooks.slack.com/services/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"
    d = {"text": format_slack_payload(flights)}
    requests.post(url, data=json.dumps(d), headers={
                  'Content-Type': 'application/json'})


def format_slack_payload(flights):
    return ",\n".join(["${0}. {1}, {2}".format(d.cost, d.destination.city, d.destination.country) for d in flights])
