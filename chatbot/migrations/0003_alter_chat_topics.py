from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot', '0002_chat_topics_alter_chat_response'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='topics',
            field=models.JSONField(blank=True, default=list),
        ),
    ]
