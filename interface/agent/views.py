import os
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.signals import user_logged_out
from django.dispatch import receiver
from django.views import generic
from main import car

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
granddir = os.path.dirname(os.path.dirname(os.path.abspath(parentdir)))
os.sys.path.insert(0, granddir)


# from drive import Drive


class AgentView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'agent.html'

    def __init__(self):
        super(AgentView, self).__init__()
        # self.dive = Drive()

    @receiver(user_logged_out)
    def on_user_logged_out(sender, request, **kwargs):
        messages.add_message(request, messages.INFO, 'Logged out.')
