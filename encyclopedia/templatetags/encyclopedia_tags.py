from django import forms, template

register = template.Library()

class SearchForm(forms.Form):
    """
    Form to search for wiki entries.
    """
    search_query = forms.CharField(
        label=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control search', 'placeholder': 'Search Encyclopedia', 'aria-label': 'search encyclopedia'}), 
        max_length=80, 
        strip=True)

@register.inclusion_tag('encyclopedia/search_form.html')
def entries_search_form():
    form = SearchForm()
    return {'the_search_form': form}
