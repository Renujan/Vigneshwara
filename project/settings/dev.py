from .db import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-6jvjb10wl+rwu0f0qn-exn6%n-+7k_&#7i14f=ga%=(pe(&*is"


# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

CORS_ALLOW_CREDENTIALS = True

#change it in production!
CORS_ALLOW_ALL_ORIGINS = True


CSRF_TRUSTED_ORIGINS = [
    "https://*.technuob.com",
    "https://*.vercel.app/",
]



#EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "clh.test.vlt@gmail.com"
EMAIL_HOST_PASSWORD = "uoqojfyrdcchathu"  

EMAIL_SENDER_NAME = "Juristquest"

# Email Header Configuration
EMAIL_CUSTOM_HEADER = {
    "text": (
        "Email sent by juristquest (JQ)<br>"
        "Hotline: +91-9677873855<br>"
        "Email: info@juristquest.com"
    ),
    "style": "font-size: 12px; color: #555; border-bottom: 1px solid #ddd; padding-bottom: 10px; margin-bottom: 10px;"
}


#When mail is disabled (set to false), emails won't be sent except for password reset.
ENABLE_EMAIL = True


try:
    from .local import *
except ImportError:
    pass
