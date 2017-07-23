from light import Light, HUE_BRIDGE_IP, HUE_BRIDGE_USERNAME
from datetime import datetime, date, time
import time as time2

START_TIME = time(11, 00)
END_TIME = time(12, 00)
STARTING_BRIGHTNESS = 254
ENDING_BRIGHTNESS = 100

# only needs computed once:
TEMP_START_TIME = datetime.combine(date.today(), time(21, 00))
TEMP_END_TIME = datetime.combine(date.today(), time(22, 00))
DROPOFF_TOTAL_SECONDS = (TEMP_END_TIME - TEMP_START_TIME).total_seconds()
BRIGHTNESS_RANGE = STARTING_BRIGHTNESS - ENDING_BRIGHTNESS
BRIGHTNESS_DROP_PER_SECOND = float(BRIGHTNESS_RANGE) / DROPOFF_TOTAL_SECONDS


def run_evening_light_dimmer():
  lights = Light.build_lights()

  while True:
    current_time = datetime.now()
    today_start_time = datetime.combine(date.today(), START_TIME)
    today_end_time = datetime.combine(date.today(), END_TIME)
    if current_time < today_start_time:
      time2.sleep(300)  # sleep 5 minutes
      continue

    if current_time > today_end_time:
      # after fading period but before 11:59pm
      desired_brightness = ENDING_BRIGHTNESS
    else:
      desired_brightness = _get_current_desired_brightness(today_start_time)
    
    Light.update_lights(lights)

    for light in lights:
      light.set_brightness(desired_brightness)

    time2.sleep(5)


def _get_current_desired_brightness(today_start_time):
  current_time = datetime.now()
  seconds_from_start = (current_time - today_start_time).total_seconds()
  return int(
    STARTING_BRIGHTNESS - seconds_from_start * BRIGHTNESS_DROP_PER_SECOND)


def _get_current_temp(bridge=None):
  if not bridge:
      bridge = Bridge(HUE_BRIDGE_IP, HUE_BRIDGE_USERNAME)
  temp_in_celcius = bridge.sensors()['4']['state']['temperature'] / 100.0
  return 9.0 / 5.0 * temp_in_celcius + 32


if __name__ == "__main__":
  run_evening_light_dimmer()