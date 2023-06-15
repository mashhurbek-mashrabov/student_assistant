from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        abstract = True
        ordering = ('-created_at',)

    @property
    def created(self):
        return f'{self.created_at.strftime("%X")} {self.created_at.strftime("%x")}'

    @property
    def updated(self):
        return f'{self.updated_at.strftime("%X")} {self.updated_at.strftime("%x")}'
