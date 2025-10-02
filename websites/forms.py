from django import forms
from .models import Website, Page, HomeSlider, Settings, HomeCarouselItem, HomeAboutPanel, HomeValueBlock


class WebsiteForm(forms.ModelForm):
    class Meta:
        model = Website
        fields = ['name', 'description', 'domain', 'meta_title', 'meta_description', 'meta_keywords', 
                 'theme', 'primary_color', 'secondary_color']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'meta_description': forms.Textarea(attrs={'rows': 3}),
            'primary_color': forms.TextInput(attrs={'type': 'color'}),
            'secondary_color': forms.TextInput(attrs={'type': 'color'}),
        }


class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ['title', 'slug', 'content', 'is_published', 'meta_title', 'meta_description']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10, 'class': 'form-control'}),
            'meta_description': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].widget.attrs.update({'id': 'content-editor'})


class HomeSliderForm(forms.ModelForm):
    class Meta:
        model = HomeSlider
        fields = ['title', 'subtitle', 'description', 'image', 'button_text', 'button_url', 'order', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class HomeCarouselItemForm(forms.ModelForm):
    class Meta:
        model = HomeCarouselItem
        fields = ['title', 'description', 'image', 'link', 'order', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class HomeAboutPanelForm(forms.ModelForm):
    class Meta:
        model = HomeAboutPanel
        fields = ['title', 'content', 'image', 'button_text', 'button_url']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 6}),
        }


class HomeValueBlockForm(forms.ModelForm):
    class Meta:
        model = HomeValueBlock
        fields = ['title', 'description', 'icon', 'order', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'icon': forms.TextInput(attrs={'placeholder': 'e.g., fas fa-star'}),
        }


class SettingsForm(forms.ModelForm):
    class Meta:
        model = Settings
        fields = ['contact_email', 'contact_phone', 'address', 'facebook_url', 'twitter_url', 
                 'linkedin_url', 'instagram_url', 'google_analytics_id', 'facebook_pixel_id']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }