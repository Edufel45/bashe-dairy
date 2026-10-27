from django.contrib import admin
from django.urls import path, re_path
from django.views.static import serve
from django.conf import settings
from django.contrib.sitemaps.views import sitemap
from shop.views import home, robots
from shop.sitemaps import HomeSitemap
admin.site.site_header = "Bashe Dairy Admin"
urlpatterns = [
    path("admin/", admin.site.urls),
    path("sitemap.xml", sitemap, {"sitemaps": {"home": HomeSitemap}}),
    path("robots.txt", robots),
    path("", home, {"lang": "en"}, name="home"),
    path("sw/", home, {"lang": "sw"}, name="home_sw"),
]
if not settings.USE_CLOUD_MEDIA:
    urlpatterns.append(re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}))
