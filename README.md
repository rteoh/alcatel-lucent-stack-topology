# Automate Alcatel Lucent Switch CLI Command Template


This Python script allows you to automate Alcatel Lucent commands for multiple switches at a time. In this case, the *show stack topology* command.
The script is designed for organizations who has to first SSH into a server before accessing any Alcatel Lucent switches. Feel free to modify this script based on your needs/commands. (*starting at line 45*)


## How to use:

Run CLI command on 10.0.0.1:
<code>python stack-topology.py 10.0.0.1</code>


Run CLI command on 10.0.0.1 along with its output:
<code>python stack-topology.py 10.0.0.1 -output</code>


Run CLI command on a list of IP addresses from a .txt file:
<code>python stack-topology.py ip_list.txt</code>


Run CLI command on a list of IP addresses with its output:
<code>python stack-topology.py ip_list.txt -output</code>

*<b>.txt files must have one IP address per a line</b>*

