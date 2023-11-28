import re
import logging
from netmiko import ConnectHandler
import getpass 

# Configure logging
logging.basicConfig(filename='script_log.txt', level=logging.INFO)

# Input validation for username
username = input('Enter Username: ')
if not re.match("^[a-zA-Z0-9_-]+$", username):
    print("Invalid username format")
    exit()

# Define device parameters
device = {
    'device_type': 'cisco_ios_ssh',  # Use SSH instead of Telnet
    'ip': '192.168.56.101',
    'username': username,  # Use the validated username
    'password': getpass.getpass('Enter Device Password: '),  # Use getpass for password input
    'secret': getpass.getpass('Enter The Secret Phrase: '),  # class123! = secret password
}

# Connect to the device
try:
    connection = ConnectHandler(**device)
    logging.info(f"Successfully connected to {device['ip']}")
except Exception as e:
    logging.error(f'Failed to connect to {device["ip"]}: {e}')
    print(f'Failed to connect to {device["ip"]}: {e}')
    exit()

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
output_file_path = 'running_config.txt'
running_config = connection.send_command('show running-config')
with open(output_file_path, 'w') as output_file:
    output_file.write(running_config)

# Display a success message - for a successful connection.
print('------------------------------------------------------')
print('')
print(f'Successfully connected to IP address: {device["ip"]}')
print(f'Username: {device["username"]}')
print('Password: ********')  # Masking the password for security
print('Hostname: Router3')
print('Loopback Interface and EIGRP Configuration: Successful')
print(f'Running Configuration saved to: {output_file_path}')
print('')
print('------------------------------------------------------')

# Disconnect from the device
connection.disconnect()
