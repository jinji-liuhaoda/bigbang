# coding: utf-8
from django.contrib import admin
from .models import (
    Temple,
    Mage,
    Category,
    Provide,
    GoodRaise,
    Good,
    Activity,
    ActivityAttendee,
    News,
    Volunteer,
    VolunteerUser,
    BuddhismKnowledge,
    User,
)


# 寺庙
class TempleAdmin(admin.ModelAdmin):

    list_display = (
        'name', 'title', 'detail', 'mage'
    )

    exclude = ('created', 'last_updated')


# 供养
class ProvideAdmin(admin.ModelAdmin):

    list_display = (
        'title', 'category', 'detail', 'price'
    )

    exclude = ('created', 'last_updated')


# 供养分类
class CategoryAdmin(admin.ModelAdmin):

    list_display = (
        'name', 'detail',
    )

    exclude = ('created', 'last_updated')

admin.site.register(Temple)
admin.site.register(Mage)
admin.site.register(GoodRaise)
admin.site.register(Good)
admin.site.register(Activity)
admin.site.register(ActivityAttendee)
admin.site.register(News)
admin.site.register(Volunteer)
admin.site.register(VolunteerUser)
admin.site.register(BuddhismKnowledge)
admin.site.register(User)
admin.site.register(Provide, ProvideAdmin)
admin.site.register(Category, CategoryAdmin)