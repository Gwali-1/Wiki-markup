from turtle import title
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
import markdown2
from django.urls import reverse
from . import util




def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })



def load_page(request,title):
    content = util.get_entry(title)
    if content:
        content_html = markdown2.markdown(content)
        return render(request,"encyclopedia/markupContent.html",{
            "content":content_html,
            "title":title
        })
        return HttpResponse(content_html)
    else:
        return render(request,"encyclopedia/error_404.html",{
            "error_message":"Page Does Not Exist"
        })



def search(request):
    entry = request.GET.get("q")
    content = util.get_entry(entry)
    if content:
        return HttpResponseRedirect(reverse("encyclopedia:load_page",args=(entry,)))
    entries = util.list_entries()
    matched = list()
    for ent in entries:
        if entry.lower() in ent.lower():
            matched.append(ent)
    return render(request,"encyclopedia/substring_results.html",{
        "matched":matched
    })



def create(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content=request.POST.get("content")
        if title and content:
            check = util.get_entry(title)
            if check:
                util.save_entry(title,content)
                return render(request,"encyclopedia/error_404.html",{
                    "error_message":"Entry With Title Already Exist, old entry replaced"
                })
            util.save_entry(title,content)
            return HttpResponseRedirect(reverse("encyclopedia:load_page",args=(title,)))
      
        return HttpResponse("error")
    return render(request,"encyclopedia/newpage.html")



def edit(request,title):
    if request.method == "POST":
        try:
            util.save_entry(title,request.POST.get("content"))
            return HttpResponseRedirect(reverse("encyclopedia:load_page",args=(title,)))
        except Exception as e:
             return render(request,"encyclopedia/error_404.html",{
                    "error_message":e})

    content = util.get_entry(title)
    return render(request,"encyclopedia/editpage.html",{
        "content":content
    })
