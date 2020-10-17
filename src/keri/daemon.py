"""
Background Server Daemon for keri


"""
import argparse
import socket
import sys

import pysodium

from core.eventing import incept, rotate, interact, receipt, chit
from core.coring import Verfer, Signer, Diger, Nexter, Prefixer

parser = argparse.ArgumentParser(description='Command description.')
parser.add_argument('--host', metavar="HOST", required=True, help="host on which server will listen")
parser.add_argument('-p', '--port', metavar="PORT", help="port on which server will listen", default=49153)

def main(args=None):
    args = parser.parse_args(args=args)
    server_address = ( args.host, args.port )
    print('Server started on: {} port {}'.format(*server_address))
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(server_address)
    sock.listen(1)

    # Generate Non
    seed = pysodium.randombytes(pysodium.crypto_sign_SEEDBYTES)
    signer0 = Signer(raw=seed, transferable=False)
    print("Generate signer key")
    keys0 = [signer0.verfer.qb64]
    serder = incept(keys=keys0)
    print("Prefix did:",serder.ked["pre"])
    print("Raw event: ", serder.raw)


    while True:
        print('Waiting for a connection ...')
        connection, client_address = sock.accept()
        try:
            while True:
                data = connection.recv(16)
                print("Received {!r}".format(data))
                if data:
                    print('sending data back to client')
                    message = "ok"
                    b_message = str.encode(message)
                    type(b_message)
                    connection.sendall(b_message)
                else:
                    print('no more data from' + client_address)
                    break
        finally:
            connection.close()


if __name__ == '__main__':
    main()