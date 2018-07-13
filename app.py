from flask import render_template, request
from datetime import timedelta
from models import Destination, Flight
from services import get_flights, post_to_slack
from serializers import DestinationSerializer, FlightSerializer
from setup import app, db
import json


def to_json(resources, klass=FlightSerializer):
    return json.dumps(resources, cls=klass)


@app.route("/flights")
def flights():
    last_in = Flight.query.order_by(Flight.id.desc()).first()
    flights = Flight.query.filter(Flight.created.between(
        last_in.created - timedelta(seconds=30),
        last_in.created
    )).order_by(Flight.cost).all()

    return to_json(flights)


@app.route("/destinations")
def destinations():
    destinations = Destination.query.order_by(Destination.city).all()

    return to_json(destinations, DestinationSerializer)


"""
Grab all destinations
{
    destinations: [
        {
            name: 'Dublin',
            flights: [
                {
                    created,
                    cost
                },
                ...
            ]
        },
        ...
    ]
}
"""
"""
data = [
  {name: 'Workout', data: {'2017-01-01 00:00:00 -0800': 3, '2017-01-02 00:00:00 -0800': 4}},
  {name: 'Call parents', data: {'2017-01-01 00:00:00 -0800': 5, '2017-01-02 00:00:00 -0800': 3}}
];
"""


@app.route("/graph")
def graph():
    all_destinations = Destination.query.all()
    destinations_data = [d.flights_to_chart_data() for d in all_destinations]

    return json.dumps(destinations_data)


@app.route("/destinations/<string:code>")
def airport(code):
    flights_at_airport = Flight.query.filter(
        Flight.airport_code == code).order_by(Flight.cost).all()

    return to_json(flights_at_airport)


@app.route("/slack", methods=["POST"])
def slack():
    request_json = request.get_json()
    n = request_json.get('number')

    last_in = Flight.query.order_by(Flight.id.desc()).first()
    top_n = Flight.query.filter(Flight.created.between(
        last_in.created - timedelta(seconds=30),
        last_in.created
    )).order_by(Flight.cost).limit(n).all()

    post_to_slack(top_n)

    return to_json(top_n)
