from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse
# Create your models here.

class Post(models.Model):
    # Posts can be created only by admin users
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    # No upper bound set for text areas
    text = models.TextField()
    # set the current time as the default value
    create_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def approve_comments(self):
        return self.comments.filter(approved_comment=True)

    # after creating the post, return to detail_view of that post
    # Django will look for get_abolute_url method where to back,
    # using reverse method, we can redirect to detail_view
    def get_absolute_url(self):
        return reverse("post_detail", kwargs={'pk':self.pk})

    def __str__(self):
        return self.title


class Comment(models.Model):
    # each comment is associated with particular post
    post = models.ForeignKey('blog.Post', related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    create_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    # after creating the comment, return to list_view of post
    def get_absolute_url(self):
        return reverse('post_list')

    def __str__(self):
        return self.text
