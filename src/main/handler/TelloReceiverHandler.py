from djitellopy import Tello


def receive():
    while True:
        print(Tello.udp_response_receiver())
