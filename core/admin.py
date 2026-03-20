from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Category, Product, Order, OrderItem

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'phone', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('phone', 'address')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('phone', 'address')}),
    )

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'price', 'category', 'available', 'created')
    list_filter = ('available', 'category', 'created')
    list_editable = ('price', 'available')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')
    raw_id_fields = ('category',)
    date_hierarchy = 'created'

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ('product',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'first_name', 'last_name', 'email', 'paid', 'status', 'created')
    list_filter = ('paid', 'status', 'created')
    inlines = [OrderItemInline]
    search_fields = ('first_name', 'last_name', 'email', 'phone')
    date_hierarchy = 'created'
