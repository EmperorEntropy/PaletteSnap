###
# Modules
###
import subprocess
from .console import console

###
# Helper Function
###
def isProgramOpen(name):
    '''checks if program is currently open or not'''
    output = subprocess.run(f"pgrep -a {name}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if output.returncode == 0:
        return True
    else:
        return False

###
# Main Function
###
def refreshProgram(program, cmd):
    '''refresh opened programs'''
    if isProgramOpen(program):
        console.log(f"Refreshing [u]{program}[/u]")
        subprocess.run(cmd.split())