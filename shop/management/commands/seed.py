from django.core.management.base import BaseCommand
from shop.models import *


class Command(BaseCommand):
    help = "Create starter settings, categories, features and info-box items"

    def handle(self, *a, **k):
        SiteSettings.load()
        for i, n in enumerate(["Cattle", "Goat", "Sheep", "Hay"]):
            Category.objects.get_or_create(name=n, defaults={"order": i})
        if not Feature.objects.exists():
            for i, (t, x) in enumerate([("Verified Health", "Every animal is checked by a qualified veterinarian."),
                ("Trusted Farms", "We work with reliable and experienced livestock breeders."),
                ("Fast Delivery", "Nationwide livestock transport and logistics available.")]):
                Feature.objects.create(title=t, text=x, order=i)
        if not InfoOption.objects.exists():
            for i, (t, x) in enumerate([("1️⃣ Order Placement", "Reply with 1 for order placement."),
                ("2️⃣ Returns & Tracking", "Reply with 2 for returns, refunds and order tracking."),
                ("3️⃣ Speak to Representative", "Reply with 3 to speak with one of our representatives.")]):
                InfoOption.objects.create(title=t, text=x, order=i)
        self.stdout.write("Seeded.")
        self.seed_products()

    def seed_products(self):
        C = {c.name: c for c in Category.objects.all()}
        rows = [
         ("Cattle","Lactating Cows & Heifers","Upgrade your herd with high-quality, high-yield genetics\n✅ Lactating cows\n• Producing 21–44 litres/day\n• Price: TSh 2,400,000 – 4,000,000\n✅ In-calf heifers\n• Expected yield: 20–34 litres/day\n• Price: TSh 1,200,000 – 1,800,000\n✅ Calves (3–15 months)\nQuality guaranteed.","TSh 300,000 – 4,000,000"),
         ("Sheep","Pure Black Head Dorper Sheep","✓ Lambs (5 months) TSh 110,000\n✓ Ready-to-serve rams TSh 200,000\n✓ Serving rams TSh 220,000 – 600,000\n✓ Ewes TSh 260,000 – 400,000\n✓ Ewes with lambs TSh 400,000 – 800,000\n✓ Twin families TSh 200,000 – 500,000\nWe offer delivery countrywide.","TSh 110,000 – 800,000"),
         ("Hay","Hay & Animal Feed","📌 LUCERNE\nTSh 8,000 per bale (18 kg) · Seeds TSh 25,000/kg\n📌 BOMA RHODES\nTSh 4,000 per bale (18 kg) · Seeds TSh 9,000/kg\n📌 BARLEY\nTSh 2,600 per bale (15 kg)\n📌 SILAGE (chopped fodder)\nFull corn TSh 240/kg · Non full-corn TSh 160/kg\nMolasses TSh 18,000 per 20-litre bucket","From TSh 160/kg"),
         ("Cattle","Jersey Cows","Why Jersey cows?\n1) They eat less\n2) Creamy milk with 5.2% butterfat\n3) Hardy in varied climates\n4) Low cost of milk production\n5) Highly fertile, short calving interval, early maturity\n6) High-value milk for cheese and butter","Call for price"),
         ("Goat","Full Blood Boer Goats","Kids (up to 3 months): TSh 140,000\nYoung goats (3–5 months): TSh 300,000\nSub-adults (5–10 months): TSh 600,000\nWell cared for and ready to boost your farm's productivity.","TSh 140,000 – 600,000"),
         ("Sheep","Hampshire Sheep","4 months (lamb): TSh 520,000 – 540,000\n6 months: TSh 620,000 – 640,000\n8 months: TSh 760,000 – 780,000\n10 months: TSh 840,000+\n12 months (mature): TSh 900,000 – 960,000","TSh 520,000 – 960,000"),
         ("Cattle","Boran & Sahiwal Calves and Heifers","Boran · Sahiwal · Brahman\nStrong, healthy, fast-growing breeds for beef farming.\nCalves from TSh 500,000\nHeifers from TSh 1,200,000\nMatured from TSh 2,400,000\n🚚 Delivery available countrywide (by agreement)","From TSh 500,000"),
         ("Goat","Dairy Goats","Milk production 3–6 litres per day\n1️⃣ 3 months TSh 70,000\n2️⃣ 5 months TSh 110,000\n3️⃣ 7 months TSh 150,000\n4️⃣ 10 months TSh 200,000\n5️⃣ First-timer mothers TSh 280,000\n6️⃣ Second-timer mothers TSh 240,000\n7️⃣ Due in 2 weeks TSh 360,000\n8️⃣ Due in 1 month TSh 320,000\n9️⃣ Males TSh 200,000","TSh 70,000 – 360,000"),
         ("Cattle","Girolando","Calves (2–3 months): TSh 400,000 – 600,000\nYoung (4–8 months): TSh 600,000 – 800,000\nGrowing heifers (8–15 months): TSh 1,200,000 – 2,600,000\nMature (not pregnant): TSh 1,400,000 – 2,000,000\nIn-calf: TSh 2,800,000 – 3,600,000+\nLactating: TSh 3,600,000 – 5,000,000+","TSh 400,000 – 5,000,000+"),
        ]
        for i, (c, n, d, p) in enumerate(rows):
            Product.objects.get_or_create(name=n, defaults={"category": C[c], "description": d, "price": p, "order": i})
        self.seed_sw()

    def seed_sw(self):
        s = SiteSettings.load()
        for k, v in dict(hero_title_sw="Soko Bora la Mifugo", hero_subtitle_sw="Nunua ng'ombe wa maziwa, mbuzi na kondoo wenye afya, tunakufikishia popote Tanzania.",
            tagline_sw="Ng'ombe wa maziwa, mbuzi, kondoo na malisho bora kutoka shamba la kuaminika Tanzania.", about_title_sw="Kuhusu Bashe Dairy Farm",
            about_text_sw="Bashe Dairy Farm inasambaza ng'ombe wa maziwa, mbuzi, kondoo na malisho ya mifugo yenye ubora wa juu kwa wakulima kote Tanzania.\n\nLengo letu ni kurahisisha biashara ya mifugo kwa ubora, uwazi na uaminifu.",
            info_title_sw="IDARA YA MAUZO NA MASOKO", info_intro_sw="Asante kwa kuwasiliana nasi.", info_footer_sw="Tunathamini ushirikiano wako na tunatarajia kukuhudumia.",
            meta_description_sw="Nunua ng'ombe wa maziwa, mbuzi, kondoo na malisho kutoka Bashe Dairy Farm, Tanzania. Tunafikisha popote nchini.",
            meta_keywords_sw="ng'ombe wa maziwa Tanzania, mbuzi, kondoo, malisho ya mifugo, Bashe Dairy Farm").items():
            if not getattr(s, k):
                setattr(s, k, v)
        s.save()
        pairs = [(Feature, "title", {"Verified Health": ("Afya Imethibitishwa", "Kila mnyama hukaguliwa na daktari wa mifugo aliyehitimu."),
            "Trusted Farms": ("Mashamba ya Kuaminika", "Tunafanya kazi na wafugaji wenye uzoefu na wanaoaminika."),
            "Fast Delivery": ("Usafirishaji wa Haraka", "Usafiri wa mifugo unapatikana nchi nzima.")}),
          (InfoOption, "title", {"1️⃣ Order Placement": ("1️⃣ Kuweka Oda", "Jibu 1 kuweka oda."),
            "2️⃣ Returns & Tracking": ("2️⃣ Marejesho na Ufuatiliaji", "Jibu 2 kwa marejesho, kurejeshewa pesa na kufuatilia oda."),
            "3️⃣ Speak to Representative": ("3️⃣ Ongea na Mwakilishi", "Jibu 3 kuongea na mmoja wa wawakilishi wetu.")})]
        for M, key, d in pairs:
            for o in M.objects.all():
                if o.title in d and not o.title_sw:
                    o.title_sw, o.text_sw = d[o.title]
                    o.save()
        for n, sw in {"Cattle": "Ng'ombe", "Goat": "Mbuzi", "Sheep": "Kondoo", "Hay": "Malisho"}.items():
            Category.objects.filter(name=n, name_sw="").update(name_sw=sw)
        for n, sw in {"Lactating Cows & Heifers": "Ng'ombe wa Maziwa na Mitamba", "Pure Black Head Dorper Sheep": "Kondoo Dorper Weusi Wasafi",
            "Hay & Animal Feed": "Nyasi na Malisho ya Mifugo", "Jersey Cows": "Ng'ombe Aina ya Jersey", "Full Blood Boer Goats": "Mbuzi Boer Damu Kamili",
            "Hampshire Sheep": "Kondoo Hampshire", "Boran & Sahiwal Calves and Heifers": "Ndama na Mitamba ya Boran na Sahiwal", "Dairy Goats": "Mbuzi wa Maziwa"}.items():
            Product.objects.filter(name=n, name_sw="").update(name_sw=sw)
