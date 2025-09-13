from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot', '0003_alter_chat_topics'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='topics',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
