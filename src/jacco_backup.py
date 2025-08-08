import housey_logging
housey_logging.configure()

import os
import time
import logging

#logger = logging.getLogger(__name__)
host_name = "192.168.192.20"
server_mac = ""
ping_interval = 1

def log_exception(type, value, tb):
    logging.exception("Uncaught exception: {0}".format(str(value)))

def check_connection(hostname_to_ping: str):

    logging.info("checking if %s is online trough ping", hostname_to_ping)

    if str(os.sys.platform).lower()=='win32':
        param = '-n' 
    else: 
        param = '-c'

    error_count = 0
    while error_count < 3:

        ping_command = f"ping {param} 1 {hostname_to_ping}"

        logging.debug("command to send to os: %s",ping_command)
        ping_response = os.system(ping_command)

        if ping_response == 0:
            ping_response = True
            logging.info("%s is online",hostname_to_ping)
            break
        else:
            error_count = error_count+1

            errors_remaining = 3-error_count
            
            if not error_count == 3:
                logging.error("%s was not reachable... trying again in %s seconds for %s more times ",hostname_to_ping, ping_interval, errors_remaining)
                time.sleep(ping_interval)

    if error_count == 3:
        send_telegram_notification()
        raise RuntimeError(f"{hostname_to_ping} is not online, tried 3 times then failed")

    return()

def enable_vpn():
    None

def wakeonlan(server_mac: str):
    wol_command = f"wakeonlan {server_mac}"

    wol_response = os.system(wol_command)

def send_telegram_notification():
    None

def check_online():
    None

def mount_samba():
    None

def launch_freefilesync():
    None

def give_root_acces_xterm():
    None

def main():
    check_connection(host_name)
    enable_vpn()
    wakeonlan()
    None


if __name__ == "__main__":
    main()
