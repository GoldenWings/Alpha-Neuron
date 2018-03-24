from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.signals import user_logged_out
from django.dispatch import receiver
from django.views import generic
from django.http import JsonResponse
import psutil
from controllers.gamepad import GamePad
from asyncore import loop


class TrainerView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'trainer.html'
    gamepad = None
    gamepad_isListening = False

    def __init__(self):
        super(TrainerView, self).__init__()
        TrainerView.gamepad = GamePad()
        TrainerView.gamepad.activate_tranier()
        # if self.gamepad_isListening is False:
        #     self.gamepad_isListening = True
        #     loop()


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
        radar = TrainerView.gamepad.radar_data
    elif command == 'deactivate':
        radar = TrainerView.gamepad.deactivate_trainer()
    elif command == 'usage':
        processor = psutil.cpu_percent()
        ram = psutil.virtual_memory().used / psutil.virtual_memory().total*100
    elif command == 'get_data':
        speed = TrainerView.gamepad.current_speed
    speed = TrainerView.gamepad.current_speed
    data = {'speed': speed, 'radar': radar, 'processor': processor, 'ram': ram}
    return JsonResponse(data)


def start_recording(request):
    TrainerView.gamepad.start_recording()
    data = {'clicked': 'start'}
    return JsonResponse(data)


def pause_recording(request):
    TrainerView.gamepad.pause_recording()
    data = {'clicked': 'pause'}
    return JsonResponse(data)


def stop_recording(request):
    TrainerView.gamepad.stop_recording()
    data = {'clicked': 'stop'}
    return JsonResponse(data)
