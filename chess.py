from client import Client
from server import Server
from arguments import get_args


def main():
    args = get_args()

    # Start as server #
    if(args.server):
        server = Server()
        server.run()
    else:
        client = Client()
        client.run()


if __name__ == "__main__":
    main()
