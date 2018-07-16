import argparse


def get_args():
    parser = argparse.ArgumentParser(description='RL')
    parser.add_argument('--server', action='store_true', default=False,
                        help='Defines current program as a server!')
    parser.add_argument('--host', type=str, default='0.0.0.0',
                        help='Default Server Connection')
    parser.add_argument('--port', type=int, default=10050,
                        help='Default Port Connection')
    args = parser.parse_args()

    return args
