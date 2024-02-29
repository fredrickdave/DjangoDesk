import zoneinfo

from django.utils import timezone


class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            # get django_timezone from cookie
            tzname = request.COOKIES["d"]
            if tzname:
                timezone.activate(zoneinfo.ZoneInfo(tzname))
            else:
                timezone.deactivate()
        except Exception as e:
            print("E", e)
            timezone.deactivate()

        return self.get_response(request)
