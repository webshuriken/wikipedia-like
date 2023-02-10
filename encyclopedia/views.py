from django.shortcuts import render
from django.http import HttpResponseRedirect

from . import util, mk2html


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    mk_doc = util.get_entry(entry)
    print(f'ENTRY FOUND: {type(mk_doc)}')
    if (mk_doc == None):
        return render(request, 'encyclopedia/404-entry.html')
    else:
        return render(request, "encyclopedia/entry.html", {
            "entry_title": entry,
            "html_entry": mk2html.parse_file(mk_doc)
        })

def entry_not_found(request):
    return render(request, "encyclopedia/404-entry.html")