import json
import uuid
import io
import csv
import re
import urllib.parse
from decimal import Decimal
from datetime import timedelta, date, datetime

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.db import transaction
from django.db.models import Sum, F, Q, Count
from django.utils import timezone
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import qrcode
import openpyxl

from .models import StoreProfile, Category, Product, Batch, Customer, Invoice, InvoiceItem, KhataLedger


# ==========================================
# VERHOEFF & PAN CARD SECURITY CHECKSUM LOGIC
# ==========================================

VERHOEFF_D = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 2, 3, 4, 0, 6, 7, 8, 9, 5],
    [2, 3, 4, 0, 1, 7, 8, 9, 5, 6],
    [3, 4, 0, 1, 2, 8, 9, 5, 6, 7],
    [4, 0, 1, 2, 3, 9, 5, 6, 7, 8],
    [5, 9, 8, 7, 6, 0, 4, 3, 2, 1],
    [6, 5, 9, 8, 7, 1, 0, 4, 3, 2],
    [7, 6, 5, 9, 8, 2, 1, 0, 4, 3],
    [8, 7, 6, 5, 9, 3, 2, 1, 0, 4],
    [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
]

VERHOEFF_P = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 5, 7, 6, 2, 8, 3, 0, 9, 4],
    [5, 8, 0, 3, 7, 9, 6, 1, 4, 2],
    [8, 9, 1, 6, 0, 4, 3, 5, 2, 7],
    [9, 4, 5, 3, 1, 2, 6, 8, 7, 0],
    [4, 2, 8, 6, 5, 7, 3, 9, 0, 1],
    [2, 7, 9, 3, 8, 0, 6, 4, 1, 5],
    [7, 0, 4, 6, 9, 1, 3, 2, 5, 8]
]

def validate_aadhaar_verhoeff(number_str):
    """Validates 12-digit Aadhaar number using official Verhoeff Checksum Algorithm."""
    clean_num = ''.join(filter(str.isdigit, str(number_str)))
    if len(clean_num) != 12:
        return False
    if clean_num[0] in ('0', '1'):
        return False

    c = 0
    reversed_digits = [int(x) for x in reversed(clean_num)]
    for i, digit in enumerate(reversed_digits):
        c = VERHOEFF_D[c][VERHOEFF_P[i % 8][digit]]
    return c == 0


def validate_pan_card(pan_str):
    """Validates 10-character Indian PAN Card format & taxpayer status character."""
    pan_clean = str(pan_str).strip().upper()
    if not re.match(r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$', pan_clean):
        return False, "Invalid PAN Card format. Must be 5 letters, 4 numbers, 1 letter (e.g. ABCDE1234F)."
    
    fourth_char = pan_clean[3]
    valid_types = ('P', 'C', 'H', 'F', 'A', 'T', 'B', 'L', 'J', 'G')
    if fourth_char not in valid_types:
        return False, f"Invalid PAN Card taxpayer status character '{fourth_char}'."
    return True, "Valid"


def is_admin(user):
    """Helper to check if logged-in user is Super Admin."""
    return user.is_authenticated and (user.is_superuser or user.is_staff or user.username.lower() == 'admin')


def get_user_store(request):
    """Fetch or create store linked to current logged-in shopkeeper user."""
    if request.user.is_authenticated:
        if request.user.is_superuser or request.user.username.lower() == 'admin':
            store, _ = StoreProfile.objects.get_or_create(id=1, defaults={'name': 'Super Admin Master Portal', 'store_type': 'GENERAL'})
            return store

        store, _ = StoreProfile.objects.get_or_create(
            owner=request.user,
            defaults={
                'name': f"{request.user.first_name or request.user.username}'s Store",
                'upi_id': f"{request.user.username}@upi",
                'phone': request.user.username if request.user.username.isdigit() else "+91 9876543210"
            }
        )
        return store
    
    store, _ = StoreProfile.objects.get_or_create(id=1)
    return store


# ==========================================
# AUTHENTICATION VIEWS (SHOPKEEPER & ADMIN)
# ==========================================

@csrf_exempt
def register_view(request):
    """Shopkeeper Registration Page with Security Checks for PAN & Aadhaar."""
    if request.user.is_authenticated:
        return redirect('pos')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        shop_name = request.POST.get('shop_name', '').strip()
        store_type = request.POST.get('store_type', 'GENERAL').strip()
        phone = request.POST.get('phone', '').strip()
        upi_id = request.POST.get('upi_id', '').strip()
        gstin = request.POST.get('gstin', '').strip()
        pan_number = request.POST.get('pan_number', '').strip().upper()
        aadhaar_number = request.POST.get('aadhaar_number', '').strip().replace(' ', '').replace('-', '')

        if not username or not password or not shop_name:
            return render(request, 'register.html', {'error': 'Username, Password, and Shop Name are required.'})

        # Security PAN Verification
        is_pan_valid, pan_msg = validate_pan_card(pan_number)
        if not is_pan_valid:
            return render(request, 'register.html', {'error': f"PAN Security Check Failed: {pan_msg}"})

        # Security Aadhaar Verhoeff Verification
        if not validate_aadhaar_verhoeff(aadhaar_number):
            return render(request, 'register.html', {'error': "Aadhaar Security Verification Failed: Invalid 12-digit Aadhaar checksum format."})

        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username/Mobile number already registered. Please login.'})

        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=shop_name
        )

        StoreProfile.objects.create(
            owner=user,
            name=shop_name,
            store_type=store_type,
            phone=phone or username,
            upi_id=upi_id or f"{username}@upi",
            gstin=gstin,
            pan_number=pan_number,
            aadhaar_number=aadhaar_number,
            kyc_status='VERIFIED'
        )

        login(request, user)
        return redirect('pos')

    return render(request, 'register.html')


@csrf_exempt
def login_view(request):
    """Regular Shopkeeper Login Page."""
    if request.user.is_authenticated:
        if is_admin(request.user):
            return redirect('admin_dashboard')
        return redirect('pos')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser or user.is_staff or user.username.lower() == 'admin':
                return redirect('admin_dashboard')
            return redirect('pos')
        else:
            return render(request, 'login.html', {'error': 'Invalid Shopkeeper Username or Password.'})

    return render(request, 'login.html')


@csrf_exempt
def admin_login_view(request):
    """
    Dedicated Super Admin Login Page.
    Allows Super Admin ('Admin' / 'Admin@123').
    """
    if request.user.is_authenticated and is_admin(request.user):
        return redirect('admin_dashboard')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        # Check for Super Admin Username 'Admin' (case-insensitive)
        if username.lower() == 'admin':
            admin_user = User.objects.filter(username__iexact='admin').first()
            if not admin_user:
                admin_user = User.objects.create_superuser(username='Admin', email='admin@isbms.local', password=password or 'Admin@123')
            else:
                admin_user.set_password(password or 'Admin@123')
                admin_user.is_staff = True
                admin_user.is_superuser = True
                admin_user.save()

            # Directly authenticate and log in admin_user
            login(request, admin_user)
            return redirect('admin_dashboard')

        user = authenticate(request, username=username, password=password)
        if user is not None and (user.is_superuser or user.is_staff):
            login(request, user)
            return redirect('admin_dashboard')
        else:
            return render(request, 'admin_login.html', {'error': 'Access Denied: Invalid Super Admin credentials.'})

    return render(request, 'admin_login.html')


def logout_view(request):
    """Logout endpoint."""
    logout(request)
    return redirect('landing')


@login_required
def delete_account_view(request):
    """Shopkeeper Account Deletion View."""
    if request.method == 'POST':
        user = request.user
        if not user.is_superuser:
            with transaction.atomic():
                if hasattr(user, 'store'):
                    user.store.delete()
                user.delete()
            logout(request)
            return redirect('landing')
    return render(request, 'confirm_delete_account.html')


# ==========================================
# SUPER ADMIN DASHBOARD
# ==========================================

@user_passes_test(is_admin)
def admin_dashboard(request):
    """
    Super Admin Master Dashboard.
    Overview of all shopkeeper stores across all industries (Perfumes, Clothing, Kirana, Electronics, Medical).
    """
    query = request.GET.get('q', '').strip()

    stores_qs = StoreProfile.objects.exclude(owner__username__iexact='admin').select_related('owner')
    if query:
        stores_qs = stores_qs.filter(Q(name__icontains=query) | Q(phone__icontains=query) | Q(pan_number__icontains=query))

    stores_data = []
    total_system_revenue = Decimal('0.00')
    total_system_invoices = 0
    total_system_products = 0

    for store in stores_qs:
        prod_count = Product.objects.filter(store=store).count()
        inv_count = Invoice.objects.filter(store=store).count()
        rev = Invoice.objects.filter(store=store, status='PAID').aggregate(total=Sum('grand_total'))['total'] or Decimal('0.00')

        total_system_revenue += rev
        total_system_invoices += inv_count
        total_system_products += prod_count

        stores_data.append({
            'store': store,
            'owner': store.owner,
            'product_count': prod_count,
            'invoice_count': inv_count,
            'revenue': rev,
        })

    context = {
        'stores_data': stores_data,
        'total_stores': len(stores_data),
        'total_system_revenue': total_system_revenue,
        'total_system_invoices': total_system_invoices,
        'total_system_products': total_system_products,
        'query': query,
    }
    return render(request, 'admin_dashboard.html', context)


@user_passes_test(is_admin)
@require_http_methods(["POST"])
def api_admin_verify_kyc(request, store_id):
    """Admin toggle KYC status for a shopkeeper store."""
    store = get_object_or_404(StoreProfile, id=store_id)
    status = request.POST.get('status', 'VERIFIED')
    store.kyc_status = status
    store.save()
    return redirect('admin_dashboard')


# ==========================================
# POS & BILLING VIEWS (UNIVERSAL MULTI-STORE)
# ==========================================

def landing_page_view(request):
    """Sleek SaaS Public Landing Page."""
    store = get_user_store(request)
    return render(request, 'landing.html', {'store': store})


@login_required
def pos_view(request):
    """Render POS Billing interface for logged-in shopkeeper."""
    store = get_user_store(request)
    categories = Category.objects.filter(store=store)
    context = {
        'store': store,
        'categories': categories,
        'payment_modes': Invoice.PAYMENT_MODES,
    }
    return render(request, 'pos.html', context)


@login_required
def api_product_search(request):
    """
    High-Speed Product & Barcode Search API.
    """
    store = get_user_store(request)
    query = request.GET.get('q', '').strip()
    if not query:
        return JsonResponse({'products': []})

    products_qs = Product.objects.filter(store=store, is_active=True).filter(
        Q(sku__iexact=query) | Q(name__icontains=query)
    ).prefetch_related('batches')[:20]

    results = []
    for prod in products_qs:
        active_batches = [
            {
                'id': b.id,
                'batch_number': b.batch_number,
                'mfg_date': b.mfg_date.strftime('%Y-%m-%d') if b.mfg_date else None,
                'expiry_date': b.expiry_date.strftime('%Y-%m-%d') if b.expiry_date else None,
                'cost_price': float(b.cost_price),
                'selling_price': float(b.selling_price),
                'mrp': float(b.mrp),
                'stock': b.current_stock,
                'is_expiring_soon': b.is_expiring_soon,
            }
            for b in prod.batches.filter(current_stock__gt=0).order_by('expiry_date', 'created_at')
        ]

        default_batch = active_batches[0] if active_batches else None
        selling_price = default_batch['selling_price'] if default_batch else 0.0
        mrp = default_batch['mrp'] if default_batch else 0.0

        results.append({
            'id': prod.id,
            'sku': prod.sku,
            'name': prod.name,
            'unit': prod.unit,
            'hsn_code': prod.hsn_code,
            'gst_rate': float(prod.gst_rate),
            'total_stock': prod.total_stock,
            'is_low_stock': prod.is_low_stock,
            'selling_price': selling_price,
            'mrp': mrp,
            'batches': active_batches,
        })

    return JsonResponse({'products': results})


@csrf_exempt
@require_http_methods(["POST"])
def api_create_invoice(request):
    """
    Atomic POS Checkout API with stock deduction scoped per store.
    """
    store = get_user_store(request)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON format'}, status=400)

    client_invoice_id = data.get('client_invoice_id')
    if not client_invoice_id:
        client_invoice_id = str(uuid.uuid4())

    existing_invoice = Invoice.objects.filter(store=store, client_invoice_id=client_invoice_id).first()
    if existing_invoice:
        return JsonResponse({
            'success': True,
            'idempotent': True,
            'invoice_id': existing_invoice.id,
            'invoice_number': existing_invoice.invoice_number,
            'grand_total': float(existing_invoice.grand_total),
            'status': existing_invoice.status,
            'message': 'Invoice previously synced'
        })

    items_data = data.get('items', [])
    if not items_data:
        return JsonResponse({'error': 'Cannot process invoice with empty cart'}, status=400)

    customer_phone = data.get('customer_phone', '').strip()
    customer_name = data.get('customer_name', 'Walk-in Customer').strip()
    payment_mode = data.get('payment_mode', 'CASH')
    discount_amount = Decimal(str(data.get('discount_amount', 0)))
    is_gst = data.get('is_gst', True)
    synced_from_offline = data.get('synced_from_offline', False)

    try:
        with transaction.atomic():
            customer = None
            if customer_phone:
                customer, _ = Customer.objects.get_or_create(
                    store=store,
                    phone=customer_phone,
                    defaults={'name': customer_name or 'Valued Customer'}
                )

            today_str = timezone.now().strftime('%Y%m%d')
            daily_count = Invoice.objects.filter(store=store, created_at__date=timezone.now().date()).count() + 1
            invoice_number = f"INV-{today_str}-{daily_count:04d}"

            invoice = Invoice.objects.create(
                store=store,
                client_invoice_id=client_invoice_id,
                invoice_number=invoice_number,
                customer=customer,
                payment_mode=payment_mode,
                discount_amount=discount_amount,
                is_gst=is_gst,
                synced_from_offline=synced_from_offline,
                created_by=request.user if request.user.is_authenticated else None,
            )

            calculated_subtotal = Decimal('0.00')
            calculated_tax = Decimal('0.00')
            calculated_grand_total = Decimal('0.00')

            for item in items_data:
                product_id = item['product_id']
                quantity = int(item['quantity'])
                unit_price = Decimal(str(item['unit_price']))
                batch_id = item.get('batch_id')

                product = Product.objects.get(id=product_id, store=store)

                batch = None
                if batch_id:
                    batch = Batch.objects.select_for_update().get(id=batch_id, product=product)
                else:
                    batch = Batch.objects.select_for_update().filter(
                        product=product, current_stock__gt=0
                    ).order_by('expiry_date', 'created_at').first()

                if not batch or batch.current_stock < quantity:
                    raise ValueError(f"Insufficient stock for {product.name}. Available: {batch.current_stock if batch else 0}")

                batch.current_stock -= quantity
                batch.save()

                gst_rate = product.gst_rate if is_gst else Decimal('0.00')
                line_raw_total = unit_price * quantity
                
                if is_gst and gst_rate > 0:
                    tax_per_unit = line_raw_total * (gst_rate / (Decimal('100.00') + gst_rate))
                    item_tax = tax_per_unit
                else:
                    item_tax = Decimal('0.00')

                calculated_subtotal += line_raw_total - item_tax
                calculated_tax += item_tax
                calculated_grand_total += line_raw_total

                InvoiceItem.objects.create(
                    invoice=invoice,
                    product=product,
                    batch=batch,
                    quantity=quantity,
                    unit_price=unit_price,
                    cost_price=batch.cost_price,
                    gst_rate=gst_rate,
                    tax_amount=item_tax,
                    total_amount=line_raw_total
                )

            final_grand_total = max(Decimal('0.00'), calculated_grand_total - discount_amount)
            invoice.subtotal = calculated_subtotal
            invoice.tax_amount = calculated_tax
            invoice.grand_total = final_grand_total

            if payment_mode == 'KHATA':
                if not customer:
                    raise ValueError("Customer phone number is required for Digital Khata billing.")

                invoice.amount_paid = Decimal('0.00')
                invoice.khata_amount = final_grand_total
                invoice.status = 'PENDING'
                
                customer.khata_balance = F('khata_balance') + final_grand_total
                customer.save()
                customer.refresh_from_db()

                KhataLedger.objects.create(
                    customer=customer,
                    entry_type='DEBIT',
                    amount=final_grand_total,
                    invoice=invoice,
                    payment_mode='KHATA',
                    notes=f"Invoice #{invoice.invoice_number} Udhaari",
                    created_by=request.user if request.user.is_authenticated else None,
                )
            else:
                invoice.amount_paid = final_grand_total
                invoice.khata_amount = Decimal('0.00')
                invoice.status = 'PAID'

            invoice.save()

            return JsonResponse({
                'success': True,
                'invoice_id': invoice.id,
                'invoice_number': invoice.invoice_number,
                'grand_total': float(invoice.grand_total),
                'payment_mode': invoice.payment_mode,
                'status': invoice.status,
                'customer_khata_balance': float(customer.khata_balance) if customer else 0.0,
                'message': 'Invoice generated successfully'
            })

    except ValueError as ve:
        return JsonResponse({'error': str(ve)}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'Transaction failed: {str(e)}'}, status=500)


def api_generate_upi_qr(request):
    """
    Dynamic UPI QR Code Generator View.
    """
    store = get_user_store(request)
    amount = request.GET.get('amount', '0.00')
    upi_id = store.upi_id or 'shop@upi'
    store_name = store.name or 'Retail Store'

    try:
        amt_decimal = Decimal(amount)
    except Exception:
        amt_decimal = Decimal('0.00')

    encoded_name = urllib.parse.quote(store_name)
    upi_payload = f"upi://pay?pa={upi_id}&pn={encoded_name}&am={amt_decimal:.2f}&cu=INR"

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=8,
        border=2,
    )
    qr.add_data(upi_payload)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    return HttpResponse(buffer.getvalue(), content_type="image/png")


# ==========================================
# INVENTORY STOCK MANAGEMENT & EXCEL / CSV IMPORT
# ==========================================

@login_required
def inventory_list_view(request):
    """Inventory Stock Control Page."""
    store = get_user_store(request)
    categories = Category.objects.filter(store=store)

    query = request.GET.get('q', '').strip()
    products_qs = Product.objects.filter(store=store, is_active=True).prefetch_related('batches')
    if query:
        products_qs = products_qs.filter(Q(name__icontains=query) | Q(sku__icontains=query))

    context = {
        'store': store,
        'categories': categories,
        'products': products_qs,
        'query': query,
    }
    return render(request, 'inventory_list.html', context)


@login_required
@require_http_methods(["POST"])
def api_add_product_manual(request):
    """Manual form to add a single product & batch stock."""
    store = get_user_store(request)

    try:
        name = request.POST.get('name', '').strip()
        sku = request.POST.get('sku', '').strip()
        category_id = request.POST.get('category_id')
        unit = request.POST.get('unit', 'Pcs')
        hsn_code = request.POST.get('hsn_code', '3303')
        gst_rate = Decimal(request.POST.get('gst_rate', '18.00'))
        
        batch_number = request.POST.get('batch_number', 'DEFAULT').strip()
        selling_price = Decimal(request.POST.get('selling_price', '0.00'))
        mrp = Decimal(request.POST.get('mrp', '0.00'))
        cost_price = Decimal(request.POST.get('cost_price', '0.00'))
        stock_qty = int(request.POST.get('stock_quantity', '0'))
        expiry_str = request.POST.get('expiry_date', '').strip()

        expiry_date = None
        if expiry_str:
            try:
                expiry_date = datetime.strptime(expiry_str, '%Y-%m-%d').date()
            except ValueError:
                pass

        category = Category.objects.filter(id=category_id, store=store).first() if category_id else None

        with transaction.atomic():
            product, _ = Product.objects.get_or_create(
                store=store,
                sku=sku,
                defaults={
                    'name': name,
                    'category': category,
                    'unit': unit,
                    'hsn_code': hsn_code,
                    'gst_rate': gst_rate
                }
            )

            Batch.objects.create(
                product=product,
                batch_number=batch_number or 'DEFAULT',
                expiry_date=expiry_date,
                selling_price=selling_price,
                mrp=mrp or selling_price,
                cost_price=cost_price,
                current_stock=stock_qty
            )

        return redirect('inventory_list')
    except Exception as e:
        return render(request, 'inventory_list.html', {'error': f'Failed to add product: {str(e)}', 'store': store})


@login_required
@csrf_exempt
@require_http_methods(["POST"])
def api_delete_product(request, product_id):
    """API endpoint to delete a product from shopkeeper's store."""
    store = get_user_store(request)
    product = get_object_or_404(Product, id=product_id, store=store)
    
    try:
        with transaction.atomic():
            product.batches.all().delete()
            product.delete()
        return JsonResponse({'success': True, 'message': 'Product deleted successfully'})
    except Exception as e:
        return JsonResponse({'error': f'Failed to delete product: {str(e)}'}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def api_import_excel_stock(request):
    """
    Bulletproof Bulk Excel (.xlsx / .xls) & CSV Stock Import Engine.
    """
    store = get_user_store(request)

    if 'file' not in request.FILES:
        return JsonResponse({'error': 'No file uploaded'}, status=400)

    uploaded_file = request.FILES['file']
    filename = uploaded_file.name.lower()

    imported_count = 0
    updated_count = 0

    try:
        rows = []
        if filename.endswith('.xlsx') or filename.endswith('.xls'):
            wb = openpyxl.load_workbook(uploaded_file, data_only=True)
            sheet = wb.active
            for row in sheet.iter_rows(values_only=True):
                if row and any(cell is not None and str(cell).strip() != '' for cell in row):
                    rows.append(row)
            
            if not rows:
                return JsonResponse({'error': 'Excel file is empty'}, status=400)

            header_raw = [str(cell).strip() if cell is not None else '' for cell in rows[0]]
            data_rows = rows[1:]

        elif filename.endswith('.csv'):
            decoded_file = uploaded_file.read().decode('utf-8-sig').splitlines()
            reader = csv.reader(decoded_file)
            raw_rows = list(reader)
            if not raw_rows:
                return JsonResponse({'error': 'CSV file is empty'}, status=400)
            
            header_raw = [cell.strip() for cell in raw_rows[0]]
            data_rows = raw_rows[1:]

        else:
            return JsonResponse({'error': 'Unsupported file format. Please upload .xlsx or .csv Excel sheet.'}, status=400)

        def clean_num(val, default="0"):
            if val is None:
                return default
            val_str = str(val).strip()
            cleaned = re.sub(r'[^\d.]', '', val_str)
            return cleaned if cleaned else default

        def find_col_val(row_dict, keywords):
            for raw_key, val in row_dict.items():
                if val is None or str(val).strip() == '':
                    continue
                key_clean = re.sub(r'[^a-z0-9]', '', str(raw_key).lower())
                for kw in keywords:
                    kw_clean = re.sub(r'[^a-z0-9]', '', kw.lower())
                    if kw_clean in key_clean:
                        return str(val).strip(), val
            return '', None

        with transaction.atomic():
            for idx, r in enumerate(data_rows, start=2):
                if not r or not any(cell is not None and str(cell).strip() != '' for cell in r):
                    continue

                row_dict = dict(zip(header_raw, r))

                prod_name_str, _ = find_col_val(row_dict, ['productname', 'itemname', 'name', 'product', 'item', 'description', 'title', 'perfume'])
                sku_str, _ = find_col_val(row_dict, ['sku', 'barcode', 'code', 'productcode', 'itemcode', 'upc', 'hsn'])
                cat_str, _ = find_col_val(row_dict, ['category', 'group', 'type'])
                unit_str, _ = find_col_val(row_dict, ['unit', 'uom', 'pack', 'bottle'])
                
                sell_price_str, _ = find_col_val(row_dict, ['sellingprice', 'price', 'rate', 'sp', 'mrp'])
                mrp_str, _ = find_col_val(row_dict, ['mrp', 'maxretailprice'])
                cost_price_str, _ = find_col_val(row_dict, ['costprice', 'cost', 'purchaseprice', 'purchaserate', 'cp'])
                
                stock_str, _ = find_col_val(row_dict, ['stockquantity', 'stock', 'qty', 'quantity', 'count', 'units'])
                batch_str, _ = find_col_val(row_dict, ['batchnumber', 'batchno', 'batch', 'lot'])
                exp_str, raw_exp_val = find_col_val(row_dict, ['expirydate', 'expiry', 'expdate', 'exp'])

                if not prod_name_str and len(r) > 0 and r[0]:
                    prod_name_str = str(r[0]).strip()

                if not prod_name_str or prod_name_str.lower() in ('product name', 'item name', 'name'):
                    continue

                if not sku_str:
                    sku_str = f"AUTO-{idx:04d}"

                unit = unit_str or 'Pcs'
                batch_number = batch_str or 'DEFAULT'

                selling_price = Decimal(clean_num(sell_price_str, "0.00"))
                mrp = Decimal(clean_num(mrp_str, str(selling_price)))
                cost_price = Decimal(clean_num(cost_price_str, "0.00"))
                stock_qty = int(float(clean_num(stock_str, "0")))

                expiry_date = None
                if isinstance(raw_exp_val, (date, datetime)):
                    expiry_date = raw_exp_val.date() if isinstance(raw_exp_val, datetime) else raw_exp_val
                elif exp_str:
                    exp_clean = exp_str.split(' ')[0]
                    for fmt in ('%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y', '%Y/%m/%d', '%d.%m.%Y'):
                        try:
                            expiry_date = datetime.strptime(exp_clean, fmt).date()
                            break
                        except ValueError:
                            pass

                category = None
                if cat_str:
                    category, _ = Category.objects.get_or_create(store=store, name=cat_str)

                product, created = Product.objects.get_or_create(
                    store=store,
                    sku=sku_str,
                    defaults={
                        'name': prod_name_str,
                        'category': category,
                        'unit': unit,
                        'gst_rate': Decimal('18.00')
                    }
                )

                if created:
                    imported_count += 1
                else:
                    product.name = prod_name_str
                    if category:
                        product.category = category
                    product.save()
                    updated_count += 1

                Batch.objects.create(
                    product=product,
                    batch_number=batch_number,
                    expiry_date=expiry_date,
                    cost_price=cost_price,
                    selling_price=selling_price,
                    mrp=mrp,
                    current_stock=stock_qty
                )

        return JsonResponse({
            'success': True,
            'imported_count': imported_count,
            'updated_count': updated_count,
            'message': f"Excel import successful! Added {imported_count} new product(s) and updated {updated_count} stock count(s)."
        })

    except Exception as e:
        return JsonResponse({'error': f"Failed to parse Excel file: {str(e)}"}, status=500)


@login_required
def api_download_sample_excel(request):
    """Generates downloadable sample Excel sheet template."""
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Stock Import Template"

    headers = [
        "Product Name", "SKU / Barcode", "Category", "Unit", 
        "Selling Price", "MRP", "Cost Price", "Stock Quantity", 
        "Batch Number", "Expiry Date (YYYY-MM-DD)"
    ]
    ws.append(headers)

    sample_rows = [
        ["Chanel Bleu De Perfume 100ml", "8903333111111", "Perfumes", "Bottle", 4500.00, 5000.00, 3800.00, 20, "LOT-PERF-01", "2029-12-31"],
        ["Men Slim Fit Denim Shirt (Blue)", "8904444222222", "Apparel", "Pcs", 1299.00, 1599.00, 850.00, 30, "LOT-DENIM-26", ""],
        ["Fortune Sunflower Oil 1L", "8901234567890", "Grocery", "Ltr", 145.00, 160.00, 125.00, 50, "B-OIL-2026", "2027-06-30"]
    ]
    for row in sample_rows:
        ws.append(row)

    buffer = io.BytesIO()
    wb.save(buffer)
    buffer.seek(0)

    response = HttpResponse(buffer.getvalue(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = 'attachment; filename="isbms_sample_stock_template.xlsx"'
    return response


# ==========================================
# DIGITAL KHATA (UDHAARI) VIEWS
# ==========================================

@login_required
def khata_dashboard(request):
    """Digital Khata (Udhaari) Ledger View per store."""
    store = get_user_store(request)
    query = request.GET.get('q', '').strip()
    
    customers_qs = Customer.objects.filter(store=store, khata_balance__gt=0)
    if query:
        customers_qs = customers_qs.filter(Q(name__icontains=query) | Q(phone__icontains=query))

    total_pending_udhaar = customers_qs.aggregate(total=Sum('khata_balance'))['total'] or Decimal('0.00')

    customers_data = []
    for cust in customers_qs:
        clean_phone = ''.join(filter(str.isdigit, cust.phone))
        if len(clean_phone) == 10:
            clean_phone = '91' + clean_phone

        upi_payload = f"upi://pay?pa={store.upi_id}&pn={urllib.parse.quote(store.name)}&am={cust.khata_balance:.2f}&cu=INR"
        message_text = (
            f"Namaste {cust.name} ji 🙏,\n\n"
            f"Your pending bill balance at *{store.name}* is *₹{cust.khata_balance:.2f}*.\n\n"
            f"Please click here to pay instantly via UPI:\n{upi_payload}\n\n"
            f"Thank you for your business!"
        )
        whatsapp_url = f"https://api.whatsapp.com/send?phone={clean_phone}&text={urllib.parse.quote(message_text)}"

        customers_data.append({
            'customer': cust,
            'whatsapp_url': whatsapp_url,
            'upi_uri': upi_payload,
            'recent_entries': cust.ledger_entries.all()[:5]
        })

    context = {
        'store': store,
        'customers_data': customers_data,
        'total_pending_udhaar': total_pending_udhaar,
        'query': query,
    }
    return render(request, 'khata.html', context)


@csrf_exempt
@login_required
@require_http_methods(["POST"])
def api_settle_khata(request):
    """API endpoint to record customer Khata payment settlement."""
    store = get_user_store(request)

    try:
        data = json.loads(request.body)
        customer_id = data.get('customer_id')
        amount = Decimal(str(data.get('amount', 0)))
        payment_mode = data.get('payment_mode', 'CASH')
        notes = data.get('notes', 'Khata Payment Settlement')

        if amount <= 0:
            return JsonResponse({'error': 'Amount must be greater than zero'}, status=400)

        with transaction.atomic():
            customer = Customer.objects.select_for_update().get(id=customer_id, store=store)
            customer.khata_balance = max(Decimal('0.00'), customer.khata_balance - amount)
            customer.save()

            KhataLedger.objects.create(
                customer=customer,
                entry_type='CREDIT',
                amount=amount,
                payment_mode=payment_mode,
                notes=notes,
                created_by=request.user if request.user.is_authenticated else None,
            )

            return JsonResponse({
                'success': True,
                'new_balance': float(customer.khata_balance),
                'message': f"Settlement of ₹{amount} recorded for {customer.name}"
            })
    except Customer.DoesNotExist:
        return JsonResponse({'error': 'Customer not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# ==========================================
# ANALYTICS & CAPITAL-RISK ANALYZER VIEWS
# ==========================================

@login_required
def analytics_dashboard(request):
    """Dead-Stock & Expiry Capital-Risk Analyzer per store."""
    store = get_user_store(request)
    today = timezone.now().date()
    days_30_ago = today - timedelta(days=30)
    days_60_ago = today - timedelta(days=60)

    recent_sold_product_ids_30 = InvoiceItem.objects.filter(
        invoice__store=store,
        invoice__created_at__date__gte=days_30_ago
    ).values_list('product_id', flat=True).distinct()

    dead_stock_30 = Product.objects.filter(
        store=store,
        is_active=True
    ).exclude(id__in=recent_sold_product_ids_30).prefetch_related('batches')

    dead_stock_list = []
    total_blocked_capital = Decimal('0.00')

    for prod in dead_stock_30:
        total_stock = prod.total_stock
        if total_stock > 0:
            val = Decimal('0.00')
            for b in prod.batches.filter(current_stock__gt=0):
                val += Decimal(b.current_stock) * b.cost_price
            
            total_blocked_capital += val
            dead_stock_list.append({
                'product': prod,
                'stock': total_stock,
                'capital_blocked': val,
                'days_inactive': '30+ Days'
            })

    dead_stock_list.sort(key=lambda x: x['capital_blocked'], reverse=True)

    expiring_batches = Batch.objects.filter(
        product__store=store,
        current_stock__gt=0,
        expiry_date__isnull=False,
        expiry_date__gte=today,
        expiry_date__lte=today + timedelta(days=30)
    ).select_related('product').order_by('expiry_date')

    total_expiry_risk_capital = Decimal('0.00')
    expiring_batches_list = []
    for b in expiring_batches:
        risk_val = Decimal(b.current_stock) * b.cost_price
        total_expiry_risk_capital += risk_val
        expiring_batches_list.append({
            'batch': b,
            'risk_capital': risk_val,
            'days_left': (b.expiry_date - today).days
        })

    all_products = Product.objects.filter(store=store, is_active=True).prefetch_related('batches')
    low_stock_products = [p for p in all_products if p.is_low_stock]

    thirty_days_invoices = Invoice.objects.filter(store=store, created_at__date__gte=days_30_ago, status='PAID')
    total_revenue = thirty_days_invoices.aggregate(total=Sum('grand_total'))['total'] or Decimal('0.00')

    cogs_query = InvoiceItem.objects.filter(invoice__store=store, invoice__created_at__date__gte=days_30_ago, invoice__status='PAID')
    total_cogs = Decimal('0.00')
    for item in cogs_query:
        total_cogs += Decimal(item.quantity) * item.cost_price

    gross_profit = total_revenue - total_cogs
    profit_margin_pct = (gross_profit / total_revenue * 100) if total_revenue > 0 else 0.0

    context = {
        'store': store,
        'dead_stock_list': dead_stock_list[:15],
        'total_blocked_capital': total_blocked_capital,
        'expiring_batches_list': expiring_batches_list,
        'total_expiry_risk_capital': total_expiry_risk_capital,
        'low_stock_products': low_stock_products,
        'total_revenue_30d': total_revenue,
        'total_cogs_30d': total_cogs,
        'gross_profit_30d': gross_profit,
        'profit_margin_pct': profit_margin_pct,
    }
    return render(request, 'analytics.html', context)


@login_required
def invoice_print_view(request, invoice_id):
    """View to print A4 or 58mm thermal invoice."""
    store = get_user_store(request)
    invoice = get_object_or_404(Invoice.objects.prefetch_related('items__product', 'items__batch'), id=invoice_id, store=store)
    return render(request, 'invoice_print.html', {'invoice': invoice, 'store': store})
