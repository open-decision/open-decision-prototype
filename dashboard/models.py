from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User

class DecisionTree(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    name       = models.CharField(max_length=200)
    owner      = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    slug       = models.SlugField(unique=True, default="")

class Node(models.Model):
    created_at      = models.DateTimeField(auto_now_add=True)
    name            = models.CharField(max_length=240)
    slug            = models.SlugField(unique=True, default="")
    decision_tree   = models.ForeignKey(DecisionTree, on_delete=models.CASCADE)
    question        = models.CharField(max_length=240)
    input_type      = models.CharField(max_length=240)
    data_answer     = models.TextField(null=True, blank=True)
    data_logic      = models.TextField(null=True, blank=True)
    new_node        = models.BooleanField()
    start_node      = models.BooleanField()
