import json
from sqlalchemy.ext.declarative import DeclarativeMeta


class AlchemySerializer(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    # this will fail on non-encodable values, like other classes
                    json.dumps(data)
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)


class FlightSerializer(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            fields['created'] = str(obj.created)
            fields['cost'] = obj.cost
            fields['dates'] = obj.dates
            fields['url'] = obj.url
            fields['code'] = obj.destination.code
            fields['destination'] = f"{obj.destination.city}, {obj.destination.country}"
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)


class DestinationSerializer(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            fields['city'] = obj.city
            fields['country'] = obj.country
            fields['code'] = obj.code
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)
