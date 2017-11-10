import jpype

jpype.startJVM(jpype.getDefaultJVMPath())

# you can then access to the basic java functions
jpype.java.lang.System.out.println("hello world")

# and you have to shutdown the VM at the end
jpype.shutdownJVM()
