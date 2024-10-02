from django.db import models
from django.utils.text import slugify
from PIL import Image as PILImage
from io import BytesIO
from django.core.files.base import ContentFile
import uuid


def unique_image_filename(instance, filename):
    ext = filename.split('.')[-1]
    unique_id = uuid.uuid4()
    return f'media/{slugify(instance.title)}_{unique_id}.{ext}'


class Post(models.Model):
    title = models.CharField(
        max_length=256,
        verbose_name='Lavha'
    )
    text = models.TextField(verbose_name='Tekst')
    image = models.ImageField(
        verbose_name='Rasm',
        upload_to=unique_image_filename,
        null=True,
        blank=True
    )
    pub_date = models.DateTimeField(
        verbose_name='E\'lon qilish sanasi va vaqti',
        help_text=(
            'Agar kelajakda sanani va vaqtni o‘rnatmoqchi bo‘lsangiz — '
            'kechiktirilgan e\'lonlar qilish mumkin.'
        )
    )
    views = models.PositiveIntegerField(default=0, verbose_name='Ko‘rishlar')

    class Meta:
        verbose_name = 'e\'lon'
        verbose_name_plural = 'e\'lonlar'
        ordering = ('-pub_date',)

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if self.pk:
            orig = Post.objects.get(pk=self.pk)
            if orig.image != self.image:
                self._process_image()
        else:
            self._process_image()
        super().save(*args, **kwargs)

    def _process_image(self):
        if self.image:
            img = PILImage.open(self.image)
            img_io = BytesIO()
            img.save(img_io, format='WEBP', quality=50)
            img_file = ContentFile(img_io.getvalue(), name=f'{self.title}.webp')
            self.image.save(f'{self.title}.webp', img_file, save=False)
