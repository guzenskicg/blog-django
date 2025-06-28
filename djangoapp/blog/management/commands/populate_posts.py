# blog/management/commands/populate_posts.py
import random
from pathlib import Path
from io import BytesIO

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.files.base import ContentFile
from django.core.files import File

from faker import Faker
from PIL import Image   # Pillow

from blog.models import Category, Tag, Post

fake = Faker('pt_BR')
User = get_user_model()

# ──────────────────────────────────────────────────────────────────────────────
# Caminho para a imagem de exemplo
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent  # djangoapp/
SAMPLE_COVER = PROJECT_ROOT / 'sample_data' / 'cover.jpg'
# ──────────────────────────────────────────────────────────────────────────────


def get_dummy_image():
    """
    Retorna um objeto ContentFile pronto para atribuir ao ImageField.

    1. Se sample_data/cover.jpg existir, usa essa imagem.
    2. Caso contrário, gera uma PNG 1×1 px em branco (fallback).
    """
    if SAMPLE_COVER.exists():
        data = SAMPLE_COVER.read_bytes()          # lê para a memória
        return ContentFile(data, name=SAMPLE_COVER.name)

    # fallback: gera imagem minúscula em branco
    buffer = BytesIO()
    Image.new("RGB", (1, 1), (255, 255, 255)).save(buffer, format="PNG")
    return ContentFile(buffer.getvalue(), name="placeholder.png")


class Command(BaseCommand):
    help = "Popula o banco com Posts, Categorias, Tags e um usuário autor."

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=10,
            help='Quantidade de posts a criar (padrão: 10)',
        )

    def handle(self, *args, **options):
        total = options['count']

        # ── Autor de demonstração ────────────────────────────────────────────
        author, _ = User.objects.get_or_create(
            username='autor_demo',
            defaults={'email': 'autor@example.com', 'is_staff': True},
        )
        author.set_unusable_password()
        author.save()

        # ── Categorias e tags ───────────────────────────────────────────────
        categories = [
            Category.objects.get_or_create(name=nome)[0]
            for nome in ('Notícias', 'Tutorial', 'Opinião', 'Release')
        ]
        tags = [
            Tag.objects.get_or_create(name=nome)[0]
            for nome in ('python', 'django', 'web', 'dev', 'tips')
        ]

        # ── Criação dos posts ───────────────────────────────────────────────
        created = 0
        for _ in range(total):
            title = fake.sentence(nb_words=6)

            post = Post.objects.create(
                title=title,
                excerpt=fake.text(max_nb_chars=100),
                content=fake.paragraph(nb_sentences=15),
                is_published=fake.boolean(chance_of_getting_true=80),
                cover=get_dummy_image(),
                cover_in_post_content=fake.boolean(),
                created_by=author,
                updated_by=author,
                category=random.choice(categories),
                created_at=timezone.now(),
                updated_at=timezone.now(),
            )

            # adiciona de 1 a 3 tags aleatórias
            post.tags.add(*random.sample(tags, k=random.randint(1, 3)))
            created += 1

        self.stdout.write(self.style.SUCCESS(f'{created} posts criados com sucesso.'))
