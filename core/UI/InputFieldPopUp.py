from Source.settings import params
from core.UI.BaseUI import BaseUI
from core.UI.DefaultButton import DefaultButton
from core.UI.InputField import InputField
from core.UI.PopUp import PopUp


def ready_code(button):
    if button.parent.child[1].ready and params["code"]:
        button.window.game.open_window("Game")
        # print(params["code"])


def ready_nickname(button):
    if button.parent.child[1].ready:
        print(f"READY {button.parent.child[1].text}, len={len(button.parent.child[1].text)}")


class InputFieldPopUp(PopUp):
    def __init__(self, window, pos, type_field, text):
        if type_field == "code":
            input_field = InputField(window, (99, 75), "C O D E", ((230, 81, 0), (255, 143, 0)), type_field,
                                     size=(96, 18))
            rendered_text = window.game.render_text("код игры", (230, 81, 0))
            size = (3, 2)
            action = ready_code
        elif type_field == "nickname":
            input_field = InputField(window, (15, 75), "nickname", ((230, 81, 0), (255, 143, 0)), type_field,
                                     size=(267, 18), align_center=True)
            size = (3, 2)
            rendered_text = window.game.render_text("никнейм", (230, 81, 0))
            action = ready_nickname
        else:
            raise Exception(f"unsupported field type {type_field}")

        text_button = DefaultButton(window, (0, 0), text, 3, action)
        text_button.pos = (size[0] * 100 - text_button.image.get_width()) // 2, 115

        description = BaseUI(window, (0, 0), image=rendered_text)
        description.pos = (size[0] * 100 - description.image.get_width()) // 2, 40

        super().__init__(window, pos, size, [text_button, input_field, description])
