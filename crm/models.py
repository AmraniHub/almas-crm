from django.db import models
from django.utils import timezone


class Restaurant(models.Model):
    STATUS_CHOICES = [
        ('vip', 'VIP'),
        ('regular', 'Regular'),
        ('new', 'New'),
        ('inactive', 'Inactive'),
        ('at_risk', 'At Risk'),
        ('lead', 'Lead'),
    ]

    name = models.CharField(max_length=200)
    owner_name = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True, default='Casablanca')
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    preferred_delivery_day = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    date_registered = models.DateTimeField(auto_now_add=True)
    last_order_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def waze_url(self):
        if self.latitude and self.longitude:
            return f'https://waze.com/ul?ll={self.latitude},{self.longitude}&navigate=yes'
        return None

    @property
    def total_spent(self):
        return sum(o.total_amount for o in self.orders.filter(status='delivered'))

    @property
    def total_orders(self):
        return self.orders.count()

    @property
    def days_since_last_order(self):
        if self.last_order_date:
            return (timezone.now() - self.last_order_date).days
        return None


class Product(models.Model):
    CATEGORY_CHOICES = [
        ('whole', 'Whole Spices'),
        ('ground', 'Ground Spices'),
        ('blend', 'Spice Blends'),
        ('herb', 'Dried Herbs'),
        ('seed', 'Seeds'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=200)
    name_ar = models.CharField(max_length=200, blank=True, verbose_name='Arabic Name')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='whole')
    price_per_kg = models.FloatField()
    stock_kg = models.FloatField(default=0)
    low_stock_threshold = models.FloatField(default=2.0)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def is_low_stock(self):
        return self.stock_kg <= self.low_stock_threshold


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    restaurant = models.ForeignKey(Restaurant, on_delete=models.SET_NULL, null=True, related_name='orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_amount = models.FloatField(default=0)
    notes = models.TextField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_delivered = models.DateTimeField(null=True, blank=True)
    payment_collected = models.BooleanField(default=False)
    driver_name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f'Order #{self.pk} — {self.restaurant}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.status == 'delivered' and self.restaurant:
            self.restaurant.last_order_date = self.date_delivered or timezone.now()
            self.restaurant.save(update_fields=['last_order_date'])


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity_kg = models.FloatField()
    unit_price = models.FloatField()

    def __str__(self):
        return f'{self.product} x {self.quantity_kg}kg'

    @property
    def subtotal(self):
        return self.quantity_kg * self.unit_price


class Note(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='note_set')
    content = models.TextField()
    author = models.CharField(max_length=100, default='Admin')
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Note for {self.restaurant} — {self.date_created.strftime("%d/%m/%Y")}'


class ChatMessage(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='messages')
    sender = models.CharField(max_length=20, choices=[('admin', 'Almas Admin'), ('restaurant', 'Restaurant')])
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f'{self.sender} → {self.restaurant} at {self.timestamp.strftime("%H:%M")}'
