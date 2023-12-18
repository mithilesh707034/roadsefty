from django.shortcuts import render

def home_page(Request):
    return render(Request,'index.html')

def about_page(Request):
    return render(Request,'about.html')

def blog_page(Request):
    return render(Request,'blog.html')

def single_blog_page(Request):
    return render(Request,'blog-single.html')

def contact_page(Request):
    return render(Request,'contact.html')
