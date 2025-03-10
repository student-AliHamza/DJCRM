
from django.urls import path
from .views import  LeadListView , LeadDetailView ,LeadUpdateView ,CategoryListView  ,LeadDeleteView  , LeadCreateView  , AssignAgentView , CategoryDetailView ,LeadCategoryUpdateView

    # lead_list , lead_detail, lead_create,lead_update,lead_delete,

app_name = "Leads"

urlpatterns = [
    path('', LeadListView.as_view(),name = 'lead-list'),
    path('<int:pk>/',LeadDetailView.as_view(), name = 'lead-detail'),
    path('<int:pk>/update/',LeadUpdateView.as_view(),name='lead-update'),
    path('<int:pk>/delete/',LeadDeleteView.as_view(),name ='lead-delete'),
    path('<int:pk>/assign-agent/',AssignAgentView.as_view(),name= 'assign-agent'),
    path('<int:pk>/category/',LeadCategoryUpdateView.as_view(),name= 'lead-category-update'),
    path('create/',LeadCreateView.as_view(),name= 'lead-create'),
    path('categories/',CategoryListView.as_view(),name= 'category-list'),
    path('categories/<int:pk>/',CategoryDetailView.as_view(),name= 'category-detail')

]

