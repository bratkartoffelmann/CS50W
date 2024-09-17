from django.shortcuts import render
from django.http import HttpResponse
import markdown2 # More information on https://github.com/trentm/python-markdown2

from . import util

import random

# Dictionary of error types / codes
error_types = {
    403: "Forbidden",
    404: "Page not found",
}

# Functions
def convert_md_to_html(title):
    """
    Convert md contents to html compatible
    """

    content = util.get_entry(title)

    if content == None:
        return None
    else: 
        return markdown2.markdown(content)

# Functions for webpages
def index(request):
    """
    Default page display
    """
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries() # returns all md entries
    })

def entry(request, title):
    """
    Shows corresponding page to entry
    """

    html_content = convert_md_to_html(title)

    # If page does not exist, i.e. no content -> error
    if html_content == None:
        error = 404
        return render(request, "encyclopedia/error.html", {
            "error": error,
            "error_type": error_types[error],
            "message": "The entry you are searching for does not exist."
        })
    
    # If page exist, display its content
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content,
        })

def search(request):
    """
    Shows corresponding page to entry for exact match in keyword,
    else, show a list of partial matching entries -> each of the matches to be redirected to their corresponding pages.
    """
    # TODO: If no matching entries, display a different text

    if request.method == "POST": # Search is used
        entry_search = request.POST['q'] # get search from q

        html_content = convert_md_to_html(entry_search)

        # To check if there is a direct match
        if html_content is not None:
            return render(request, "encyclopedia/entry.html", {
                "title": entry_search,
                "content": html_content,
            })
        
        # To check if there is a partial match
        else: 
            all_entries = util.list_entries() # Get all entries available
            matches = []

            for entry in all_entries: # Get a list of partial matches to q
                if entry_search.lower() in entry.lower():
                    matches.append(entry)


            # If no matches, display a corresponding comment
            if len(matches) == 0:
                error = 404
                return render(request, "encyclopedia/error.html", {
                    "error": error,
                    "error_type": error_types[error],
                    "message": f"There is no match to '{entry_search}' in this existing wiki."
                })

            # Return a page with list of matches, and each of the matches has its own redirect link to their corresponding pages
            return render(request, "encyclopedia/search.html", {
                "matches": matches,
            })
        

def new_page(request):
    """
    Create new page
    """

    if request.method == "GET":
        return render(request, "encyclopedia/new_page.html")
    else: 
        title = request.POST['title']
        content = request.POST['content']

        # For null inputs
        if title == "" or content == "" :
            error = 403
            return render(request, "encyclopedia/error.html", {
                "error": 403,
                "error_type": error_types[error],
                "message": "Both title and content are required.",
            })

        # For existing inputs
        titleExist = util.get_entry(title)
        if titleExist is not None:
            error = 403
            return render(request, "encyclopedia/error.html", {
                "error": error,
                "error_type": error_types[error],
                "message": "Entry page already exists. Please edit page instead."
            })
        
        # For valid inputs
        util.save_entry(title, content)
        html_content = convert_md_to_html(title)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content,
        })
        
def edit(request):
    """
    To display the edit page of entry
    - i.e. Title and Content to be displayed
    """
    if request.method == 'POST':
        title = request.POST['entry_title']
        content = util.get_entry(title)

        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content,
        })


def save_edit(request):
    """
    To save the edited content of entry, and display the entry
    """

    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']

        util.save_entry(title, content) # Save updated entry
        html_content = convert_md_to_html(title)

        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content,
        })

def randomised(request):
    """
    Returns a randomly selected page
    """

    title = random.choice(util.list_entries()) # random selection of titles
    html_content = convert_md_to_html(title)

    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": html_content,
    })