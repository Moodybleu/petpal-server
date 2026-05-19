from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_pet_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=128),
        ),
    ]
