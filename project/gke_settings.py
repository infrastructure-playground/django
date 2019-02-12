import os
import json
from google.oauth2 import service_account

SB_SA_FILE = os.environ.get('STORAGE_BUCKETS_FILE',
                            'storageBucketsBackendServiceKey.json')
STATICFILES_STORAGE = 'utils.classes.GoogleStaticFilesStorage'  # static
DEFAULT_FILE_STORAGE = 'utils.classes.GoogleMediaFilesStorage'  # media
GS_AUTO_CREATE_BUCKET = True
GS_DEFAULT_ACL = 'publicRead'
GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
    f'/usr/src/app/{SB_SA_FILE}'
)
GS_BUCKET_NAME = os.environ.get('GS_BUCKET_NAME')

try:
    import googleclouddebugger
    googleclouddebugger.enable(module='django',
                               version=os.environ.get('ENV', 'master'))
    print('worked debugger on try')
    # Will work upon GKE deployment
except:
    print('cloud debugger execption')
    pass

# with open('/usr/src/app/django_email.json') as data_file:  # required for error notification
#     data = json.load(data_file)
#     EMAIL_HOST = data['EMAIL_HOST']
#     EMAIL_HOST_USER = data['EMAIL_HOST_USER']
#     SERVER_EMAIL = EMAIL_HOST_USER
#     EMAIL_HOST_PASSWORD = data['EMAIL_HOST_PASSWORD']
#     EMAIL_PORT = int(data['EMAIL_PORT'])
#     EMAIL_USE_TLS = True
#     DEFAULT_TO_EMAIL = data['DEFAULT_TO_EMAIL'].split(',')
#     DEFAULT_DEBUG_EMAIL = os.environ.get('DEFAULT_DEBUG_EMAIL',
#                                          'manila@unnotech.com')
#     ADMINS = [('DEFAULT_DEBUG_EMAIL', DEFAULT_DEBUG_EMAIL)]