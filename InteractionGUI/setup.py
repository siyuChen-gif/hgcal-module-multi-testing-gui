import PySimpleGUI as sg
from InteractionGUI.display import Display, MAX_TESTSTAND_NUM

class StateHandler: 
    def __init__(self, window):
        self.window = window

    def update_value(self, key, value):
        """Update value of a GUI element."""
        try:
            self.window[key].update(value)
        except Exception as e:
            raise

    def update_combo(self, key, values):
        """Update the combo value of a GUI combo."""
        if values:
            self.window[key].update(values=values, value=values[0])
        else:
            self.window[key].update(values=[], value='')
    
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
    
    def delete_element(self, key):
        """Delete the placeholder element.
        """
        try:
            self.window[key].Widget.pack_forget()
        except Exception as e:
            raise
    
    def add_element(self, key, element):
        """Add the element to the GUI.
        """
        parent_elem = self.window[key]

        try:
            self.window.extend_layout(parent_elem, [[element]])
        except Exception as e:
            raise



class GUISetUp(StateHandler):
    """
    This class contains all the functions that will be auto used to set up the BaseGUI window.
    """
    def __init__(self, window):
        super().__init__(window)
        self.display = Display()

        self.teststands_layout_key = '-TESTSTANDS-LAYOUT-'
        self.tests_selection_layout_key = '-TESTS-SELECTION-LAYOUT-'


    # ============================================================
    # === Interactions  ==========================================
    # ============================================================

    """ Functions for enabling/disabling teststand setup fields. """
    def enable_all_teststands(self):
        _, keys = self.display.setup_all_teststands()
        self.enable_all(keys)
    def disable_all_teststands(self):
        _, keys = self.display.setup_all_teststands()
        self.disable_all(keys)
    
    """ Functions for enabling/disabling one teststand setup fields. """
    def enable_one_teststand(self, teststand_no):
        _, keys = self.display.setup_single_teststand(teststand_no)
        self.enable_all(keys)
    def disable_one_teststand(self, teststand_no):
        _, keys = self.display.setup_single_teststand(teststand_no)
        self.disable_all(keys)

    """ Functions for checking/unchecking teststand checkboxs """
    def check_all_teststands_checkboxs(self):
        keys = self._get_all_teststands_checkboxs_keys()
        self.update_all_value(keys, True)
    def uncheck_all_teststands_checkboxs(self):
        keys = self._get_all_teststands_checkboxs_keys()
        self.update_all_value(keys, False)

    """ Functions for clear the Scan QR Code input """
    def clear_scanned_qr_code(self, key):
        self.update_value(key, '')
    
    """ Functions for displaying/hiding the entire Teststand Setup section """
    def show_teststands_setup(self):
        self.set_visibility(self.teststands_layout_key, True)
    def hide_teststands_setup(self):
        self.set_visibility(self.teststands_layout_key, False)

    """ Functions for displaying/hiding the tests selection section """
    def show_tests_selection_setup(self):
        self.set_visibility(self.tests_selection_layout_key, True)
    def hide_tests_selection_setup(self):
        self.set_visibility(self.tests_selection_layout_key, False)
    
    """ Functions for adding/deleting the tests selection section """
    def add_tests_selection_setup(self, element):
        self.add_element(self.tests_selection_layout_key, element)
    def delete_tests_selection_setup(self):
        self.delete_element(self.tests_selection_layout_key)
    def destroy_test_selection_setup(self):
        print(">>>>> try destroying...")
        if self.tests_selection_layout_key in self.window.AllKeysDict:
            self.window[self.tests_selection_layout_key].Widget.destroy()
            del self.window.AllKeysDict[self.tests_selection_layout_key]
            print(f">>>>>{self.tests_selection_layout_key} deleted")
    
    """ Functions for updating the default test for test selection section """
    def update_test(self, key, test):
        self.update_value(key, test)


    # ============================================================
    # === Helper Functions  ======================================
    # ============================================================

    def _get_all_teststands_checkboxs_keys(self):
        keys = []
        for teststand_no in range(1, MAX_TESTSTAND_NUM + 1):
            key = f'-TESTSTAND-{teststand_no}-'
            keys.append(key)
        return keys
