from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_pet_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='pet',
            name='owner',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='pets',
                to='main.user',
            ),
        ),
    ]
