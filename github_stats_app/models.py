from django.db import models


class GitHubStats(models.Model):
    username = models.CharField(max_length=255)
    repos_count = models.IntegerField(default=0)
    followers_count = models.IntegerField(default=0)
    following_count = models.IntegerField(default=0)

    def __str__(self):
        return self.username
