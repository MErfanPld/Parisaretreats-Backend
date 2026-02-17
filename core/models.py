from django.db import models

# Create your models here.


class Slider(models.Model):
    title = models.CharField(max_length=100, verbose_name="عنوان اسلایدر")
    description = models.TextField(blank=True, verbose_name="توضیحات")
    image = models.ImageField(upload_to="sliders/", verbose_name="تصویر")
    link = models.URLField(blank=True, null=True, verbose_name="لینک")
    is_active = models.BooleanField(default=True, verbose_name="فعال؟")
    order = models.PositiveIntegerField(default=0, verbose_name="ترتیب")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']
        verbose_name = "اسلایدر"
        verbose_name_plural = "اسلایدر ها"

    def __str__(self):
        return self.title
