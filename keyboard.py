def convert_keyboard(buttons=[], one_time=False):
    keyboard = {}
    if one_time:
        keyboard["one_time"] = True
    if buttons:
        keyboard["buttons"] = []
        for row in buttons:
            this_row = []
            for button in row:
                but = { 
                        "action": { 
                            "type": "text", 
                            "label": str(button[0]) 
                            }, 
                        "color": str(button[1]) 
                        }
                this_row.append(but)
            keyboard["buttons"].append(this_row)

    keyboard = str(keyboard)
    if one_time:
        keyboard = keyboard.replace("True", "true")
    keyboard = keyboard.replace("'", '"')
    return keyboard


if __name__ == '__main__':
    print(convert_keyboard([[[1,'red'], ['2', 'green']], ['123', 'primary']]))