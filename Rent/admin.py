from importlib.resources import path

from django.conf.urls import url
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import admin
from .models import Inventory, SupplyAplication ,RentApplication
from django.utils.html import format_html
from django.contrib.auth.models import User, Group

admin.site.site_header = 'Administration'

@admin.register(RentApplication)
class RentApplicationAdmin(admin.ModelAdmin):
    list_display = ('id','student', 'item', 'reason', 'type', 'account_actions_rent')
    list_display_links = (
        'student','item'
    )
    list_filter = ("status",)
    search_fields = ["student__username",'item__name','status' ]


    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            url(
                r'^(?P<req_id>.+)/accept_rent/$',
                self.admin_site.admin_view(self.accept_rent),
                name='accept_rent',
            ),
            url(
                r'^(?P<req_id>.+)/decline_rent/$',
                self.admin_site.admin_view(self.decline_rent),
                name='decline_rent',
            ),
        ]
        return custom_urls + urls

    def account_actions_rent(self, obj):
        if obj.status == 'Accepted':
            return "Accepted"
        elif obj.status == 'Rejected':
            return "Rejected"
        else:
            return format_html(
                '<a class="button" href="{}">Accept</a>&nbsp;'
                '<a class="button" href="{}">Decline</a>',
                reverse('admin:accept_rent', args=[obj.pk]),
                reverse('admin:decline_rent', args=[obj.pk]),
            )


    account_actions_rent.short_description = 'Check'
    account_actions_rent.allow_tags = True


    def accept_rent(self,request,req_id):
        #print(req_id)

        req = self.get_object(request,req_id)
        if req.type == 'Add':
            req.status = "Accepted"
            item = req.item
            item.status = 'Available'
            item.save()
            req.item = item
            #print(user)
            req.save()
        if req.type == 'Rent':
            req.status = "Accepted"
            item = req.item
            item.status = 'Taken'
            item.save()
            req.item = item
            # print(user)
            req.save()

        return HttpResponseRedirect('/admin/Rent/rentapplication/')


    def decline_rent(self,request,req_id):
        print(req_id)
        req = self.get_object(request,req_id)
        req.status = "Rejected"
        req.save()
        return HttpResponseRedirect('/admin/Rent/rentapplication/')


@admin.register(Inventory)
class Inventory(admin.ModelAdmin):
    list_display = ('id','name', 'status', 'supplier')
    list_display_links = [
        'supplier','id','name'
    ]
    list_filter = ("status",)
    search_fields = ["supplier__username", 'status','name']


@admin.register(SupplyAplication)
class SupplyAplication(admin.ModelAdmin):
    list_display = ['id','student',"status",'account_actions']

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            url(
                r'^(?P<req_id>.+)/accept/$',
                self.admin_site.admin_view(self.accept),
                name='accept',
            ),
            url(
                r'^(?P<req_id>.+)/decline/$',
                self.admin_site.admin_view(self.decline),
                name='decline',
            ),
        ]
        return custom_urls + urls

    def account_actions(self, obj):
        if obj.status == 'Accepted':
            return "Accepted"
        elif obj.status == 'Rejected':
            return "Rejected"
        else:
            return format_html(
                '<a class="button" href="{}">Accept</a>&nbsp;'
                '<a class="button" href="{}">Decline</a>',
                reverse('admin:accept', args=[obj.pk]),
                reverse('admin:decline', args=[obj.pk]),
            )

    account_actions.short_description = 'Check'
    account_actions.allow_tags = True

    def accept(self, request, req_id):
        print(req_id)
        item = self.get_object(request, req_id)
        item.status = "Accepted"
        user = item.student
        print('look here')
        print(user)
        group = Group.objects.get(name='Supplier')
        user.groups.add(group)
        item.student = user
        item.save()
        return HttpResponseRedirect('/admin/Rent/supplyaplication/')

    def decline(self, request, req_id):
        # print(req_id)
        item = self.get_object(request, req_id)
        item.status = "Rejected"
        item.save()
        return HttpResponseRedirect('/admin/Rent/supplyaplication/')
