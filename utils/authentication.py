# from django.contrib.auth.models import User
# from rest_framework import authentication
# from rest_framework import exceptions
# import firebase_admin as admin
# import firebase_admin.auth as auth
#
# # Resource: https://jrizmal.medium.com/how-to-authenticate-firebase-users-in-django-rest-framework-c2d90f5a0a11
# class FirebaseAuthentication(authentication.BaseAuthentication):
#     def authenticate(self, request):
#         print(f"request: {request.META['HTTP_AUTHORIZATION']}")
#         token = request.META.get('HTTP_AUTHORIZATION')
#         if not token:
#             return None
#
#         try:
#             decoded_token = auth.verify_id_token(token)
#             # print(f"decoded_token: {decoded_token}")
#             # e.g. {'iss': 'https://securetoken.google.com/my-diary-app-281215',
#             #       'aud': 'my-diary-app-281215', 'auth_time': 1629807364,
#             #       'user_id': 'v82GOTvXfVXGmcEbBgIn70yiNbq1',
#             #       'sub': 'v82GOTvXfVXGmcEbBgIn70yiNbq1',
#             #       'iat': 1629809530, 'exp': 1629813130,
#             #       'email': 'armadadean@yahoo.com',
#             #       'email_verified': False,
#             #       'firebase': {'identities': {'email': ['armadadean@yahoo.com']},
#             #                    'sign_in_provider': 'password'},
#             #       'uid': 'v82GOTvXfVXGmcEbBgIn70yiNbq1'}
#             uid = decoded_token["uid"]
#             email = decoded_token["email"]
#         except:
#             return None
#
#         try:
#             # Can use trigger in IDP instead with a Cloud Function
#             # Only email and passwords are in IDP
#             user = User.objects.get_or_create(username=uid, email=email)
#             return user
#
#         except exceptions.ObjectDoesNotExist:
#             return None
