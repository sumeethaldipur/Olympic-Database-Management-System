from events.models import Event, Comment, Imp, Athlete, Participation
from events.owner import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView
from events.forms import CreateForm, CommentForm
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from events.utils import dump_queries
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.db.models import Q

from django.core.files.uploadedfile import InMemoryUploadedFile


from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.utils import IntegrityError


class EventListView(OwnerListView):
    model = Event

    template_name = "events/event_list.html"
    def get(self, request) :
        event_list = Event.objects.all()
        important = list()
        if request.user.is_authenticated:
            rows = request.user.important_events.values('id')
            important = [ row['id'] for row in rows ]

        strval =  request.GET.get("search", False)
        if strval :

            query = Q(name__contains=strval)
            query.add(Q(stadium__contains=strval), Q.OR)
            objects = Event.objects.filter(query).select_related().order_by('-updated_at')[:10]
        else :

            objects = Event.objects.all().order_by('-updated_at')[:10]

        for obj in objects:
            obj.natural_updated = naturaltime(obj.updated_at)

        ctx = {'event_list0' : event_list, 'important': important, 'event_list' : objects, 'search': strval}
        retval = render(request, self.template_name, ctx)

        dump_queries()
        return retval;





class EventDetailView(OwnerDetailView):
    model = Event
    template_name = "events/event_detail.html"
    #athletes = list()
    def get(self, request, pk) :
        x = Event.objects.get(id=pk)
        comments = Comment.objects.filter(event=x).order_by('-updated_at')
        comment_form = CommentForm()
        #rows = request.x.athlete_list.values('id')
        athletes = Participation.objects.filter(event=x)

        #athletes = Participation.objects.filter(event=x)
        context = { 'event' : x, 'comments': comments, 'comment_form': comment_form, 'athlete_list': athletes }
        return render(request, self.template_name, context)


class EventCreateView(LoginRequiredMixin, View):
    template_name = 'events/event_form.html'
    success_url = reverse_lazy('events:all')
    def get(self, request, pk=None) :
        form = CreateForm()
        ctx = { 'form': form }
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None) :
        form = CreateForm(request.POST, request.FILES or None)

        if not form.is_valid() :
            ctx = {'form' : form}
            return render(request, self.template_name, ctx)

        event = form.save(commit=False)
        event.owner = self.request.user
        event.save()
        return redirect(self.success_url)


class EventUpdateView(LoginRequiredMixin, View):
    template_name = 'events/event_form.html'
    success_url = reverse_lazy('events:all')
    def get(self, request, pk) :
        event = get_object_or_404(Event, id=pk, owner=self.request.user)
        form = CreateForm(instance=event)
        ctx = { 'form': form }
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None) :
        event = get_object_or_404(Event, id=pk, owner=self.request.user)
        form = CreateForm(request.POST, request.FILES or None, instance=event)

        if not form.is_valid() :
            ctx = {'form' : form}
            return render(request, self.template_name, ctx)

        event = form.save(commit=False)
        event.save()

        return redirect(self.success_url)


class EventDeleteView(OwnerDeleteView):
    model = Event


def stream_file(request, pk) :
    event = get_object_or_404(Event, id=pk)
    response = HttpResponse()
    response['Content-Type'] = event.content_type
    response['Content-Length'] = len(event.picture)
    response.write(event.picture)
    return response


class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        e = get_object_or_404(Event, id=pk)
        comment = Comment(text=request.POST['comment'], owner=request.user, event=e)
        comment.save()
        return redirect(reverse('events:event_detail', args=[pk]))


class CommentDeleteView(OwnerDeleteView):
    model = Comment
    template_name = "events/comment_delete.html"

    def get_success_url(self):
        event = self.object.event
        return reverse('events:event_detail', args=[event.id])


@method_decorator(csrf_exempt, name='dispatch')
class AddImportantView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        print("Add PK",pk)
        t = get_object_or_404(Event, id=pk)
        imp = Imp(user=request.user, event=t)
        try:
            imp.save()
        except IntegrityError as e:
            pass
        return HttpResponse()


@method_decorator(csrf_exempt, name='dispatch')
class DeleteImportantView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        print("Delete PK",pk)
        t = get_object_or_404(Event, id=pk)
        try:
            imp = Imp.objects.get(user=request.user, event=t).delete()
        except Imp.DoesNotExist as e:
            pass

        return HttpResponse()
