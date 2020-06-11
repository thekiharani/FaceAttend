from django.views.generic import TemplateView
from django.urls import reverse_lazy

class HomeView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['classes'] = Post.objects.all()
        return context

    template_name = 'attendance/home.html'
