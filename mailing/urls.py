from django.urls import path

#from mailing.views import MailingListView, MailingDetailView, MailingCreate
from mailing.views import MailingListView, MailingDetailView, MailingCreateView


urlpatterns = [
    path('', MailingListView.as_view(), name='mailing_list'),
    path('<int:pk>', MailingDetailView.as_view(), name='mailing_detail'),
    path('create/', MailingCreateView.as_view(), name='mailing_create'),
]