from django.contrib.postgres.search import (
    SearchVector,
    SearchQuery,
    SearchRank,
    SearchHeadline,
)
from django.db.models import Q

from goods.models import Products


def q_search(query):
    if query.isdigit() and len(query) <= 5:
        return Products.objects.filter(id=int(query))

    vector = SearchVector("name", "description")
    query = SearchQuery(query)

    search_results = (
        Products.objects.annotate(rank=SearchRank(vector, query))
        .filter(rank__gt=0)
        .order_by("-rank")
    )

    search_results = search_results.annotate(
        headline=SearchHeadline(
            "name",
            query,
            start_sel="<span style='background-color: red;'>",
            stop_sel="</span>",
        )
    )

    search_results = search_results.annotate(
        bodyline=SearchHeadline(
            "description",
            query,
            start_sel="<span style='background-color: red;'>",
            stop_sel="</span>",
        )
    )

    return search_results

    # keywords = [word for word in query.split() if len(word) > 2]
    # q_objects = Q()
    # for keyword in keywords:
    #     q_objects |= Q(name__icontains=keyword) | Q(description__icontains=keyword)
    # return Products.objects.filter(q_objects)
