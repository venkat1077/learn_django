from django.contrib import admin
from first_app.models import Topic, Webpage, AccessRecord

# Register your models here.
# Register is required to access this models from admin interface
# super user is required
admin.site.register(Topic)
admin.site.register(Webpage)
admin.site.register(AccessRecord)
