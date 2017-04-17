# Copyright (c) 2012-2016 Seafile Ltd.
from django.conf import settings

ONLYOFFICE_APIJS_URL = getattr(settings, 'ONLYOFFICE_APIJS_URL', '')
ONLYOFFICE_FILE_EXTENSION = getattr(settings, 'ONLYOFFICE_FILE_EXTENSION', ())
VERIFY_ONLYOFFICE_CERTIFICATE = getattr(settings, 'VERIFY_ONLYOFFICE_CERTIFICATE', True)
