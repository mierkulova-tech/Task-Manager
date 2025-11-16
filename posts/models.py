from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=75)
    body = models.TextField()
    slug = models.SlugField()
    date = models.DateTimeField(auto_now_add=True)
    banner = models.ImageField(default='fallback.jpg', blank=True)

    def __str__(self):
        return self.title

    def get_banner_url(self):
        if self.banner and hasattr(self.banner, 'url'):
            return self.banner.url
        return f"/media/{self.banner.name}"

