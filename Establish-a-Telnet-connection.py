from netmiko import ConnectHandler

# Define device information
device = {
    'device_type': 'cisco_ios',
    'ip': '192.168.56.101',
    'username': input('Enter Username (e.g., cisco): '), #cisco = username 
    'password': input('Enter Password (e.g., cisco123!): '),#cisco123! = password
}

#Creating session
try:
    connection = ConnectHandler(**device)
except Exception as e:
    print('--- FAILURE! Creating Telnet session for:', device['ip'])
    exit()

#Device configurtions 
try:
    connection.enable()  # Enter enable mode
    connection.config_mode()  # Enter configuration mode
    connection.send_config_set(['hostname R3'])  # Set the hostname to 'R3'
    connection.exit_config_mode()  # Exit configuration mode
except Exception as e:
    print('--- FAILURE! Configuring the device:', e)
    connection.disconnect()
    exit()

#Code for saving the file locally 
try:
    output = connection.send_command('show running-config')
    with open('running-config.txt', 'w') as file:
        file.write(output)
except Exception as e:
    print('Failed to save the file!:', e)
    connection.disconnect()
    exit()

#Show a success message - for successful connection
print('-------------------------------------------------')
print('')
print('--- Success! Connecting to:', device['ip'])
print('---               Username:', device['username'])
print('---               Password: ********')  # Masking the password for security
print('---               Hostname: R3')
print('--- Running configuration saved as running-config.txt')
print('')
print('---------------------------------')

# Disconnect from the device
connection.disconnect()
