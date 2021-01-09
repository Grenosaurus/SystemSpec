# SystemSpec
Program gives system spec details (CPU, RAM, GPU, Disk, ...). The program can be used to test the benchmarking of a specific program. Program is operated in the following method, depending on the operating system (OS).

Windows:
      
      python .\System_Information\systemSpec.py

Linux:
      
      python3 /System_Information/systemSpec.py


The program is written in Python 3 and the modules used in the program can be found in the requirments.txt file. Some of the modules used to write this program will not function in Python 2 so it is recomended to download Python 3.

When installing the packets 'speedtest', remeber to check that you are installing the correct packets. In python there are two packages named 'speedtest' and 'speedtest-cli', the one we use in this program is called 'speedtest-cli'. If you have accidentally installed both or just 'speedtest', you can uninstall the packages with the following command:
      
      pip uninstall speedtest

If they both are installed then the program will not recognize the right python packets and cry the following error message:
      
      AttributeError: module 'speedtest' has no attribute 'Speedtest'

# Purpose
SystemSpec program was orginaly created to aid in testing and analyzing the benchmarking of a specific program while observing the systems spec data.
