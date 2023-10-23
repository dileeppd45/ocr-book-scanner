from django.shortcuts import render

from django.shortcuts import render, HttpResponse, redirect
from django.db import connection
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from . import views
from PIL import Image
import pytesseract
import numpy as np
import os

# Create your views here.
def login(request):
    if request.method == "POST":
        userid = request.POST['userid']
        password = request.POST['password']
        cursor = connection.cursor()
        cursor.execute("select * from login where admin_id= '" + userid + "' AND password = '" + password + "'")
        admin = cursor.fetchone()
        if admin == None:
            messages.error(request, 'Invalid Username Or Password!!')
            return redirect('login')


        else:
            return redirect("admin_home")
    return render(request, "login.html")

def logout(request):
    return redirect('login')

def admin_home(request):
    return render(request, "index.html")

def register_categoryform(request):
    return render(request,"register_categoryform.html")

def register_category(request):
    if request.method == "POST":
        name = request.POST['txtName']
        cursor = connection.cursor()
        cursor.execute("insert into category values(null,'" + name + "')")
        return redirect("view_category")
    else:
        messages.info(request, "Error Adding")






def view_category(request):#admin view
    cursor = connection.cursor()
    cursor.execute("select * from category")
    cdata = cursor.fetchall()
    l = list(cdata)
    length = len(l)
    if length == 0:
        val = "categories"
        return render(request, "ano_carts.html", {'val': val})

    return render(request, "view_all_category.html", {'cdata': cdata})

def edit_categoryform(request, id):#admin view
    request.session['aid'] = id
    cursor = connection.cursor()
    cursor.execute("select * from category where idcategory='" + str(id) + "' ")
    data = cursor.fetchone()
    return render(request, "edit_category.html", {'data': data})

def update_category(request):#admin view
    cursor = connection.cursor()
    name = request.POST['txtName']
    bid=request.session['aid']
    cursor.execute("update category set name='"+name+"' where idcategory= '" + str(bid) + "' ")
    return redirect('view_category')

def delete_category(request, id):#admin view
    cursor = connection.cursor()
    cursor.execute("delete from category where idcategory = '" + str(id) + "' ")
    return redirect('view_category')
def register_bookform(request, id):
    return render(request, "register_item.html",{"id":id})

def register_book(request):#admin view
    if request.method == "POST":
        cid = request.POST['cid']
        name = request.POST['txtname']
        author = request.POST['autname']
        description = request.POST['txtdes']
        pages= request.POST['pages']
        cursor = connection.cursor()
        cursor.execute("insert into books values(null,'" + cid + "', '" + name + "', '" + author + "','" + description + "','" + pages + "')")
        cursor = connection.cursor()
        cursor.execute("select * from books where idcategory ='" + cid + "' ")
        data = cursor.fetchall()
        return render(request, "view_items.html", {'data': data})

def view_book(request, id):  # admin view
    request.session['cid']=id
    cursor = connection.cursor()
    cursor.execute("select * from books where idcategory='" + str(id) + "' ")
    data = cursor.fetchall()
    l = list(data)
    length = len(l)
    if length == 0:
        val = "Books"
        return render(request, "no_carts.html", {'val': val})
    else:
        return render(request, "view_items.html ", {"data": data })


def add_index(request, id):
    cid = request.session['cid']
    return render(request, "add_index.html",{'bid':id,'cid':cid})

def reg_index(request,id):
    if request.method =="POST":
        name = request.POST['iname']
        cursor = connection.cursor()
        cursor.execute("insert into book_index values(null,'" + str(id) + "','" + str(name) + "','empty')")
        return redirect('view_index',id=int(id))

def view_index(request,id):
    cursor=connection.cursor()
    cid = request.session['cid']
    request.session['bkid'] = id
    cursor.execute("select * from book_index where idbooks='"+ str(id)+"'")
    cdata=cursor.fetchall()
    return render(request,"view_index.html",{'cdata':cdata,'cid':cid})


def delete_page(request, id):
    bid=request.session['bkid']
    cursor=connection.cursor()
    cursor.execute("select total_pages from books where idbooks='" + str(bid) + "' ")
    tp = cursor.fetchone()
    tp = list(tp)
    tp = int(tp[0])
    l=[]
    for i in range(tp):
        p = i + 1
        cursor.execute("select * from book_pages where idbooks ='" + str(bid) + "' and page_no ='" + str(p) + "' and index_id= '"+str(id)+"' ")
        page = cursor.fetchone()
        if page == None:
            continue
        else:
            m=list(page)
            m=m[3]
            l.append(m)
    return render(request,'delete_page.html',{'pageno':l,'id':id,'bid':bid})

def remove_page(request):
    bid = request.session['bkid']

    if request.method == "POST":
        id = request.POST['id']
        pageno = request.POST['pgno']
        cursor = connection.cursor()
        print(pageno)
        cursor.execute("select file_name from book_pages where idbooks = '" + str(bid) + "' and page_no='"+str(pageno)+"' ")
        fname=cursor.fetchone()
        print(fname)
        print("hello")
        fname=list(fname)
        fname=fname[0]
        print(fname)

        file_path = "../bookpro/media/cart/"+str(fname)
        if fname == None:
            cursor.execute(
                "delete from book_pages where idbooks = '" + str(bid) + "' and page_no='" + str(pageno) + "' ")
            cursor.execute("select total_pages from books where idbooks='" + str(bid) + "' ")
            tp = cursor.fetchone()
            tp = list(tp)
            tp = int(tp[0])
            l = []
            for i in range(tp):
                p = i + 1
                cursor.execute("select * from book_pages where idbooks ='" + str(bid) + "' and page_no ='" + str(
                    p) + "' and index_id= '" + str(id) + "' ")
                page = cursor.fetchone()
                if page == None:
                    continue
                else:
                    m = list(page)
                    m = m[3]
                    l.append(m)
            cursor = connection.cursor()
            cursor.execute(
                "select page_no from book_pages where idbooks ='" + str(bid) + "' and index_id = '" + str(id) + "' ")
            indpages = cursor.fetchall()
            pg = []
            pages = list(indpages)
            for i in pages:
                v = list(i)
                pg.append(int(v[0]))
            print(pg)
            pg.sort()
            print(pg)
            if len(pg) == 0:
                return redirect('view_category')
            else:
                cursor.execute("update book_index set page_no ='" + str(pg[0]) + "' where idbook_index = '" + str(
                    id) + "' and idbooks = '" + str(bid) + "' ")
                return render(request, 'delete_page.html', {'pageno': l, 'id': id, 'bid': bid})
        else:
            cursor.execute("delete from book_pages where idbooks = '" + str(bid) + "' and page_no='"+str(pageno)+"' ")
            cursor.execute("select total_pages from books where idbooks='" + str(bid) + "' ")
            tp = cursor.fetchone()
            tp = list(tp)
            tp = int(tp[0])
            l = []
            for i in range(tp):
                p = i + 1
                cursor.execute("select * from book_pages where idbooks ='" + str(bid) + "' and page_no ='" + str(p) + "' and index_id= '"+str(id)+"' ")
                page = cursor.fetchone()
                if page == None:
                    continue
                else:
                    m = list(page)
                    m = m[3]
                    l.append(m)
            cursor = connection.cursor()
            cursor.execute("select page_no from book_pages where idbooks ='" + str(bid) + "' and index_id = '" + str(id) + "' ")
            indpages = cursor.fetchall()
            pg = []
            pages = list(indpages)
            for i in pages:
                v = list(i)
                pg.append(int(v[0]))
            print(pg)
            pg.sort()
            print(pg)
            if len(pg) == 0:
                return redirect('view_category')
            else:
                cursor.execute("update book_index set page_no ='" + str(pg[0]) + "' where idbook_index = '" + str(id) + "' and idbooks = '" + str(bid) + "' ")
                return render(request, 'delete_page.html', {'pageno': l, 'id': id, 'bid':bid})

def add_cart(request,id):
    bid = request.session['bkid']
    cursor = connection.cursor()
    cursor.execute("select total_pages from books where idbooks ='" + str(bid) + "' ")
    pageno = cursor.fetchone()
    pageno = list(pageno)
    pgno = pageno[0]
    cursor.execute("select total_pages from books where idbooks='" + str(bid) + "' ")
    tp = cursor.fetchone()
    tp = list(tp)
    tp = int(tp[0])
    l = []
    for i in range(tp):
        p = i + 1
        cursor.execute("select * from book_pages where idbooks ='" + str(bid) + "' and page_no ='" + str(p) + "' and index_id='"+str(id)+"' ")
        page = cursor.fetchone()
        if page == None:
            continue
        else:
            m = list(page)
            m = m[3]
            l.append(m)
    return render (request, "add_cart_form.html",{'bid':bid,'id':id, 'pgno':pgno,'pageno': l})



def upload_page(request, id):
    bid = request.session['bkid']
    cursor = connection.cursor()
    cursor.execute("select total_pages from books where idbooks ='" + str(bid) + "' ")
    pageno=cursor.fetchone()
    pageno=list(pageno)
    pgno=pageno[0]
    return render(request, "upload_page.html",{'id':id, 'pgno':pgno,'bid':bid})


def add_page(request):
    if request.method == "POST" and request.FILES['file']:
        cid = request.session['cid']
        bid = request.session['bkid']
        id=request.POST['id']
        print(id)
        pageno = request.POST['pageno']
        fname = request.FILES['file']
        upload = request.FILES['file']
        cursor = connection.cursor()
        cursor.execute("select * from book_pages where page_no ='"+str(pageno)+"' and idbooks ='"+str(bid)+"' ")
        page=cursor.fetchone()
        if page == None:
            cursor.execute("select * from book_pages where file_name = '"+str(fname)+"' ")
            fn=cursor.fetchone()
            if fn == None:
                fss = FileSystemStorage(location='../bookpro/media/cart')
                file = fss.save( upload.name, upload)
                file_url = fss.url(file)
                nodata="no data"
                pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
                print("in fun")
                filename = fname
                img1 = np.array(Image.open(filename))
                text = pytesseract.image_to_string(img1)
                print(text)
                text = text.replace("«", " ")
                text =text.replace("—", " ")
                text = text.replace("“", " ")


                try:
                    cursor.execute("insert into book_pages values(null,'" + str(bid) + "', '" + str(fname) + "','" + str(pageno) + "', '" + str(fname) + "', '" + str(text) + "','"+str(id)+"') ")
                    cursor = connection.cursor()
                    cursor.execute("select total_pages from books where idbooks ='" + str(bid) + "' ")
                    pageno = cursor.fetchone()
                    pageno = list(pageno)
                    pgno = pageno[0]
                    cursor = connection.cursor()
                    cursor.execute("select page_no from book_pages where idbooks ='"+str(bid)+"' and index_id = '"+str(id)+"' ")
                    indpages = cursor.fetchall()
                    pg = []
                    pages = list(indpages)
                    for i in pages:
                        v = list(i)
                        pg.append(int(v[0]))
                    print(pg)
                    pg.sort()
                    if len(pg) == 0:
                        return redirect('view_category')
                    else:
                        cursor.execute("update book_index set page_no ='" +str(pg[0]) + "' where idbook_index = '" + str(id) + "' and idbooks = '" + str(bid) + "' ")
                        return render(request, "upload_page.html", {'id': id, 'pgno': pgno,'bid':bid})



                except:
                    content="sorry unable to fetch text from image"
                    cursor.execute("insert into book_pages values(null,'" + str(bid) + "', '" + str(fname) + "','" + str(pageno) + "', '" + str(fname) + "', '" + str(content) + "','"+str(id)+"') ")
                    cursor = connection.cursor()
                    cursor.execute("select total_pages from books where idbooks ='" + str(bid) + "' ")
                    pageno = cursor.fetchone()
                    pageno = list(pageno)
                    pgno = pageno[0]
                    cursor = connection.cursor()
                    cursor.execute("select page_no from book_pages where idbooks ='"+str(bid)+"' and index_id = '"+str(id)+"' ")
                    indpages = cursor.fetchall()
                    pg = []
                    pages = list(indpages)
                    for i in pages:
                        v = list(i)
                        pg.append(int(v[0]))
                    print(pg)
                    pg.sort()
                    print(pg)
                    print(pg[0])
                    if len(pg) == 0:
                        return redirect('view_category')
                    else:
                        cursor.execute("update book_index set page_no ='" +str(pg[0]) + "' where idbook_index = '" + str(id) + "' and idbooks = '" + str(bid) + "' ")
                        return render(request, "upload_page.html", {'id': id, 'pgno': pgno, 'bid': bid})

            else:
                return HttpResponse("<script>alert('file_name already exist');window.location='../view_category';</script>")

        else:
            return HttpResponse("<script>alert('page_number already exist');window.location='../view_category';</script>")


def add_image_cart(request):
    if request.FILES['file']:
        upload = request.FILES['file']
        cart=FileSystemStorage(location='../bookpro/media/cart')
        file=cart.save(upload.name, upload)
        file_url = cart.url(file)
        return redirect('view_category')


def view_content(request, id):
    bid = request.session['bkid']

    cursor =connection.cursor()
    cursor.execute("select total_pages from books where idbooks='" + str(bid) + "' ")
    tp = cursor.fetchone()
    tp = list(tp)
    tp = int(tp[0])
    l = {}
    for i in range(tp):
        p = i + 1
        cursor.execute("select page_content from book_pages where idbooks ='" + str(bid) + "' and page_no ='" + str(p) + "' and index_id='"+str(id)+"' ")
        page = cursor.fetchone()
        if page == None:
            continue
        else:
            m = list(page)
            m = m[0]
            l[p] = m
    return render(request, 'view_content.html', {'tp': tp, 'page': l, 'id': id, 'bid':bid})

def update_content(request,pgno):
    if request.method == "POST":
        bid = request.session['bkid']
        id = request.POST['id']
        content = request.POST['content']
        print(content)
        cursor= connection.cursor()
        cursor.execute("update book_pages set page_content ='"+content+"' where page_no = '" +str(pgno)+"' and idbooks = '" +str(bid)+"' ")
        return redirect('view_index',id=bid)


def view_pages(request, id):
    bid=request.session['bkid']
    cursor = connection.cursor()
    cursor.execute("select total_pages from books where idbooks='" + str(bid) + "' ")
    tp = cursor.fetchone()
    tp=list(tp)
    tp=int(tp[0])
    l={}
    for i in range(tp):
        p=i+1
        cursor.execute("select file_name from book_pages where idbooks ='"+str(bid)+"' and page_no ='"+str(p)+"' and index_id='"+str(id)+"' ")
        page=cursor.fetchone()
        if page == None:
            continue
        else:
            m=list(page)
            m=m[0]
            l[p] = m
    return render(request,'view_pages.html',{'tp':tp,'page':l, 'id':bid})



def edit_book(request, id):#admin view
    request.session['kid'] = id
    cid=request.session['cid']
    cursor = connection.cursor()
    cursor.execute("select * from books where idbooks='" + str(id) + "' ")
    data = cursor.fetchone()
    return render(request, "edit_item.html", {'data': data,'cid':cid})

def edit_index(request,id):
    bid=request.session['bkid']
    cursor = connection.cursor()
    cursor.execute("select * from book_index where idbook_index='" + str(id) + "' ")
    data = cursor.fetchone()
    return render(request,"edit_index.html",{'data':data,'id':id,'bid':bid})

def update_index(request,id):
    if request.method == "POST":
        iname = request.POST['iname']
        cursor= connection.cursor()
        cursor.execute("update book_index set index_name ='"+str(iname)+"' where idbook_index = '" +str(id)+"' ")
        return redirect('view_category')

def update_book(request):#admin view
    cursor = connection.cursor()
    name = request.POST['pname']
    author= request.POST['autname']
    bid=request.session['kid']
    description = request.POST['discription']
    pages= request.POST['pages']
    cursor.execute("update books set book_name='"+name+"' where idbooks= '" + str(bid) + "' ")
    cursor.execute("update books set author='" + author + "' where idbooks= '" + str(bid) + "' ")
    cursor.execute("update books set book_description='"+description+"' where idbooks= '" + str(bid) + "' ")
    cursor.execute("update books set total_pages='"+pages+"' where idbooks= '" + str(bid) + "' ")
    return redirect('view_category')

def delete_book(request, id):#admin view
    cursor = connection.cursor()
    cursor.execute("delete from books where idbooks= '" + str(id) + "' ")
    return redirect('view_category')

def example(request):
    cursor = connection.cursor()
    cursor.execute("select page_no from book_pages where idbooks ='2' and index_id = '8' ")
    indpages = cursor.fetchall()
    pg=[]
    pages = list(indpages)
    for i in pages:
        v=list(i)
        pg.append(int(v[0]))
    print(pg)
    pg.sort()
    print(pg)
    print(pg[0])

    return redirect('view_category')