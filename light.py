from qhue import Bridge
import json
import os
import yaml

HUE_BRIDGE_IP = os.environ['HUE_BRIDGE_IP']
HUE_BRIDGE_USERNAME = os.environ['HUE_BRIDGE_USERNAME']


class Light():
  def __init__(self, bridge, light_num, light_json):
    self.bridge = bridge
    self.num = light_num
    self.light_json = light_json

  @property
  def name(self):
    return self.light_json['name']

  @property
  def is_on(self):
    return self.light_json['state']['on']

  @property
  def brightness(self):
    return self.light_json['state']['bri']

  @property
  def color_mode(self):
    return self.light_json['state']['colormode']

  @property
  def saturation(self):
    return self.light_json['state'].get('sat', 'Not supported')

  @property
  def is_custom_color(self):
    if isinstance(self.saturation, int) and self.saturation > 200:
      return True
    return False

  def set_brightness(self, brightness):
    if self.is_on and not self.is_custom_color:
      print "Setting {} to {}".format(self.name, brightness)
      self.bridge.lights[self.num].state(bri=brightness)
    else:
      print "{} set to custom color".format(self.name)

  def update_json(self):
    Light.update_lights([self], self.bridge)
  
  def _update_from_lights_json(self, lights_json):
    self.light_json = lights_json[self.num]


  @classmethod
  def build_lights(cls):
    bridge = Bridge(HUE_BRIDGE_IP, HUE_BRIDGE_USERNAME)
    lights_json = cls.get_updated_lights_json(bridge)
    return [Light(bridge, light_num, light_json) for light_num, light_json
            in lights_json.iteritems()]

  @classmethod
  def update_lights(cls, all_lights):
    bridge = all_lights[0].bridge
    lights_json = cls.get_updated_lights_json(bridge)
    for light in all_lights:
      light._update_from_lights_json(lights_json)

  @classmethod
  def get_updated_lights_json(cls, bridge):
    return yaml.safe_load(json.dumps(bridge.lights()))

