import os

G1 = True
USE_PROD_DB = True
USE_LOCAL_DB = not USE_PROD_DB


def databases():
    if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine'):
        return {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'HOST': '/cloudsql/mealsloth-minotaur-db01:us-central1:mealsloth-minotaur-in01',
                'NAME': 'minotaur_prod01',
                'USER': 'root',
                'PASSWORD': '9XD8XkZ8q3SygQHfDPSVEJf9e5FZrH75gtJYCR9k4wfqp8PQ6EXvDBQrKZanfBVY',
            },
        }
    elif os.getenv('SETTINGS_MODE') == 'prod' or USE_PROD_DB is True:
        return {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'HOST': '104.154.147.252',
                'NAME': 'minotaur_prod01',
                'USER': 'root',
                'PASSWORD': '9XD8XkZ8q3SygQHfDPSVEJf9e5FZrH75gtJYCR9k4wfqp8PQ6EXvDBQrKZanfBVY',
                'OPTIONS': {
                    'ssl': {
                        'ca': '~/.ssl/mealsloth-minotaur-in01-server-ca.pem',
                        'cert': '~/.ssl/mealsloth-minotaur-in01-client-cert.pem',
                        'key': '~/.ssl/mealsloth-minotaur-in01-client-key.pem',
                    },
                },
            },
        }
    else:
        return {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': 'chimera_test01',
                'USER': 'root',
                'HOST': 'localhost',
                'PORT': '3306',
            },
        }
