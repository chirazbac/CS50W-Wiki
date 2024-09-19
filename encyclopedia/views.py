from django.shortcuts import render
import markdown
import random

from . import util

def convert_html(title):
    content = util.get_entry(title)
    markdowner = markdown.Markdown()
    if content == None:
        return None
    else :
        return markdowner.convert(content)



def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def add(request):
    if request.method == "GET":
          return render(request, "encyclopedia/new_page.html")
    else:
        title = request.POST['q']
        content = request.POST['c']

        if  util.get_entry(title) != None:
            return render(request, "encyclopedia/error_page.html", {
                            "error" : "this title already exisits"

                        })

        else:
            util.save_entry(title, content)
            html_content = convert_html(title)
            return render(request, "encyclopedia/entrypage.html", {
            "content" : html_content,
            "title" : title

        })



def entry(request, title):
        content = convert_html(title)
        if content is not None:
          return render(request, "encyclopedia/entrypage.html", {
            "content" : content,
            "title" : title,
        })
        else:
         return render(request, "encyclopedia/error_page.html", {

                    "error" : "the requested page is not found",
                })

def search(request):
    if request.method == "POST":
        query = request.POST['q']
        html_content = convert_html(query)
        if html_content != None :
            return render(request, "encyclopedia/entrypage.html", {
                              "query": query ,
                              "content" : html_content
           })
        else:
            recommendations = []
            all_entries = util.list_entries()
            for entry in all_entries:
                if query.lower() in entry.lower():
                      recommendations.append(entry)

            return render(request, "encyclopedia/search.html", {
                               "recommendations": recommendations

            })

def edit(request):
    if request.method == 'POST':
        title = request.POST['entry_title']
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit_page.html", {
                                     "title": title ,
                                     "content" : content
       })

def save(request):
    if request.method == 'POST':
        title = request.POST['q']
        content = request.POST['c']
        util.save_entry(title, content)
        html_content = convert_html(title)
        return render(request, "encyclopedia/entrypage.html", {
             "title" : title,
             "content" : html_content

                })

def rand(request):
    entries = util.list_entries()
    random_entry= random.choice(entries)
    html_content = convert_html(random_entry)
    return render(request, "encyclopedia/entrypage.html", {
        "title" : random_entry,
        "content" : html_content

                    })


