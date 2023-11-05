from django.db import models
import uuid
from users.models import Profile

# Create your models here.

class Project(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True,blank=True)
    featured_image = models.ImageField(null=True, blank=True, default="default.jpg")
    demo_link= models.CharField(max_length=255,null=True,blank=True)
    source_link = models.CharField(max_length=255, null=True, blank=True)
    tags = models.ManyToManyField('tags',blank=True)
    vote_total = models.IntegerField(default=0,null=True, blank=True)
    vote_ratio = models.IntegerField(default=0,null=True, blank=True)
    created = models.DateField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4,unique=True, primary_key=True,editable=False)


    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-vote_ratio', '-vote_total','title']  # [-created] - will use as New first

    @property
    def imageURL(self):
        try:
            url = self.featured_image.url
        except:
            url = ""
        return url

    @property
    def reviewers(self):
        queryset = self.review_set.all().values_list('owner__id', flat=True)
        return queryset

    @property
    def getVoteCount(self):
        reviews = self.review_set.all()
        upVotes = reviews.filter(value='up').count()
        totalVotes = reviews.count()

        ratio = (upVotes/totalVotes) * 100
        self.vote_total = totalVotes
        self.vote_ratio = ratio

        self.save()

class Review(models.Model):
    VOTE_TYPE = (('up','Up Vote'),('down','Down Vote'))

    owner = models.ForeignKey(Profile,on_delete=models.CASCADE, null=True, blank=True)
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    body=models.TextField()
    value=models.CharField(max_length=255, choices=VOTE_TYPE)
    created=models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4,primary_key=True,editable=True,unique=True)

    class Meta:
        unique_together = [['owner','project']]
        
    def __str__(self):
        return self.value
    


class Tags(models.Model):
    name = models.CharField(max_length=200)
    created= models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4,unique=True,editable=False,primary_key=True)

    def __str__(self):
        return self.name




