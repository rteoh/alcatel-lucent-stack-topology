import os
import sys
from datetime import datetime
import paramiko
import getpass
import time
import ipaddress


# Define hostname
hostname = "localhost"


# Define switch list
switch_list = []

# Switch Credentials
switch_user = ""
switch_pass = ""


# Define File Output
file_output = []

# Define text file
textFile = False


# Alcatel Lucent Switch commands
def input_switch_password(statseeker):
	statseeker.send(switch_pass + '\n')
	time.sleep(10)

	output = statseeker.recv(5000).decode("ascii")
	print(output)

	# Waiting for switch response
	while output == "":
		time.sleep(1)
		print(".",end="")
		output = statseeker.recv(5000).decode("ascii")
		print(output)
	return output

def show_stack_topology(statseeker):

	global file_output

	statseeker.send('\n')
	statseeker.send('show stack topology\n')
	time.sleep(1)
	output = statseeker.recv(50000).decode("ascii")
	print(output)
	file_output.append(output)
	return output

def exit_switch_ssh(statseeker):
	statseeker.send('exit\n')
	time.sleep(1)
	output = statseeker.recv(5000).decode("ascii")
	print(output)
	return output



# Script commands
def shell(statseeker):

	global switch_list, switch_user, switch_pass


	# Define Switch SSH
	switch_ssh = paramiko.SSHClient()

	# Set Host Key Policy
	switch_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())


	# Run every IP
	for position in range(len(switch_list)):


		# SSH into switch
		statseeker.send('\n')
		statseeker.send('ssh ' + switch_user + '@' + switch_list[position] + '\n')
		time.sleep(3)

		check_login_prompt = statseeker.recv(5000).decode("ascii")

		# Check to see if no fingerprint
		if "yes/no" in check_login_prompt:

			# Type 'yes' to add host
			statseeker.send('yes\n')
			time.sleep(2)
			print(statseeker.recv(5000).decode("ascii"))

			input_switch_password(statseeker)

			# Show Stack topology
			show_stack_topology(statseeker)

			# Exit Switch
			exit_switch_ssh(statseeker)

			continue



		# If asking for password 
		elif "keyboard-interactive" in check_login_prompt:

			input_switch_password(statseeker)

			# Show Stack topology
			show_stack_topology(statseeker)

			# Exit Switch
			exit_switch_ssh(statseeker)

			continue


		else:
			print(check_login_prompt)
			print("Please try again. Could not enter password for the switch.")
			exit()




def connect_statskr():


	global switch_user, switch_pass


	# Define SSH
	ssh = paramiko.SSHClient()

	# Set Host Key Policy
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())


	# Input username and password
	username = input("Statseeker Username:")
	password = getpass.getpass(prompt = "Statseeker Password:")


	# Connect SSH
	try:
		ssh.connect( hostname = hostname , username = username, password = password )
		statseeker = ssh.invoke_shell()

		# Print Statseeker message
		print(statseeker.recv(5000).decode("ascii"))

		# Log into switch
		switch_user = input("Switch Username:")
		switch_pass = getpass.getpass(prompt = "Switch Password:")

		# Go SSH to Switch IP
		shell(statseeker)

	except paramiko.BadAuthenticationType:
		print("Invalid Statseeker Credentials.")
		exit()

	return



try: 

	# Get argument length
	arg_length = len(sys.argv)


	# If argument length is one
	if(arg_length == 1):
		exit()


	# Parse through IP Addresses
	for arg_position in range(1, arg_length):


		# Fetch IP address given to the script
		inputted_ip = sys.argv[arg_position]


		# If output option is given
		if "-output" in inputted_ip:


			# If no text file, look through switch_list
			if textFile == False:

				# Log in to Statseeker if no text file
				connect_statskr()


			# Get script directory
			directory = os.path.dirname(__file__)
			# Get text file directory
			filename = os.path.join(directory, 'statseeker_' + datetime.today().strftime("%m_%d_%Y") + '.txt')
			

			# Write to file
			print("=========[ OUTPUT ]=========")
			
			f = open(filename, "w")

			# Write each switch output
			for i in range(len(file_output)):
				f.write(file_output[i])
				print(file_output[i])

			f.close()
			print("============================")

			# Exit script
			sys.exit(0)


		# If txt file is given
		elif ".txt" in inputted_ip:

			# Determine if text file is gven
			textFile = True


			# Check to see if file exist
			if os.path.isfile(inputted_ip):
									

				# Read file
				f = open(inputted_ip, "r")


				# Parse through each IP line by line
				for ip in f:


					# Remove newline from each line to get only IP address
					ip = ip.replace("\n", "")


					# Verify if IP address
					try:
						ipaddress.ip_address(ip)
					except ValueError:
						print('Invalid IP in input file.')
						continue

					# Append IP
					switch_list.append(ip)

			else:

				# If file does not exist
				print('Input file does not exist.')
				exit()


			# Log in to Statseeker
			connect_statskr()
			continue


		# If adding switch IP manually
		else:

			# Check to see if IP is valid
			try:
				ipaddress.ip_address(inputted_ip)
			except ValueError:
				print('You have inputted an invalid IP.')
				continue

			# Append IP to switch list
			switch_list.append(inputted_ip)


	# If no text file, look through switch_list
	if textFile == False:

		# Log in to Statseeker if no text file
		connect_statskr()


# IP address is invalid
except ValueError:

	print('\n')
	print('Error: Invalid IP Address')
	print('Usage: python stack-topology.py <ip or .txt file> -output')
	exit()

except SystemExit:

	exit()

except:

	print('\n')
	print('Usage: python stack-topology.py <ip or .txt file> -output')
	exit()
