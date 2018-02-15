
import subprocess
import os

module_dir = os.path.split(__file__)[0]
print module_dir



dir_path = os.path.dirname(os.path.realpath(__file__))
print dir_path

path = os.path.join(dir_path, "../")
print path

print os.getcwd()

jar_path = "~/Sikuli/sikulix.jar"

package = "org.python.util.jython"
init_path = "~/Sikuli/test.py"

cmd = ['java', '-cp', jar_path, package, init_path]
print cmd
p = subprocess.Popen(cmd).communicate()