from django.core.management.base import BaseCommand
from insurance.models import InsuranceProvider

class Command(BaseCommand):
    help = 'Insert Demo providers into the InsuranceProvider model'

    def handle(self, *args, **kwargs):
        providers = [
            {
                "name": "Demo Provider",
                "interface": "demo",
                "provides_health": True,
                "provides_auto": True,
                "provides_travel": True,
                "is_active": True
            },
        ]

        for provider_data in providers:
            provider, created = InsuranceProvider.objects.get_or_create(
                name=provider_data["name"],
                defaults={
                    "interface": provider_data["interface"],
                    "provides_health": provider_data["provides_health"],
                    "provides_auto": provider_data["provides_auto"],
                    "provides_travel": provider_data["provides_travel"],
                    "is_active": provider_data["is_active"]
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully inserted {provider.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'{provider.name} already exists'))