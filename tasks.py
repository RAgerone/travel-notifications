import atexit
from services import get_flights
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger


def run_backgrounder():
    scheduler = BackgroundScheduler()
    scheduler.start()
    scheduler.add_job(
        func=get_flights,
        trigger=IntervalTrigger(minutes=1),
        id='getting_flights',
        name='Scrape flights and place them into the database'
    )
    atexit.register(lambda: scheduler.shutdown())
