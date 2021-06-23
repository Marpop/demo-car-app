from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cars", "0003_auto_20210623_1457"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="car",
            name="unique name",
        ),
        migrations.RenameField(
            model_name="car",
            old_name="maker",
            new_name="make",
        ),
        migrations.AddConstraint(
            model_name="car",
            constraint=models.UniqueConstraint(
                fields=("make", "model"), name="unique name"
            ),
        ),
    ]
