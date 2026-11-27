# Generated manually to match Django schema for Paytm Dynamic QR auto-detection

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0005_storeprofile_razorpay_and_upipaymentsession'),
    ]

    operations = [
        migrations.AddField(
            model_name='storeprofile',
            name='payment_gateway',
            field=models.CharField(choices=[('NONE', 'Manual UPI'), ('PAYTM', 'Paytm for Business'), ('RAZORPAY', 'Razorpay')], default='NONE', max_length=20),
        ),
        migrations.AddField(
            model_name='storeprofile',
            name='paytm_is_staging',
            field=models.BooleanField(default=False, help_text='Use Paytm staging environment for testing'),
        ),
        migrations.AddField(
            model_name='storeprofile',
            name='paytm_merchant_key',
            field=models.CharField(blank=True, default='', help_text='Paytm Merchant Key', max_length=120),
        ),
        migrations.AddField(
            model_name='storeprofile',
            name='paytm_mid',
            field=models.CharField(blank=True, default='', help_text='Paytm Merchant ID (MID)', max_length=100),
        ),
        migrations.AddField(
            model_name='upipaymentsession',
            name='gateway',
            field=models.CharField(default='PAYTM', max_length=20),
        ),
        migrations.AddField(
            model_name='upipaymentsession',
            name='order_id',
            field=models.CharField(blank=True, db_index=True, default='', max_length=100),
        ),
    ]
