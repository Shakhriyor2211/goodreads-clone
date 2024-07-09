import itertools

from django.utils.text import slugify


def generate_unique_slug(model_instance, title, slug_field_name="slug"):
    slug = slugify(title)
    model_class = model_instance.__class__

    if not model_class.objects.filter(**{slug_field_name: slug}).exists():
        return slug

    for i in itertools.count(1):
        unique_slug = f"{slug}-{i}"
        if not model_class.objects.filter(**{slug_field_name:unique_slug}).exists():
            return unique_slug
