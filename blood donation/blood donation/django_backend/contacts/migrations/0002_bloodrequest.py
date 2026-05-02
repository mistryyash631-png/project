from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("contacts", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="BloodRequest",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("request_id", models.CharField(max_length=20, unique=True)),
                ("patient_name", models.CharField(max_length=150)),
                ("patient_age", models.PositiveIntegerField(blank=True, null=True)),
                ("hospital", models.CharField(max_length=200)),
                ("ward", models.CharField(blank=True, max_length=150)),
                ("blood_group", models.CharField(max_length=5)),
                ("units_required", models.PositiveIntegerField(default=1)),
                ("required_by_date", models.DateField(blank=True, null=True)),
                ("contact_phone", models.CharField(max_length=30)),
                ("urgency", models.CharField(choices=[("High", "High"), ("Medium", "Medium"), ("Low", "Low")], default="Medium", max_length=10)),
                ("notes", models.TextField(blank=True)),
                ("status", models.CharField(choices=[("Open", "Open"), ("In Progress", "In Progress"), ("Closed", "Closed")], default="Open", max_length=20)),
                ("user_email", models.EmailField(blank=True, max_length=254)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "ordering": ["-id"],
            },
        ),
    ]
