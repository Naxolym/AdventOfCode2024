import sys


class ArgumentException(Exception):
    pass


def usage():
    print(f'{sys.argv[0]} [test]')


def process_args() -> str:
    """
    Process Command line Arguments
    Prints usage on wrong usage
    :return: test mode
    """
    if len(sys.argv) > 2:
        usage()
        raise ArgumentException("Too many Arguments!")
    if len(sys.argv) == 2:
        if sys.argv[1] != "test":
            usage()
            raise ArgumentException("Wrong Arguments!")
        return sys.argv[1]
    return "full"
