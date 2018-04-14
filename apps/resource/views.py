from django.shortcuts import render_to_response
from pure_pagination import Paginator
from django.views import View

from resource.models import YearBookDes, YearBookContent, YearBook


class ResourceView(View):
    def get(self, request):
        year = request.GET.get('select', "2016")
        yearlist = YearBookDes.objects.all().order_by('-year')
        yearsinfo = yearlist.get(year=year)

        sunxu = request.GET.get('shunxu', 0)

        page = request.GET.get('page', 0)
        content = YearBookContent.objects.filter(year=year)
        if sunxu:
            mulu = YearBookContent.objects.get(year=year, index=sunxu).content
            items = YearBook.objects.filter(year=year, category=mulu).order_by("id")
        else:
            items = YearBook.objects.filter(year=year).order_by("id")

        counts = items.count()
        items = Paginator(items, 20, request=request)
        items = items.page(page)
        return render_to_response("years.html",
                                  context={
                                      "yearsinfo": yearsinfo,
                                      "content": content,
                                      "items": items,
                                      "yearlist": yearlist,
                                      "counts": counts,
                                  })

