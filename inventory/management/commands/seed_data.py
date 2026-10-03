from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from inventory.models import StoreProfile, Category, Product, Batch, Customer, Invoice, InvoiceItem, KhataLedger


class Command(BaseCommand):
    help = 'Seeds initial sample data for Kirana, General Store, and Pharmacy testing.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Seeding ISBMS Retail Sample Data...'))

        # 1. Create or update Store Profile
        store, _ = StoreProfile.objects.get_or_create(id=1)
        store.name = "Gupta Kirana & Pharmacy Store"
        store.tagline = "Apki Apni Dukan - Fast POS & Udhaar Ledger"
        store.address = "Shop #12, Main Market Road, Near City Bus Stand"
        store.phone = "+91 9876543210"
        store.email = "guptakirana@gmail.com"
        store.gstin = "07AAAAA0000A1Z5"
        store.upi_id = "guptakirana@upi"
        store.gst_enabled = True
        store.default_tax_rate = Decimal('18.00')
        store.save()

        # 2. Categories
        cat_grocery, _ = Category.objects.get_or_create(name="Grocery & Staples")
        cat_dairy, _ = Category.objects.get_or_create(name="Dairy & Bakery")
        cat_personal, _ = Category.objects.get_or_create(name="Personal Care & Soap")
        cat_pharma, _ = Category.objects.get_or_create(name="Medicines & Pharma")

        today = timezone.now().date()

        # 3. Products & Batches
        products_data = [
            {
                'sku': '8901234567890',
                'name': 'Fortune Sunlite Sunflower Oil 1L',
                'category': cat_grocery,
                'unit': 'Ltr',
                'hsn_code': '1512',
                'gst_rate': Decimal('5.00'),
                'min_stock_alert': 5,
                'batch_number': 'B-OIL-2026',
                'expiry_date': today + timedelta(days=180),
                'cost_price': Decimal('125.00'),
                'selling_price': Decimal('145.00'),
                'mrp': Decimal('160.00'),
                'stock': 40
            },
            {
                'sku': '8909876543210',
                'name': 'Amul Butter 500g Pack',
                'category': cat_dairy,
                'unit': 'Pack',
                'hsn_code': '0405',
                'gst_rate': Decimal('12.00'),
                'min_stock_alert': 8,
                'batch_number': 'B-BUTTER-MAY',
                'expiry_date': today + timedelta(days=20),  # Expiring soon for FIFO test!
                'cost_price': Decimal('235.00'),
                'selling_price': Decimal('260.00'),
                'mrp': Decimal('275.00'),
                'stock': 15
            },
            {
                'sku': '8901030000010',
                'name': 'Paracetamol 650mg Tablets (Strip of 15)',
                'category': cat_pharma,
                'unit': 'Strip',
                'hsn_code': '3004',
                'gst_rate': Decimal('12.00'),
                'min_stock_alert': 20,
                'batch_number': 'PCM-2026-X',
                'expiry_date': today + timedelta(days=15),  # Expiring soon!
                'cost_price': Decimal('18.00'),
                'selling_price': Decimal('32.00'),
                'mrp': Decimal('38.00'),
                'stock': 100
            },
            {
                'sku': '8901030999999',
                'name': 'Old Inactive Hair Oil 200ml (Dead Stock Test)',
                'category': cat_personal,
                'unit': 'Pcs',
                'hsn_code': '3305',
                'gst_rate': Decimal('18.00'),
                'min_stock_alert': 5,
                'batch_number': 'OLD-STOCK-01',
                'expiry_date': today + timedelta(days=365),
                'cost_price': Decimal('90.00'),
                'selling_price': Decimal('130.00'),
                'mrp': Decimal('150.00'),
                'stock': 25
            },
            {
                'sku': '8901234111111',
                'name': 'Tata Salt Vacuum Evaporated 1kg',
                'category': cat_grocery,
                'unit': 'Kg',
                'hsn_code': '2501',
                'gst_rate': Decimal('0.00'),
                'min_stock_alert': 15,
                'batch_number': 'SALT-2026',
                'expiry_date': today + timedelta(days=700),
                'cost_price': Decimal('22.00'),
                'selling_price': Decimal('28.00'),
                'mrp': Decimal('28.00'),
                'stock': 50
            }
        ]

        for item in products_data:
            prod, _ = Product.objects.get_or_create(
                sku=item['sku'],
                defaults={
                    'name': item['name'],
                    'category': item['category'],
                    'unit': item['unit'],
                    'hsn_code': item['hsn_code'],
                    'gst_rate': item['gst_rate'],
                    'min_stock_alert': item['min_stock_alert']
                }
            )

            Batch.objects.get_or_create(
                product=prod,
                batch_number=item['batch_number'],
                defaults={
                    'expiry_date': item['expiry_date'],
                    'cost_price': item['cost_price'],
                    'selling_price': item['selling_price'],
                    'mrp': item['mrp'],
                    'current_stock': item['stock']
                }
            )

        # 4. Customers with Khata balances
        cust1, _ = Customer.objects.get_or_create(
            phone="9876543210",
            defaults={'name': 'Ramesh Sharma (Neighbor)', 'khata_balance': Decimal('1450.00')}
        )

        cust2, _ = Customer.objects.get_or_create(
            phone="9123456789",
            defaults={'name': 'Suresh Verma', 'khata_balance': Decimal('820.50')}
        )

        self.stdout.write(self.style.SUCCESS('Successfully seeded Kirana POS sample products, batches, and Khata customers!'))
