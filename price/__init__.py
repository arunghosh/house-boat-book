from .exception import DatePriceNotFoundException
from datetime import date, timedelta
import calendar
from dateutil import rrule
class PricePicker:
    def __init__(self, boat):
        self.boat = boat
        self.primary = boat.price
        self.season = boat.season_prices.active()

    def for_date(self, date):
        season = [p for p in self.season if p.date_from <= date <= p.date_to]
        if len(season) > 0:
            price = season[-1].price
        else:
            price = self.primary
        price.boat = self.boat
        return price


class MonthPriceHelper():

    def __init__(self, request, month, year):
        self.boat = request.boat
        year = int(year)
        month = int(month)
        self.start = date(month=month, year=year, day=1)
        self.end = self.start + timedelta(days=calendar.monthrange(year, month)[1] - 1)

    def get_prices(self):
        picker = PricePicker(self.boat)
        result = []
        for d in [d.date() for d in rrule.rrule(rrule.DAILY, dtstart=self.start, until=self.end)]:
            order = [o for o in self.boat.orders.all() if o.date_in == d]
            if len(order) > 0:
                order_id = order[0].id
                price = order[0].price
            else:
                order_id = -1
                price = picker.for_date(d)

            result.append({
                'date': d,
                'order_id': order_id,
                'price': price.base
            })
        return result