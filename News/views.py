from django.shortcuts import render, redirect
from .models import Artciels,Comments,Category
# Create your views here.


def blog(request):
    articles = Artciels.objects.all().order_by('-date')
    return render(request,'news.html',{'articles':articles})

def category_blog(request, category_name):
    articles = Artciels.objects.filter(news_category__name = 
                                       category_name).order_by('-date')
    return render(request,'news.html',{'articles':articles})


def blog_detail(request, title1):
    article = Artciels.objects.get(title = title1 )
    comments = Comments.objects.filter(post__title = article.title ) 
    print(article.news_category)
    related_articles = Artciels.objects.filter(news_category__name = article.news_category).exclude(title = title1)

    if request.method == 'POST':
      email  = request.POST.get('user_email')
      text  = request.POST.get('user_comment')
      comment_obj  = Comments()
      comment_obj.email = email
      comment_obj.comment = text
      comment_obj.post = Artciels.objects.get(title = title1 )
      comment_obj.save()

    return render(request,'news_detail.html',{'article':article,'related_articles':related_articles,'comments':comments})


def category_list(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name')
        obj = Category()
        obj.name = name
        obj.save()
    return render(request, 'category.html',{'categories':categories})


def news_admin(request):
    news = Artciels.objects.filter(visble = True)
    categories = Category.objects.values('name')
    if request.method =='POST':
        title  = request.POST.get('title')
        news_category  = request.POST.get('news_category')
        image = request.FILES.get('image')
        description  = request.POST.get('description')
        print(news_category)
        obj = Artciels()
        obj.title  = title
        obj.description = description
        obj.image  = image
        obj.news_category = Category.objects.get(name = news_category)
        obj.save()

    return render(request, 'news_admin.html',{'news':news,'categories':categories})


def article_edit(request,news_id):
    news = Artciels.objects.get(id = news_id)
    if request.method =='POST':
        title  = request.POST.get('title')
        news_category  = request.POST.get('news_category')
        image = request.FILES.get('image')
        description  = request.POST.get('description')
        print(news_category)
        obj = news
        obj.title  = title
        obj.description = description
        obj.image = image if image != None else obj.image 
        obj.news_category = Category.objects.get(id = news_category)
        obj.save()


    categories = Category.objects.values('name','id')
    return render(request,'edit_news.html',{'article':news,'categories':categories})



def delete_news(request, news_id):
    news = Artciels.objects.get(id = news_id)
    news.visble = False
    news.save()
    return redirect( 'news_admin_url')