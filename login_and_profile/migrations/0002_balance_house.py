# Generated by Django 2.2 on 2021-06-13 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login_and_profile', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='balance',
            name='house',
            field=models.ManyToManyField(related_name='house_balances', to='login_and_profile.House'),
        ),
    ]