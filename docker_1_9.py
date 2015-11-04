"""ShutIt module. See http://shutit.tk
"""

from shutit_module import ShutItModule


class docker_1_9(ShutItModule):


	def build(self, shutit):
		# Some useful API calls for reference. See shutit's docs for more info and options:
		#
		# ISSUING BASH COMMANDS
		# shutit.send(send,expect=<default>) - Send a command, wait for expect (string or compiled regexp)
		#                                      to be seen before continuing. By default this is managed
		#                                      by ShutIt with shell prompts.
		# shutit.multisend(send,send_dict)   - Send a command, dict contains {expect1:response1,expect2:response2,...}
		# shutit.send_and_get_output(send)   - Returns the output of the sent command
		# shutit.send_and_match_output(send, matches) 
		#                                    - Returns True if any lines in output match any of 
		#                                      the regexp strings in the matches list
		# shutit.send_until(send,regexps)    - Send command over and over until one of the regexps seen in the output.
		# shutit.run_script(script)          - Run the passed-in string as a script
		# shutit.install(package)            - Install a package
		# shutit.remove(package)             - Remove a package
		# shutit.login(user='root', command='su -')
		#                                    - Log user in with given command, and set up prompt and expects.
		#                                      Use this if your env (or more specifically, prompt) changes at all,
		#                                      eg reboot, bash, ssh
		# shutit.logout(command='exit')      - Clean up from a login.
		# 
		# COMMAND HELPER FUNCTIONS
		# shutit.add_to_bashrc(line)         - Add a line to bashrc
		# shutit.get_url(fname, locations)   - Get a file via url from locations specified in a list
		# shutit.get_ip_address()            - Returns the ip address of the target
		# shutit.command_available(command)  - Returns true if the command is available to run
		#
		# LOGGING AND DEBUG
		# shutit.log(msg,add_final_message=False) -
		#                                      Send a message to the log. add_final_message adds message to
		#                                      output at end of build
		# shutit.pause_point(msg='')         - Give control of the terminal to the user
		# shutit.step_through(msg='')        - Give control to the user and allow them to step through commands
		#
		# SENDING FILES/TEXT
		# shutit.send_file(path, contents)   - Send file to path on target with given contents as a string
		# shutit.send_host_file(path, hostfilepath)
		#                                    - Send file from host machine to path on the target
		# shutit.send_host_dir(path, hostfilepath)
		#                                    - Send directory and contents to path on the target
		# shutit.insert_text(text, fname, pattern)
		#                                    - Insert text into file fname after the first occurrence of 
		#                                      regexp pattern.
		# shutit.delete_text(text, fname, pattern)
		#                                    - Delete text from file fname after the first occurrence of
		#                                      regexp pattern.
		# shutit.replace_text(text, fname, pattern)
		#                                    - Replace text from file fname after the first occurrence of
		#                                      regexp pattern.
		# ENVIRONMENT QUERYING
		# shutit.host_file_exists(filename, directory=False)
		#                                    - Returns True if file exists on host
		# shutit.file_exists(filename, directory=False)
		#                                    - Returns True if file exists on target
		# shutit.user_exists(user)           - Returns True if the user exists on the target
		# shutit.package_installed(package)  - Returns True if the package exists on the target
		# shutit.set_password(password, user='')
		#                                    - Set password for a given user on target
		#
		# USER INTERACTION
		# shutit.get_input(msg,default,valid[],boolean?,ispass?)
		#                                    - Get input from user and return output
		# shutit.fail(msg)                   - Fail the program and exit with status 1
		# 
		shutit.send('rm -rf /tmp/docker1_9')
		box = shutit.send_and_get_output('vagrant box list 2>/dev/null | grep jayunit100/centos7')
		if box == '':
			shutit.send('vagrant box add https://atlas.hashicorp.com/jayunit100/boxes/centos7',note='Download the ubuntu vagrant box')
		shutit.send('mkdir /tmp/docker1_9 && cd /tmp/docker1_9 && vagrant init jayunit100/centos7 && vagrant up',note='vagrant up')
		shutit.login(command='vagrant ssh',note='Log into the VM')
		shutit.login(user='root',command='sudo su - root')
		shutit.send('curl https://get.docker.com/builds/Linux/x86_64/docker-latest > /usr/bin/docker')
		shutit.send('chmod +x /usr/bin/docker')
		shutit.send('nohup docker daemon &')
		shutit.send('VID=$(docker volume create --name mydata)',note='Create a volume called "mydata" and store its id')
		shutit.send('docker volume ls',note='List the volumes')
		# TODO: Flocker? https://docs.clusterhq.com/en/1.5.0/install/docker-plugin.html
		# http://docs.docker.com/engine/extend/plugins_volume/
		shutit.send('docker network create --subnet 192.168.1.0/4 bob',note='Create a network in the specified subnet called "bob"')
		shutit.send('docker network ls',note='List networks available')
		shutit.send('docker run -d --name c1 debian sleep infinity',note='Start a container')
		shutit.send('docker inspect c1',note='''Inspect this container's network section''')
		shutit.send('docker network connect bob c1',note='Connect the container just-created ')
		shutit.send('docker inspect c1',note='See how bob is now connected to this container, and it has been allocated an IP address in the subnet we specified.')
		shutit.login(command='docker exec -ti c1 bash',note='See how bob is now connected to this container, and it has been allocated an IP address in the subnet we specified.')
		shutit.send('apt-get upgrade && apt-get install net-tools',note='Install net tools')
		shutit.send('ifconfig',note='Observer that this container now has another eth interface with the relevant address')
		shutit.logout()
		shutit.send_file('/tmp/Dockerfile','''FROM debian
ARG string
RUN echo $string > /bakedstr''',note='create a simple image with a build-time arg')
		shutit.send('cd /tmp')
		shutit.send('docker build -t image1 --build-arg=string="I am image 1" .',note='Build image 1 with a build-time argument from a Dockerfile')
		shutit.send('docker build -t image2 --build-arg=string="I am image 2" .',note='Build image 2 with a different build-time argument from the same Dockerfile')
		shutit.send('docker run image1 cat /tmp/bakedstr" .',note='Show baked-in string on image 1')
		shutit.send('docker run image2 cat /tmp/bakedstr" .',note='Show baked-in string on image 2')
		shutit.pause_point('')
		shutit.logout()
		return True

	def get_config(self, shutit):
		# CONFIGURATION
		# shutit.get_config(module_id,option,default=None,boolean=False)
		#                                    - Get configuration value, boolean indicates whether the item is 
		#                                      a boolean type, eg get the config with:
		# shutit.get_config(self.module_id, 'myconfig', default='a value')
		#                                      and reference in your code with:
		# shutit.cfg[self.module_id]['myconfig']
		return True

	def test(self, shutit):
		# For test cycle part of the ShutIt build.
		return True

	def finalize(self, shutit):
		# Any cleanup required at the end.
		return True
	
	def is_installed(self, shutit):
		return False


def module():
	return docker_1_9(
		'shutit.docker_1.9.docker_1_9.docker_1_9', 1113159394.00,
		description='',
		maintainer='',
		delivery_methods=['bash'],
		depends=['tk.shutit.vagrant.vagrant.vagrant']
	)

