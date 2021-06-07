'''Check whether a domain has SNI RST.'''
import socket
import ssl
import sys
import logging


logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())
_ctx = ssl.create_default_context()


def check(hostname: str, dfip='104.131.212.184'):
    '''True if no SNI RST, False if has, None if DFIP timeout.'''
    try:
        with socket.create_connection((dfip, 443), 5) as sock:
            with _ctx.wrap_socket(sock, server_hostname=hostname):
                return True
    except ssl.SSLCertVerificationError:
        logger.info('\x1B[32mNo SNI RST.\x1B[m')  # or \033
        return True
    except ConnectionResetError:
        logger.warning('\x1B[31mHas SNI RST.\x1B[m')
        return False
    except socket.timeout:
        logger.error('\x1B[33mDFIP timed out.\x1B[m')


def _main():
    global logger
    logger = logging
    logging.basicConfig(format='%(message)s', level=logging.INFO)
    if len(sys.argv) != 2:
        print('Invalid arguments.')
    elif sys.argv[1][0] == '-':
        print('There is no flags.')
    else:
        sys.exit(not check(sys.argv[1]))


if __name__ == "__main__":
    _main()
