from django.db import models


# * ArticleSwint
class Temperature(models.Model):
    """Model for Articles."""

    time = models.DateTimeField(verbose_name=u"时间", auto_now_add=True)
    value = models.TextField(verbose_name=u"温度")

    class Meta():
        ordering = [
            'time',
        ]

    def __unicode__(self):
        return self.title

    __str__ = __unicode__


# Create your models here.
