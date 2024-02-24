from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import profile, post
# Register your models here.
admin.site.unregister(Group)
class profileinline(admin.StackedInline):
    model = profile
class useradmin(admin.ModelAdmin):
    model = User
    fields = ["username"]
    inlines = [profileinline]
admin.site.unregister(User)
admin.site.register(User, useradmin)
admin.site.register(post)
