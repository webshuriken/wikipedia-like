from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django import forms
from django.urls import reverse

from . import util, mk2html

class CreateNewPage(forms.Form):
    title = forms.CharField(label="Title", strip=True)
    content = forms.CharField(widget=forms.Textarea, label="Content", strip=True)

    def clean_title(self):
        """
        To pass the cleaning, the title name must not exist.
        """
        data = self.cleaned_data["title"]
        if util.get_entry(data) != None:
            raise ValidationError(f"Entry with the name '{data}' already exists")
        return data

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    mk_doc = util.get_entry(entry)
    if (mk_doc == None):
        return render(request, "encyclopedia/404-entry.html")
    else:
        return render(request, "encyclopedia/entry.html", {
            "entry_title": entry,
            "html_entry": mk2html.parse_file(mk_doc)
        })

def entry_not_found(request):
    return render(request, "encyclopedia/404-entry.html")

def new_page(request):
    # catch form submission
    if request.method == 'POST':
        # create new form with user submitted data
        form = CreateNewPage(request.POST)
        # does the submitted form follow the rules
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            # prepend the title to the content
            content = f"# {title}\n\n{content}"
            # save the new entry to file
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse(f"encyclopedia:entry", args=[title]))

        else:
            return render(request, "encyclopedia/new-page.html", {
                "form": form
            })

    # fresh request, fresh form
    return render(request, "encyclopedia/new-page.html", {
        "form": CreateNewPage()
    })