# import required modules/packages/library
import pexpect
# Define variables
ip_address = '192.168.56.101'
username = 'prne'
password = 'cisco123!'
password_enable = 'class123!'
# creat the ssh session
session = pexpect.spawn('ssh ' + username + '@' + ip_address, encoding='utf-8', timeout=20)

result = session.expect(['Password:', pexpect.TIMEOUT, pexpect.EOF])
# Check the error, if exists then display error and exit
if result != 0:
    print('--- FAILURE! creating session for: ', ip_address)
    exit()
# Session expecting password, enter details
session.sendline(password)
result = session.expect(['>', pexpect.TIMEOUT, pexpect.EOF])
# Check for error, if exists then display error and exit
if result != 0:
    print('--- FALLURE! entering password: ', password)
    exit()

# Enter enable mode
session.sendline('enable')
result = session.expect(['Password:', pexpect.TIMEOUT, pexpect.EOF])

# Check for error, if exists the display error and exit
if result != 0:
    print('--- Failure! entering enable mode')
    exit()

# Send enable password details
session.sendline (password_enable)
result = session.expect(['#', pexpect.TIMEOUT, pexpect.EOF])

# Check for error, if exist then display error and exit
if result != 0:
    print('--- Failure! entering enable mode after sending password')
    exit()

# Enter configuration mode
session.sendline('configure terminal')
result = session.expect([r'.\(config\)#', pexpect.TIMEOUT, pexpect.EOF])

# Check for error, if exists then display error and exit
if result != 0:
    print('--- Failure! entering config mode')
    exit()
# change the hostname to R1
session.sendline('hostname R1')
result = session.expect([r'R1\(config\)#', pexpect.TIMEOUT, pexpect.EOF])    

# check for error, if exists then display error and exit
if result != 0:
    print('--- Failure! setting hostname')

# Saving the file locally
with open("example_file.txt", "w") as open_file:
    # Write the text to the file
    open_file.write("establish-a-ssh-connection.py")


    
# Exit config mode
session.sendline('exit')

# Display a success message if works
print('                  ----------------------             ')
print('         --------------------------------------------')
print('         --------------------------------------------')
print('')
print('         --- success! connecting to: ', ip_address)
print('         ---               Username: ', username)
print('')
print('         --------------------------------------------')
print('         --------------------------------------------')
print('                  ----------------------             ')

import difflib
startup_config  = session.sendline("show startup-config")
running_config = session.sendline("show running-config")
# Assuming session.sendline() returns strings, if not, convert them to strings
startup_config_str = str(startup_config)
running_config_str = str(running_config)

# Create a Differ object
differ = difflib.Differ()
# Compare sequences
diff = differ.compare(startup_config_str.splitlines(), running_config_str.splitlines())

# Display the differences
print('')
print('                 ***********************                      ')
print('**************************************************************')
print('             *******************************                  ')
print('Comparing the current configuration with startup configuration')
print('--------------------------------------------------------------')
print('The Numbers of Differences are:','\n'.join(diff))
print('--------------------------------------------------------------')
print('            ********************************                  ')
print('**************************************************************')
print('                ************************                      ')

# Terminate SSH session
session.close()
