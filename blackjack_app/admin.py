from django.contrib import admin
from django.urls import path
from .admin_views import edit_all_session_balances

class BlackjackAdminSite(admin.AdminSite):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('edit_all_session_balances/', self.admin_view(edit_all_session_balances), name='edit_all_session_balances'),
        ]
        return custom_urls + urls

admin_site = BlackjackAdminSite(name='blackjack_admin')
