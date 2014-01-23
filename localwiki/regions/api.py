from django.conf import settings

from rest_framework import viewsets
from rest_framework_filters import filters, FilterSet
from rest_framework_gis.filters import GeoFilterSet

from main.api import router

from .models import Region, RegionSettings
from .serializers import RegionSerializer


class RegionSettingsFilter(GeoFilterSet, FilterSet):
    region_center = filters.AllLookupsFilter(name='region_center')

    class Meta:
        model = RegionSettings
        fields = ('default_language',)


class RegionFilter(GeoFilterSet, FilterSet):
    slug = filters.AllLookupsFilter(name='slug')
    geom = filters.AllLookupsFilter(name='geom')
    settings = filters.RelatedFilter(RegionSettingsFilter, name='regionsettings')

    class Meta:
        model = Region
        fields = ('slug',)


allowed_languages = ''
for l in settings.LANGUAGES[:-1]:
    allowed_languages += '`%s`, ' % l[0]
allowed_languages += '`%s`' % settings.LANGUAGES[-1][0]


class RegionViewSet(viewsets.ReadOnlyModelViewSet):
    __doc__ = """
    API endpoint that allows regions to be viewed.

    Filter fields
    -------------

    You can filter the result set by providing the following query parameters:

      * `slug` -- Filter by region slug. Supports the [standard lookup types](../../api_docs/filters)
      * `geom` -- Filter by the region's geography.  Supports the [standard geographic lookup types](../../api_docs/geo_filters)
      * `settings`
        * `settings__default_language` -- Filter by the region's default language.  Accepts one of %(allowed_languages)s.
        * `settings__region_center` -- Filter by the region's center geography.  Supports the [standard geographic lookup types](../../api_docs/geo_filters)
    """ % {'allowed_languages': allowed_languages}

    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    filter_class = RegionFilter


router.register(u'regions', RegionViewSet)
