from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


# Register your models here.
from marketplace.models import Trader, Publication, Product


@admin.register(Trader)
class TraderAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("city",)
    fieldsets = UserAdmin.fieldsets + (
        (("Additional info", {"fields": ("city",)}),)
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (("Additional info", {"fields": ("first_name", "last_name", "city",)}),)
    )


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    search_fields = ("title",)
    list_filter = ("author",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_filter = ("author",)
