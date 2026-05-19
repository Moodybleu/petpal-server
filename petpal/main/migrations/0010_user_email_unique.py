from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_user_dedupe_emails'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.CharField(max_length=254, unique=True),
        ),
    ]
