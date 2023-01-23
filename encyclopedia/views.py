from django.shortcuts import render
from django.http import HttpResponseRedirect

from . import util, mk2html


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, entry):
    mk_doc = util.get_entry(entry)
    if (mk_doc == 'NONE'):
        return HttpResponseRedirect('PAGE WAS NOT FOUND')
    else:
        return render(request, "encyclopedia/entry.html", {
            "html_entry": mk2html.parse_file(mk_doc)
        })
