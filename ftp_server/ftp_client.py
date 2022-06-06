import argparse
import logging
from ftplib import FTP


def main(args):
    logging.basicConfig(format='%(asctime)s %(message)s', level=getattr(logging, args.log_level.upper()))
    logging.info('Starting client')

    with FTP("") as ftp:
        ftp.connect(host=args.host, port=args.port)
        ftp.login(user=args.login, passwd=args.password)
        logging.info(ftp.getwelcome())
        ftp.storbinary(f'STOR {args.file_to_upload}', open(f"data/{args.file_to_upload}", 'rb'))
        logging.info(f'Sending file {args.file_to_upload}')
        ftp.close()
        logging.info('Closing client...')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('--host', help='', type=str, default='0.0.0.0')
    parser.add_argument('--port', help='', type=int, default=21)
    parser.add_argument('--file-to-upload', help='File to upload on ftp server',
                        type=str, default='example-1.mov')
    parser.add_argument('--login', help='', type=str, default='user')
    parser.add_argument('--password',  help='', default='12345')
    parser.add_argument("-l", "--log-level", help="log severity level", type=str.upper,
                        choices=logging._levelToName.values(), default=logging.getLevelName(logging.INFO))

    main(parser.parse_args())
