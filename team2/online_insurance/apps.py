from django.apps import AppConfig

class OnlineInsuranceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'online_insurance'



class OnlineInsuranceConfig(AppConfig):
    name = 'online_insurance'

    def ready(self):
        import online_insurance.signals
