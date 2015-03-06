from django import forms
from boat.models import Amenity, Boat

from .filters import AmenityFilter, RoomFilter


# class FilterForm(forms.Form):
#     amenities = Amenity.objects.searchable()
#     AMENITY_OPTS = ((a.id, a.name) for a in amenities)
#
#     # hall_types = HallType.objects.all()
#     # HALL_TYPES_OPTS = ((a.id, a.name) for a in hall_types)
#
#     # seats = forms.IntegerField()
#     # price = forms.IntegerField()
#     ROOM_OPTS = [(r, str(r) + " rooms") for r in set([b.no_rooms for b in Boat.objects.active()])]
#     rooms = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(), choices=ROOM_OPTS)
#     ac_types = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(), choices=Boat.AC_CHOICES)
#     amenities = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(), choices=AMENITY_OPTS)
#     # hall_types = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(), choices=HALL_TYPES_OPTS)
#
#     def get_filters(self):
#         self.is_valid()
#         # seat_filter = SeatFilter(self.cleaned_data['seats'] if ('seats' in self.cleaned_data) else 0)
#         amenity_filter = AmenityFilter(self.cleaned_data['amenities'] if ('amenities' in self.cleaned_data) else 0)
#         room_filter = RoomFilter(self.cleaned_data['rooms'] if ('rooms' in self.cleaned_data) else 0)
#         result = [amenity_filter, room_filter]
#         return result