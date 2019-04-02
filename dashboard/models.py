from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User

class DecisionTree(models.Model):
     name       = models.CharField(max_length=200)
     owner      = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
     slug       = models.SlugField(unique=True, default="")

class Node(models.Model):
    decision_tree   = models.ForeignKey(DecisionTree, on_delete=models.CASCADE)
    name            = models.CharField(max_length=120)
    data            = JSONField(null=True, blank=True)
    slug         = models.SlugField(unique=True, default="")

#    id              = False
#    var             = False
