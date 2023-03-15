# Wikipedia-like project plan

The plan to complete the wikipedia-like, Django, app.

## App requirements

### Entry Page ✅

Visiting `/wiki/TITLE`, where `TITLE` is the title of an encyclopedia entry, should render a page that displays the contents of that encyclopedia entry.

- The view should get the content of the encyclopedia entry by calling the appropriate `util` function. ✅
- If an entry is requested that does not exist, the user should be presented with an error page indicating that their requested page was not found. ✅
- If the entry does exist, the user should be presented with a page that displays the content of the entry. The title of the page should include the name of the entry. ✅

#### entry page steps

- Inside `encylopedia/` ✅

Prepares the view for each **entry**.

- in `urls.py` add `app_name = 'encyclopedia'` for best practice ✅
  - update `urlpatterns` with new path that:
    - checks for this url `wiki/<ENTRY_NAME>` capturing the param as string called `entry` ✅
    - points to the view called `entry` ✅
    - with `name="entry"` ✅
- in `views.py` ✅
  - inport the mk2html parser I built for this project ✅
  - add a function called `entry`, capturing two params, `(request, entry)` ✅
    - use the `get_entry` function to get the `entry` file, storing it in `mk_doc` var ✅
    - if `get_entry` was no successful ✅
      - redirect user to `404` page ✅
    - else on success ✅
      - render page and parse the markdown doc in `mk_doc` using the `mk2html.parse_file()` function with name html_entry ✅
      - pass the page title to template as 'entry_title' ✅
- in `templates/`
  - create a html file called `entry.html` ✅
    - extends the layout.html ✅
    - create the django blocks to display the HTML file. ✅

Prepares the view for the **error** page.

- in `urls.py` update the `urlpatterns` with path: ✅
  - `entry-not-found` ✅
  - pointing to `views.entry_not_found` ✅
  - with `name="entry_not_found"` ✅
- in `templates/`
  - create `404-entry.html` template with the message to let the user know the page was not found ✅
- in `views.py`
  - add a view called `entry_not_found` that displays the `404-entry.html` template ✅

### Index Page ✅

Update `index.html` such that, instead of merely listing the names of all pages in the encyclopedia, user can click on any entry name to be taken directly to that entry page. ✅

#### index page steps

- Inside `encylopedia/` ✅
  - in `templates/index.html` amend the list of name to use anchor tags with `href="{% url 'encyclopedia:entry' %}/{{ entry }}"`, dynamically creating the links to each entry. ✅

### New Page ✅

Clicking “Create New Page” in the sidebar should take the user to a page where they can create a new encyclopedia entry.

- Users should be able to enter a title for the page and, in a `textarea`, should be able to enter the Markdown content for the page. ✅
- Users should be able to click a button to save their new page. ✅
- When the page is saved, if an encyclopedia entry already exists with the provided title, the user should be presented with an error message. ✅
- Otherwise, the encyclopedia entry should be saved to disk, and the user should be taken to the new entry’s page. ✅

#### new page steps

- Inside `encyclopedia/templates` ✅
  - create a new file called `new-page.html` that extends the layout.html template ✅
  - create a form: ✅
    - use the dynamic form ✅
    - submit button that says Save ✅
    - add the csrf token ✅
    - add action that points to the create-new-page url with a POST method ✅
- Inside `encyclopedia/urls` add a path that points to: ✅
  - new page template ✅
  - new page view ✅
  - has a name of `new-page` ✅
- Inside `encyclopedia/views` ✅
  - import the form module ✅
  - create a form class ✅
    - taking in the page title, label = Page Title ✅
    - taking in the page body, label = Page Body ✅
    - create custom function to validate the entry title. Make sure it doesnt exist. ✅
  - create a function named `new_page` ✅
    - check if its a POST request: ✅
      - create a new form with the POST data ✅
      - check if data is valid ✅
        - import the reverse() function form django.urls ✅
        - clean the string data ✅
        - prepend the title to the content with an empty line inbetween. `# title \n\n` ✅
        - redirect to the new entry ✅
      - else if POST data is not valid ✅
        - reload new_page.html and give back the POSTed form ✅
    - else, its a GET request: ✅
      - render the `create-new-page` template ✅
      - to the template pass in the new form class ✅

### Edit Page ✅

On each entry page, the user should be able to click a link to be taken to a page where the user can edit that entry’s Markdown content in a `textarea`.

- The `textarea` should be pre-populated with the existing Markdown content of the page. (i.e., the existing content should be the initial `value` of the `textarea`). ✅
- The user should be able to click a button to save the changes made to the entry. ✅
- Once the entry is saved, the user should be redirected back to that entry’s page. ✅

#### edit page steps

- in `encyclopedia/templates/` ✅
  - create new html file `edit-page.html` ✅
  - populate the file with the same form code used in the new-page template ✅
  - For the `entry.html` template we are now using separate body and title properties
    - Use `<section></section>` tags with header and body to separate the entry ✅
      - within the section->header add the entry title ✅
      - next to the title add a link to edit the entry ✅
      - using `divs` display the body of the entry. ✅
    - edit the view.py for this template so that:
      - we remove the first two list item and return only the entry body ✅
- in `encyclopedia/urls.py` ✅
  - create new path to edit-page ✅
  - grap a string argument ✅
  - new page template ✅
  - new page view ✅
  - has a name of `edit-page.html` ✅
- in `encyclopedia/views.py`
  - create a new form Class called `EditPage` ✅
    - has a title, with the page title as readonly. dont want unwanted name changes. ✅
      - we need to secure this value so people cant change it on the browser side ✅
    - has a textarea input ✅
  - create function `edit_page`, taking in the page title as arg ✅
    - deal with the GET request as default by ✅
      - grab the url parameters with the page name ✅
      - util.get_entry to get the raw data from disk, store it in `mk_doc` ✅
      - provide error message if file not found ✅
      - store the first line of content in `title` property ✅
      - remove the first two lines from `content`. removes the title text and empty line below ✅
      - create a new form and populate the initial value of textarea to be `content` ✅
      - render the page with the bound form ✅
    deal with POST requests
      - check if its a POST request ✅
      - create new form and bind the data in POST ✅
      - check that it is valid ✅
        - store the clean `content` ✅
        - use util.save_entry to store the updated page ✅
        - redirect to the page that was edited ✅

After implementing this page I realised that the input element, for the title, in the form is not required, therefore it will be hidden from view.

- in `encyclopedia/views.py`
  - update the input for title to be type=hidden and ✅
    - give it a name of 'entry-title' ✅
    - give it id = 'entry-title' ✅

### Random Page

Clicking “Random Page” in the sidebar should take user to a random encyclopedia entry.

#### Random page steps

- in `encyclopedia/views.py`
  - create a function called `randon` and inside it ✅
    - use the utility `list_entries` to load all the entries available ✅
    - import random module ✅
    - store the name of a random list entry to var `entry_name`: ✅
      - use random method `randrange()` to return a random number between 0 and the length of the list and get an item from the `list` var. ✅
    - use HttpResponseRedirect, reversing to the entry view passing in the page title as arg ✅
- in `encyclopedia/urls.py`
  - create a new entry to the `random` view ✅
  - name it `random-page` ✅
- in `encyclopedia/templates/layout.html`
  - amend the list item for the random, creating an an anchor link pointint to the random url ✅

### Search ✅

Allow the user to type a query into the search box in the sidebar to search for an encyclopedia entry.

- If the query matches the name of an encyclopedia entry, the user should be redirected to that entry’s page.

- If the query does not match the name of an encyclopedia entry, the user should instead be taken to a search results page that displays a list of all encyclopedia entries that have the query as a substring. For example, if the search query were `ytho`, then `Python` should appear in the search results.
- Clicking on any of the entry names on the search results page should take the user to that entry’s page.

#### Seach steps

The UI doesn't have a search button and the instructions speak of a results page so I have assumed the app will only go ahead with the search once the use presses enter after typing in some text in the search box.

- in `encyclopedia/urls.py` add path to the list ✅
  - "search-results/" ✅
  - linking to 'views.search_results' ✅
  - with name 'search_results' ✅
- in `encyclopedia/views.py`
  - use the form class to create a form with:
    - has a text input ✅
    - clean the text when someone tries to search for something that is not valid or empty input
  - create view 'search_entries()' ✅
    - capture only POST requests ✅
      - creates a form using the POST request and form class ✅
      - check form validity ✅
        - clean the seach input data and store in 'search_text' ✅
        - util.get_entries and store in var 'entries' ✅
        - create variable 'entries_found' and init to [] ✅
        - using a loop, check if current item in list matches the search query ✅
          - YES. ✅
          - check if current item length == search query length ✅
            - YES. ✅
            - assign True to 'exact_match' ✅
            - clear the 'entried_found' from other partial matches added ✅
            - store current item in 'entries_found' ✅
            - exit loop premature ✅
            - NO ✅
            - add current item to list of 'entries_found' ✅
        - check that 'entries_found' is not empty ✅
          - now check if its an exact match ✅
            - redirect to the exact entry ✅
        - redirect to the 'search_results' template passing entries found and search query ✅
      - on a GET, which means someone is trying to access the url directly ✅
        - redirect the user back to the home page ✅
- in `encyclopedia/templates/` ✅
  - create a template called 'search-results.html' to display ✅
    - a title with the search string ✅
    - a list of items as links with the matched results ✅
    - or a message saying 'no results found' ✅
- in `encyclopedia/templates/layout.html` ✅
  - load the 'encyclopedia_tags' ✅
  - replace the current search form with the 'entries_search_form' template ✅

**Note:** I came across a chanllenge when turning the search bar into a django form.
I need to create a form that is used by the 'layout.html' template but is independent of the views.
This form will be processed by a view when submitted.

After some research I came across custom inclusion tags, a new concept for me. Seems interesting and promissing so let's try it out. New steps to add:

- in `encyclopedia/`
  - add a new directory called 'templatetags' and inside ✅
    - create a file `__init__.py` so the folder is treated as a module ✅
    - create a file called 'encyclopedia_tags' and inside ✅
      - import the form and template from django ✅
      - register the template library ✅
      - create the form class: ✅
        - will have a single text field ✅
        - to clean the text field with valid string
      - register the inclusion tag, pointing to the template 'search_form.html' ✅
      - create function 'entries_search_form' ✅
        - create new form with var name 'form' ✅
        - return dictionary with form as 'the_search_form' ✅
- in `encyclopedia/templates/`
  - create new template named 'search_form.html' ✅
    - add html form with method=post, action=ponting to 'search_results' url ✅
      - add the token for csrf ✅
      - use 'the_search_form' tag ✅

**Note2:** The search form does not have any custom cleaning and I am currently wondering if its good practice to do so or if the built-in form class takes care of it. More research required here.

### Challenge ✅

- Challenge for those more comfortable: If you’re feeling more comfortable, try implementing the Markdown to HTML conversion without using any external libraries, supporting headings, boldface text, unordered lists, links, and paragraphs. You may find using regular expressions in Python helpful.

The Markdown to HTML conversion was create as a separate project therefore kept in its own [repo](markdown-to-html-parser).
