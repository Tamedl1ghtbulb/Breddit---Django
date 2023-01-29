from django.contrib.auth.models import AbstractUser
from django.db import models
from vote.models import VoteModel
from django.utils.timezone import now


class User(AbstractUser):
    pass

class Postovi(VoteModel,models.Model):
    title = models.CharField(max_length = 32)
    post1 = models.CharField(max_length = 140)
    userid = models.ForeignKey(User, on_delete=models.CASCADE, related_name="korisnici")
    date = models.DateTimeField()
    likes = models.IntegerField()
    username = models.CharField(max_length = 24)

    def __str__(self):
        return self.title

class Follow4Follow(models.Model):
    kogaprate = models.ForeignKey(User, on_delete=models.CASCADE, related_name="korisnikfo")
    pratioci = models.ForeignKey(User, on_delete=models.CASCADE, related_name="pratioci")

    def is_valid_pratioci(self):
        return self.kogaprate != self.pratioci

class Komentar(VoteModel,models.Model):
    Iid= models.AutoField(primary_key=True)
    comment=models.TextField(max_length=240)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    post=models.ForeignKey(Postovi, on_delete=models.CASCADE)
    parent=models.ForeignKey('self',on_delete=models.CASCADE, null=True )
    timestamp= models.DateTimeField(default=now)

