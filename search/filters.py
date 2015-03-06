from boat.models import Boat
import json
import pdb


class BoatFinder():

    def __init__(self, request):
        query = json.loads(request.body)
        self.filters = [AmenityFilter(query), ACFilter(query)]

    def get_boats(self):
        boats = Boat.objects.all()
        for f in self.filters:
            boats = f.execute(boats)
        return boats


class RoomFilter():

    def __init__(self, count_list):
        self.count_list = count_list

    def execute(self, boats):
        if self.count_list:
            boats = boats.filter(no_rooms__in=self.count_list)
        return boats


class ACFilter:
    def __init__(self, query):
        self.ac_types = query.get('AC', [])

    def execute(self, boats):
        if len(self.ac_types) > 0:
            boats = boats.filter(ac_type__in=self.ac_types)
        return boats


class AmenityFilter:

    def __init__(self, query):
        self.amenities = query.get('amenities', [])

    def execute(self, boats):
        for a in self.amenities:
            boats = boats.filter(amenities__id=int(a))
        return boats


# class HallTypeFilter():
#
#     def __init__(self, types):
#         self.types = types
#
#     def execute(self, halls):
#         if self.types:
#             for t in self.types:
#                 # [h for h in halls if x in b]
#                 halls = halls.filter(hall_types__id=t)
#         return halls