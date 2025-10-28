from django.contrib import admin
from django.contrib.admin import AdminSite

# Custom admin site configuration
admin_site = AdminSite(name='resume_admin')
admin_site.site_header = 'Edgar Thornton Resume Admin'
admin_site.site_title = 'Resume Admin'
admin_site.index_title = 'Resume Website Administration'

