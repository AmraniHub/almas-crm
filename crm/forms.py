from django import forms
from .models import Restaurant, Product, Order, OrderItem, Note, ChatMessage


class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['name', 'owner_name', 'phone', 'email', 'address', 'city',
                  'latitude', 'longitude', 'status', 'preferred_delivery_day', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
            'address': forms.Textarea(attrs={'rows': 2}),
            'preferred_delivery_day': forms.TextInput(attrs={'placeholder': 'e.g. Monday, Thursday'}),
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'name_ar', 'category', 'price_per_kg', 'stock_kg',
                  'low_stock_threshold', 'description', 'image', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['restaurant', 'status', 'total_amount', 'notes', 'driver_name', 'payment_collected']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 2}),
        }


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity_kg', 'unit_price']


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add a note about this restaurant...'}),
        }


class ChatMessageForm(forms.ModelForm):
    class Meta:
        model = ChatMessage
        fields = ['content']
        widgets = {
            'content': forms.TextInput(attrs={'placeholder': 'Type a message...', 'autocomplete': 'off'}),
        }
