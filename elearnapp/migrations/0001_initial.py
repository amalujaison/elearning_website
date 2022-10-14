# Generated by Django 4.1.1 on 2022-09-19 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='tbl_reguser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=20)),
                ('user_email', models.EmailField(max_length=20)),
                ('user_pswd', models.TextField(max_length=20)),
                ('user_phnNo', models.IntegerField(max_length=10)),
                ('user_address', models.CharField(max_length=100)),
                ('user_state', models.CharField(max_length=20)),
                ('user_country', models.CharField(max_length=20)),
                ('user_pincode', models.IntegerField(max_length=10)),
            ],
        ),
    ]