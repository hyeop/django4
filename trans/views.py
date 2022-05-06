from django.shortcuts import render
from googletrans import Translator
import googletrans

# Create your views here.
def index(req):
    context = {
        "nd" : googletrans.LANGUAGES
    }
    if req.method == "POST":
        b = req.POST.get("bf")
        f = req.POST.get("fr")
        t = req.POST.get("to")
        trans = Translator()
        a = trans.translate(b, src=f, dest=t)
        context.update({ 
            "af" : a.text,
            "fr" : f,
            "to" : t,
            "bf" : b
        })
    return render(req, "trans/index.html", context)