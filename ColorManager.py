class ColorManager:
    def __init__(self, col_dict: {}):
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


class ColorTheme:
    def __init__(self, bg_col: str, text_col: str, highlight_col: str, **optional_arguments):
        self.bg_col = bg_col
        if 'bg_col2' in optional_arguments:
            self.bg_col2 = optional_arguments['bg_col2']
        else:
            self.bg_col2 = self.bg_col
        self.text_col = text_col
        self.highlight_col = highlight_col

        self.button_colors = {'button_bg_col': self.bg_col,
                              'button_text_col': self.text_col,
                              'button_pressed_bg': self.bg_col,
                              'button_pressed_text': self.text_col}
        self.file_display_colors = {'bg_col': self.bg_col,
                                    'button_colors': self.button_colors,
                                    'date_selection_colors':
                                        {
                                            'bg_col': self.bg_col,
                                            'drop_down_colors':
                                                {
                                                    'bg_col': self.bg_col,
                                                    'text': self.text_col,
                                                    'highlighted_color': self.bg_col2
                                                },
                                            'entry_colors':
                                                {
                                                    'bg_col': self.bg_col,
                                                    'text': self.text_col,
                                                    'cursor': self.text_col
                                                },
                                            'button_colors': self.button_colors
                                        }
                                    }
        self.table_visualizer_colors = {}
        self.data_visualizer_colors = {'bg_col': self.bg_col,

                                       'pie_chart_colors':
                                           {
                                               'bg_col': self.bg_col,
                                               'text_col': self.text_col,
                                               'chart_col': self.highlight_col
                                           }

                                       }
        self.theme = {'FileDisplay': self.file_display_colors,
                      'TableVisualizer': self.table_visualizer_colors,
                      'DataVisualizer': self.data_visualizer_colors}

    @staticmethod
    def get_dark_theme_dict() -> {}:
        dark_bg_col = ColorManager.rgb_to_hex(40, 40, 40)
        dark_bg_col2 = ColorManager.rgb_to_hex(50, 50, 50)
        dark_text_col = ColorManager.rgb_to_hex(255, 255, 255)
        dark_highlight_col = ColorManager.rgb_to_hex(120, 120, 120)
        return ColorTheme(dark_bg_col, dark_text_col, dark_highlight_col, bg_col2=dark_bg_col2).theme

    @staticmethod
    def get_default_theme_dict() -> {}:
        default_file_display_colors = None
        default_table_visualizer_colors = None
        default_data_visualizer_colors = None
        default_theme = {'FileDisplay': default_file_display_colors,
                         'TableVisualizer': default_table_visualizer_colors,
                         'DataVisualizer': default_data_visualizer_colors}
        return default_theme


def test():
    assert ColorManager.rgb_to_hex(270, 255, 255) == "#FFFFFF"
    assert ColorManager.rgb_to_hex(0, -6, 0) == "#000000"
    assert ColorManager.rgb_to_hex(255, 0, 0) == "#FF0000"
    print("rgb_to_hex works")


if __name__ == "__main__":
    test()