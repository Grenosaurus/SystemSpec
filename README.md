# SystemSpec
Program gives system spec details (CPU, RAM, GPU, Disk, ...). The program can be used to test the benchmarking of a specific program. Program is operated in the following method, depending on the operating system (OS).

Windows:
      
      python .\System_Information\systemSpec.py

Linux:
      
      python3 /System_Information/systemSpec.py


The program is written in Python 3 and the modules used in the program can be found in the requirments.txt file. Some of the modules used to write this program will not function in Python 2 so it is recomended to download Python 3.

When installing the packets 'speedtest', remeber to check that you are installing the correct packets. In python there are two packages named 'speedtest' and 'speedtest-cli', the one we use in this program is called 'speedtest-cli'. If accidentally installed both or just 'speedtest' module is installed the program will not run and the following error will be cied out:

      AttributeError: module 'speedtest' has no attribute 'Speedtest'
      
The module can be uninstalled with the following command:
      
      pip uninstall speedtest

# Purpose
SystemSpec program was orginaly created to aid in testing and analyzing the benchmarking of a specific program while observing the systems spec data.
