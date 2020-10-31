'''Check whether a domain has SNI RST.'''
import socket
import ssl
import sys
import logging
import time


logger = logging.getLogger(__name__)
logger.disabled = True
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


def checkmany(hostnames: list[str]):
    '''Try to auto avoid temporary blocking when checking multiple domains in a short time.'''
    def retry(fun, n=1, /, **kw):
        if (status := fun(**kw)) != None:
            return status
        for _ in range(n):
            time.sleep(60)
            if (status := fun(**kw)) != None:
                return status

    for host in hostnames:
        if (status := retry(check, hostname=host)) != None:
            yield status
        else:
            break


def _main():
    logger.disabled = False
    logging.basicConfig(format='%(message)s', level=logging.INFO)
    if len(sys.argv) != 2:
        print('Invalid arguments.')
    elif sys.argv[1][0] == '-':
        print('There is no flag.')
    else:
        sys.exit(not check(sys.argv[1]))


if __name__ == "__main__":
    _main()
