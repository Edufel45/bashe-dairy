import io
from django.core.files.base import ContentFile
from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.utils.text import slugify
from PIL import Image


def _webp(f, size):
    img = Image.open(f).convert("RGB")
    img.thumbnail((size, size))
    buf = io.BytesIO()
    img.save(buf, "WEBP", quality=78, method=6)
    return ContentFile(buf.getvalue())


class Optimised(models.Model):
    """Auto-resizes uploads to WebP so pages stay tiny and fast."""
    IMAGES = {}  # field -> max px

    class Meta:
        abstract = True

    def save(self, *a, **kw):
        for name, size in self.IMAGES.items():
            f = getattr(self, name)
            if f and not f._committed:
                base = f.name.rsplit(".", 1)[0].split("/")[-1]
                f.save(base + ".webp", _webp(f, size), save=False)
        super().save(*a, **kw)


class SiteSettings(Optimised):
    IMAGES = {"hero_image": 1600, "about_image": 1000, "og_image": 1200}
    site_name = models.CharField(max_length=80, default="Bashe Dairy Farm")
    tagline = models.CharField(max_length=160, default="Quality dairy cattle, goats, sheep and feed from a trusted Tanzanian farm.")
    hero_title = models.CharField(max_length=120, default="Premium Livestock Marketplace")
    hero_subtitle = models.CharField(max_length=200, default="Healthy dairy cows, goats and sheep, delivered across Tanzania.")
    hero_image = models.ImageField(upload_to="site/", blank=True)
    whatsapp = models.CharField("WhatsApp number (no +)", max_length=20, default="255750512272")
    phone = models.CharField(max_length=20, default="+255750512272")
    email = models.EmailField(blank=True)
    about_title = models.CharField(max_length=100, default="About Bashe Dairy Farm")
    about_text = models.TextField(default="Bashe Dairy Farm supplies healthy, premium-quality dairy cattle, goats, sheep and animal feed to farmers across Tanzania.\n\nOur mission is to simplify livestock trading while maintaining quality, transparency, and reliability.")
    about_image = models.ImageField(upload_to="site/", blank=True)
    info_title = models.CharField("Info box title", max_length=150, default="SALES & MARKETING DEPARTMENT")
    info_intro = models.CharField(max_length=200, default="Thank you for contacting us.")
    info_footer = models.CharField(max_length=200, default="We appreciate your cooperation and look forward to assisting you.")
    show_info_box = models.BooleanField(default=True)
    footer_text = models.CharField(max_length=200, blank=True)
    meta_description = models.CharField(max_length=160, default="Buy healthy dairy cows, goats, sheep and animal feed from Bashe Dairy Farm, Tanzania. Delivery available countrywide.")
    meta_keywords = models.CharField(max_length=250, default="dairy cows for sale Tanzania, Friesian, Jersey cows, Boer goats, Dorper sheep, animal feed, Bashe Dairy Farm")
    location = models.CharField(max_length=120, default="Tanzania")
    og_image = models.ImageField("Social share image", upload_to="site/", blank=True)
    google_tag_id = models.CharField("Google tag ID (optional)", max_length=30, blank=True)

    tagline_sw = models.CharField("Tagline (Kiswahili)", max_length=250, blank=True)
    hero_title_sw = models.CharField("Hero Title (Kiswahili)", max_length=250, blank=True)
    hero_subtitle_sw = models.CharField("Hero Subtitle (Kiswahili)", max_length=250, blank=True)
    about_title_sw = models.CharField("About Title (Kiswahili)", max_length=250, blank=True)
    about_text_sw = models.TextField("About Text (Kiswahili)", blank=True)
    info_title_sw = models.CharField("Info Title (Kiswahili)", max_length=250, blank=True)
    info_intro_sw = models.CharField("Info Intro (Kiswahili)", max_length=250, blank=True)
    info_footer_sw = models.CharField("Info Footer (Kiswahili)", max_length=250, blank=True)
    meta_description_sw = models.CharField("Meta Description (Kiswahili)", max_length=250, blank=True)
    meta_keywords_sw = models.CharField("Meta Keywords (Kiswahili)", max_length=250, blank=True)

    class Meta:
        verbose_name = verbose_name_plural = "Site settings"

    def __str__(self):
        return "Site settings"

    @classmethod
    def load(cls):
        return cls.objects.first() or cls.objects.create()


class Feature(models.Model):
    title = models.CharField(max_length=80)
    title_sw = models.CharField("Title (Kiswahili)", max_length=250, blank=True)
    text_sw = models.CharField("Text (Kiswahili)", max_length=250, blank=True)
    text = models.CharField(max_length=250)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title


class InfoOption(models.Model):
    title = models.CharField(max_length=80)
    title_sw = models.CharField("Title (Kiswahili)", max_length=250, blank=True)
    text_sw = models.CharField("Text (Kiswahili)", max_length=250, blank=True)
    note_sw = models.CharField("Note (Kiswahili)", max_length=250, blank=True)
    text = models.CharField(max_length=250)
    note = models.CharField(max_length=250, blank=True, help_text="Red note under the item")
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=50)
    name_sw = models.CharField("Name (Kiswahili)", max_length=250, blank=True)
    slug = models.SlugField(unique=True, blank=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name_plural = "categories"

    def save(self, *a, **kw):
        self.slug = self.slug or slugify(self.name)
        super().save(*a, **kw)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    name_sw = models.CharField("Name (Kiswahili)", max_length=250, blank=True)
    description_sw = models.TextField("Description (Kiswahili)", blank=True)
    name = models.CharField(max_length=200)
    description = models.TextField(help_text="Line breaks and emojis are kept as typed.")
    price = models.CharField(max_length=200, blank=True, help_text="e.g. 20,000-250,000 ksh")
    weight = models.CharField(max_length=60, blank=True)
    is_active = models.BooleanField("Visible", default=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "-id"]

    def __str__(self):
        return self.name


class ProductImage(Optimised):
    IMAGES = {"image": 900}
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="products/")
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]


