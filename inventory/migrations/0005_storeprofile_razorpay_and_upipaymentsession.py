# Generated manually to match Django schema for Razorpay auto-detection

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0004_storeprofile_store_type_alter_batch_cost_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='storeprofile',
            name='razorpay_key_id',
            field=models.CharField(blank=True, default='', help_text='Razorpay Key ID for automatic UPI QR detection', max_length=120),
        ),
        migrations.AddField(
            model_name='storeprofile',
            name='razorpay_key_secret',
            field=models.CharField(blank=True, default='', help_text='Razorpay Key Secret for automatic UPI QR detection', max_length=120),
        ),
        migrations.CreateModel(
            name='UpiPaymentSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qr_id', models.CharField(db_index=True, max_length=100, unique=True)),
                ('client_invoice_id', models.CharField(blank=True, db_index=True, default='', max_length=100)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.CharField(choices=[('PENDING', 'Pending Payment'), ('PAID', 'Paid'), ('EXPIRED', 'Expired / Closed')], default='PENDING', max_length=20)),
                ('razorpay_payment_id', models.CharField(blank=True, default='', max_length=100)),
                ('customer_vpa', models.CharField(blank=True, default='', max_length=120)),
                ('image_url', models.URLField(blank=True, default='', max_length=500)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('paid_at', models.DateTimeField(blank=True, null=True)),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='upi_sessions', to='inventory.storeprofile')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
