import PySimpleGUI as sg

class display:
    def __init__():
        pass

    def LEDIndicator(key=None, radius=30):
        return sg.Graph(canvas_size=(radius, radius),
                        graph_bottom_left=(-radius, -radius),
                        graph_top_right=(radius, radius),
                        pad=(0, 0), key=key, visible=True)