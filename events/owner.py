from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView

from django.contrib.auth.mixins import LoginRequiredMixin


class OwnerListView(ListView):
    '''
       Using OOPs
    '''


class OwnerDetailView(DetailView):
    '''
        Using OOPs
    '''


class OwnerCreateView(LoginRequiredMixin, CreateView):

    def form_valid(self, form):
        print('form_valid called')
        object = form.save(commit=False)
        object.owner = self.request.user
        object.save()
        return super(OwnerCreateView, self).form_valid(form)


class OwnerUpdateView(LoginRequiredMixin, UpdateView):

    def get_queryset(self):
        print('update get_queryset called')

        qs = super(OwnerUpdateView, self).get_queryset()
        return qs.filter(owner=self.request.user)


class OwnerDeleteView(LoginRequiredMixin, DeleteView):

    def get_queryset(self):
        print('delete get_queryset called')
        qs = super(OwnerDeleteView, self).get_queryset()
        return qs.filter(owner=self.request.user)
