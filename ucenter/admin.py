# coding: utf-8


from django.contrib import admin

from .models import (
    Cuser,
    Order,
    GoodId,
)


# 用户
class CuserAdmin(admin.ModelAdmin):

    list_display = (
        'phone', 'name', 'openid',
    )

    exclude = ('created', 'last_updated')

admin.site.register(Cuser, CuserAdmin)
admin.site.register(Order)
admin.site.register(GoodId)