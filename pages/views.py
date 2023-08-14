from django.shortcuts import render # here by default
from django.http import HttpResponse, HttpResponseRedirect # new
from django.views.generic import TemplateView
from django.views import View
from django import forms
from django.shortcuts import render, redirect


class Product:
    products = [
        {"id":"1", "name":"TV", "description":"It's a TV", "price":2500000},
        {"id":"2", "name":"iPhone", "description":"Why not an iPhone", "price":5500000},
        {"id":"3", "name":"Chromecast", "description":"Just a Chromecast", "price":500000},
        {"id":"4", "name":"Glasses", "description":"Cheap Glasses","price":99 }
    ]

class ProductIndexView(View):
    template_name = 'products/index.html'

    def get(self, request):
        viewData = {}
        viewData["title"] = "Products - Online Store"
        viewData["subtitle"] =  "List of products"
        viewData["products"] = Product.products

        return render(request, self.template_name, viewData)

class ProductShowView(View):
    template_name = 'products/show.html'
    def get(self, request, id):
        viewData = {}
        try:
            product = Product.products[int(id)-1]
            viewData["title"] = product["name"] + " - Online Store"
            viewData["subtitle"] =  product["name"] + " - Product information"
            viewData["product"] = product
            return render(request, self.template_name, viewData)
        except:
            return HttpResponseRedirect("/")
       
        



# Create your views here.
def homePageView(request): # new
    return HttpResponse('Hello World!') # new
class HomePageView(TemplateView):
    template_name = "pages/home.html"


class AboutPageView(TemplateView):
    template_name = "pages/about.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "About us - Online Store",
            "subtitle": "About us",
            "description": "This is an about page ...",
            "author": "Developed by: Daniel Gonzalez",
        })

        return context

class ContactPageView(TemplateView):
    template_name = "pages/contact.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Contact us - Online Store",
            "subtitle": "Contact us",
            "author": "Developed by: Daniel Gonzalez",
        })

        return context
    
class ProductForm(forms.Form):
    name = forms.CharField(required=True)
    price = forms.FloatField(required=True)
    description = forms.CharField(required=True)
    def clean_price(self):
        price = self.cleaned_data['price']
        if (price <= 0):
            raise forms.ValidationError("Precio errado")
        return price


class ProductCreateView(View):
    template_name = 'products/create.html'
    creado = 'products/creado.html'

    def get(self, request):
        form = ProductForm()
        viewData = {}
        viewData["title"] = "Create product"
        viewData["form"] = form
        return render(request, self.template_name, viewData)

    def post(self, request):
        form = ProductForm(request.POST)
        viewData = {}
        viewData["form"] = form.data
        if form.is_valid():
            id = len(Product.products)+1
            Product.products.append({"id":id, "name":form.data['name'], "description":form.data['description'], "price":int(form.data['price'])})
            return render(request,self.creado,viewData) 
        else:
            viewData = {}
            viewData["title"] = "Create product"
            viewData["form"] = form
            return render(request, self.template_name, viewData)
        
class ProductCreadoView(TemplateView):
    template_name = 'products/creado.html'


