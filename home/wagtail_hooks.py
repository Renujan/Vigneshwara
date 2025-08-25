from wagtail import hooks
from wagtail.admin.menu import MenuItem
from django.urls import reverse
from django.contrib.auth.models import Group
from django.utils.html import format_html
from django.shortcuts import render
from Items.models import Brand
from contact_details.models import Contact






@hooks.register('register_admin_menu_item')
def register_main_admin_menu_item():
    return MenuItem(
        'Home',
        reverse('wagtailadmin_home'),
        icon_name='home',
        order=1
    )

@hooks.register('construct_main_menu')
def hide_explorer_menu_item_from_frank(request, menu_items):
    new_menu_items = []
    for item in menu_items:
        if not item.name in ['reports','help','explorer','documents','images']:
            new_menu_items.append(item)
    menu_items[:] = new_menu_items

@hooks.register('construct_settings_menu')
def hide_settings_items(request, menu_items):
    new_menu_items = []
    for item in menu_items:
        if not item.name in ['redirects','sites','collections','workflows','workflow-tasks']:
            new_menu_items.append(item)
    menu_items[:] = new_menu_items


@hooks.register('insert_global_admin_css')
def global_admin_css():
    return format_html('<link rel="stylesheet" href="/static/css/custom-admin.css">')

def new_admin_home(request):
    total_items = Brand.objects.count()
    total_contacts = Contact.objects.count()
    

    return render(request, 'wagtailadmin/home.html', {
        'total_items': total_items,
        'total_contacts': total_contacts,
        
    })

@hooks.register('replace_wagtail_admin_home_page')
def override_wagtail_admin_home_page():
    return new_admin_home
