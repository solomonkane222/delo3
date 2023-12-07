import re
from netmiko import ConnectHandler
import getpass

#connecting to device and creating input to enter username, password and secret phrase using getpass for security.
device = {
    'device_type': 'cisco_ios',
    'ip': '192.168.56.101',
    'username': getpass.getpass('Enter Username: '),  # Use getpass for username input
    'password': getpass.getpass('Enter the Device Password: '),  # Use getpass for password input
    'secret': getpass.getpass('Enter the Secret Phrase: '),  # class123! = secret password
}

#Connect to the Router - if connection fails, failiure mesage will be displayed along with the device/IP.
try:
    connection = ConnectHandler(**device)
except Exception as e:
    print(f'Failed to connect to {device["ip"]}: {e}')
    exit()

# Enter enable mode
connection.enable()

# changing the hostname to 'Router3' 
config_commands = ['hostname Router3']

#Creating a configuration for Loopback0 Interface - this will be shown when entering 'show ip interface brief' on the router
config_commands.extend([
    'interface Loopback0',
    'ip address 1.1.1.2 255.255.255.255',  
    'description Loopback Interface'
])

# Adding configuration for GigabitEthernet 2 Interface - this be shown when entering 'show ip int brief' on the router
config_commands.extend([
    'interface GigabitEthernet2',
    'ip address 192.168.1.1 255.255.255.0', 
    'description GigabitEthernet2 Interface'
])

# Adding configuration for EIGRP Protocol 
config_commands.extend([
    'router eigrp 1',
    'network 1.1.1.1 0.0.0.0',  # Loopback0 Interface
    'network 192.168.1.0 0.0.0.255'  # GigabitEthernet2 network
])

# Applying the configuration
output = connection.send_config_set(config_commands)

# Saving the file locally in the PRNE Folder as 'running_config.txt' to display the configuration. 
output_file_path = 'running_config.txt'
running_config = connection.send_command('show running-config')
with open(output_file_path, 'w') as output_file:
    output_file.write(running_config)

# Display a success message - this will appear if the configuration is successful. 
print('------------------------------------------------------')
print('')
print(f'Successfully connected to IP address: {device["ip"]}')
print(f'Username: {device["username"]}')
print('Password: ********')  # Masking the password for an added layer of security
print('Hostname: Router3')
print('Loopback0 and EIGRP successfully configured')
print(f'Running Configuration saved to: {output_file_path}')
print('')
print('------------------------------------------------------')

# Disconnect from the device and end session. 
connection.disconnect()
