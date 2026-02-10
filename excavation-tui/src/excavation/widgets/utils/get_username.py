import getpass


def username() -> str:
    try:
        name = getpass.getuser()
        return name
    except OSError as e:
        print(f"Could not determine username: {e}")
        return "PLAYER"
