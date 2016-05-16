# coding: utf-8


from django.contrib import admin

from .models import (
    User,
    Order,
    GoodId,
)


# 用户
class UserAdmin(admin.ModelAdmin):

    list_display = (
        'phone', 'name', 'openid',
    )

    exclude = ('created', 'last_updated')

admin.site.register(User, UserAdmin)
admin.site.register(Order)
admin.site.register(GoodId)