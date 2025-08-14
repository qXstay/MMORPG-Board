from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.conf import settings

class Category(models.Model):
    name = models.CharField(_("Category Name"), max_length=100, unique=True)
    subscribers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='subscribed_categories',
        blank=True
    )

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.name


class Post(models.Model):
    CATEGORY_CHOICES = [
        ('tanks', _('Tanks')),
        ('healers', _('Healers')),
        ('dd', _('Damage Dealers')),
        ('merchants', _('Merchants')),
        ('guildmasters', _('Guild Masters')),
        ('questgivers', _('Quest Givers')),
        ('blacksmiths', _('Blacksmiths')),
        ('tanners', _('Tanners')),
        ('potionmakers', _('Potion Makers')),
        ('spellmasters', _('Spell Masters')),
    ]

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    title = models.CharField(_("Title"), max_length=200)
    content = models.TextField(_("Content"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    def get_responses_count(self):
        return self.responses.count()

    class Meta:
        ordering = ['-created_at']


class Response(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='responses')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    text = models.TextField(_("Response Text"))
    created_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"Response to {self.post.title} by {self.author.email}"
