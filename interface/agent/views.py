import os
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.signals import user_logged_out
from django.dispatch import receiver
from django.views import generic
from main import Main as Access
from django.views.decorators import gzip
from django.http import HttpResponseServerError, StreamingHttpResponse, JsonResponse

Main = Access()
logger = Access.logger


class AgentView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'agent.html'

    def __init__(self):
        super(AgentView, self).__init__()

    @receiver(user_logged_out)
    def on_user_logged_out(sender, request, **kwargs):
        messages.add_message(request, messages.INFO, 'Logged out.')


def get_logs(request):
    data = {}
    while not logger.interface_msgs.empty():
        logs = []
        log = logger.interface_msgs.get().replace('\n', '')
        log = log.replace('##', '')
        logs.append(log)
        data = {'log': logs}
    return JsonResponse(data)


def gen(is_rest):
    while not is_rest:
        frame = Main.car.camera.byte_frame
        if frame is None:
            print('now')
            continue
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
    http_rest = False


http_rest = True


@gzip.gzip_page
def video(request):
    try:
        is_rest = not http_rest
        return StreamingHttpResponse(gen(is_rest), content_type="multipart/x-mixed-replace;boundary=frame")
    except HttpResponseServerError as e:
        print("aborted")