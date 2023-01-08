# Generated by Django 4.1.3 on 2022-12-28 04:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_coupan_coupan_applied_category_offer'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product_offer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date_and_time', models.DateField()),
                ('end_date_and_time', models.DateField()),
                ('discount_amount', models.CharField(blank=True, max_length=5)),
                ('discount_percentage', models.CharField(blank=True, max_length=5)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product')),
            ],
        ),
    ]
