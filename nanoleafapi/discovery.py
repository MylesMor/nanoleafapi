# Module to aid with Nanoleaf discovery

import socket

def discover_devices(timeout=30, debug=False):
    """
    Discovers Nanoleaf devices on the network using SSDP

    :param timeout: The timeout on the search in seconds (default 30)
    :param debug: Prints each device string in for the SSDP discovery
    :returns: Dictionary of found devices in format {name: ip}
    """
    ssdp = "M-SEARCH * HTTP/1.1\r\nHOST: 239.255.255.250:1900\r\nMAN: \"ssdp:discover\"\r\nMX: 1\r\nST: nanoleaf:nl29\r\n\r\n"

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(timeout)
    sock.sendto(ssdp.encode(), ("239.255.255.250", 1900))

    nanoleaves = []

    while True:
        try:
            data = sock.recv(1024).decode()
        except:
            break
        nanoleaves.append(data)

    nanoleaf_dict = {}

    for device in nanoleaves:
        if debug:
            print(device)
        headers = device.split('\r\n')
        ip = None
        name = None
        for header in headers:
            if "Location" in header:
                ip = header.split("http://")[1][:-6]
            if "nl-devicename" in header:
                name = header.split("nl-devicename: ")[1]
        if ip is not None:
            nanoleaf_dict[name] = ip
    return nanoleaf_dict
