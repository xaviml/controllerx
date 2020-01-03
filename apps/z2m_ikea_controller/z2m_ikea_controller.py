"""
Bring full functionality to IKEA light controllers

https://github.com/xaviml/z2m_ikea_controller
"""
import appdaemon.plugins.hass.hassapi as hass
import time

DEFAULT_MANUAL_STEPS = 10
DEFAULT_AUTOMATIC_STEPS = 10
DEFAULT_DELAY = 350
DEFAULT_COLORTEMP_ONLY = 0

attribute_minmax = {
    "brightness": {"min": 1, "max": 255},
    "color_temp": {"min": 153, "max": 500},
}

sign_mapping = {"up": 1, "down": -1}


class IkeaController(hass.Hass):
    def initialize(self):
        self.sensors = self.get_sensors(self.args["sensor"])
        self.light = self.args["light"]
        # Since time.sleep is not recommended I limited to 1s
        self.delay = min(1000, self.args.get("delay", DEFAULT_DELAY))
        self.manual_steps = self.args.get("manual_steps", DEFAULT_MANUAL_STEPS)
        self.automatic_steps = self.args.get("automatic_steps", DEFAULT_AUTOMATIC_STEPS)
        self.colortemp_only = self.args.get("colortemp_only", DEFAULT_COLORTEMP_ONLY)
        self.on_hold = False
        for sensor in self.sensors:
            self.listen_state(self.state, sensor)

    def get_sensors(self, sensors):
        type_ = type(sensors)
        if type_ == str:
            return sensors.replace(" ", "").split(",")
        elif type_ == list:
            return sensors

    def process_state(self, state):
        """
        This function should be implemented. It should return a tuple with:
            * attribute: Attribute of the light (e.g. brightness or color_temp)
            * direction: Directiom that the attribute takes: up, down
            * action: Action to take: toggle, click, hold and release
        """
        pass

    def state(self, entity, attribute, old, new, kwargs):
        if new == "":
            return
        attribute, direction, action = self.process_state(new)
        light_state = self.get_state(self.light)
        if self.colortemp_only == 0:
            if action == "toggle":
                self.toggle(self.light)
            elif action == "on":
                self.turn_on(self.light)
            elif action == "off":
                self.turn_off(self.light)
        if action == "release":
            self.on_hold = False
        elif light_state == "off":
            return
        sign = sign_mapping[direction]
        value = self.get_attr_value(self.light, attribute)
        max_ = attribute_minmax[attribute]["max"]
        min_ = attribute_minmax[attribute]["min"]
        if action == "click":
            self.turn_on_light(attribute, value, sign, self.manual_steps)
        elif action == "hold":
            self.on_hold = True
            while self.on_hold and value is not None:
                value = self.turn_on_light(
                    attribute, value, sign, self.automatic_steps
                )
                # The use of the time.sleep is due to not have a support of seconds
                # in run_every function. It is also fine to use as long is in control:
                # https://github.com/home-assistant/appdaemon/issues/26#issuecomment-274798324
                time.sleep(self.delay / 1000)

    def get_attr_value(self, light, attribute):
        if "group." in light:
            lights = self.get_state(self.light, attribute="entity_id")
            light = lights[0]
        out = self.get_state(light, attribute=attribute)
        return out

    def turn_on_light(self, attribute, old, sign, steps):
        """
        It returns the new value if it didn't reached min or max. Otherwise None.
        """
        max_ = attribute_minmax[attribute]["max"]
        min_ = attribute_minmax[attribute]["min"]
        step = (max_ - min_) // steps
        new_state_attribute = old + sign * step
        attributes = {attribute: new_state_attribute, "transition": self.delay / 1000}
        if min_ <= new_state_attribute <= max_:
            self.turn_on(self.light, **attributes)
            return new_state_attribute
        else:
            new_state_attribute = max(min_, min(new_state_attribute, max_))
            attributes[attribute] = new_state_attribute
            self.turn_on(self.light, **attributes)
            return None


class E1810Controller(IkeaController):
    # Different states reported from the controller:
    # toggle, brightness_up_click, brightness_down_click
    # arrow_left_click, arrow_right_click, brightness_up_hold
    # brightness_up_release, brightness_down_hold, brightness_down_release,
    # arrow_left_hold, arrow_left_release, arrow_right_hold
    # arrow_right_release
    def process_state(self, state):
        if state == "toggle" and self.colortemp_only == 0:
            return (None, None, "toggle")
        else:
            attribute, direction, action = state.split("_")
            if attribute == "arrow":
                attribute = "color_temp"
            direction_mapping = {"left": "down", "right": "up"}
            direction = direction_mapping.get(direction, direction)
            return attribute, direction, action


class E1743Controller(IkeaController):
    # Different states reported from the controller:
    # on, off, brightness_up, brightness_down, brightness_stop
    def process_state(self, state):
        splitted = state.split("_")
        if len(splitted) == 1:
            # For on and off
            return (None, None, splitted[0])
        else:
            attribute, action = splitted
            if action == "up" or action == "down":
                return attribute, action, "hold"
            else:
                return attribute, None, "release"
