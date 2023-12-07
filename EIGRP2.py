import re
from netmiko import ConnectHandler
import getpass

# Define device parameters
device = {
    'device_type': 'cisco_ios',
    'ip': '192.168.56.101',
    'username': getpass.getpass('Enter Username: '),  # Use getpass for username input
    'password': getpass.getpass('Enter the Device Password: '),  # Use getpass for password input
    'secret': getpass.getpass('Enter the Secret Phrase: '),  # class123! = secret password
}

# Connect to the Router
try:
    connection = ConnectHandler(**device)
except Exception as e:
    print(f'Failed to connect to {device["ip"]}: {e}')
    exit()

# Enter enable mode
connection.enable()

# changing the hostname to 'Router3' 
config_commands = ['hostname Router3']

# Adding configuration for Loopback0 Interface
config_commands.extend([
    'interface Loopback0',
    'ip address 127.0.0.1 255.255.255.0',  # Change IP address and subnet mask
    'description Loopback Interface'
])

# Adding configuration for GigabitEthernet 2 Interface
config_commands.extend([
    'interface GigabitEthernet2',
    'ip address 192.168.1.1 255.255.255.0', 
    'description GigabitEthernet2 Interface'
])

# Adding configuration for EIGRP Protocol 
config_commands.extend([
    'router eigrp 1',
    'network 127.0.0.1 0.0.0.0',  # Loopback0 Interface
    'network 192.168.1.0 0.0.0.255'  # GigabitEthernet2 network
])

# Applying the configuration
output = connection.send_config_set(config_commands)

# Saving the file locally in PRNE as 'running_config.txt' to display the configuration. 
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
print(f'Running Configuration saved to: {output_file_path}')
print('')
print('------------------------------------------------------')

# Disconnect from the device and end session. 
connection.disconnect()