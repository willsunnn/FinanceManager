class ColorManager:
    def __init__(self, col_dict):
        self.col_dict = col_dict

    def get_file_display_colors(self):
        return self.col_dict['FileDisplay']

    def get_table_visualizer_colors(self):
        return self.col_dict['TableVisualizer']

    def get_data_visualizer_colors(self):
        return self.col_dict['DataVisualizer']

    @staticmethod
    def rgb_to_hex(red: int, green: int, blue: int) -> str:
        red = ColorManager.assert_range(red, 0, 255)
        green = ColorManager.assert_range(green, 0, 255)
        blue = ColorManager.assert_range(blue, 0, 255)

        decimal_to_hexadecimal = ["0", "1", "2", "3", "4", "5", "6", "7",
                                  "8", "9", "A", "B", "C", "D", "E", "F"]

        return "#{}{}{}{}{}{}".format(decimal_to_hexadecimal[int(red/16)],   decimal_to_hexadecimal[red % 16],
                                      decimal_to_hexadecimal[int(blue/16)],  decimal_to_hexadecimal[blue % 16],
                                      decimal_to_hexadecimal[int(green/16)], decimal_to_hexadecimal[green % 16])

    @staticmethod
    # returns num within the specified number range
    def assert_range(num: int, minimum: int, maximum: int) -> int:
        if minimum is not None and num < minimum:
            return minimum
        elif maximum is not None and num > maximum:
            return maximum
        else:
            return num


class ColorThemes:
    # default theme
    default_file_display_colors = None
    default_table_visualizer_colors = None
    default_data_visualizer_colors = None
    default_theme = {'FileDisplay': default_file_display_colors,
                     'TableVisualizer': default_table_visualizer_colors,
                     'DataVisualizer': default_data_visualizer_colors}

    # dark theme
    dark_button_colors = {'button_bg_col': ColorManager.rgb_to_hex(0, 0, 0),
                          'button_fg_col': ColorManager.rgb_to_hex(255, 255, 255),
                          'button_pressed_bg': ColorManager.rgb_to_hex(0, 0, 0),
                          'button_pressed_fg': ColorManager.rgb_to_hex(255, 255, 255)}
    dark_file_display_colors = {'bg_col': ColorManager.rgb_to_hex(40, 40, 40),
                                'button_colors': dark_button_colors,
                                'date_selection_colors': {
                                    'bg_col': ColorManager.rgb_to_hex(40, 40, 40),
                                    'drop_down_colors': {
                                        'bg': ColorManager.rgb_to_hex(40, 40, 40),
                                        'text': ColorManager.rgb_to_hex(255, 255, 255),
                                        'highlighted_color': ColorManager.rgb_to_hex(50, 50, 50)
                                    },
                                    'entry_colors': {
                                        'bg': ColorManager.rgb_to_hex(40, 40, 40),
                                        'text': ColorManager.rgb_to_hex(255, 255, 255)
                                    },
                                    'button_colors': dark_button_colors
                                   }
                                   }
    dark_table_visualizer_colors = {}
    dark_data_visualizer_colors = {}
    dark_theme = {'FileDisplay': dark_file_display_colors,
                  'TableVisualizer': dark_table_visualizer_colors,
                  'DataVisualizer': dark_data_visualizer_colors}


def test():
    assert ColorManager.rgb_to_hex(270, 255, 255) == "#FFFFFF"
    assert ColorManager.rgb_to_hex(0, -6, 0) == "#000000"
    assert ColorManager.rgb_to_hex(255, 0, 0) == "#FF0000"
    print("rgb_to_hex works")


if __name__ == "__main__":
    test()