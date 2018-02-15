
import subprocess
import os



module_dir = os.path.split(__file__)[0]

path = os.path.join(module_dir, "..")

print path

jar_path = "~/Sikuli/sikulix.jar"

package = "org.python.util.jython"
init_path = "~/Sikuli/test.py"

cmd = ['java', '-cp', jar_path, package, init_path]
print cmd
p = subprocess.Popen(cmd).communicate()