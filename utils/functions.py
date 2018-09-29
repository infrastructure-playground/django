from rest_framework.response import Response
from django.template.loader import render_to_string
from django.conf import settings


def send_mail(subject, body, from_email, recipient_list, fail_silently=False,
              html_message=None, *args, **kwargs):
    '''
    @brief
        - to replace django send mail which is synchronous and costs time
        in the process
    '''

    from . classes import EmailThread  # to avoid import conflict in model
    EmailThread(subject, body, from_email, recipient_list, fail_silently,
                html_message).start()


def response_with_email(data, status_code, title, email_data, remarks=None):
    """
    title: 'INSUFFICIENT FUNDS'
    email_data: {'username': 'dean', 'balance': 31.0, 'bet': 50}
    """
    print('===EMAIL DATA===')
    print(email_data)
    msg_html = render_to_string(
        'email-templates/client_request_errors.html',
        {'data': email_data, 'remarks': remarks})
    send_mail(title, '',
              settings.EMAIL_HOST_USER,
              settings.EMAIL_CLIENT_ERRORS,
              fail_silently=False, html_message=msg_html)
    return Response(data=data, status=status_code)
