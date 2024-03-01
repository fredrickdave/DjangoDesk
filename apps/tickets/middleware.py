import zoneinfo

from django.utils import timezone


class TimezoneMiddleware:
    """
    Middleware for activating the request.user's chosen time zone if it exists in the database. Otherwise, it
    captures the user's timezone from the browser cookie.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        try:
            # Get user-defined time zone. Returns ZoneInfo object
            tzname = request.user.timezone

            if tzname:
                # https://docs.python.org/3/library/zoneinfo.html#string-representations
                timezone.activate(zoneinfo.ZoneInfo(str(tzname)))
            else:
                tzname = request.COOKIES.get("django_timezone")
                if tzname:
                    timezone.activate(zoneinfo.ZoneInfo(tzname))
                else:
                    timezone.deactivate()
        except Exception as e:
            timezone.deactivate()

        return self.get_response(request)
