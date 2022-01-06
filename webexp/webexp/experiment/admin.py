from django.contrib import admin

from .models import Participant, Trial, Code, Log


admin.site.register(Participant)
admin.site.register(Trial)
admin.site.register(Code)
admin.site.register(Log)