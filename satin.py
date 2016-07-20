 #!/usr/bin/python
import tokenizer


def prompt():
    """
    prompt which asks for input and return splited words.
    """
    intext = input('input :> ')
    args = intext.split()
    return args


def talker(args_in):
    """
    It takes input text given by user and returns the reply
    to user.
    """
    return 'hello'


def satin():
    while True:
        args_in = prompt()
        args_out = talker(args_in)
        print('satin :> '+args_out)


if __name__ == '__main__':
    satin()
