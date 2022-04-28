commands_official = {
    "newn":
}

commands_lobby = {

}

commands_game = {

}

commands_social = {

}

commands_ui = {

}


def set_new_nickname(clients, peer, nick):
    if not clients[peer][1]:
        clients[peer][1] = nick
        return True
    return False
