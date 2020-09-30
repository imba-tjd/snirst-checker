import socket
import ssl
import sys


def check(hostname: str, dfip='104.131.212.184'):
    try:
        with socket.create_connection((dfip, 443), 5) as sock:
            with ssl.create_default_context().wrap_socket(sock, server_hostname=hostname):
                return True
    except ConnectionResetError:
        print('\033[31mHas SNI RST.')
        return False
    except ssl.SSLCertVerificationError:
        print('\033[32mNo SNI RST.')
        return True
    except socket.timeout:
        print('\033[33mDFIP timed out.')
    except ConnectionRefusedError:
        print('\033[33mDFIP invalid.')


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('Wrong arguments.')
    elif sys.argv[1][0] == '-':
        print('There is no flags.')
    else:
        exit(not check(sys.argv[1]))
