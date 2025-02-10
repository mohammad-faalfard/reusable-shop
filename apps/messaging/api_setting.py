from django.conf import settings

KAVENEGAR_APIKEY = getattr(settings, "MESSAGING_KAVENEGAR_APIKEY", "not-set")
NAJVA_APIKEY = getattr(settings, "MESSAGING_NAJVA_APIKEY", "not-set")
NAJVA_TOKEN = getattr(settings, "MESSAGING_NAJVA_TOKEN", "not-set")
