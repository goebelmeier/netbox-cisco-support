from django.http import HttpResponse
from django.urls import path


def dummy_view(request):
    html = "<html><body>Cisco Support API plugin.</body></html>"
    return HttpResponse(html)


urlpatterns = [
    path("", dummy_view, name="cisco_support_list"),
]
