from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Playlist(models.Model):
    url = models.URLField(_("youtube playlist"), max_length=200)