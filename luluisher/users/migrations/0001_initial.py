# Generated by Django 4.0.4 on 2022-05-27 06:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100, unique=True)),
                ('password', models.CharField(max_length=100)),
                ('mobile_number', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=100)),
                ('email_subscribe', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'users',
            },
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('image_url', models.URLField(max_length=1000)),
                ('quantity', models.IntegerField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user')),
            ],
            options={
                'db_table': 'carts',
            },
        ),
        migrations.AddConstraint(
            model_name='cart',
            constraint=models.UniqueConstraint(fields=('user', 'product'), name='name of constraint'),
        ),
    ]
