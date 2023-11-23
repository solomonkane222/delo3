import re
from netmiko import ConnectHandler
import getpass 

# Step 1: Create an empty list called device_list.
devices_list = []

# Step 2: Read devices and create a list
file_path = 'devices-06.txt'  # Assuming the file is in the same directory as the script

# Create the outer list for all devices
with open(file_path, 'r') as file:
    for line in file:
        # Get device info into list
        device_info_list = line.strip().split(',')
        devices_list.append(device_info_list)

# Iterate through the list of devices
for device_info in devices_list:
    # Define device parameters
    device = {
        'device_type': 'cisco_ios',
        'ip': device_info[1],  # Assuming IP address is in the second position in the list
        'username': getpass.getpass(f'Enter Username for {device_info[0]}: '),  # Use getpass for username input
        'password': getpass.getpass(f'Enter Password for {device_info[0]}: '),  # Use getpass for password input
        'secret': getpass.getpass(f'Enter The Secret Phrase for {device_info[0]}: '),  #class123! = secret password
    }

    # Connect to the device
    try:
        connection = ConnectHandler(**device)
    except Exception as e:
        print(f'Failed to connect to {device["ip"]}: {e}')
        continue  # Continue with the next device in case of connection failure

    # Enter enable mode
    connection.enable()

    # Configuring the hostname to Router3
    config_commands = ['hostname Router3']
    output = connection.send_config_set(config_commands)

    # Configuring loopback interface
    config_commands = ['interface loopback 0', 'ip address 192.168.56.101 255.255.255.255']
    output = connection.send_config_set(config_commands)

    # Configuring serial interface with IP address
    config_commands = ['interface serial 0/0/0', 'ip address 10.0.0.1 255.255.255.0']
    output = connection.send_config_set(config_commands)

    # Configuring EIGRP on the serial interface
    config_commands = ['router eigrp 1', 'network 10.0.0.0 0.255.255.255']
    output = connection.send_config_set(config_commands)

    # Saving the file locally as 'running_config.txt 
    output_file_path = f'running_config_{device_info[0]}.txt'  # Use device name in the output file name
    running_config = connection.send_command('show running-config')
    with open(output_file_path, 'w') as output_file:
        output_file.write(running_config)

    # Display a success message - for a successful connection.
    print('------------------------------------------------------')
    print('')
    print(f'Successfully connected to IP address: {device["ip"]}')
    print(f'Username: {device["username"]}')
    print('Password: ********')  # Masking the password for security
    print(f'Hostname: Router3 ({device_info[0]})')
    print('Loopback Interface and EIGRP Configuration: Successful')
    print(f'Running Configuration saved to: {output_file_path}')
    print('')
    print('------------------------------------------------------')

    # Disconnect from the device
    connection.disconnect()
