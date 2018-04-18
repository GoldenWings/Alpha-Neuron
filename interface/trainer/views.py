import psutil
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.signals import user_logged_out
from django.dispatch import receiver
from django.http import HttpResponseServerError, StreamingHttpResponse, HttpResponse
from django.http import JsonResponse
from django.views import generic
from django.views.decorators import gzip
from main import Main as Access
Main = Access()
logger = Access.logger


class TrainerView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'trainer.html'

    def __init__(self):
        super(TrainerView, self).__init__()

    @receiver(user_logged_out)
    def on_user_logged_out(sender, request, **kwargs):
        messages.add_message(request, messages.INFO, 'Logged out.')


def send_command(request):
    radar = []
    processor = 0
    ram = 0
    command = request.GET.get('command', None)
    if command is None:
        return
    elif command == 'radar':
        radar = list(Main.car.ultrasonic.get_frame().values())
    elif command == 'usage':
        processor = psutil.cpu_percent()
        ram = psutil.virtual_memory().used / psutil.virtual_memory().total*100
    elif command == 'get_data':
        speed = Main.car.current_speed
    speed =Main.car.current_speed
    data = {'speed': speed, 'radar': radar, 'processor': processor, 'ram': ram, 'status':
        Main.car.status.is_agent}
    return JsonResponse(data)


def gen():
    while True:
        frame = Main.car.camera.byte_frame
        if frame is None:
            continue
        elif Main.car.status.is_agent:
            break
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@gzip.gzip_page
def video(request):
    try:
        return StreamingHttpResponse(gen(), content_type="multipart/x-mixed-replace;boundary=frame")
    except HttpResponseServerError as e:
        print("aborted")


def get_logs(request):
    data = {'status': Main.car.status.is_agent}
    while not logger.interface_msgs.empty():
        logs = []
        log = logger.interface_msgs.get().replace('\n', '')
        log = log.replace('##', '')
        logs.append(log)
        data['log'] = logs
        if Main.car.status.is_agent:
            print('UMMM')
            break
    return JsonResponse(data)
