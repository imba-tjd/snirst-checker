'''Check whether a domain has SNI RST.'''
import socket
import ssl
import sys
import logging


def check(hostname: str, dfip='104.131.212.184'):
    '''True if no SNI RST, False if has, None if DFIP timeout or invalid.'''
    try:
        with socket.create_connection((dfip, 443), 5) as sock:
            with ssl.create_default_context().wrap_socket(sock, server_hostname=hostname):
                return True
    except ConnectionResetError:
        logging.warning('\x1B[31mHas SNI RST.\x1B[m')  # or \033
        return False
    except ssl.SSLCertVerificationError:
        logging.info('\x1B[32mNo SNI RST.\x1B[m')
        return True
    except socket.timeout:
        logging.exception('\x1B[33mDFIP timed out.\x1B[m')
    except ConnectionRefusedError:
        logging.exception('\x1B[33mDFIP invalid.\x1B[m')


def _main():
    logging.basicConfig(format='%(message)s', level=logging.INFO)
    if len(sys.argv) != 2:
        print('Invalid arguments.')
    elif sys.argv[1][0] == '-':
        print('There is no flags.')
    else:
        exit(not check(sys.argv[1]))


if __name__ == "__main__":
    _main()
