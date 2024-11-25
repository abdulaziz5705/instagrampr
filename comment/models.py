from django.db import models

from users.models import UserModel

class TweetModel(models.Model):
    parent = models.ForeignKey( 'self', on_delete=models.CASCADE, null=True, blank=True )
    user = models.ForeignKey( UserModel, on_delete=models.CASCADE, related_name='tweets' )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to = 'tweet/', null=True, blank=True)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Tweet'
        verbose_name_plural = 'Tweets'




class CommentModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE,related_name='comments')
    twit = models.ForeignKey(TweetModel, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()
    parent = models.ForeignKey( 'self', on_delete=models.SET_NULL,  null=True, blank=True, related_name='children' )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'


class PostModelLike(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE,related_name='post_likes')
    tweet = models.ForeignKey(TweetModel, on_delete=models.CASCADE, related_name='postlikes')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.id} liked {self.tweet}"

    class Meta:
        verbose_name = ' post Like'
        verbose_name_plural = ' post Likes'
        unique_together = ('user', 'tweet')


class CommentModelLike(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='comments_likes')
    comment = models.ForeignKey(TweetModel, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.id} liked {self.comment}"

    class Meta:
        verbose_name = ' Comment Like'
        verbose_name_plural = ' Comment Likes'
        unique_together = ('user', 'comment')




