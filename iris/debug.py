
import subprocess
import os

temp = os.path.expanduser(os.getcwd()).split("/")
jar_path = os.path.join(temp[1], temp[2], "Sikuli/sikulix.jar")


package = "org.python.util.jython"



init_path = os.path.join(temp[1], temp[2], "Sikuli/test.py")


cmd = ['java', '-cp', jar_path, package, init_path]
print cmd
p = subprocess.Popen(cmd).communicate()