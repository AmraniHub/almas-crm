from django.contrib import admin
from .models import Restaurant, Product, Order, OrderItem, Note, ChatMessage

admin.site.register(Restaurant)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Note)
admin.site.register(ChatMessage)
