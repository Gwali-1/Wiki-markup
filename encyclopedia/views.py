from django.shortcuts import render
from django.http import HttpResponse
import markdown2

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def load_page(request,title):
    content = util.get_entry(title)
    if content:
        content_html = markdown2.markdown(content)
        return HttpResponse(content_html)
    else:
        return HttpResponse("Page does not exist")


