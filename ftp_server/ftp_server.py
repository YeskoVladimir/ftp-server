import asyncio
import argparse
import logging
import os
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.servers import FTPServer

from s3_requester import S3Requester
from handler import Handler


async def main(args):
    logging.basicConfig(format='%(asctime)s %(message)s', level=getattr(logging, args.log_level.upper()))

    authorizer = DummyAuthorizer()

    logging.info(f'Started with parameters: {args}')

    authorizer.add_user('user', '12345', '.', perm='elradfmwMT')
    authorizer.add_anonymous(os.getcwd())

    handler = Handler
    handler.kafka_topic = args.kafka_topic
    handler.kafka_server = args.kafka_server
    handler.authorizer = authorizer
    handler.banner = "Connected to FTP server"

    if args.masquerade:
        handler.masquerade_address = args.masquerade

    if args.passive:
        passive_ports = [int(p) for p in args.passive.split('-')]
        assert len(passive_ports) == 2
        handler.passive_ports = range(passive_ports[0], passive_ports[1])

    server = FTPServer(address_or_socket=(args.host, args.port), handler=handler)

    server.max_cons = args.max_cons
    server.max_cons_per_ip = args.max_cons_per_ip

    server.serve_forever()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('--host', help='', type=str, default='0.0.0.0')
    parser.add_argument('--port', help='', type=int, default=21)
    parser.add_argument('--max-cons', help='Limit of server connections', type=int, default=256)
    parser.add_argument('--max-cons-per-ip', help='Limit of connections per ip', type=int, default=5)
    parser.add_argument('--passive', help='Range of passive ports', type=str, default=None)
    parser.add_argument('--masquerade', help='NAT address', type=str, default=None)
    parser.add_argument('--kafka-server',  help='Kafka <host>:<port> values separated by space', nargs='+')
    parser.add_argument("--kafka-topic", help="Yandex object storage ", type=str)
    parser.add_argument("-l", "--log-level", help="log severity level", type=str.upper,
                        choices=logging._levelToName.values(), default=logging.getLevelName(logging.INFO))

    asyncio.run(main(parser.parse_args()))
