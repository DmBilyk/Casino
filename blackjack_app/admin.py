from django.contrib import admin
from django.urls import path
from blackjack_app.admin_views import edit_session_balance

class BlackjackAdminSite(admin.AdminSite):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('edit_session_balance/', self.admin_view(edit_session_balance), name='edit_session_balance'),
        ]
        return custom_urls + urls

admin_site = BlackjackAdminSite(name='blackjack_admin')