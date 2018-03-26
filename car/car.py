class Car:
    def __init__(self, objects, threaded_objects):
        self.__threaded_objects = threaded_objects
        self.__motor = objects.get('Motor')
        self.__servo = objects.get('Servo')
        self.__status = objects.get('Status')
        self.__camera = objects.get('Camera')
        self.__ultrasonic = objects.get('Ultrasonic')

    def start_threads(self):
        for obj in self.__threaded_objects:
            obj.start()

    def turn_right(self):
        self.__servo.turn_right()

    def turn_left(self):
        self.__servo.turn_left()

    def move_forward(self):
        self.__motor.move_forward()

    def move_backward(self):
        self.__motor.move_backward()

    def brake(self):
        self.__motor.brake()

    def __del__(self):
        del self.__motor
        del self.__servo
        del self.__camera
        del self.__ultrasonic
        del self.__status
