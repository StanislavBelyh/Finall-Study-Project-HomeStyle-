from django.http import HttpResponse
from django.shortcuts import render
from django.template import context
from django.views.generic import TemplateView

from goods.models import Categories


class IndexView(TemplateView):
    template_name = "main/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "HomeStyle - Главная страница"
        context["content"] = "Магазин мебели HomeStyle"
        return context


class AboutView(TemplateView):
    template_name = "main/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "HomeStyle - О нас"
        context["content"] = "HomeStyle - О нас:"
        context["text_on_page"] = (
            "Мы предлагаем широкий ассортимент мебели для вашего дома и офиса. Наша миссия - сделать ваш дом уютным и стильным с помощью качественной мебели по доступным ценам."
        )
        return context


# def index(request):

#     context = {
#         "title": "HomeStyle - Главная страница",
#         "content": "Магазин мебели HomeStyle",
#     }
#     return render(request, "main/index.html", context)


# def about(request):
#     context = {
#         "title": "HomeStyle - О нас",
#         "content": " HomeStyle - О нас:",
#         "text_on_page": "Мы предлагаем широкий ассортимент мебели для вашего дома. Наша миссия - сделать ваш дом уютным и стильным с помощью качественной мебели по доступным ценам.",
#     }
#     return render(request, "main/about.html", context)
