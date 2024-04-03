# Session model stores the session data
from django.contrib.sessions.models import Session
from django.core.exceptions import ObjectDoesNotExist

from django.contrib import messages
from django.shortcuts import redirect
from django.urls import resolve

from password_expire.util import PasswordChecker


class OneSessionPerUserMiddleware:
    # Called only once when the web server starts
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        if request.user.is_authenticated:
            stored_session_key = request.user.logged_in_user.session_key

            # if there is a stored_session_key  in our database, and it is
            # different from the current session, delete the stored_session_key
            # session_key with from the Session table
            if stored_session_key and stored_session_key != request.session.session_key:
                try:
                    Session.objects.get(session_key=stored_session_key).delete()
                except ObjectDoesNotExist:
                    pass

            request.user.logged_in_user.session_key = request.session.session_key
            request.user.logged_in_user.save()

        response = self.get_response(request)

        # This is where you add any extra code to be executed for each request/response after
        # the view is called.
        # For this tutorial, we're not adding any code, so we just return the response

        return response

class PasswordExpireMiddleware:
    """
    Adds Django message if password expires soon.
    Checks if user should be redirected to change password.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if self.is_page_for_warning(request):
            # add warning if within the notification window for password expiration
            if request.user.is_authenticated:
                checker = PasswordChecker(request.user)
                if checker.is_expired():
                    msg = f'Please change your password. It has expired.'
                    self.add_warning(request, msg)
                else:
                    time_to_expire_string = checker.get_expire_time()
                    if time_to_expire_string:
                        msg = f'Please change your password. It expires in {time_to_expire_string}.'
                        self.add_warning(request, msg)

        response = self.get_response(request)

        # picks up flag for forcing password change
        if getattr(request, 'redirect_to_password_change', False):
            return redirect('app_index:usuario:password_change')

        return response

    def is_page_for_warning(self, request):
        """
        Only warn on pages that are GET requests and not ajax. Also ignore logouts.
        """
        if request.method == "GET" and not request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            match = resolve(request.path)
            if match and match.url_name == 'logout':
                return False
            return True
        return False

    def add_warning(self, request, text):
        storage = messages.get_messages(request)
        for message in storage:
            # only add this message once
            if message.extra_tags is not None and 'password_expire' in message.extra_tags:
                return
        messages.warning(request, text, extra_tags='password_expire')
