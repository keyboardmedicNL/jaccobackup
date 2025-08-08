import housey_logging
housey_logging.configure()

import os
import time
import logging
import config_loader
from smb.SMBConnection import SMBConnection
import sys


def log_exception(type, value, tb):
    logging.exception("Uncaught exception: {0}".format(str(value)))

def check_connection_to_vpn_host(hostname_to_ping: str, ping_interval: int):

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
                logging.error("%s was not reachable... trying again in %s seconds for %s more times and waiting for %s more seconds ",hostname_to_ping, ping_interval, errors_remaining, ping_interval)
                time.sleep(ping_interval)

    if error_count == 3:
        send_telegram_notification()
        raise RuntimeError(f"{hostname_to_ping} is not online, tried 3 times then failed")

    return()

def enable_vpn():
    None

def wakeonlan(server_mac: str):

    logging.info("sending wake on lan magic packet to adress %s",server_mac)

    wol_command = f"wakeonlan {server_mac}"
    logging.debug("command to send to os: %s",wol_command)

    os.system(wol_command)

def check_if_samba_accessible(server_adress: str, share_name: str, user_name: str, pass_word: str, samba_wait_time: int):
    logging.info("attempting connection to samba share at adress %s", server_adress)
    error_count = 0
    while error_count < 3:

        try:
            conn = SMBConnection(user_name, pass_word, "python", server_adress)
            conn.connect(server_adress)

            for share in conn.listShares():
                if share_name in share.name:
                    logging.info("%s is accessible on server %s",share_name, server_adress)
            break

        except:
            error_count = error_count+1
            errors_remaining = 3-error_count

            if not error_count == 3:
                logging.error("unable to connect to samba share from server %s trying %s more times and waiting for %s seconds", server_adress, errors_remaining, samba_wait_time)
                time.sleep(samba_wait_time)
                
    if error_count == 3:
        send_telegram_notification()
        raise RuntimeError ("tried to connect to samba share 3 times and failed")

def send_telegram_notification():
    None

def mount_samba():
    None

def launch_freefilesync():
    None

def give_root_acces_xterm():
    None

def main():
    sys.excepthook = log_exception

    loaded_config = config_loader.load_config()

    check_connection_to_vpn_host(loaded_config.host_name,loaded_config.ping_interval)
    enable_vpn()
    #wakeonlan(loaded_config.server_mac)
    check_if_samba_accessible(loaded_config.server_adress, loaded_config.samba_share_name, loaded_config.samba_user_name, loaded_config.samba_password, loaded_config.samba_wait_time)

    logging.info("script finished...")


if __name__ == "__main__":
    main()
