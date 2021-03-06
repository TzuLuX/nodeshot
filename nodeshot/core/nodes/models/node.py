from django.contrib.gis.db import models
from django.contrib.gis.geos.collections import GeometryCollection
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.core.exceptions import ValidationError

from nodeshot.core.base.models import BaseAccessLevel, BaseOrdered
from nodeshot.core.base.utils import choicify

from ..signals import node_status_changed
from .status import Status

HSTORE_ENABLED = settings.NODESHOT['SETTINGS'].get('HSTORE', True)

if HSTORE_ENABLED:
    from django_hstore.fields import DictionaryField
    from nodeshot.core.base.managers import HStoreGeoAccessLevelPublishedManager as NodeManager
else:
    from nodeshot.core.base.managers import GeoAccessLevelPublishedManager as NodeManager


class Node(BaseAccessLevel):
    """
    Nodes are generic geo-referenced records
    Can be assigned to 'Layers' if nodeshot.core.layers is installed
    Can belong to 'Users'
    """
    name = models.CharField(_('name'), max_length=75, unique=True)
    slug = models.SlugField(max_length=75, db_index=True, unique=True)
    address = models.CharField(_('address'), max_length=150, blank=True, null=True)
    status = models.ForeignKey(Status, blank=True, null=True)
    is_published = models.BooleanField(default=settings.NODESHOT['DEFAULTS'].get('NODE_PUBLISHED', True))
    
    if 'nodeshot.core.layers' in settings.INSTALLED_APPS:
        # layer might need to be able to be blank, would require custom validation
        layer = models.ForeignKey('layers.Layer')
    
    # nodes might be assigned to a foreign layer, therefore user can be left blank, requires custom validation
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
    
    # positioning
    geometry = models.GeometryField(_('geometry'), help_text=_('geometry of the node (point, polygon, line)'))
    elev = models.FloatField(_('elevation'), blank=True, null=True)
    
    description = models.TextField(_('description'), max_length=255, blank=True, null=True)
    notes = models.TextField(_('notes'), blank=True, null=True, help_text=_('for internal use only'))
    
    if HSTORE_ENABLED:
        data = DictionaryField(_('extra data'), null=True, blank=True,
                            help_text=_('store extra attributes in JSON string'))
    
    # manager
    objects = NodeManager()
    
    # this is needed to check if the status is changing
    # explained here:
    # http://stackoverflow.com/questions/1355150/django-when-saving-how-can-you-check-if-a-field-has-changed
    _current_status = None
    
    # needed for extensible validation
    _additional_validation = []
    
    class Meta:
        db_table = 'nodes_node'
        app_label= 'nodes'
        permissions = (('can_view_nodes', 'Can view nodes'),)
    
    def __unicode__(self):
        return '%s' % self.name
    
    def __init__(self, *args, **kwargs):
        """ Fill __current_status """
        super(Node, self).__init__(*args, **kwargs)
        # set current status, but only if it is an existing node
        if self.pk:
            self._current_status = self.status_id
    
    def clean(self , *args, **kwargs):
        """ call extensible validation """
        self.extensible_validation()
    
    def save(self, *args, **kwargs):
        """
        Custom save method does the following things:
            * converts geometry collections of just 1 item to that item (eg: a collection of 1 Point becomes a Point)
            * intercepts changes to status and fires node_status_changed signal
            * set default status
        """
        # geometry collection check
        if isinstance(self.geometry, GeometryCollection) and 0 < len(self.geometry) < 2:
            self.geometry = self.geometry[0]
        
        # if no status specified
        if not self.status and not self.status_id:
            try:
                self.status = Status.objects.filter(is_default=True)[0]
            except IndexError:
                pass
        
        super(Node, self).save(*args, **kwargs)
        
        # if status of a node changes
        if (self.status and self._current_status and self.status.id != self._current_status) or (
            self.status_id and self._current_status and self.status_id != self._current_status
        ):
            # send django signal
            node_status_changed.send(sender=self.__class__, instance=self, old_status=Status.objects.get(pk=self._current_status), new_status=self.status)
        # update _current_status
        self._current_status = self.status_id
    
    def extensible_validation(self):
        """
        Execute additional validation that might be defined elsewhere in the code.
        Additional validation is introduced through the class method Node.add_validation_method()
        """
        # loop over additional validation method list
        for validation_method in self._additional_validation:
            # call each additional validation method
            getattr(self, validation_method)()
    
    @classmethod
    def add_validation_method(class_, method):
        """
        Extend validation of Node by adding a function to the _additional_validation list.
        The additional validation function will be called by the clean method
        
        :method function: function to be added to _additional_validation
        """
        method_name = method.func_name
        
        # add method name to additional validation method list
        class_._additional_validation.append(method_name)
        
        # add method to this class
        setattr(class_, method_name, method)
    
    @property
    def owner(self):
        return self.user
    
    @property
    def point(self):
        """ returns location of node. If node geometry is not a point a centroid point will be returned """
        if not self.geometry:
            raise ValueError('geometry attribute must be set before trying to get point property')
        if self.geometry.geom_type == 'Point':
            return self.geometry
        else:
            # centroid is the aproximative center of a geometry
            return self.geometry.centroid
    
    if 'grappelli' in settings.INSTALLED_APPS:
        @staticmethod
        def autocomplete_search_fields():
            return ('name__icontains', 'slug__icontains', 'address__icontains')
    
    # some more properties are added by the layer app
    #  * intersecting_layers