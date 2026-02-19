from django.apps import AppConfig


class TourConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tour'
    verbose_name = ' مدیریت تور ها'
    
    def ready(self):
        import tour.signals