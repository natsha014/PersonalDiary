from diary.apps import DiaryConfig
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from diary.views import NoteListView, NoteDetailView, NoteCreateView, NoteUpdateView, NoteDeleteView, NoteTemplateView

app_name = DiaryConfig.name

urlpatterns = [
    path('', NoteListView.as_view(), name='note_list'),
    path('diary/<int:pk>/', NoteDetailView.as_view(), name='note_detail'),
    path('diary/create/', NoteCreateView.as_view(), name='note_create'),
    path('diary/<int:pk>/update/', NoteUpdateView.as_view(), name='note_update'),
    path('diary/<int:pk>/delete/', NoteDeleteView.as_view(), name='note_delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
