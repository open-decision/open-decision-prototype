import graphene
from graphene import relay
from graphene_django.types import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from dashboard.models import DecisionTree, Node
from pages.models import PublishedTree
from users.models import CustomUser
from django.conf import settings

user = CustomUser.objects.get(email=settings.API_TEST_USER_MAIL)

class DecisionTreeNode(DjangoObjectType):
    class Meta:
        model = DecisionTree
        filter_fields = '__all__'
        interfaces = (relay.Node, )

    @classmethod
    def get_queryset(cls, queryset, info):
        return queryset.filter(owner=user)


class NodeNode(DjangoObjectType):
    class Meta:
        model = Node
        filter_fields = {
            'name': ['exact', 'icontains', 'istartswith'],
            'question': ['exact', 'icontains', 'istartswith'],
            'decision_tree': ['exact'],
            'start_node': ['exact'],
                }
        #fields = ('id', 'question', 'name', 'inputs')
        interfaces = (relay.Node, )

    @classmethod
    def get_queryset(cls, queryset, info):
        return queryset.filter(decision_tree__owner=user)

class UserNode(DjangoObjectType):
    class Meta:
        model = CustomUser
        filter_fields = {
            'email': ['exact'],
                }
        interfaces = (relay.Node, )

class Query(graphene.ObjectType):

    decision_tree = relay.Node.Field(DecisionTreeNode)
    all_decision_trees = DjangoFilterConnectionField(DecisionTreeNode)

    node = relay.Node.Field(NodeNode)
    all_nodes = DjangoFilterConnectionField(NodeNode)

    user = relay.Node.Field(UserNode)
