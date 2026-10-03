from django.contrib import admin
from .models import StoreProfile, Category, Product, Batch, Customer, Invoice, InvoiceItem, KhataLedger


@admin.register(StoreProfile)
class StoreProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'upi_id', 'gstin', 'gst_enabled', 'default_tax_rate')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name',)


class BatchInline(admin.TabularInline):
    model = Batch
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'category', 'unit', 'gst_rate', 'total_stock', 'min_stock_alert', 'is_active')
    list_filter = ('category', 'unit', 'is_active')
    search_fields = ('name', 'sku', 'hsn_code')
    inlines = [BatchInline]


@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ('product', 'batch_number', 'selling_price', 'mrp', 'cost_price', 'current_stock', 'expiry_date')
    list_filter = ('expiry_date',)
    search_fields = ('batch_number', 'product__name', 'product__sku')


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'khata_balance', 'created_at')
    search_fields = ('name', 'phone')


class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    readonly_fields = ('total_amount',)
    extra = 0


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'customer', 'payment_mode', 'grand_total', 'status', 'synced_from_offline', 'created_at')
    list_filter = ('payment_mode', 'status', 'synced_from_offline', 'created_at')
    search_fields = ('invoice_number', 'customer__name', 'customer__phone', 'client_invoice_id')
    readonly_fields = ('client_invoice_id', 'invoice_number', 'created_at')
    inlines = [InvoiceItemInline]


@admin.register(KhataLedger)
class KhataLedgerAdmin(admin.ModelAdmin):
    list_display = ('customer', 'entry_type', 'amount', 'payment_mode', 'notes', 'created_at')
    list_filter = ('entry_type', 'payment_mode', 'created_at')
    search_fields = ('customer__name', 'customer__phone', 'notes')
