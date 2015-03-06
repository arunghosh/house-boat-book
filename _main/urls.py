from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin

from rest_framework import routers

from search.views import home, BoatIdsView
from boat import views as boat_views
from amenity.views import UpdateBoatAmenityView
from helper import list_views
# from order.views import get_booked_boat_ids, OrderCreateView, BoatOrdersView, OrdersDetailsView
from order import views as order_v
from price import views as price_v
from cancel import views as cancel_views
from maintenance import views as blockViews
from review.views import AddReviewView, BoatReviewsView
from manager import views as manager_v
from company import views as company_v

admin.autodiscover()

router = routers.DefaultRouter()
router.register(r'boats', boat_views.AllBoatsViewSet)
router.register(r'companies', company_v.CompanyViewSet)
# router.register(r'maintenance', MaintenanceViewSet)
# router.register(r'prices', PriceViewSet)

DATE_FORMAT = "(?P<year>\d{4})-(?P<month>[0-9]*)-(?P<day>[0-9]*)"
BOAT_ID = "(?P<boat_id>[0-9]*)"
ORDER_ID = "(?P<order_id>[0-9]*)"
COMPANY_ID = "(?P<company_id>[0-9]*)"

list_urls = [
    url(r'^ac_types/$', list_views.ac_opts),
    url(r'^amenities/$', list_views.amenities), ]

company_urls = [
    url(r'^$', company_v.home),
    url(r'^/self/$', company_v.CompanyDetailsView.as_view()),
    url(r'^%s/owners/$' % COMPANY_ID, company_v.OwnersAPI.as_view()),
    url(r'^%s/boats/$' % COMPANY_ID, company_v.BoatsAPI.as_view()),
    url(r'^%s/orders/$' % COMPANY_ID, company_v.OrdersAPI.as_view()),
    url(r'^%s/orders/upcoming/$' % COMPANY_ID, company_v.UpcomingOrdersAPI.as_view())]

manager_urls = [
    # url(r'^boats/$', manager_v.BoatsAPI.as_view()),
    url(r'^orders/$', manager_v.OrderAPI.as_view()),
    url(r'^logout/$', manager_v.logout_user),
    url(r'^menus/$', manager_v.MenuView.as_view()),
    url(r'^$', manager_v.HomeView.as_view())]

order_urls = [
    url(r'^%s/$' % ORDER_ID, order_v.OrdersDetailsView.as_view()),
    url(r'^create/$', order_v.OrderCreateView.as_view()),
    url(r'^review/$', AddReviewView.as_view()),
    url(r'^cancel/$', cancel_views.OrderCancelView.as_view())]

price_urls = [
    url(r'^date/{0}/$'.format(DATE_FORMAT), price_v.DatePricesView.as_view()),
    url(r'^boat/{0}/{1}/$'.format(BOAT_ID, DATE_FORMAT), price_v.BoatDatePricesView.as_view()),
    url(r'^season/$', price_v.UpdateSeasonPriceView.as_view()),
    url(r'^base/$', price_v.UpdateBoatPriceView.as_view()),
    url(r'^month/%s/(?P<year>\d{4})/(?P<month>[0-9]*)/$' % BOAT_ID, price_v.MonthView.as_view()),
    url(r'^boat/%s/$' % BOAT_ID, price_v.BoatPricesView.as_view())]

boat_urls = [
    url(r'^$', boat_views.boat_detail),
    url(r'^update/$', boat_views.BoatUpdateView.as_view()),
    url(r'^%s/c_policy/$' % BOAT_ID, cancel_views.BoatCancelPolicyView.as_view()),
    url(r'^%s/reviews/$' % BOAT_ID, BoatReviewsView.as_view()),
    url(r'^%s/orders/$' % BOAT_ID, order_v.BoatOrdersView.as_view()),
    url(r'^%s/orders/upcoming/$' % BOAT_ID, order_v.UpcomingBoatOrdersView.as_view()),
    url(r'^%s/maintenance/$' % BOAT_ID, blockViews.MaintenanceView.as_view()),
    url(r'^{0}/policies/{1}/$'.format(BOAT_ID, DATE_FORMAT), cancel_views.BoatDatePoliciesView.as_view()),
    url(r'^booked/{0}/$'.format(DATE_FORMAT), order_v.get_booked_boat_ids),
    url(r'^amenities/update/$', UpdateBoatAmenityView.as_view()),
    url(r'^c_policy/$', cancel_views.CommonCancelPolicyView.as_view()),
    url(r'^active/', boat_views.ActiveBoatsAPI.as_view())]

urlpatterns = patterns(
    '',
    url(r'^$', home),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^search/ids/$', BoatIdsView.as_view()),
    url(r'^boats/', include(boat_urls)),
    url(r'^list/', include(list_urls)),
    url(r'^order/', include(order_urls)),
    url(r'^price/', include(price_urls)),
    url(r'^company/', include(company_urls)),
    url(r'^api/', include(router.urls)),
    url(r'^manage/', include(manager_urls)),
)

          # + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)