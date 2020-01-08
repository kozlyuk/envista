from django.views.generic import DetailView

from product.models import Product


class MainView(DetailView):
    """ MainView - main landing page """
    model = Product
    template_name = 'main.j2'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news_list'] = News.objects.filter(
            houses=None,
            actual_from__lte=date.today(), actual_to__gte=date.today())
        return context

    def get_object(self, queryset=None):
        try:
            return Product.objects.first()
        except self.model.DoesNotExist:
            raise PermissionDenied
