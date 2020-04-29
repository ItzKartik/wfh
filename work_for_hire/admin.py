from django.contrib import admin
from .models import p_service, port_folio, orders, order_chat, buyer_request, inbox_members, direct_message, report_services


admin.site.register(direct_message)
admin.site.register(inbox_members)
admin.site.register(buyer_request)
admin.site.register(order_chat)
admin.site.register(orders)
admin.site.register(port_folio)
admin.site.register(p_service)
admin.site.register(report_services)


# class report(admin.TabularInline):
#     model = report_services
#
#
# @admin.register(p_service)
# class reportAdmin(admin.ModelAdmin):
#     inlines = [report]