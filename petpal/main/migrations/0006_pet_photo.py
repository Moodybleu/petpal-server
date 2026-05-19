from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_health_other'),
    ]

    operations = [
        migrations.AddField(
            model_name='pet',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='pets/'),
        ),
    ]
