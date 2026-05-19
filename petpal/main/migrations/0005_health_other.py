from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_diary_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='health',
            name='other',
            field=models.TextField(blank=True),
        ),
    ]
