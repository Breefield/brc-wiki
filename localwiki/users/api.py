from django.contrib.auth.models import User, Group

from rest_framework import viewsets
from rest_framework_filters import filters, FilterSet

from main.api import router

from .serializers import UserSerializer

DATETIME_INPUT_FORMATS = (
    '%Y-%m-%dT%H:%M:%S.%f',
)

class UserFilter(FilterSet):
    date_joined = filters.AllLookupsFilter(name='date_joined')
    username = filters.AllLookupsFilter(name='username')

    class Meta:
        model = User
        fields = ('date_joined', 'username', 'first_name', 'last_name')


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed.

    Filter fields
    -------------

    You can filter the result set by providing the following query parameters:

      * `username` -- Filter by username. Supports the [standard lookup types](../../api_docs/filters)
      * `first_name` -- Filter by first name, exact match.
      * `last_name` -- Filter by last name, exact match.
      * `date_joined` -- Filter by date joined. Supports the [standard lookup types](../../api_docs/filters).
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_class = UserFilter


router.register(r'users', UserViewSet)