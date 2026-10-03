import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal


class StoreProfile(models.Model):
    """Universal Store Profile for any retail business type (Perfumes, Clothing, Electronics, Kirana, Pharma)."""
    STORE_TYPE_CHOICES = [
        ('PERFUME', 'Perfumes, Fragrances & Cosmetics'),
        ('CLOTHING', 'Apparel, Fashion & Footwear'),
        ('ELECTRONICS', 'Mobiles, Gadgets & Electronics'),
        ('GROCERY', 'Kirana, Staples & Supermarket'),
        ('PHARMA', 'Pharmacy & Medical Store'),
        ('HARDWARE', 'Hardware, Electrical & Plumbing'),
        ('GENERAL', 'General Retail & Gift Shop'),
    ]

    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='store', null=True, blank=True)
    name = models.CharField(max_length=150, default="Retail Shop & Boutique")
    store_type = models.CharField(max_length=30, choices=STORE_TYPE_CHOICES, default='GENERAL')
    tagline = models.CharField(max_length=255, blank=True, default="Your Trusted Retail Store")
    address = models.TextField(default="Main Road, Market Square, City")
    phone = models.CharField(max_length=15, default="+91 9876543210")
    email = models.EmailField(blank=True, default="contact@retail.local")
    gstin = models.CharField(max_length=15, blank=True, null=True, help_text="GST Identification Number")
    upi_id = models.CharField(max_length=100, default="store@upi", help_text="Store VPA for dynamic QR billing (GPay/Paytm/PhonePe)")
    pan_number = models.CharField(max_length=10, blank=True, null=True, help_text="PAN Card Number for Merchant KYC")
    aadhaar_number = models.CharField(max_length=12, blank=True, null=True, help_text="12-digit Aadhaar Card Number")
    kyc_status = models.CharField(max_length=20, choices=[('VERIFIED', 'KYC Verified'), ('PENDING', 'Verification Pending'), ('REJECTED', 'Rejected')], default='VERIFIED')
    gst_enabled = models.BooleanField(default=True)
    default_tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('18.00'), help_text="Default GST %")
    thermal_printer_width = models.IntegerField(default=58, help_text="58 or 80 mm")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} [{self.get_store_type_display()}] (Owner: {self.owner.username if self.owner else 'Default'})"

    class Meta:
        verbose_name = "Store Profile"
        verbose_name_plural = "Store Profiles"


class Category(models.Model):
    """Product category grouping per store."""
    store = models.ForeignKey(StoreProfile, on_delete=models.CASCADE, related_name='categories', null=True, blank=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.store.name if self.store else 'Global'})"

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']
        unique_together = ['store', 'name']


class Product(models.Model):
    """Universal master product catalog tracking items across all retail industries."""
    UNIT_CHOICES = [
        ('Bottle', 'Bottle (Perfume/Liquids)'),
        ('Ml', 'Milliliters (Ml)'),
        ('Pcs', 'Pieces (Pcs)'),
        ('Pair', 'Pair (Footwear/Items)'),
        ('Set', 'Set / Combo'),
        ('Box', 'Box'),
        ('Pack', 'Pack'),
        ('Kg', 'Kilograms (Kg)'),
        ('Gm', 'Grams (Gm)'),
        ('Ltr', 'Liters (Ltr)'),
        ('Strip', 'Strip (Pharma)'),
    ]

    store = models.ForeignKey(StoreProfile, on_delete=models.CASCADE, related_name='products', null=True, blank=True)
    sku = models.CharField(max_length=100, db_index=True, help_text="Barcode or SKU Code")
    name = models.CharField(max_length=200, db_index=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    hsn_code = models.CharField(max_length=20, blank=True, default="3303")
    unit = models.CharField(max_length=20, choices=UNIT_CHOICES, default='Pcs')
    gst_rate = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('18.00'), help_text="GST percentage e.g. 0, 5, 12, 18, 28")
    min_stock_alert = models.IntegerField(default=5, help_text="Reorder threshold trigger")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.sku})"

    class Meta:
        unique_together = ['store', 'sku']

    @property
    def total_stock(self):
        """Aggregate available stock across all active batches."""
        total = self.batches.aggregate(total=models.Sum('current_stock'))['total']
        return total or 0

    @property
    def is_low_stock(self):
        return self.total_stock <= self.min_stock_alert


class Batch(models.Model):
    """Batch-level tracking for pricing, FIFO management, and expiry dates."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='batches')
    batch_number = models.CharField(max_length=100, default='DEFAULT')
    mfg_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True, db_index=True)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Purchase price per unit")
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Actual POS billing price")
    mrp = models.DecimalField(max_digits=10, decimal_places=2, help_text="Maximum Retail Price")
    current_stock = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['expiry_date', 'created_at']
        verbose_name_plural = "Batches"

    def __str__(self):
        exp_str = self.expiry_date.strftime('%Y-%m') if self.expiry_date else 'N/A'
        return f"{self.product.name} | Batch: {self.batch_number} | Exp: {exp_str} | Stock: {self.current_stock}"

    @property
    def is_expiring_soon(self):
        if not self.expiry_date:
            return False
        today = timezone.now().date()
        return today <= self.expiry_date <= today + timedelta(days=30)

    @property
    def is_expired(self):
        if not self.expiry_date:
            return False
        return self.expiry_date < timezone.now().date()


class Customer(models.Model):
    """Customer profile and Khata balance ledger owner per store."""
    store = models.ForeignKey(StoreProfile, on_delete=models.CASCADE, related_name='customers', null=True, blank=True)
    name = models.CharField(max_length=150, db_index=True)
    phone = models.CharField(max_length=15, db_index=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, default='')
    khata_balance = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), help_text="Positive value means customer owes money to store")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.phone}) - Khata: ₹{self.khata_balance}"

    class Meta:
        ordering = ['name']
        unique_together = ['store', 'phone']


class Invoice(models.Model):
    """Sales invoice header representing a POS transaction per store."""
    PAYMENT_MODES = [
        ('CASH', 'Cash'),
        ('UPI', 'UPI / QR Code'),
        ('KHATA', 'Digital Khata (Udhaari)'),
        ('CARD', 'Debit/Credit Card'),
        ('MIXED', 'Mixed Payment'),
    ]

    STATUS_CHOICES = [
        ('PAID', 'Fully Paid'),
        ('PENDING', 'Pending Khata'),
        ('CANCELLED', 'Cancelled'),
    ]

    store = models.ForeignKey(StoreProfile, on_delete=models.CASCADE, related_name='invoices', null=True, blank=True)
    client_invoice_id = models.CharField(max_length=100, db_index=True, help_text="Client side UUID for offline sync idempotency")
    invoice_number = models.CharField(max_length=50, db_index=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, related_name='invoices')
    payment_mode = models.CharField(max_length=20, choices=PAYMENT_MODES, default='CASH')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PAID')
    
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    khata_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    
    is_gst = models.BooleanField(default=True)
    synced_from_offline = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now, db_index=True)

    def __str__(self):
        return f"Invoice #{self.invoice_number} - ₹{self.grand_total} ({self.get_payment_mode_display()})"

    class Meta:
        ordering = ['-created_at']


class InvoiceItem(models.Model):
    """Line item in a POS invoice."""
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    batch = models.ForeignKey(Batch, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    gst_rate = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'))
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} x {self.quantity} = ₹{self.total_amount}"


class KhataLedger(models.Model):
    """Ledger history tracking credit given and payments received for Digital Khata."""
    ENTRY_TYPES = [
        ('DEBIT', 'Udhaar Given (Credit Sales)'),
        ('CREDIT', 'Payment Received (Settlement)'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='ledger_entries')
    entry_type = models.CharField(max_length=10, choices=ENTRY_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    invoice = models.ForeignKey(Invoice, on_delete=models.SET_NULL, null=True, blank=True, related_name='khata_entries')
    payment_mode = models.CharField(max_length=20, default='CASH')
    notes = models.CharField(max_length=255, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.name} - {self.entry_type}: ₹{self.amount} at {self.created_at.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        ordering = ['-created_at']
