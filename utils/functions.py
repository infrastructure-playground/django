from google.oauth2 import service_account
from google.cloud import recaptchaenterprise_v1
from rest_framework.response import Response
from django.template.loader import render_to_string
from django.conf import settings


def send_mail(  # pylint: disable=too-many-arguments
    subject,
    body,
    from_email,
    recipient_list,
    fail_silently=False,
    html_message=None,
):
    """
    @brief
        - to replace django send mail which is synchronous and costs time
        in the process
    """
    # to avoid import conflict in model
    from .classes import EmailThread  # pylint: disable=import-outside-toplevel

    EmailThread(
        subject, body, from_email, recipient_list, fail_silently, html_message
    ).start()


def response_with_email(data, status_code, title, email_data, remarks=None):
    """
    title: 'INSUFFICIENT FUNDS'
    email_data: {'username': 'dean', 'balance': 31.0, 'bet': 50}
    """
    msg_html = render_to_string(
        'email-templates/client_request_errors.html',
        {'data': email_data, 'remarks': remarks},
    )
    send_mail(
        title,
        '',
        settings.EMAIL_HOST_USER,
        settings.EMAIL_CLIENT_ERRORS,
        fail_silently=False,
        html_message=msg_html,
    )
    return Response(data=data, status=status_code)


def check_google_recaptcha(token):
    """
    :param token: xxxxxxxxxx
    :return: boolean
    """
    CREDENTIALS = service_account.Credentials.from_service_account_file(
        f'/usr/src/app/recaptcha.json'
    )
    project_id = "resources-practice"
    recaptcha_site_key = "6Ld4Lg0cAAAAAGE1fZWLxmIwucTYfAVLXzV81stl"
    assessment_name = "login_assessment_2"
    client = recaptchaenterprise_v1.RecaptchaEnterpriseServiceClient(
        credentials=CREDENTIALS)
    event = recaptchaenterprise_v1.Event()
    event.site_key = recaptcha_site_key
    event.token = token

    assessment = recaptchaenterprise_v1.Assessment()
    assessment.event = event
    assessment.name = assessment_name
    project_name = f'projects/{project_id}'

    request = recaptchaenterprise_v1.CreateAssessmentRequest()
    request.assessment = assessment
    request.parent = project_name

    response = client.create_assessment(request)
    response.token_properties.valid
