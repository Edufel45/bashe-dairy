from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.cache import cache_control
from .models import *

UI = {
 "en": dict(home="Home", livestock="Livestock", about="About", contact="Contact", browse="Browse Livestock",
  avail="Available Livestock", browse_sub="Browse our premium livestock collection", all="All", inquire="Inquire",
  weight="Weight", contact_title="Contact Us", contact_sub="Send us your livestock inquiries", name_ph="Your Name",
  email_ph="Email Address", inquiry_ph="Your Inquiry", send="Send Inquiry on WhatsApp", rights="All rights reserved.",
  note="NOTE", wa_prod="Hello {site}, I am interested in {p}.", wa_gen="Hello {site}, I am interested in your livestock and would like more details.", other="KISW", other_label="Kiswahili"),
 "sw": dict(home="Nyumbani", livestock="Mifugo", about="Kuhusu Sisi", contact="Wasiliana Nasi", browse="Tazama Mifugo",
  avail="Mifugo Inayopatikana", browse_sub="Tazama mkusanyiko wetu wa mifugo bora", all="Yote", inquire="Uliza Bei",
  weight="Uzito", contact_title="Wasiliana Nasi", contact_sub="Tutumie maswali yako kuhusu mifugo", name_ph="Jina lako",
  email_ph="Barua pepe", inquiry_ph="Swali lako", send="Tuma Swali kupitia WhatsApp", rights="Haki zote zimehifadhiwa.",
  note="TAHADHARI", wa_prod="Habari {site}, nimevutiwa na {p}.", wa_gen="Habari {site}, nimevutiwa na mifugo yenu na ningependa maelezo zaidi.", other="ENG", other_label="English"),
}
HERO = "https://images.unsplash.com/photo-1500595046743-cd271d694d30?auto=format&fit=crop&w=1600&q=70"


def loc(objs, fields, lang):
    """Attach l_<field> = Swahili text when available, else English."""
    for o in objs:
        for f in fields:
            v = getattr(o, f + "_sw", "") if lang == "sw" else ""
            setattr(o, "l_" + f, v or getattr(o, f))
    return objs


@cache_control(public=True, s_maxage=60, stale_while_revalidate=600)
def home(request, lang="en"):
    s = loc([SiteSettings.load()], ["tagline", "hero_title", "hero_subtitle", "about_title", "about_text", "info_title", "info_intro", "info_footer", "meta_description", "meta_keywords"], lang)[0]
    t = dict(UI[lang])
    t["wa_prod"] = t["wa_prod"].replace("{site}", s.site_name)
    t["wa_gen"] = t["wa_gen"].format(site=s.site_name)
    products = loc(list(Product.objects.filter(is_active=True).select_related("category").prefetch_related("images")), ["name", "description"], lang)
    for p in products:
        p.wa = t["wa_prod"].replace("{p}", p.l_name)
    return render(request, "home.html", {
        "s": s, "t": t, "lang": lang, "hero": s.hero_image.url if s.hero_image else HERO,
        "features": loc(list(Feature.objects.all()), ["title", "text"], lang),
        "info": loc(list(InfoOption.objects.all()), ["title", "text", "note"], lang),
        "cats": loc(list(Category.objects.all()), ["name"], lang),
        "products": products,
    })


def robots(request):
    return HttpResponse(f"User-agent: *\nAllow: /\nDisallow: /admin/\nSitemap: {request.build_absolute_uri('/sitemap.xml')}\n", content_type="text/plain")
