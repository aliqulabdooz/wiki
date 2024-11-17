from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from random import choice
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def get_title(request, title=None):
    try:
        check = False
        tit, enc = util.markdown_md(title)
    except TypeError:
        return redirect("encyclopedia:index")

    else:
        if "add" in request.session and tit in request.session["add"]:
            check = True
        context = {
            'check': check,
            "enc": enc,
            "title": tit,
        }
        return render(request, "encyclopedia/encyclopedia_title.html", context)


def random_encyclopedia(request):
    title = choice(util.list_entries())
    return redirect('encyclopedia:get_title', title)


def get_query_search(request):
    if request.method == 'POST':
        query = request.POST.get('q')
        return redirect("encyclopedia:get_title", query)
    else:
        return redirect("encyclopedia:index")


def add_encyclopedia(request):
    if request.method == 'POST':
        query_md, query_title = request.POST.get('md_text'), request.POST.get('title')
        titles = util.list_entries()

        if query_title in titles:
            messages.warning(request, "This encyclopedia already used")

        else:
            if "add" not in request.session:
                request.session["add"] = []
            # save a md file
            util.save_entry(query_title, query_md)
            # add session
            request.session["add"] += [query_title.lower()]
            print(request.session["add"])
            messages.success(request, "Encyclopedia successfully added")

        return redirect("encyclopedia:index")
    else:
        return render(request, 'encyclopedia/Add_encyclopedia.html')


def update_encyclopedia(request, title):
    if request.method == "POST":
        query_md, query_title = request.POST.get('md_text'), request.POST.get('title')
        if query_title != title:
            titles = util.list_entries()
            if query_title in titles:
                messages.warning(request, 'This encyclopedia already used')
                return redirect("encyclopedia:index")
            else:
                util.del_entry(title)
        util.save_entry(query_title, query_md)
        ind = list(request.session["add"]).index(title)
        request.session["add"][ind] = query_title.lower()
        request.session.modified = True
        messages.success(request, "Encyclopedia successfully updated")
        return redirect("encyclopedia:index")
    else:
        enc = "".join(util.get_entry(title)[1])
        print(enc.strip())

        context = {
            'enc': enc.strip(),
            'title': title,
        }
        return render(request, 'encyclopedia/Update_encyclopedia.html', context)


def delete_encyclopedia(request, title):
    util.del_entry(title)
    messages.warning(request, "Encyclopedia successfully deleted")
    return redirect("encyclopedia:index")
