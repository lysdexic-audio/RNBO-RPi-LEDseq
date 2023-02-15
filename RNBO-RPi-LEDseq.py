from gpiozero import LEDBoard, Button
import liblo as OSC
import sys

# set up OSC client - send all messages to port 1234 on the local machine (rnbo runner)
try:
    target = OSC.Address(1234)
except OSC.AddressError as err:
    print(err)
    sys.exit()
    
# set up OSC server - listening on port 4321
try:
    server = OSC.Server(4321)
except OSC.ServerError as err:
    print(err)

def update_transport_state(path, args):
    i = args[0]
    global transport_running
    transport_running = bool(i)

def handle_step(path, args):
    i = args[0]
    global transport_running
    print("current step:", i)
    led_vals = [0] * len(leds)
    led_vals[i] = 1
    leds.value = tuple(led_vals)

def fallback(path, args, types, src):
    print("got unknown message '%s' from '%s'" % (path, src.url))
    print("don't panic - probably just the runner echoing back your changes :)")
    for a, t in zip(args, types):
        print("argument of type '%s': %s" % (t, a))

# register callback methods for server routes
server.add_method("/rnbo/jack/transport/rolling", None, update_transport_state)
server.add_method("/rnbo/inst/0/messages/out/step", 'i', handle_step)

# Finally add fallback method for unhandled OSC addrs
server.add_method(None, None, fallback)

# Set up RNBO OSC listener
OSC.send(target, "/rnbo/listeners/add", f"127.0.0.1:4321")

# create a button object
button = Button(21)

# create an LEDBoard object representing our array of LEDs
leds = LEDBoard(17, 27, 22, 5, 6, 13, 19, 26)

def toggle_transport():
    global transport_running
    transport_running = not transport_running
    OSC.send(target, "/rnbo/jack/transport/rolling", transport_running)⁠

button.when_pressed = toggle_transport

transport_running = True
OSC.send(target, "/rnbo/jack/transport/rolling", transport_running)

try:
    while True:
        server.recv(100)        
        
except KeyboardInterrupt:
    print("exiting cleanly...")
                