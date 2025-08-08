from gpiozero import LEDBoard, Button
from pythonosc import udp_client, osc_server
from pythonosc.dispatcher import Dispatcher

# Set up RNBO listener
client = udp_client.SimpleUDPClient("127.0.0.1", 1234)
client.send_message("/rnbo/listeners/add", "127.0.0.1:4321")

# Create a button object connected to Pin 21
button = Button(21)

# Create an LEDBoard object using the pins connected to our LEDs
leds = LEDBoard(17, 27, 22, 5, 6, 13, 19, 26)

# Initialize the local transport state
transport_running = False


def update_transport_state(path, transport_state):
    transport_state = bool(transport_state)
    print(path, transport_state)
    global transport_running
    # set the local transport state to the state received from RNBO
    transport_running = transport_state


def handle_step(path, step_idx):
    step_idx = int(step_idx)
    global transport_running, leds
    print("current step:", step_idx)
    led_vals = [0] * len(leds)
    led_vals[step_idx] = 1
    leds.value = tuple(led_vals)


def toggle_transport():
    global transport_running
    transport_running = not transport_running
    client.send_message("/rnbo/jack/transport/rolling", transport_running)


# Assign the toggle_transport function to the button callback
button.when_pressed = toggle_transport

# Create the OSC server and dispatcher map
dispatcher = Dispatcher()
dispatcher.map("/rnbo/jack/transport/rolling", update_transport_state)
dispatcher.map("/rnbo/inst/0/messages/out/step", handle_step)
dispatcher.set_default_handler(None)
server = osc_server.ThreadingOSCUDPServer(
    ("127.0.0.1", 4321), dispatcher)

print("Starting OSC server listening to RNBO... (Ctrl-C to exit)")
try:
    server.serve_forever(poll_interval=0.1)
except KeyboardInterrupt:
    pass
finally:
    print("Exiting...")
    server.server_close()
