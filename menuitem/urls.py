from django.urls import path
from menuitem.views import dashboard, get_menulist, add_item, get_item, update_item, delete_item

app_name = "menuitem"


urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("restaurant/<uuid:restaurant_id>/menus", get_menulist, name="menulist"),
    path("item/create/", add_item, name="item_create"),
    path("item/update/<uuid:item_id>", update_item, name="item_update"),
    path("item/detail/<uuid:item_id>", get_item, name="item_detail"),
    path("item/delete/<uuid:item_id>", delete_item, name="item_delete"),
]