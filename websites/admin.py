from django.contrib import admin
from .models import (
    Website, Page, HomeSlider, HomeCarouselItem, HomeAboutPanel, 
    HomeValueBlock, AboutPage, AboutBenefit, Settings
)


@admin.register(Website)
class WebsiteAdmin(admin.ModelAdmin):
    list_display = ['name', 'domain', 'owner', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at', 'theme']
    search_fields = ['name', 'domain', 'owner__username']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ['title', 'website', 'slug', 'is_published', 'is_homepage', 'created_at']
    list_filter = ['is_published', 'is_homepage', 'created_at']
    search_fields = ['title', 'slug', 'website__name']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(HomeSlider)
class HomeSliderAdmin(admin.ModelAdmin):
    list_display = ['title', 'website', 'order', 'is_active']
    list_filter = ['is_active', 'website']
    search_fields = ['title', 'website__name']
    ordering = ['website', 'order']


@admin.register(HomeCarouselItem)
class HomeCarouselItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'website', 'order', 'is_active']
    list_filter = ['is_active', 'website']
    search_fields = ['title', 'website__name']
    ordering = ['website', 'order']


@admin.register(HomeAboutPanel)
class HomeAboutPanelAdmin(admin.ModelAdmin):
    list_display = ['title', 'website']
    search_fields = ['title', 'website__name']


@admin.register(HomeValueBlock)
class HomeValueBlockAdmin(admin.ModelAdmin):
    list_display = ['title', 'website', 'order', 'is_active']
    list_filter = ['is_active', 'website']
    search_fields = ['title', 'website__name']
    ordering = ['website', 'order']


@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    list_display = ['title', 'website']
    search_fields = ['title', 'website__name']


@admin.register(AboutBenefit)
class AboutBenefitAdmin(admin.ModelAdmin):
    list_display = ['title', 'about_page', 'order']
    list_filter = ['about_page__website']
    search_fields = ['title', 'about_page__website__name']
    ordering = ['about_page', 'order']


@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    list_display = ['website', 'contact_email', 'contact_phone']
    search_fields = ['website__name', 'contact_email']
