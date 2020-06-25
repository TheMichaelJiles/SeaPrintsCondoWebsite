from django.contrib import admin
from django.contrib.auth.models import User, Group

from home.models import Globals

admin.site.unregister(User)
admin.site.unregister(Group)

admin.site.register(Globals)

# More site options can be set here.

admin.site.site_header = 'PUT TITLE HERE'
admin.site.site_title = 'PUT SITE TAB TITLE HERE'

admin.site.index_title = 'Data Management'