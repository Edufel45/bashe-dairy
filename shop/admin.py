from django.contrib import admin
from django.utils.html import format_html
from .models import *


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Brand & contact", {"fields": ["site_name", "tagline", "whatsapp", "phone", "email", "location", "footer_text"]}),
        ("Hero", {"fields": ["hero_title", "hero_subtitle", "hero_image"]}),
        ("About", {"fields": ["about_title", "about_text", "about_image"]}),
        ("Info box", {"fields": ["show_info_box", "info_title", "info_intro", "info_footer"]}),
        ("Kiswahili (leave blank to show English)", {"classes": ["collapse"], "fields": ["hero_title_sw", "hero_subtitle_sw", "tagline_sw", "about_title_sw", "about_text_sw", "info_title_sw", "info_intro_sw", "info_footer_sw", "meta_description_sw", "meta_keywords_sw"]}),
        ("SEO & tracking", {"fields": ["meta_description", "meta_keywords", "og_image", "google_tag_id"]}),
    ]

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


class ImageInline(admin.StackedInline):
    model = ProductImage
    extra = 1
    fields = ["image", "order"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["thumb", "name", "category", "price", "is_active", "order"]
    list_editable = ["is_active", "order"]
    list_filter = ["category", "is_active"]
    search_fields = ["name", "description"]
    inlines = [ImageInline]

    @admin.display(description="")
    def thumb(self, o):
        i = o.images.first()
        return format_html('<img src="{}" style="height:44px;border-radius:6px">', i.image.url) if i else "-"


for m in (Feature, InfoOption, Category):
    admin.site.register(m, list_display=["__str__", "order"], list_editable=["order"])