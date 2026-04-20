from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from diary.models import Note
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied


class NoteListView(LoginRequiredMixin, ListView):
    model = Note

    def get_queryset(self):
        queryset = Note.objects.filter(author=self.request.user)

        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(content__icontains=query)
            )
        return queryset


class NoteDetailView(LoginRequiredMixin, DetailView):
    model = Note

    def get_queryset(self):
        queryset = Note.objects.filter(author=self.request.user)


class NoteCreateView(LoginRequiredMixin, CreateView):
    model = Note
    fields = ('title', 'content', 'preview',)
    success_url = reverse_lazy('diary:note_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class NoteUpdateView(LoginRequiredMixin, UpdateView):
    model = Note
    fields = ('title', 'content', 'preview',)
    success_url = reverse_lazy('diary:note_list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.author != self.request.user:
            raise PermissionDenied  # Ошибка 403, если полез в чужое
        return obj


class NoteDeleteView(LoginRequiredMixin, DeleteView):
    model = Note
    success_url = reverse_lazy('diary:note_list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.author != self.request.user:
            raise PermissionDenied
        return obj
