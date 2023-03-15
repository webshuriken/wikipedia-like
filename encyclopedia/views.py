from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django import forms
from django.urls import reverse
from random import randrange
import re

from . import util, mk2html
from .templatetags.encyclopedia_tags import SearchForm

class CreateNewPage(forms.Form):
    """
    Form used in the new page view
    """
    title = forms.CharField(label="Title", max_length=80, strip=True)
    content = forms.CharField(widget=forms.Textarea, label="Content", strip=True)

    def clean_title(self):
        """
        To pass the cleaning, the title name must not exist.
        """
        data = self.cleaned_data["title"]
        if util.get_entry(data) != None:
            raise ValidationError(f"Entry with the name '{data}' already exists")
        return data

class EditPage(forms.Form):
    """
    Form used when editing a page, the title is readonly.
    We will only allow users to change the main content and not the title.
    """
    title = forms.CharField(widget=forms.HiddenInput(attrs={'name': 'entry-title', 'id': 'entry-title'}))
    content = forms.CharField(widget=forms.Textarea, label="Content", strip=True)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    mk_doc = util.get_entry(entry)
    if (mk_doc == None):
        return render(request, "encyclopedia/404-entry.html")
    else:
        html_doc = mk2html.parse_file(mk_doc)
        # lets remove the page title as we only need the body
        html_doc.pop(0)
        return render(request, "encyclopedia/entry.html", {
            "entry_title": entry,
            "html_entry": html_doc
        })

def entry_not_found(request):
    """
    This template is for non existent entry
    """
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

def edit_page(request, entry):
    # let grab that form POST
    if request.method == 'POST':
        form = EditPage(request.POST)
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

    # this check will stop a user from abusing the edit form by manually going to the 
    # url and typing in any text as parameter, adding content to the form and saving it
    # as if they were creating a new entry.
    mk_doc = util.get_entry(entry)
    if mk_doc == None:
        return render(request, "encyclopedia/404-entry.html")

    # split the entry to separate the main title from the content
    doc = mk_doc.splitlines(True)
    # remove the '# ' before the title and strip trailing newlines
    title = doc[0][2:].rstrip("\r\n")
    # this is the only way I can get it to keep the line breaks when joining the list
    content = ""
    for i in range(2, len(doc)):
        content += doc[i]

    # create editing form and setup initial values
    form = EditPage()
    form["title"].initial = title
    form["content"].initial = content

    return render(request, "encyclopedia/edit-page.html", {
        "form": form,
        "title": title
    })

def random(request):
    """
    loads a random entry
    """
    list = util.list_entries()
    # lets get arandom name
    entry_name = list[randrange(len(list))]
    # lets retrieve and parse the entry
    return HttpResponseRedirect(reverse(f"encyclopedia:entry", args=[entry_name]))

def search_results(request):
    """
    displays the results, if any, of a search for a wiki entry
    """
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            search_query = form.cleaned_data["search_query"]
            entries = util.list_entries()
            # loop around the list of entries
            entries_found = []
            exact_match = False
            for entry in entries:
                if re.search(f'{search_query}', entry, re.IGNORECASE):
                    # is it exact match?
                    if len(search_query) == len(entry):
                        exact_match = True
                        # in case other partial matches were added, lets clear the entries found
                        entries_found = []
                        entries_found.append(entry)
                        break
                    entries_found.append(entry)
            # now lets see what we have found
            if len(entries_found) != 0:
                if exact_match:
                    return HttpResponseRedirect(reverse(f"encyclopedia:entry", args=[entries_found[0]]))
  
            # handle both part match and no match results
            return render(request, "encyclopedia/search_results.html", {
                "search_query": search_query,
                "search_results": entries_found
            })
    # anyone trying to access this page directly will be sent back home
    return HttpResponseRedirect(reverse(f"encyclopedia:index"))
