import PySimpleGUI as sg

"""
A class to control the state of the GUI elements.
"""

class StateHandler: 
    def __init__(self, window):
        self.window = window

    def update_value(self, key, value):
        """Update value of a GUI element."""
        try:
            self.window[key].update(value)
        except Exception as e:
            raise
    
    def update_all_value(self, keys, value):
        """Update value of multiple GUI elements."""
        for key in keys:
            self.update_value(key, value)
    
    def get_value(self, key):
        """Get value of a GUI element."""
        try:
            return self.window[key].get()
        except Exception:
            return None

    def enable(self, key):
        """Enable a GUI element."""
        try:
            self.window[key].update(disabled=False)
        except Exception as e:
            raise
    
    def enable_all(self, keys):
        """Enable all GUI elements."""
        for key in keys:
            self.enable(key)

    def disable(self, key):
        """Disable a GUI element."""
        try:
            self.window[key].update(disabled=True)
        except Exception as e:
            raise
    
    def disable_all(self, keys):
        """Disable all GUI elements."""
        for key in keys:
            self.disable(key)

    def clear_inputs(self, keys):
        """Clear text inputs."""
        try:
            self.update_all_value(keys, '')
        except Exception as e:
            raise
    
    def set_visibility(self, key, visible=True):
        """Set visibility of a GUI element."""
        self.window[key].update(visible=visible)

    def set_led(self, key, color='green', empty=False):
        """Set LED color on a Graph element."""
        try:
            graph = self.window[key]
            graph.erase()
            if empty:
                graph.draw_circle((0, 0), 12, fill_color=None, line_color=color)
            else:
                graph.draw_circle((0, 0), 12, fill_color=color, line_color=color)
        except Exception as e:
            raise