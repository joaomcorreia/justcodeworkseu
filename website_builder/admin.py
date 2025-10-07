"""
Website Builder Admin Interface
"""
from django.contrib import admin
from django.utils.html import format_html
from django.urls import path, reverse
from django.shortcuts import get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import (
    WebsiteProject, BusinessService, WebsiteTemplate, 
    WebsiteBuilderConversation, IndustryTemplate
)


@admin.register(WebsiteProject)
class WebsiteProjectAdmin(admin.ModelAdmin):
    list_display = [
        'business_name', 'user', 'industry', 'page_type', 
        'status', 'completion_percentage', 'created_at', 'project_actions'
    ]
    list_filter = ['status', 'page_type', 'industry', 'created_at']
    search_fields = ['business_name', 'user__username', 'user__email', 'industry']
    readonly_fields = ['project_id', 'created_at', 'updated_at', 'completion_percentage']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('project_id', 'user', 'tenant', 'project_name', 'business_name')
        }),
        ('Business Details', {
            'fields': ('industry', 'page_type', 'business_description', 'target_audience', 'location')
        }),
        ('Contact Information', {
            'fields': ('phone', 'email', 'website_url', 'social_media')
        }),
        ('Design & Content', {
            'fields': ('template_id', 'color_scheme', 'font_style', 'content_tone', 'language')
        }),
        ('Project Status', {
            'fields': ('status', 'completion_percentage', 'assistant_conversation_id')
        }),
        ('Generated Content', {
            'fields': ('generated_content', 'final_html', 'final_css'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'published_at'),
            'classes': ('collapse',)
        })
    )
    
    def project_actions(self, obj):
        """Custom actions for each project"""
        actions = []
        
        if obj.status == 'completed':
            preview_url = reverse('admin:preview_website', args=[obj.project_id])
            actions.append(f'<a href="{preview_url}" target="_blank" class="button">Preview</a>')
        
        if obj.assistant_conversation_id:
            chat_url = reverse('admin:view_conversation', args=[obj.project_id])
            actions.append(f'<a href="{chat_url}" class="button">View Chat</a>')
        
        export_url = reverse('admin:export_website', args=[obj.project_id])
        actions.append(f'<a href="{export_url}" class="button">Export</a>')
        
        return format_html(' '.join(actions))
    
    project_actions.short_description = 'Actions'
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('preview/<uuid:project_id>/', self.preview_website, name='preview_website'),
            path('conversation/<uuid:project_id>/', self.view_conversation, name='view_conversation'),
            path('export/<uuid:project_id>/', self.export_website, name='export_website'),
        ]
        return custom_urls + urls
    
    @method_decorator(staff_member_required)
    def preview_website(self, request, project_id):
        """Preview the generated website"""
        project = get_object_or_404(WebsiteProject, project_id=project_id)
        
        if not project.final_html:
            return JsonResponse({'error': 'Website not yet generated'}, status=404)
        
        # Return the HTML content directly
        from django.http import HttpResponse
        return HttpResponse(project.final_html)
    
    @method_decorator(staff_member_required)
    def view_conversation(self, request, project_id):
        """View the AI conversation for this project"""
        project = get_object_or_404(WebsiteProject, project_id=project_id)
        
        # This would show the conversation history
        # For now, redirect to the project detail page
        return redirect('admin:website_builder_websiteproject_change', project.id)
    
    @method_decorator(staff_member_required)
    def export_website(self, request, project_id):
        """Export website files as ZIP"""
        project = get_object_or_404(WebsiteProject, project_id=project_id)
        
        if not project.final_html:
            return JsonResponse({'error': 'Website not yet generated'}, status=404)
        
        # Create ZIP file with HTML, CSS, and assets
        import zipfile
        import io
        from django.http import HttpResponse
        
        zip_buffer = io.BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            # Add HTML file
            zip_file.writestr('index.html', project.final_html)
            
            # Add CSS file
            if project.final_css:
                zip_file.writestr('style.css', project.final_css)
            
            # Add project info
            project_info = f"""
Project: {project.business_name}
Created: {project.created_at}
Status: {project.status}
Industry: {project.industry}
Services: {', '.join([s.service_name for s in project.services.all()])}
            """.strip()
            zip_file.writestr('project_info.txt', project_info)
        
        zip_buffer.seek(0)
        
        response = HttpResponse(zip_buffer.getvalue(), content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename="{project.business_name.replace(" ", "_")}_website.zip"'
        return response


@admin.register(BusinessService)
class BusinessServiceAdmin(admin.ModelAdmin):
    list_display = ['service_name', 'project', 'is_primary', 'display_order']
    list_filter = ['is_primary', 'project__industry']
    search_fields = ['service_name', 'project__business_name']
    ordering = ['project', 'display_order', 'service_name']
    
    fieldsets = (
        ('Service Information', {
            'fields': ('project', 'service_name', 'service_description', 'is_primary', 'display_order')
        }),
        ('AI Generated Content', {
            'fields': ('short_description', 'detailed_description', 'features'),
            'classes': ('collapse',)
        })
    )


@admin.register(WebsiteTemplate)
class WebsiteTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'usage_count', 'rating', 'is_active', 'is_ai_generated']
    list_filter = ['category', 'is_active', 'is_ai_generated', 'supports_one_page', 'supports_multi_page']
    search_fields = ['name', 'description', 'category']
    
    fieldsets = (
        ('Template Information', {
            'fields': ('template_id', 'name', 'category', 'description')
        }),
        ('Template Code', {
            'fields': ('html_template', 'css_template', 'js_template'),
            'classes': ('collapse',)
        }),
        ('Configuration', {
            'fields': ('supports_one_page', 'supports_multi_page', 'color_schemes', 'font_options')
        }),
        ('Preview & Media', {
            'fields': ('preview_image', 'thumbnail_image', 'demo_url')
        }),
        ('Status & Analytics', {
            'fields': ('is_active', 'is_ai_generated', 'usage_count', 'rating')
        })
    )
    
    readonly_fields = ['usage_count']
    
    actions = ['generate_ai_template', 'activate_templates', 'deactivate_templates']
    
    def generate_ai_template(self, request, queryset):
        """Generate new AI template (placeholder for now)"""
        self.message_user(request, "AI template generation feature coming soon!")
    
    generate_ai_template.short_description = "Generate AI Template"
    
    def activate_templates(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} templates activated.')
    
    activate_templates.short_description = "Activate selected templates"
    
    def deactivate_templates(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} templates deactivated.')
    
    deactivate_templates.short_description = "Deactivate selected templates"


@admin.register(WebsiteBuilderConversation)
class WebsiteBuilderConversationAdmin(admin.ModelAdmin):
    list_display = ['project', 'current_step', 'total_messages', 'assistant_personality', 'created_at']
    list_filter = ['current_step', 'assistant_personality', 'user_expertise_level']
    search_fields = ['project__business_name', 'project__user__username']
    readonly_fields = ['created_at', 'updated_at', 'total_messages']
    
    fieldsets = (
        ('Conversation Info', {
            'fields': ('project', 'current_step', 'total_messages')
        }),
        ('AI Settings', {
            'fields': ('assistant_personality', 'user_expertise_level')
        }),
        ('Progress Data', {
            'fields': ('conversation_data', 'step_progress'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        })
    )


@admin.register(IndustryTemplate)
class IndustryTemplateAdmin(admin.ModelAdmin):
    list_display = ['display_name', 'industry_name', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['industry_name', 'display_name', 'description']
    filter_horizontal = ['recommended_templates']
    
    fieldsets = (
        ('Industry Information', {
            'fields': ('industry_name', 'display_name', 'description')
        }),
        ('Common Services', {
            'fields': ('common_services',)
        }),
        ('Content Templates', {
            'fields': ('business_description_template', 'services_intro_template', 'about_us_template'),
            'classes': ('collapse',)
        }),
        ('SEO & Marketing', {
            'fields': ('common_keywords', 'target_audience_suggestions'),
            'classes': ('collapse',)
        }),
        ('Design Recommendations', {
            'fields': ('recommended_colors', 'recommended_templates')
        }),
        ('Status', {
            'fields': ('is_active',)
        })
    )


# Custom admin site configuration
admin.site.site_header = 'JustCodeWorks Website Builder'
admin.site.site_title = 'Website Builder Admin'
admin.site.index_title = 'Website Builder Administration'