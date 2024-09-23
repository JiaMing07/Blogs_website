from django.db.models import Q
from django.shortcuts import render
from django.utils import timezone
import time
from .models import Blog, Comment
import os
import json
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.http import Http404
from django.core.paginator import Paginator
from django.shortcuts import redirect


# Create your views here.
def home(request):
    show_list = Blog.objects.all().order_by('?')[:20]
    return render(request, 'blog/home_page.html', {'show_list': show_list})


def init_data():
    if Blog.objects.count() > 0:
        Blog.objects.all().delete()
    file_list = os.listdir("./blog/data")
    file_list1 = os.listdir("./blog/datas")
    print(len(file_list))
    print(len(file_list1))
    # print(len(file_list))
    num = 0
    for i in range(0, len(file_list)):
        file = file_list[i]
        num = num + 1
        with open(f"./blog/data/{file}", "r", encoding="utf-8") as t:
            blog_data = json.load(t)
        file1 = file_list1[i]
        with open(f"./blog/datas/{file1}", "r", encoding="utf-8") as f1:
            blog_datas = json.load(f1)
            # if num < 10:
            #    print(blog_data)
        date_int = blog_data['pub_date']
        date_int = date_int.strip()
        date_list = date_int.split("-")
        date_ = int(date_list[0]) * 10000 + int(date_list[1]) * 100 + int(date_list[2])
        read = blog_data['read']
        if read[-1] == 'k':
            hot_ = int(float(read[0:-1]) * 1000)
        else:
            hot_ = int(read)
            # if num<10:
            #     print(date_int)
            #     print(date_)
            #     print(read)
            #     print(hot_)

        b = Blog(article=blog_datas['new_article'], title=blog_data['title'], text=blog_data['text'],
                 pub_date=blog_data['pub_date'], author_name=blog_data['author_name'],
                 author_popularity=blog_data['author_popularity'], author_fans=blog_data['author_fans'],
                 like=blog_data['like'], author_pic=blog_data['author_pic'],
                 collect=blog_data['collect'], read=blog_data['read'], hot=hot_,
                 url=blog_data['url'], show_text=blog_data['show_text'], date=date_,
                 tag_text=blog_datas['text'])
        print(b)
        b.save()


def give_tags(objects_list):
    python_lst = objects_list.filter(Q(title__icontains='python') | Q(text__icontains='python'))
    for obj in python_lst:
        obj.tags.add("Python")
    c1_lst = objects_list.filter(Q(title__icontains='C++') | Q(text__icontains='C++'))
    for obj in c1_lst:
        obj.tags.add("C++")
    c2_lst = objects_list.filter(Q(title__icontains='C#') | Q(text__icontains='C#'))
    for obj in c2_lst:
        obj.tags.add("C#")
    java_lst1 = objects_list.filter(Q(title__icontains='Java') | Q(tag_text__icontains='Java'))
    for obj in java_lst1:
        obj.tags.add("Java")
    javascript_lst = objects_list.filter(Q(title__icontains='Jav1Script') | Q(tag_text__icontains='Jav1Script'))
    for obj in javascript_lst:
        obj.tags.add("JavaScript")
    sql_lst = objects_list.filter(Q(title__icontains='SQL') | Q(text__icontains='SQL'))
    for obj in sql_lst:
        obj.tags.add("SQL")
    php_lst = objects_list.filter(Q(title__icontains='PHP') | Q(text__icontains='PHP'))
    for obj in php_lst:
        obj.tags.add("PHP")
    for obj in objects_list:
        if len(obj.tags.all()) == 0:
            obj.tags.add("else")


def blog_detail(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    comments = blog.comment_set.all().order_by("-public_date")
    return render(request, 'blog/blog_detail.html', {'blog': blog, 'comments': comments})


def submit_comment(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if 'comment_text' in request.POST:
        if request.POST['comment_text'] == "":
            comments = blog.comment_set.all().order_by("-public_date")
            return HttpResponseRedirect(reverse('blog:blog_detail', args=(pk,)))
        else:
            blog.comment_set.create(comment_text=request.POST['comment_text'], public_date=timezone.now())
            return HttpResponseRedirect(reverse('blog:blog_detail', args=(pk,)))


def delete_comment(request, pk, comment_id):
    blog = get_object_or_404(Blog, pk=pk)
    try:
        comment = blog.comment_set.filter(pk=comment_id)
    except Comment.DoesNotExist:
        raise Http404("Question does not exist")
    print(request.POST)
    if 'delete' in request.POST:
        comment.delete()
    return HttpResponseRedirect(reverse('blog:blog_detail', args=(pk,)))


def show_list(request):
    try:
        page = int(request.GET.get("page", 1))
    except ValueError:
        return render(request, 'blog/nothing.html')
    if page > (int(Blog.objects.count() / 20 + 1)) or page < 1:
        return render(request, 'blog/nothing.html')
    paginator = show_page(Blog.objects.all(), page)
    return render(request, 'blog/blog_list.html', {'paginator': paginator, })


def category(request):
    return render(request, 'blog/category.html')


def show_category(request, tag):
    if tag == "C2":
        print("C#")
        tag = 'C#'
    blog_list = Blog.objects.all().filter(tags__name__in=[tag])
    if len(blog_list) > 0:
        try:
            page = int(request.GET.get("page", 1))
        except ValueError:
            return render(request, 'blog/nothing.html')
        if page > (len(blog_list) / 20 + 1) or page < 1:
            return render(request, 'blog/nothing.html')
        if len(blog_list) > 20:
            paginator = show_page(blog_list, page)
            return render(request, 'blog/category_list.html', {'blog_list': blog_list, 'paginator': paginator})
        else:
            print("C#")
            return render(request, 'blog/category_list.html', {'blog_list': blog_list})
    else:
        return render(request, 'blog/nothing.html')


def search(request):
    blog_list = Blog.objects.all()
    base_url = "keyword="
    keyword = request.GET.get('keyword')
    print(keyword)
    base_url = base_url + keyword + "&order_choice="
    choice = request.GET.get('order_choice')
    base_url = base_url + choice
    blog_list = blog_list.filter(Q(title__contains=keyword) | Q(text__contains=keyword))
    search_tags = []
    options_str = ','.join(search_tags)
    if 'inlineRadioOptions' in request.GET:
        options = request.GET.getlist('inlineRadioOptions')
        for option in options:
            base_url = base_url + "&inlineRadioOptions=" + option
            if option == 'C1':
                search_tags.append("C++")
            elif option == 'C2':
                search_tags.append("C#")
            else:
                search_tags.append(option)
    options_str = ','.join(search_tags)
    if options_str == '':
        options_str = 'no_options'
    print(options_str)
    choice = request.GET.get('order_choice')
    return redirect('blog:go_to_search',keyword=keyword, choice=choice, options=options_str)



def go_to_search(request, keyword, choice, options):
    start = time.time()
    blog_list = Blog.objects.all()
    base_url = "keyword="
    keyword = keyword
    print(keyword)
    base_url = base_url + keyword + "&order_choice="
    choice = choice
    base_url = base_url + choice
    blog_list = blog_list.filter(Q(title__contains=keyword) | Q(text__contains=keyword))
    print(options)
    if options != 'no_options':
        print(time.time()-start)
        options = options.split(',')
        q_list = []
        print(options)
        # for option in options:
        #     if option == 'Python':
        #         q_list.append(Q(python_tag=True))
        #     elif option == 'C++':
        #         q_list.append(Q(c1_tag=True))
        #     elif option == 'C#':
        #         q_list.append(Q(c2_tag=True))
        #     elif option == 'Java':
        #         q_list.append(Q(java_tag=True))
        #     elif option == 'JavaScript':
        #         q_list.append(Q(javascript_tag=True))
        #     elif option == 'PHP':
        #         q_list.append(Q(php_tag=True))
        #     elif option == 'SQL':
        #         q_list.append(Q(sql_tag=True))
        #     elif option == 'else':
        #         q_list.append(Q(else_tag=True))
        # print(time.time()-start)
        # condition = q_list[0]
        # for idx in range(1, len(q_list)):
        #     condition = condition | q_list[idx]
        # blog_list = blog_list.filter(condition)
        # print(time.time() - start)
        blog_list = blog_list.filter(tags__name__in=options).distinct()
    choice = choice
    if choice == 'time':
        blog_list = blog_list.order_by('-date')
    elif choice == 'hot':
        blog_list = blog_list.order_by('-hot')
    print(time.time() - start)
    end = time.time()

    if len(blog_list) > 0:
        try:
            page = int(request.GET.get("page", 1))
            print(time.time() - start)
        except ValueError:
            return render(request, 'blog/nothing.html')
        if page > (len(blog_list) / 20 + 1) or page < 1:
            return render(request, 'blog/nothing.html')
        if len(blog_list) > 20:
            print(time.time()-start)
            paginator = show_page(blog_list, page, "", choice)
            total_time = end - start
            length = len(blog_list)
            print(total_time)
            return render(request, 'blog/search_result.html', {'blog_list': blog_list, 'paginator': paginator,
                                                               'total_time': total_time, 'length': length})
        else:
            total_time = end - start
            length = len(blog_list)
            print(total_time)
            return render(request, 'blog/search_result.html', {'blog_list': blog_list, 'total_time': total_time,
                                                               'length': length})
    else:
        return render(request, 'blog/find_nothing.html')


def show_page(lst, page, url="", str=""):
    p = Paginator(lst, 20)
    show_lst = p.page(page)
    first_page = False
    last_page = False
    front_dots = False
    back_dots = False
    pages = p.num_pages
    print(pages)
    if page == 1:
        end = 4 if pages >= 4 else pages
        right_list = p.page_range[1:end]
        left_list = []
        if end < pages:
            last_page = True
        if end < (pages - 1):
            back_dots = True
    elif page == pages:
        start = (page - 4) if (page - 4) > 0 else 0
        left_list = p.page_range[start:(page - 1)]
        right_list = []
        if start > 0:
            first_page = True
        if start > 1:
            front_dots = True
    else:
        start = (page - 3) if (page - 3) > 0 else 0
        end = (page + 2) if (page + 2) <= pages else pages
        left_list = p.page_range[start:(page - 1)]
        right_list = p.page_range[page:end]
        if start > 0:
            first_page = True
        if start > 1:
            front_dots = True
        if end < pages:
            last_page = True
        if end < (pages - 1):
            back_dots = True
    next_page = page + 1
    previous_page = page - 1
    print(pages)
    paginator = {'first_page': first_page, 'last_page': last_page, 'front_dots': front_dots,
                 'back_dots': back_dots, 'page': page, 'pages': pages, 'left_list': left_list,
                 'right_list': right_list, 'show_lst': show_lst, 'next_page': next_page,
                 'previous_page': previous_page, 'url': url}
    return paginator

def give_tag_list():
    blog_list = Blog.objects.all()
    for blog in blog_list:
        tags_list = blog.tags.all()
        tags_name_list = []
        for tag in tags_list:
            tags_name_list.append(tag.name)
        tags_str = ','.join(tags_name_list)
        blog.tag_list = tags_str
        blog.save()


def give_bool_tag():
    blog_list = Blog.objects.all()
    lst = ['Python', 'C++', 'C#', 'Java', 'JavaScript', 'PHP', 'SQL', 'else']
    for blog in blog_list:
        tags_list = blog.tags.all()
        for tag in tags_list:
            if tag.name == 'Python':
                blog.python_tag = True
            elif tag.name == 'C++':
                blog.c1_tag = True
            elif tag.name == 'C#':
                blog.c2_tag = True
            elif tag.name == 'Java':
                blog.java_tag = True
            elif tag.name == 'JavaScript':
                blog.javascript_tag = True
            elif tag.name == 'PHP':
                blog.php_tag = True
            elif tag.name == 'SQL':
                blog.sql_tag = True
            elif tag.name == 'else':
                blog.else_tag = True
        blog.save()
