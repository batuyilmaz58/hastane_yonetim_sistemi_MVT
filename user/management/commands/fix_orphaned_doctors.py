from django.core.management.base import BaseCommand
from django.db import transaction
from user.models import CustomUser
from doctor.models import Doctor


class Command(BaseCommand):
    help = 'DOCTOR rolü olup Doctor kaydı olmayan kullanıcıları listeler ve düzeltir'

    def add_arguments(self, parser):
        parser.add_argument(
            '--fix',
            action='store_true',
            help='Otomatik olarak sorunları düzelt (varsayılan olarak sadece listeler)',
        )

    @transaction.atomic
    def handle(self, *args, **options):
        # DOCTOR rolü olup Doctor kaydı olmayan kullanıcıları bul
        doctors_without_record = CustomUser.objects.filter(
            role='DOCTOR'
        ).exclude(
            id__in=Doctor.objects.values_list('user_id', flat=True)
        )

        if not doctors_without_record.exists():
            self.stdout.write(
                self.style.SUCCESS('✓ Tüm doktorların Doctor kaydı mevcut!')
            )
            return

        self.stdout.write(
            self.style.WARNING(
                f'⚠ {doctors_without_record.count()} doktor(u) Doctor kaydı eksik:'
            )
        )

        for user in doctors_without_record:
            self.stdout.write(f'  - {user.username} (ID: {user.id})')

        if options.get('fix'):
            self.stdout.write(
                self.style.WARNING('\n📝 Doctor kaydı eksik kullanıcılar için işlem yapılıyor...')
            )

            # Not: Bu durumda license_number ve specialization eksik olacak
            # Admin paneli aracılığıyla bu bilgileri doldurması gerekecek
            for user in doctors_without_record:
                Doctor.objects.get_or_create(
                    user=user,
                    defaults={
                        'license_number': f'TEMP_{user.id}',  # Temporary placeholder
                        'specialization': 'Tanımlanmamış'
                    }
                )

            self.stdout.write(
                self.style.SUCCESS(
                    f'✓ {doctors_without_record.count()} doktor için geçici Doctor kaydı oluşturuldu.'
                )
            )
            self.stdout.write(
                self.style.WARNING(
                    '\n⚠ DİKKAT: Admin paneline giderek her doktor için lisans numarası ve '
                    'uzmanlık alanını güncelleyin!'
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    '\n💡 Sorunları otomatik olarak düzeltmek için şu komutu çalıştırın:\n'
                    '   python manage.py fix_orphaned_doctors --fix'
                )
            )
