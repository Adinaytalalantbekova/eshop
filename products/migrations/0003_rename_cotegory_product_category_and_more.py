# Generated by Django 4.0.2 on 2022-02-18 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_category_review_product_cotegory'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='cotegory',
            new_name='category',
        ),
        migrations.RemoveField(
            model_name='product',
            name='update_at',
        ),
        migrations.AddField(
            model_name='product',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]