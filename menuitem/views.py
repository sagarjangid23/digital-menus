from django.contrib.auth.decorators import login_required
from menuitem.decorators import for_owner
from django.contrib import messages
from django.shortcuts import render, HttpResponseRedirect
from menuitem.forms import MenuItemForm
from menuitem.models import MenuItem
from account.models import Restaurant
import qrcode
import qrcode.image.svg
from io import BytesIO
from django.views.decorators.cache import cache_page


def get_menulist(request, restaurant_id):
    try:
        restaurant = Restaurant.objects.get(id=restaurant_id)
    except:
        messages.error(request, 'Restaurant not found.')
        return HttpResponseRedirect("/")
    
    menuitems = MenuItem.objects.filter(restaurant__id=restaurant.id)

    if not menuitems:
        messages.error(request, 'Menus not found.')
        return HttpResponseRedirect("/")
    return render(request, "menuitem/menus.html", {'restaurant_name': restaurant.name, "menuitems": menuitems})


def dashboard(request):
    context = {}

    if not request.user.is_anonymous:
        context['user_name'] = request.user.first_name if request.user.first_name else request.user.username

    if not request.user.is_anonymous and request.user.is_owner:
        owner = request.user.is_owner
    
        if owner:
            restaurant_id = request.user.restaurant.id
            menuitems = MenuItem.objects.filter(restaurant__id=restaurant_id)

            url = f'https://online-menus.herokuapp.com/restaurant/{restaurant_id}/menus'
            qr = qrcode.QRCode(
                version=16,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=6,
                border=4,
                image_factory=qrcode.image.svg.SvgImage,
            )
            qr.add_data(data=url, optimize=20)
            qr.make(fit=True)
            img = qr.make_image(back_color='white', fill_color='black')
            stream = BytesIO()
            img.save(stream)

            context['owner'] = owner
            context['menuitems'] = menuitems
            context['restaurant'] = stream.getvalue().decode()

    else:
        qrs = {}
        restaurants = Restaurant.objects.all()

        for restaurant in restaurants:
            url = f'https://online-menus.herokuapp.com/restaurant/{restaurant.id}/menus'
            qr = qrcode.QRCode(
                version=16,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=6,
                border=4,
                image_factory=qrcode.image.svg.SvgImage,
            )
            qr.add_data(data=url, optimize=20)
            qr.make(fit=True)
            img = qr.make_image(back_color='white', fill_color='black')
            stream = BytesIO()
            img.save(stream)
            qrs[restaurant.name] = stream.getvalue().decode()
            qr.clear()
        
        context['restaurants'] = qrs
    return render(request, "menuitem/dashboard.html", context)


@login_required
@for_owner
def add_item(request):
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES)

        if form.is_valid():
            item = form.save(commit=False)
            item.restaurant = request.user.restaurant
            if 'image' in request.FILES:
                item.image =request.FILES['image']
            form.save()
            messages.success(request,'Item successfully created.')
            return HttpResponseRedirect('/')
    else:
        form = MenuItemForm()
    return render(request, 'menuitem/create.html', {'form':form})


@login_required
@for_owner
def get_item(request, item_id):
    try:
        menuitem = MenuItem.objects.get(restaurant__id=request.user.restaurant.id, id=item_id)
    except:
        messages.error(request, 'Item not found.')
        return HttpResponseRedirect("/")
    return render(request, "menuitem/detail.html", {"menuitem": menuitem})


@login_required
@for_owner
def update_item(request, item_id):
    try:
        menuitem = MenuItem.objects.get(restaurant__id=request.user.restaurant.id, id=item_id)
    except:
        messages.error(request, 'Item not found.')
        return HttpResponseRedirect("/")

    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES, instance=menuitem)

        if form.is_valid():
            item = form.save(commit=False)
            if 'image' in request.FILES:
                item.image =request.FILES['image']
            form.save()
            messages.success(request,'Item successfully updated.')
            return HttpResponseRedirect('/')
    else:
        form = MenuItemForm(instance=menuitem)
    return render(request, 'menuitem/update.html', {'form':form})


@login_required
@for_owner
def delete_item(request, item_id):
    try:
        MenuItem.objects.get(restaurant__id=request.user.restaurant.id, id=item_id).delete()
        messages.error(request, 'Item deleted successfully.')
    except:
        messages.error(request, 'Item can not be deleted.')
    return HttpResponseRedirect("/")