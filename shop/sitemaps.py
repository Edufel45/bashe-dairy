from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Product


class HomeSitemap(Sitemap):
    changefreq = "daily"; priority = 1.0
    def items(self): return ["home", "home_sw"]
    def location(self, i): return reverse(i)
    def lastmod(self, i): return None
