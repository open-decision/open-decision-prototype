from django.db import models
from django.conf import settings
from ckeditor.fields import RichTextField
import bleach

ALLOWED_TAGS = set(bleach.ALLOWED_TAGS + [
    'a',  'abbr', 'blockquote', 'code', 'del', 'dd', 'dl', 'dt',
    'h1', 'h2', 'h3', 'h3', 'h4', 'h5', 'i', 'img', 'kbd',
    'li', 'ol', 'ul', 'p', 'pre', 's', 'span', 'sup', 'sub', 'em',
    'strong', 'strike', 'ul', 'br', 'hr' ])

ALLOWED_STYLES = set(bleach.ALLOWED_STYLES + [
    'color', 'background-color', 'font', 'font-weight',
    'height', 'max-height', 'min-height',
    'width', 'max-width', 'min-width', ])

ALLOWED_ATTRIBUTES = {}
ALLOWED_ATTRIBUTES.update(bleach.ALLOWED_ATTRIBUTES)
ALLOWED_ATTRIBUTES.update({
    '*': ['id', 'class', 'title'],
    'a': ['href', 'rel'],
    'img': ['alt', 'src', 'width', 'height', 'align', 'style'],
})

ALLOWED_TAGS_STRICT = set(bleach.ALLOWED_TAGS + [
    'blockquote', 'code', 'del', 'dd', 'dl', 'dt',
    'h1', 'h2', 'h3', 'h3', 'h4', 'h5', 'i', 'img', 'kbd',
    'li', 'ol', 'ul', 'p', 'pre', 's', 'span', 'sup', 'sub', 'em',
    'strong', 'strike', 'ul', 'br', 'hr' ])

def bleach_clean(html):
    """ Cleans given HTML with bleach.clean() """
    return bleach.clean(
        html,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        styles=ALLOWED_STYLES,
        strip=True
    )

def bleach_clean_strict(html):
    """ Cleans given HTML with bleach.clean() """
    return bleach.clean(
        html,
        tags=['b'],
        strip=True
    )


class RichTextBleachField(RichTextField):
    def __init__(self, *args, **kwargs):
        super(RichTextBleachField, self).__init__(*args, **kwargs)
    def to_python(self, value):
        if not value:
            return ''
        return bleach_clean(value)


class DecisionTree(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    name       = models.CharField(max_length=200)
    owner      = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    slug       = models.SlugField(default="")
    tags       = models.TextField(null=True, blank=True)
    extra_data      = models.TextField(null=True, blank=True)

    class Meta:
        constraints = [
        models.UniqueConstraint(fields= ['owner','slug'], name='unique tree slug per user'),
        ]

class Node(models.Model):
    created_at      = models.DateTimeField(auto_now_add=True)
    name            = models.CharField(max_length=240)
    slug            = models.SlugField(default="")
    decision_tree   = models.ForeignKey(DecisionTree, on_delete=models.CASCADE)
    path            = models.TextField(null=True, blank=True)
    question        = RichTextBleachField()
    inputs          = models.TextField(null=True, blank=True)
    new_node        = models.BooleanField()
    start_node      = models.BooleanField()
    end_node        = models.BooleanField()
    extra_data      = models.TextField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields= ['slug','decision_tree'], name='unique nodeslug per tree')
            ]
