from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Sum, Count, Q
from django.http import JsonResponse
from .models import Restaurant, Product, Order, OrderItem, Note, ChatMessage
from .forms import RestaurantForm, ProductForm, OrderForm, NoteForm, ChatMessageForm
import json
from datetime import timedelta


@login_required
def dashboard(request):
    today = timezone.now().date()
    thirty_days_ago = timezone.now() - timedelta(days=30)

    total_restaurants = Restaurant.objects.exclude(status='lead').count()
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status__in=['pending', 'confirmed']).count()
    delivered_today = Order.objects.filter(status='delivered', date_delivered__date=today).count()

    revenue_this_month = Order.objects.filter(
        status='delivered',
        date_delivered__gte=thirty_days_ago
    ).aggregate(total=Sum('total_amount'))['total'] or 0

    churn_risk = Restaurant.objects.filter(
        last_order_date__lt=timezone.now() - timedelta(days=14),
        status__in=['vip', 'regular']
    )

    low_stock = Product.objects.filter(is_active=True).filter(
        stock_kg__lte=2.0
    )

    recent_orders = Order.objects.select_related('restaurant').order_by('-date_created')[:8]

    vip_count = Restaurant.objects.filter(status='vip').count()
    regular_count = Restaurant.objects.filter(status='regular').count()
    new_count = Restaurant.objects.filter(status='new').count()
    inactive_count = Restaurant.objects.filter(status='inactive').count()
    lead_count = Restaurant.objects.filter(status='lead').count()

    unread_messages = ChatMessage.objects.filter(sender='restaurant', is_read=False).count()

    context = {
        'total_restaurants': total_restaurants,
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'delivered_today': delivered_today,
        'revenue_this_month': revenue_this_month,
        'churn_risk': churn_risk,
        'low_stock': low_stock,
        'recent_orders': recent_orders,
        'vip_count': vip_count,
        'regular_count': regular_count,
        'new_count': new_count,
        'inactive_count': inactive_count,
        'lead_count': lead_count,
        'unread_messages': unread_messages,
    }
    return render(request, 'dashboard.html', context)


@login_required
def restaurant_list(request):
    status_filter = request.GET.get('status', '')
    search = request.GET.get('q', '')

    restaurants = Restaurant.objects.all()
    if status_filter:
        restaurants = restaurants.filter(status=status_filter)
    if search:
        restaurants = restaurants.filter(
            Q(name__icontains=search) | Q(owner_name__icontains=search) | Q(city__icontains=search)
        )

    restaurants = restaurants.order_by('-date_registered')

    context = {
        'restaurants': restaurants,
        'status_filter': status_filter,
        'search': search,
        'status_choices': Restaurant.STATUS_CHOICES,
    }
    return render(request, 'restaurants/list.html', context)


@login_required
def restaurant_detail(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    orders = restaurant.orders.order_by('-date_created')
    notes = restaurant.note_set.order_by('-date_created')
    messages = restaurant.messages.order_by('timestamp')

    note_form = NoteForm()
    chat_form = ChatMessageForm()

    if request.method == 'POST':
        if 'add_note' in request.POST:
            note_form = NoteForm(request.POST)
            if note_form.is_valid():
                note = note_form.save(commit=False)
                note.restaurant = restaurant
                note.save()
                return redirect('restaurant_detail', pk=pk)

        elif 'send_message' in request.POST:
            chat_form = ChatMessageForm(request.POST)
            if chat_form.is_valid():
                msg = chat_form.save(commit=False)
                msg.restaurant = restaurant
                msg.sender = 'admin'
                msg.save()
                return redirect('restaurant_detail', pk=pk)

    restaurant.messages.filter(sender='restaurant', is_read=False).update(is_read=True)

    context = {
        'restaurant': restaurant,
        'orders': orders,
        'notes': notes,
        'messages': messages,
        'note_form': note_form,
        'chat_form': chat_form,
    }
    return render(request, 'restaurants/detail.html', context)


@login_required
def restaurant_create(request):
    form = RestaurantForm()
    if request.method == 'POST':
        form = RestaurantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('restaurant_list')
    return render(request, 'restaurants/form.html', {'form': form, 'title': 'Add Restaurant'})


@login_required
def restaurant_edit(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    form = RestaurantForm(instance=restaurant)
    if request.method == 'POST':
        form = RestaurantForm(request.POST, instance=restaurant)
        if form.is_valid():
            form.save()
            return redirect('restaurant_detail', pk=pk)
    return render(request, 'restaurants/form.html', {'form': form, 'title': 'Edit Restaurant', 'restaurant': restaurant})


@login_required
def restaurant_delete(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    if request.method == 'POST':
        restaurant.delete()
        return redirect('restaurant_list')
    return render(request, 'confirm_delete.html', {'item': restaurant, 'type': 'restaurant'})


@login_required
def order_list(request):
    status_filter = request.GET.get('status', '')
    orders = Order.objects.select_related('restaurant').order_by('-date_created')
    if status_filter:
        orders = orders.filter(status=status_filter)
    context = {
        'orders': orders,
        'status_filter': status_filter,
        'status_choices': Order.STATUS_CHOICES,
    }
    return render(request, 'orders/list.html', context)


@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    items = order.items.select_related('product').all()
    return render(request, 'orders/detail.html', {'order': order, 'items': items})


@login_required
def order_create(request):
    form = OrderForm()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('order_list')
    return render(request, 'orders/form.html', {'form': form, 'title': 'New Order'})


@login_required
def order_edit(request, pk):
    order = get_object_or_404(Order, pk=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            order = form.save(commit=False)
            if order.status == 'delivered' and not order.date_delivered:
                order.date_delivered = timezone.now()
            order.save()
            return redirect('order_detail', pk=pk)
    return render(request, 'orders/form.html', {'form': form, 'title': 'Edit Order', 'order': order})


@login_required
def product_list(request):
    products = Product.objects.filter(is_active=True).order_by('category', 'name')
    low_stock = [p for p in products if p.is_low_stock]
    return render(request, 'products/list.html', {'products': products, 'low_stock': low_stock})


@login_required
def product_create(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    return render(request, 'products/form.html', {'form': form, 'title': 'Add Product'})


@login_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = ProductForm(instance=product)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    return render(request, 'products/form.html', {'form': form, 'title': 'Edit Product', 'product': product})


@login_required
def chat_inbox(request):
    restaurants_with_messages = Restaurant.objects.filter(
        messages__isnull=False
    ).distinct().annotate(
        unread=Count('messages', filter=Q(messages__sender='restaurant', messages__is_read=False))
    ).order_by('-unread')
    return render(request, 'chat/inbox.html', {'restaurants': restaurants_with_messages})


@login_required
def delivery_list(request):
    deliveries = Order.objects.filter(
        status__in=['confirmed', 'out_for_delivery']
    ).select_related('restaurant').order_by('date_created')
    return render(request, 'delivery/list.html', {'deliveries': deliveries})


@login_required
def reports(request):
    thirty_days_ago = timezone.now() - timedelta(days=30)

    top_restaurants = Restaurant.objects.annotate(
        spent=Sum('orders__total_amount', filter=Q(orders__status='delivered'))
    ).order_by('-spent')[:10]

    monthly_revenue = Order.objects.filter(
        status='delivered',
        date_delivered__gte=thirty_days_ago
    ).aggregate(total=Sum('total_amount'))['total'] or 0

    top_products = OrderItem.objects.values('product__name').annotate(
        total_kg=Sum('quantity_kg')
    ).order_by('-total_kg')[:10]

    orders_by_status = {
        s[0]: Order.objects.filter(status=s[0]).count()
        for s in Order.STATUS_CHOICES
    }

    context = {
        'top_restaurants': top_restaurants,
        'monthly_revenue': monthly_revenue,
        'top_products': top_products,
        'orders_by_status': orders_by_status,
    }
    return render(request, 'reports/index.html', context)
