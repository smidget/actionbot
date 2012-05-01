import sys
sys.path.append("./")
import robochair
import time
import os

chair_speed = { "slow" : 1000,
                "medium" : 1300,
                "fast" : 1500,
                "fast2" : 2900 }

chair_ticks_per_rev = 14000

drive_distance_per_rev = None
drive_ticks_per_rev = None

drive_speed = {}

turn_speed = {}

history = []

def chair_degrees_to_ticks(degrees):
    ticks_per_degree = chair_ticks_per_rev / 360.0
    return degrees * ticks_per_degree

def drive_distance_to_ticks(meters):
    pass

class Motor:
    def __init__(self):
        self.name = "Disconnected"
        self.rd = robochair.RoboteqDevice()

    def setup(self, device):
        self.rd.Connect(device)
        self.name = self.rd.GetName()
        print "Successfully connected to motor " + self.name

    def shutdown(self):
        self.rd.Disconnect()

    def is_connected(self):
        return self.rd.IsConnected()

    def send_command(self, command, index, value):
        return self.rd.SetCommand(command, index, value)

    def get_revolutions(self):
        return int(self.rd.GetValue(robochair._ABCNTR, 1))

    def get_rpm(self):
        return ( int(self.rd.GetValue(robochair._ABSPEED, 1)),int(self.rd.GetValue(robochair._ABSPEED, 1)) )

    def get_config(self, config):
        return ( self.rd.GetConfig(config, 1), self.rd.GetConfig(config, 2) )

    def get_value(self, config):
        return ( int(self.rd.GetValue(config, 1)),int(self.rd.GetValue(config, 2)) )

class RoboChair:

  command_queue = []
  command_history = []
  dryrun = False
  rd = None

  def __init__(self):
      self.motors = {}

  def setup(self):
      # Cycle through all of the devices on /dev/tty.usb* and make objects for them
      motor_list = []
      device_names = []
      print "Attempting to connect to all three motors."
      while len(motor_list) < 3:
          time.sleep(0.5)
          for filename in os.listdir("/dev"):
              if "tty.usbmodem" in filename and filename not in device_names:
                  self.sleep()
                  m = Motor()
                  m.setup("/dev/"+filename)
                  if m.is_connected() and m.name in ["Left", "Right", "Chair"]:
                    motor_list.append(m)
                    device_names.append(filename)
                    print "SUCCESS: Connected to motor " + m.name
          motors_connected = [m.name for m in motor_list]
          if len(motors_connected) < 3:
              print "ERROR, unable to connect to a motor. Connected to " + " ".join(motors_connected)
              #exit()

      print "Successfully connected to motors " + " ".join(motors_connected)

      for m in motor_list:
          self.motors[m.name] = m



  def shutdown(self):
      for m in self.motors:
          self.motors[m].shutdown()

  def drive_turn(self, direction, degrees):
      pass

  def drive_forward(self):
    #print r.send_command("Left", robochair._ACCEL, 1, 10000)
    #print r.send_command("Left", robochair._ACCEL, 2, 10000)
    #print r.send_command("Right", robochair._ACCEL, 1, 10000)
    #print r.send_command("Right", robochair._ACCEL, 2, 10000)
    #self.sleep()
    for i in range(30):
        print r.send_command("Left", robochair._GO, 1, -300)
        print r.send_command("Left", robochair._GO, 2, -300)
        print r.send_command("Right", robochair._GO, 1, 300)
        print r.send_command("Right", robochair._GO, 2, 300)

    time.sleep(2)

  # Have this maybe step down into known intervals instead of percents?
  def rotate_chair(self, speed, direction, runtime, num_revs):
    start_time = time.time()
    rot_speed = chair_speed[speed]
    ticks_per_turn = chair_ticks_per_rev
    decel_ticks = 7000.0
    target_decel_speed = 550.0

    if direction == "ccw" or direction == "left" or direction == "l":
        rot_speed = -rot_speed
        num_revs = -num_revs
        target_decel_speed = -target_decel_speed

    start_rot = rot_speed
    decel_slope = -(start_rot - target_decel_speed) / decel_ticks
    start_ticks = r.get_revolutions("Chair")
    stop_ticks = start_ticks + (ticks_per_turn * num_revs)
    #while time.time() - start_time < runtime:

    curr_ticks = r.get_revolutions("Chair")

    print "Turning chair"
    i = 0
    ticks_remaining = (ticks_per_turn * num_revs) - (curr_ticks - start_ticks)
    while abs(ticks_remaining) > 0:
        ticks_remaining = (ticks_per_turn * num_revs) - (curr_ticks - start_ticks)
        if abs(ticks_remaining) < 100:
            self.send_go("Chair", 0)
            break
        elif abs(ticks_remaining) < decel_ticks: # Decelerate over 1/3 of the final turn
            rot_speed = int(decel_slope * (decel_ticks - abs(ticks_remaining)) + start_rot)

        print rot_speed
        self.send_go("Chair", rot_speed)

        curr_ticks = r.get_revolutions("Chair")
        i += 1

    self.send_go("Chair", 0)
    print curr_ticks - start_ticks

    #r.send_command("Chair", reobotchair._ESTOP, 1)

    #time.sleep(5)
    end_ticks = r.get_revolutions("Chair")

    print "Total ticks = ", end_ticks - start_ticks
    print time.time() - start_time
    #time.sleep(2)

  def send_command(self, motor_name, command, index, value):
    return self.motors[motor_name].send_command(command, index, value)

  def send_go(self, motorname, value):
      self.send_command(motorname, robochair._GO, 1, value)

  def get_revolutions(self, motor_name):
      return self.motors[motor_name].get_revolutions()

  def get_rpm(self, motor_name):
      return self.motors[motor_name].get_rpm()

  def get_config(self, motor_name, config):
      return self.motors[motor_name].get_config(config)

  def move_base(direction, **kwargs):
    distance = kwargs.get('distance', None)
    speed = kwargs.get('speed', None)
    time = kwargs.get('time', None)

    # Need two of the above vars to be defined in order to do anything

  def turn_base(self, degrees, speed):
    # Negative rotation is ccw, positive is cw
    #for i in range(100):
    for i in range(50):
        r.send_command("Left", robochair._GO, 1, -2000)
        r.send_command("Left", robochair._GO, 2, -2000)
        #r.send_command("Right", robochair._GO, -1024, 500)
        r.send_command("Right", robochair._GO, 1, 2000)
        r.send_command("Right", robochair._GO, 2, 2000)

        print "LEFT MOTOR", self.get_rpm("Left")
        #print r.send_command("Left", robochair._GO, 2, -400)
        print "RIGHT MOTOR", self.get_rpm("Right")
        #print r.send_command("Right", robochair._GO, 2, -40)

  def wait_for_input(self):
    pass

  def wait(self):
    pass

  def sleep(self):
    time.sleep(0.01)

  def handleReturnCode(code):
      pass

  def replay_history(self):
      pass

  def reverse_history(self):
      pass

r = RoboChair()
r.setup()
#print r.rd.IsConnected()
#print("set up")
#print("getting config")
#r.sleep()
#print r.rd.GetName()
#print r.get_config(robochair._TELES, 1)
#r.sleep()
#print r.send_command(robochair._ACCEL, 1, 100)

#print r.send_command(robochair._ACCEL, 0, 1500)
#r.sleep()
#print r.send_command(robochair._ACCEL, 1, 1000)
#print r.send_command(robochair._GO, -1024, 2000)
#r.sleep()
#print r.send_command(robochair._GO, 5, 4000)
#r.sleep()
#print r.send_command(robochair._GO, 2, 4000)
#r.sleep()
#print r.send_command(robochair._GO, 2, 2000)
#r.drive_forward()
#for i in range(30):
    #r.rotate_chair("fast", "ccw", 10, 0.5)
    #time.sleep(2)
    #r.rotate_chair("fast", "cw", 10, 0.5)
    #time.sleep(5)
#r.rotate_chair("fast", "ccw", 10, 0.5)
print r.get_config("Left", robochair._MAC)
#r.turn_base(0,0)
#while True:
    #pass
    #print r.get_revolutions("Chair")
#print r.get_revolutions("Chair")
#print r.send_command(robochair._ESTOP, 0, 1)
r.shutdown()
print("shut down")
