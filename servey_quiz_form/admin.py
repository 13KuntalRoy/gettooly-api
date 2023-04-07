from django.contrib import admin

# Register your models here.
from servey_quiz_form.models import Choices,Questions,Answer,Form,Responses


admin.site.register(Choices)

admin.site.register(Questions)

admin.site.register(Answer)

admin.site.register(Form)

admin.site.register(Responses)
