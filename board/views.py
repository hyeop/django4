from django.shortcuts import render, redirect
from .models import Board, Reply
from django.utils import timezone
from django.core.paginator import Paginator

# Create your views here.
def unlikey(req, bpk):
    b = Board.objects.get(id=bpk)
    b.likey.remove(req.user)
    return redirect("board:detail", bpk)

def likey(req, bpk):
    b = Board.objects.get(id=bpk)
    b.likey.add(req.user)
    return redirect("board:detail", bpk)

def index(req):
    kw = req.GET.get("kw", "")
    cate = req.GET.get("cate", "")
    pg = req.GET.get("page", 1)

    if kw:
        if cate == "sub":
            b = Board.objects.filter(subject__startswith=kw)
        elif cate == "wri":
            try:
                from acc.models import User
                u = User.objects.get(username=kw)
                b = Board.objects.filter(writer=u)
            except:
                b = Board.objects.none()
        elif cate == "con":
            b = Board.objects.filter(content__contains=kw)
        else:
            b = Board.objects.all()
    else:
        b = Board.objects.all()

    pag = Paginator(b, 5)
    obj = pag.get_page(pg)
    context ={
        "bset": obj,
        "kw":kw,
        "cate":cate
    }
    return render(req, "board/index.html", context)


def dreply(req, bpk, rpk):
    r = Reply.objects.get(id=rpk)
    if r.replyer == req.user:
        r.delete()
    else:
        pass # 경고메세지 대기중
        return redirect("board:index")
    return redirect("board:detail", bpk)

def creply(req, bpk):
    b = Board.objects.get(id=bpk)
    c = req.POST.get("com")
    Reply(board=b, comment=c, replyer=req.user).save()
    return redirect("board:detail", bpk)

def update(req, bpk):
    b = Board.objects.get(id=bpk)

    if b.writer != req.user:
        # 협박
        return redirect("board:index")

    if req.method == "POST":
        s = req.POST.get("sub")
        c = req.POST.get("con")
        b.subject = s
        b.content = c
        b.save()
        return redirect("board:detail", bpk)
    context = {
        "b": b
    }
    return render(req, "board/update.html", context)

def create(req):
    if req.method == "POST":
        s = req.POST.get("sub")
        c = req.POST.get("con")
        Board(subject=s, writer=req.user, content=c, pubdate=timezone.now()).save()
        return redirect("board:index")
    return render(req, "board/create.html")

def delete(req, bpk):
    b = Board.objects.get(id=bpk)
    if b.writer == req.user:
        b.delete()
    else:
        pass # 경고메세지 줌!
    return redirect("board:index")

def detail(req, bpk):
    b = Board.objects.get(id=bpk)
    r = b.reply_set.all()
    context = {
        "b" : b,
        "rset": r
    }
    return render(req, "board/detail.html", context)


