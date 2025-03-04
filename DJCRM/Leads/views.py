from django.core.mail import send_mail
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.views import generic 
# its used for her ik ko apna login admin ban saky 
from django.contrib.auth.mixins import LoginRequiredMixin
# from django.views.generic import TemplateView , ListView ,DetailView,CreateView, UpdateView, DeleteView
from .models import Lead, Agent,Category
from agents.mixins import OrganisorAndLoginRequiredMixin
from .forms import LeadForm , LeadModelForm ,CustomUsercreationForm , AssignAgentForm, LeadCategoryUpdateForm
# Create your views here.

# CRUD+L - Create , Retrieve, update and Delete - List
class SignupView(generic.CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUsercreationForm

    def get_success_url(self):
        return reverse("login")

class LandingPageView(generic.TemplateView):
    template_name = "landing.html"


# def landing_page(request):
#     return render(request,"landing.html")


class LeadListView(LoginRequiredMixin , generic.ListView):
    template_name = "Leads/lead_list.html"
    context_object_name = "leads"
    
    def get_queryset(self):
        user = self.request.user
            # initial Queryset of leads for the entire organisation
        if user.is_organisor:
            queryset = Lead.objects.filter(organisation=user.userprofile,agent__isnull= False)
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organisation,agent__isnull=False)
            # filter for the agent that is logged in 
            queryset = queryset.filter(agent__user=user)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super(LeadListView,self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organisor:
            queryset = Lead.objects.filter(
                organisation=user.userprofile,
                agent__isnull=True
                )
            context.update({
                "unassigned_leads":queryset
            })
        return context 
      

# def lead_list(request):
#     # return HttpResponse("hello world")
#     # return render(request, "Leads/home_page.html")
#     Leads = Lead.objects.all()
#     context={
#        "Leads" : Leads
#     }
#     return render(request,"Leads/lead_list.html",context)


class  LeadDetailView(LoginRequiredMixin , generic.DetailView):
    template_name = "Leads/lead_detail.html"
    # queryset = Lead.objects.all()
    context_object_name = "lead"

    def get_queryset(self):
        user = self.request.user
            # initial Queryset of leads for the entire organisation
        if user.is_organisor:
            queryset = Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organisation)
            # filter for the agent that is logged in 
            queryset = queryset.filter(agent__user=user)
        return queryset




# def lead_detail(request,pk):
#     lead = Lead.objects.get(id=pk)
#     context ={
#        "lead": lead
#    }
#     return render(request,"Leads/lead_detail.html",context)

# class LeadCreateView(LoginRequiredMixin ,generic.CreateView):

class LeadCreateView(OrganisorAndLoginRequiredMixin, generic.CreateView):
    template_name = "leads/lead_create.html"
    form_class = LeadModelForm

    def get_success_url(self):
        return reverse("Leads:lead-list")

    def form_valid(self, form):
        lead = form.save(commit=False)
        lead.organisation = self.request.user.userprofile
        lead.save()
        send_mail(
            subject="A lead has been created",
            message="Go to the site to see the new lead",
            from_email="test@test.com",
            recipient_list=["test2@test.com"]
        )
        # messages.success(self.request, "You have successfully created a lead")
        return super(LeadCreateView, self).form_valid(form)
    
        
# def lead_create(request):
#     form = LeadModelForm()
#     if request.method == "POST":
#         form = LeadModelForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect("Leads/")
#     context={
#         "form" : form
#     }
#     return render(request,"Leads/lead_create.html",context)


# def lead_create(request):
#     form = LeadForm()
#     if request.method == "POST":
#         form = LeadForm(request.POST)
#         if form.is_valid():
#             first_name = form.cleaned_data['first_name']
#             last_name = form.cleaned_data['last_name']
#             age = form.cleaned_data['age']
#             agent = form.cleaned_data['agent']
#             Lead.objects.create(
#                 first_name=first_name,
#                 last_name= last_name,
#                 age=age,
#                 agent=agent,
#             )
#             return redirect("Leads/")
#     context={
#         "form" : LeadForm()
#     }
#     return render(request,"Leads/lead_create.html",context)




# def lead_update(request,pk):
#     lead = Lead.objects.get(id=pk)
#     form = LeadForm()
#     if request.method == "POST":
#         form = LeadForm(request.POST)
#         if form.is_valid():
#             first_name = form.cleaned_data['first_name']
#             last_name = form.cleaned_data['last_name']
#             age = form.cleaned_data['age']
#             lead.first_name = first_name
#             lead.last_name = last_name
#             lead.age = age
#             lead.save()
#             return redirect("/Leads")
#     context = {
#         "form" : form,
#         "lead" : lead 
#     }
#     return render(request, "Leads/lead_update.html",context)

class LeadUpdateView(OrganisorAndLoginRequiredMixin ,generic.UpdateView):
    template_name = "Leads/lead_update.html"
    # queryset = Lead.objects.all()
    form_class = LeadModelForm
    def get_queryset(self):
        user = self.request.user
            # initial Queryset of leads for the entire organisation
        return  Lead.objects.filter(organisation=user.userprofile)
    def get_success_url(self):
        return  reverse("Leads:lead-list")
  

# def lead_update(request,pk):
#     lead = Lead.objects.get(id=pk)
#     form = LeadModelForm(instance=lead)
#     if request.method == "POST":
#         form = LeadModelForm(request.POST,instance=lead)
#         if form.is_valid():
#             form.save()
#             return redirect("/Leads")
#     context = {
#         "form" : form,
#         "lead" : lead 
#     }
#     return render(request, "Leads/lead_update.html",context)



class LeadDeleteView(OrganisorAndLoginRequiredMixin, generic.DeleteView):
    template_name = "Leads/lead_delete.html"

    def get_success_url(self):
        return reverse("Leads:lead-list")

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        return Lead.objects.filter(organisation=user.userprofile)

# def lead_delete(request,pk):
#     lead = Lead.objects.get(id=pk)
#     lead.delete()
#     return redirect("/Leads")


class AssignAgentView(OrganisorAndLoginRequiredMixin,generic.FormView):
    template_name = "Leads/assign_agent.html"
    form_class = AssignAgentForm

    def get_form_kwargs(self,**kwargs):
        kwargs = super(AssignAgentView,self).get_form_kwargs(**kwargs)
        kwargs.update({
            "request":self.request
        })
        return kwargs

    def get_success_url(self):
        return reverse("Leads:lead-list")
    
    def form_valid(self, form):
        agent = form.cleaned_data["agent"]
        lead = Lead.objects.get(id=self.kwargs["pk"])
        lead.agent = agent
        lead.save()
        return super(AssignAgentView,self).form_valid(form)
    
class CategoryListView(LoginRequiredMixin,generic.ListView):
    template_name = "Leads/category_list.html"
    context_object_name = "category_list"
    
    def get_context_data(self, **kwargs):
        context = super(CategoryListView,self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organisor:
            queryset = Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organisation)
           
        context.update({
            "unassigned_lead_count":queryset.filter(Category__isnull=True).count()
        })
        return context


    def get_queryset(self):
        user = self.request.user
            # initial Queryset of leads for the entire organisation
        if user.is_organisor:
            queryset = Category.objects.filter(organisation=user.userprofile)
        else:
            queryset = Category.objects.filter(organisation=user.agent.organisation)
            # filter for the agent that is logged in 
        return queryset
    



class CategoryDetailView(LoginRequiredMixin,generic.DetailView):
    template_name = "Leads/category_detail.html"
    context_object_name = "category"
 
    # def get_context_data(self, **kwargs):
    #     context = super(CategoryDetailView,self).get_context_data(**kwargs)
    #     leads = self.get_object().leads.all()
    #     context.update({
    #        "leads":leads
    #     })
    #     return context

    def get_queryset(self):
        user = self.request.user
            # initial Queryset of leads for the entire organisation
        if user.is_organisor:
            queryset = Category.objects.filter(organisation=user.userprofile)
        else:
            queryset = Category.objects.filter(organisation=user.agent.organisation)
            # filter for the agent that is logged in 
        return queryset

    
class LeadCategoryUpdateView(LoginRequiredMixin,generic.UpdateView):
    template_name = "Leads/lead_category_update.html"
    # queryset = Lead.objects.all()
    form_class = LeadCategoryUpdateForm  
    
    
    def get_queryset(self):
        user = self.request.user
            # initial Queryset of leads for the entire organisation
        if user.is_organisor:
            queryset = Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organisation)
            # filter for the agent that is logged in 
            queryset = queryset.filter(agent__user=user)
        return queryset
   
    def get_success_url(self):
        return  reverse("Leads:lead-detail",kwargs={"pk":self.get_object().id})
  

# class LeadCategoryUpdateView(LoginRequiredMixin, generic.UpdateView):
#     template_name = "Leads/lead_category_update.html"
#     form_class = LeadCategoryUpdateForm  

#     def get_queryset(self):
#         user = self.request.user
#         # Initial queryset of leads for the entire organization
#         if user.is_organisor:
#             queryset = Lead.objects.filter(organisation=user.userprofile)
#         else:
#             # Filter for leads related to the agent's organization
#             queryset = Lead.objects.filter(organisation=user.agent.organisation)
#             # Further filter for the agent who is logged in
#             queryset = queryset.filter(agent__user=user)
#         return queryset

#     def get_success_url(self):
#         return reverse("Leads:lead-list")




# command k and command 0 is close the all function