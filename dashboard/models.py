from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
import bleach

ALLOWED_TAGS = set(bleach.ALLOWED_TAGS + [
    'a', 'blockquote', 'code', 'del', 'dd', 'dl', 'dt',
    'h1', 'h2', 'h3', 'h3', 'h4', 'h5', 'i', 'img', 'kbd',
    'li', 'ol', 'ul', 'p', 'pre', 's', 'sup', 'sub', 'em',
    'strong', 'strike', 'ul', 'br', 'hr' ])

ALLOWED_STYLES = set(bleach.ALLOWED_STYLES + [
    'color', 'background-color', 'font', 'font-weight',
    'height', 'max-height', 'min-height',
    'width', 'max-width', 'min-width', ])

ALLOWED_ATTRIBUTES = {}
ALLOWED_ATTRIBUTES.update(bleach.ALLOWED_ATTRIBUTES)
ALLOWED_ATTRIBUTES.update({
    '*': ['class', 'title'],
    'a': ['href', 'rel'],
    'img': ['alt', 'src', 'width', 'height', 'align', 'style'],
})


def bleach_clean(html):
    """ Cleans given HTML with bleach.clean() """
    return bleach.clean(
        html,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        styles=ALLOWED_STYLES,
        strip=True
    )

class RichTextBleachField(RichTextField):
    def __init__(self, *args, **kwargs):
        super(RichTextBleachField, self).__init__(*args, **kwargs)
    def to_python(self, value):
        return bleach_clean(value)


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
    question        = RichTextBleachField()
    input_type      = models.CharField(max_length=240)
    data_answer     = models.TextField(null=True, blank=True)
    data_logic      = models.TextField(null=True, blank=True)
    new_node        = models.BooleanField()
    start_node      = models.BooleanField()
    end_node        = models.BooleanField()
