from django.shortcuts import render
from product.models import Product
from django.db.models import Q

# Create your views here.


def search(request):
    query = request.GET.get("search", None)

    if query is not None and query != "":
        result =Product.objects.search(query)
    else:
        result = Product.objects.none()
    return render(request, "search/search.html", {"result": result})
