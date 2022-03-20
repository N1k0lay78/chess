from settings import debug


def special_print(*message, **args):
    if debug:
        # if "level" in args:
        # print(args["level"])
        print(*message)