from company.models import Company, Owner
from account.models import BaseUser
from boat.models import Boat
from price.models import Price
from amenity.models import Amenity
from django.db import transaction


# import urls
#
# def show_urls(urllist, depth=0):
#     for entry in urllist:
#         print "  " * depth, entry.regex.pattern
#         if hasattr(entry, 'url_patterns'):
#             show_urls(entry.url_patterns, depth + 1)
#
# show_urls(urls.urlpatterns)

@transaction.atomic
def fill_db():
    su = BaseUser.objects.create_superuser(email="a@g.com", password="abcd1234", name="Arun")
    c = Company.objects.create(name="Lake Lagoons")
    c1 = Company.objects.create(name="Alleppey Boats")
    u = BaseUser.objects.create_user(name="Arun", email="user@ll.com", password="abcd1234")
    o = Owner.objects.create(user=u, company=c)
    a1 = Amenity.objects.create(name="Swing", searchable=True)
    a2 = Amenity.objects.create(name="Television", searchable=True)
    a3 = Amenity.objects.create(name="Liquor", searchable=False)
    a4 = Amenity.objects.create(name="Fishing", searchable=True)
    a5 = Amenity.objects.create(name="Wi-Fi", searchable=True)
    b1 = Boat.objects.create(name="LL1",
                             company=c,
                             no_room=1,
                             no_adult=2,
                             max_adult=3,
                             max_child=2,
                             status=Boat.STAT_ACTIVE,
                             ac_type=Boat.AC_PARTIAL)

    b2 = Boat.objects.create(name="LL2",
                             company=c,
                             no_room=2,
                             no_adult=4,
                             max_adult=6,
                             max_child=4,
                             status=Boat.STAT_ACTIVE,
                             ac_type=Boat.AC_FULL)

    b3 = Boat.objects.create(name="AB1",
                             company=c1,
                             no_room=1,
                             no_adult=2,
                             max_adult=3,
                             max_child=2,
                             status=Boat.STAT_ACTIVE,
                             ac_type=Boat.AC_FULL)


    b4 = Boat.objects.create(name="AB4",
                             company=c1,
                             no_room=1,
                             no_adult=2,
                             max_adult=3,
                             max_child=2,
                             status=Boat.STAT_ACTIVE,
                             ac_type=Boat.AC_FULL)

    Price.objects.create(boat=b1, base=10000, adult=400, child=200, is_primary=True)
    Price.objects.create(boat=b2, base=12000, adult=400, child=200, is_primary=True)
    Price.objects.create(boat=b3, base=14000, adult=400, child=200, is_primary=True)
    Price.objects.create(boat=b4, base=14000, adult=400, child=200, is_primary=True)

    b1.amenities.add(a1)
    b1.amenities.add(a2)
    b1.amenities.add(a3)
    b1.save()
    b2.amenities.add(a2)
    b2.amenities.add(a5)
    b2.amenities.add(a4)
    b2.save()

    b3.amenities.add(a1)
    b3.amenities.add(a2)
    b3.amenities.add(a5)
    b3.amenities.add(a4)
    b3.save()

    b4.amenities.add(a1)
    b4.amenities.add(a2)
    b4.amenities.add(a5)
    b4.amenities.add(a4)
    b4.save()