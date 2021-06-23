from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("cars", "0002_auto_20210623_0009"),
    ]

    operations = [
        migrations.RenameField(
            model_name="rate",
            old_name="rate",
            new_name="rating",
        ),
    ]
