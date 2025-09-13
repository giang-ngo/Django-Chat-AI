from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='topics',
            field=models.JSONField(default=list),
        ),
        migrations.AlterField(
            model_name='chat',
            name='response',
            field=models.TextField(blank=True, null=True),
        ),
    ]
