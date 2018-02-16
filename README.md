# iris
Visual Test Suite for Firefox

* Supports Mac, Windows and Ubuntu Linux.
* Requires Java SDK 8 (Mac) or 7/8 (Linux). Does not work with Java 9.
* All instructions assume that Git is already installed.
* Please note that this project is in its earliest stage and may have issues.

## Mac instructions:

1. Download and install the [Java 8 JRE](http://www.oracle.com/technetwork/java/javase/downloads/jre8-downloads-2133155.html
).
2. In your file `~/.bash_profile`, add this line:
```
export JAVA_HOME=/Library/Java/JavaVirtualMachines/jdk1.8.0_161.jdk/Contents/Home
```
3. Download and install the [Sikuli IDE](https://launchpad.net/sikuli/sikulix/1.1.1/+download/sikulixsetup-1.1.1.jar). When prompted for options, choose all three packages.
* Note: Sikuli must be installed in `/Applications/Sikuli`
4. In your console, type the following to run the test suite.
```
git clone https://github.com/mozilla/iris
cd iris
virtualenv .
source bin/activate
pip install -e .
iris
````

## Windows instructions:

1. Install Python 2.7
2. Add the following paths to your system environment variable for PATH:
```
C:\Python27;C:\Python27\Scripts
```
3. Download and install the [Java 8 JRE](http://www.oracle.com/technetwork/java/javase/downloads/jre8-downloads-2133155.html
).
4. Create a directory for ```C:\Sikuli```
5. Download and install the [Sikuli IDE](https://launchpad.net/sikuli/sikulix/1.1.1/+download/sikulixsetup-1.1.1.jar) into this directory. When prompted for options, choose all three packages.
6. Launch the terminal and run the following commands:
```
git clone https://github.com/mozilla/iris
cd iris
virtualenv .
Scripts\activate
pip install -e .
iris
```

## Ubuntu Linux instructions:

Note: We are having some problems on Linux at the moment, but the tests can be run via a workaround.

1. Launch the terminal and run the following commands:
```
cd ~
git clone https://github.com/mozilla/iris
cd iris
cd bootstrap
./linux_bootstrap.sh
```
2. Create a directory under your home directory called `Sikuli`.
3. Download and install the [Sikuli IDE](https://launchpad.net/sikuli/sikulix/1.1.1/+download/sikulixsetup-1.1.1.jar) into this directory. When prompted for options, choose all three packages.
4. Return to your terminal and run the following commands:
```
cd ~/iris
virtualenv .
source bin/activate
pip install -e .
```
5. This next line is the workaround.
```
java -cp ~/Sikuli/sikulix.jar org.python.util.jython ./iris/iris.py
```
    
