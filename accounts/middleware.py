from .models import Activity


class ActivityMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            activity, created = Activity.objects.get_or_create(
                user=request.user)
            activity.save()
        return self.get_response(request)
