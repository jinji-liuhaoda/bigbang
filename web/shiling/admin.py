# coding: utf-8
from django.contrib import admin
from .models import (
    Temple,
    Mage,
    ProvideClassification,
    Provide,
    GoodRaise,
    Goods,
    Activity,
    ActivityUser,
    News,
    Volunteers,
    VolunteersUser,
    BuddhismKnowledge,
    User,
)


# 寺庙
class ProvideAdmin(admin.ModelAdmin):

    list_display = (
        'title', 'provideclassification', 'detail', 'price'
    )

    exclude = ('created', 'last_updated')


# 供养
class ProvideAdmin(admin.ModelAdmin):

    list_display = (
        'title', 'provideclassification', 'detail', 'price'
    )

    exclude = ('created', 'last_updated')


# 供养分类
class ProvideClassificationAdmin(admin.ModelAdmin):

    list_display = (
        'name', 'detail',
    )

    exclude = ('created', 'last_updated')

admin.site.register(Temple)
admin.site.register(Mage)
admin.site.register(GoodRaise)
admin.site.register(Goods)
admin.site.register(Activity)
admin.site.register(ActivityUser)
admin.site.register(News)
admin.site.register(Volunteers)
admin.site.register(VolunteersUser)
admin.site.register(BuddhismKnowledge)
admin.site.register(User)
admin.site.register(Provide, ProvideAdmin)
admin.site.register(ProvideClassification, ProvideClassificationAdmin)