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

# Connect to the device
try:
    connection = ConnectHandler(**device)
except Exception as e:
    print(f'Failed to connect to {device["ip"]}: {e}')
    exit()

# Enter enable mode
connection.enable()

# Configuring the hostname to Router3
config_commands = ['hostname Router3']

# Adding configuration for loopback interface
config_commands.extend([
    'interface Loopback0',
    'ip address 1.1.1.2 255.255.255.255',  # Change the IP address and subnet mask accordingly
    'description Loopback Interface'
])

# Adding configuration for GigabitEthernet 0/2 interface
config_commands.extend([
    'interface GigabitEthernet2',
    'ip address 192.168.1.1 255.255.255.0',  # Change the IP address and subnet mask accordingly
    'description GigabitEthernet 0/2 Interface'
])

# Adding EIGRP configuration
config_commands.extend([
    'router eigrp 1',
    'network 1.1.1.1 0.0.0.0',  # Loopback network
    'network 192.168.1.0 0.0.0.255'  # GigabitEthernet 0/2 network
])

# Applying the configuration
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
print(f'Running Configuration saved to: {output_file_path}')
print('')
print('------------------------------------------------------')

# Disconnect from the device
connection.disconnect()
