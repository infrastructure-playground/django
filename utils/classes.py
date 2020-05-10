import threading
import os

from django.conf import settings
from django.core.mail import EmailMultiAlternatives

from storages.backends.gcloud import GoogleCloudStorage

from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg.openapi import ReferenceResolver
from drf_yasg.utils import get_consumes, get_produces
from drf_yasg import openapi

from rest_framework.settings import api_settings


class EmailThread(threading.Thread):
    """
    @brief      Avoids the usual delay on the backend when sending an e-mail
    """
    def __init__(self, subject, body, from_email, recipient_list,
                 fail_silently, html_message):
        self.subject = subject
        self.body = body
        self.recipient_list = recipient_list
        self.from_email = from_email
        self.fail_silently = fail_silently
        self.html_message = html_message
        threading.Thread.__init__(self)

    def run(self):
        msg = EmailMultiAlternatives(self.subject, self.body, self.from_email,
                                     self.recipient_list)
        if self.html_message:
            msg.attach_alternative(self.html_message, "text/html")
        msg.send(self.fail_silently)


class GoogleMediaFilesStorage(GoogleCloudStorage):

    def _save(self, name, content):
        name = f'{settings.MEDIA_URL[1:]}{name}'
        return super()._save(name, content)

    def url(self, name):
        """
        @brief      for implementation of CDN using image field url
        @return     Dynamic return of CDN or local URL
        """
        if settings.CDN_HOSTNAME:
            url = f'{settings.CDN_HOSTNAME}/{name}'
            return url
        return super().url(name)


class GoogleStaticFilesStorage(GoogleCloudStorage):
    def url(self, name):
        name = f'static/{name}'
        return super().url(name)


class GoogleEndpointSchemaGenerator(OpenAPISchemaGenerator):
    """
    Custom generator for compatibility w/ Google Cloud Endpoints format.
    Preferably CORS
    """
    def get_schema(self, request=None, public=False):
        """
        allow CORS in Google Cloud Endpoint
        """
        endpoints = self.get_endpoints(request)
        components = ReferenceResolver(openapi.SCHEMA_DEFINITIONS)
        extra = dict(components)
        extra['x-google-endpoints'] = [
            {'name': f"\"{os.environ.get('OPENAPI_HOST')}\"", 'allowCors': True}
        ]
        extra['x-google-allow'] = 'all'
        self.consumes = get_consumes(api_settings.DEFAULT_PARSER_CLASSES)
        self.produces = get_produces(api_settings.DEFAULT_RENDERER_CLASSES)
        paths, prefix = self.get_paths(endpoints, components, request, public)

        security_definitions = self.get_security_definitions()
        if security_definitions:
            security_requirements = self.get_security_requirements(
                security_definitions)
        else:
            security_requirements = None

        url = self.url
        if url is None and request is not None:
            url = request.build_absolute_uri()

        return openapi.Swagger(
            info=self.info, paths=paths, consumes=self.consumes or None,
            produces=self.produces or None,
            security_definitions=security_definitions,
            security=security_requirements,
            _url=url, _prefix=prefix, _version=self.version, **extra,
        )
