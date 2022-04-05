from Source.settings import params


def print(*message, **args):
    if params["debug"]:
        pass
        # if "level" in args:
        # print(args["level"])
        # print(*message)