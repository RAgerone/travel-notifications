from setup import db
from sqlalchemy.orm import relationship
from datetime import datetime


class TimestampMixin(object):
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow)


class PersistableMixin(object):
    @classmethod
    def create_by(cls, d):
        if 'city' in d:
            c = cls(city=d['city'], country=d['country'], code=d['code'])
        c.save()
        return c

    @classmethod
    def find_or_create_by(cls, d):
        return cls.find(d) or cls.create_by(d)

    def save(self):
        db.session.add(self)
        db.session.commit()


class Flight(TimestampMixin, PersistableMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    destination_id = db.Column(db.Integer, db.ForeignKey('destination.id'))
    destination = relationship("Destination", back_populates="flights")
    beginning = db.Column(db.Date, nullable=False)
    end = db.Column(db.Date, nullable=False)
    cost = db.Column(db.Float, nullable=False)
    url = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"<Flight id='{self.id}' cost='{self.cost}'"

    def to_csv(self):
        return ", ".join([
            str(self.id),
            self.created.strftime('%e %b %Y %H:%M:%S%p'),
            self.beginning.strftime('%e %b %Y'),
            self.end.strftime('%e %b %Y'),
            str(self.cost),
            self.url
        ])

    @property
    def dates(self):
        return f"{self.beginning.strftime('%b %d')} - {self.end.strftime('%b %d')}"

    def num_days(self):
        return (self.end - self.beginning).days

    def month(self):
        return self.beginning.strftime("%B")

    def chart_timestamp(self):
        return self.created.strftime("%Y-%m-%d %H:%M:%S ") + "-0800"


class Destination(TimestampMixin, PersistableMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(50), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    code = db.Column(db.String(10), nullable=False)
    flights = relationship("Flight", back_populates="destination")

    def __repr__(self):
        return f"<Destination id='{self.id}' city='{self.city}' code='{self.code}' />"

    @classmethod
    def find(cls, d):
        return cls.query.filter(cls.city == d['city']).one_or_none()

    def flights_to_chart_data(self):
        data = {
            'name': self.code,
            'data': {f.chart_timestamp(): f.cost for f in self.flights}
        }

        return data


def flights_backup_to_csv():
    file = open('flights.csv', 'w+')

    while flights:
        file.write(flights[0].to_csv() + "\n")
        flights.pop(0)

    file.close()


def destinations_backup_to_csv():
    file = open('destinations.csv', 'w+')

    while destinations:
        file.write(destinations[0].to_csv() + "\n")
        destinations.pop(0)

    file.close()


"""
id, created, city, country, airport_code, beginning, end, cost, url
3358, 16 Jun 2018 20:39:57PM, Marseille, FR, MRS, 10 Jul 2018, 19 Jul 2018, 1520.0, /cheap-flights/seattle-wa-sea-to-marseille-france-mrs/?fare_id=8055510

take this line:
Create the Destination using city, country, airport_code, and created
"""


def seed_database():
    file = open("data.csv", "r")
    header = None
    for line in file:
        if header is None:
            header = line
        else:
            d, f = deconstruct_line(line)
            destination = Destination.find_or_create_by(d)
            flight = Flight(
                created=datetime.strptime(
                    f['created'], '%d %b %Y %H:%M:%S%p'),
                beginning=f['beginning'],
                end=f['end'],
                cost=f['cost'],
                url=f['url'])
            flight.destination_id = destination.id
            flight.save()


def deconstruct_line(line):
    id, created, city, country, code, beginning, end, cost, url = line.split(
        ', ')

    destination = {
        'city': city, 'country': country, 'code': code
    }
    flight = {
        'created': created,
        'beginning': beginning,
        'end': end,
        'cost': float(cost),
        'url': url
    }
    return destination, flight
