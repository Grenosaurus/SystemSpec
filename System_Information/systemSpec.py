"""
 This program is used to check and get the operating systems spec information. These details can later be used 
 for illustrating benchmarking result of a specific program (Made: Jauaries).
"""


# Python packets
import psutil
import GPUtil
import platform
import speedtest
import time

from tabulate import tabulate
from win32com.client import GetObject
from datetime import datetime



# Gathering basic informations of the system
def System_Information():
    print('System Information:')
    
    # System details
    system_name = platform.uname()
    os = system_name.system
    os_Node = system_name.node
    os_Version = system_name.version
    os_Release = system_name.release
    os_Machine = system_name.machine
    os_Process = system_name.processor
    
    print(f'OS: {os}')
    print(f' - Node: {os_Node}')
    print(f' - Version: {os_Version}')
    print(f' - Release: {os_Release}')
    print(f' - Machine: {os_Machine}')
    print(f' - Processor Family: {os_Process}')
    
    # System Boot detail
    boot_Timestamp = psutil.boot_time()
    BootTime = datetime.fromtimestamp(boot_Timestamp)
    print(f'Systems Latest Boot Time: {BootTime.year}-{BootTime.month}-{BootTime.day} {BootTime.hour}:{BootTime.minute}:{BootTime.second}')


"""
 Program can also observe the internet connection speed (Upload and Download speed) if wnated.
"""


# Network detail object
class Network_Information(object):
    def __init__(self):
        self.parser = psutil.net_if_addrs()
        self.speed_parser = speedtest.Speedtest()
        self.interfaces = self.interface()[0]
    
    # Interface detail of the internet
    def interface(self):
        interfaces = []
        for interface_name, _ in self.parser.items():
            interfaces.append(str(interface_name))

        return interfaces
    
    # Stores the details into a table and returns the table
    def __repr__(self):
        interface = self.interfaces
        download = str(f'{self.speed_parser.download() / 1_000_000 :.2f}Mbps')
        upload = str(f'{self.speed_parser.upload() / 1_000_000 :.2f}Mbps')
        
        data = {'Interface' : [interface], 'Download Speed' : [download], 'Upload Speed' : [upload]}
        data_table = tabulate(data, headers = 'keys', tablefmt = 'pretty')
        
        return data_table



"""
 Due to a certain module the program can only identify NVIDIA GPU drivers and not AMD GPU drivers.
"""


# CPU details
def CPU_Information():
    print('\nCPU Information:')
    
    # CPU name
    root_winmgmts = GetObject('winmgmts:root\cimv2')
    cpu = root_winmgmts.ExecQuery('Select * from Win32_Processor')
    CPU_Name = cpu[0].name
    print(f'CPU: {CPU_Name}')

    # Number of Cores and threads
    core_Total = psutil.cpu_count(logical = True)
    core_Physical = psutil.cpu_count(logical = False)
    print(f'CPU Core: {core_Physical}\nCPU Thread: {core_Total}')

    # CPU frequency
    CPU_Freq = psutil.cpu_freq()
    Freq_Current = CPU_Freq.current # Shows actual frequency of the system
    print(f'CPU frequency: {Freq_Current :.0f}MHz')

    # Usege presentage of CPU cores (single and total)
    core_UsageTotal = psutil.cpu_percent()
    core_Percentage = psutil.cpu_percent(percpu = True, interval = 1)

    print('CPU Single Thread Usage:')
    
    for i, percentage in enumerate(core_Percentage):
        thread = i + 1
        thread_UsagePresentage = percentage
        print(f' - Thread {thread}: {thread_UsagePresentage}%')
    
    print(f'CPU Total Core Usage: {core_UsageTotal}%')


# Converst large numbers of bytes into scaled Byte format
def ByteScale(bytes, suffix = 'B'):

    factor = 1024
    data_VolumeUnit = ["", "K", "M", "G", "T", "P", "E", "Z", "Y"]

    for unit in data_VolumeUnit:
        if(bytes < factor):
            return f'{bytes :.2f}{unit}{suffix}'
        
        bytes = bytes / factor


# RAM details
def RAM_Information():
    print('\nRAM Information:')

    # Systems RAM details
    ram_Memory = psutil.virtual_memory()
    ram_Total = ByteScale(ram_Memory.total)
    ram_Available = ByteScale(ram_Memory.available)
    ram_Use = ByteScale(ram_Memory.used)
    ram_Percentage = ram_Memory.percent

    print('Memory:')
    print(f' - Total Memory: {ram_Total}')
    print(f' - Available Memory: {ram_Available}')
    print(f' - Memory Used: {ram_Use}')
    print(f' - Usage Percentage: {ram_Percentage}%')

    # Swap space details
    ram_SwapMemory = psutil.swap_memory()
    ram_SwapTotal = ByteScale(ram_SwapMemory.total)
    ram_SwapFree = ByteScale(ram_SwapMemory.free)
    ram_SwapUse = ByteScale(ram_SwapMemory.used)
    ram_SwapPrecent = ByteScale(ram_SwapMemory.percent)

    print('Swap Space:')
    print(f' - Total Memory: {ram_SwapTotal}')
    print(f' - Free Memory: {ram_SwapFree}')
    print(f' - Memory Used: {ram_SwapUse}')
    print(f' - Usage Percentage: {ram_SwapPrecent}%')


# Memory Disk details
def Disk_Information():
    print('\nDisk Information:')

    # Gets systems disk partitions
    disk_Partition = psutil.disk_partitions()

    # One or more disks in the system
    for partition in disk_Partition:
        devicePath = partition.device
        mountPoint = partition.mountpoint
        fileSystem = partition.fstype

        print(f'Disk Device Path: {devicePath}')
        print(f' - Mount Point Path: {mountPoint}')
        print(f' - Filesystem Type: {fileSystem}')

        try:
            partition_Usage = psutil.disk_usage(mountPoint)
        
        except PermissionError:
            continue

        disk_Size = ByteScale(partition_Usage.total)
        memory_Used = ByteScale(partition_Usage.used)
        memory_Free = ByteScale(partition_Usage.free)
        memory_UsagePercentage = partition_Usage.percent

        print(f' - Total Size of Disk: {disk_Size}')
        print(f' - Free Space: {memory_Free}')
        print(f' - Used Space: {memory_Used}')
        print(f' - Usage Percentage: {memory_UsagePercentage}%')
    
    # Write and read byte sizes
    disk_io = psutil.disk_io_counters()
    disk_read = ByteScale(disk_io.read_bytes)
    disk_write = ByteScale(disk_io.write_bytes)

    print(f' - Disk Total Read: {disk_read}')
    print(f' - Disk Total Write: {disk_write}')


# GPU details
def GPU_Information():
    print('\nGPU Information:')

    # Getting systems GPU
    gpu = GPUtil.getGPUs()
    
    # One or multiple GPU in the system
    for gpu_i in gpu:
        gpu_Name = gpu_i.name
        gpu_Load = gpu_i.load * 100 # In percentage [%]
        gpu_TotalMemory = ByteScale(gpu_i.memoryTotal)
        gpu_UsedMemory = ByteScale(gpu_i.memoryUsed)
        gpu_FreeMemory = ByteScale(gpu_i.memoryFree)
        gpu_Temperature = gpu_i.temperature # In celcius [C]
        
        print(f'GPU: {gpu_Name}')
        print(f' - GPU Load: {gpu_Load}%')
        print(f' - Total Memory: {gpu_TotalMemory}')
        print(f' - Used Memory: {gpu_UsedMemory}')
        print(f' - Free Memory: {gpu_FreeMemory}')
        print(f' - Temperature: {gpu_Temperature}\N{DEGREE SIGN}C')

  

def main():
    System_Information()
    
    # System Spec details
    CPU_Information()
    RAM_Information()
    Disk_Information()
    GPU_Information()
    
    # Network speed (Optional)
    Network = Network_Information()
    print(f'\n {Network}')

# Generates teh total time used by teh program to complete
if __name__ == "__main__":
    # Time of main function
    start_time = time.time() # Start time of the main function
    main()
    end_time = time.time() # End time of the main function

    # Delta time
    Delta_time_milliseconds = (end_time - start_time) * 1000 # Difference between start and end time (defined in milliseconds) | 1s = 1000 ms
    Delta_time_minutes = Delta_time_milliseconds/(60 * 1000) # Difference between start and end time (defined in minutes) | 1 min = 60 s

    # Round value of delta time
    Delta_time_milliseconds_round = round(Delta_time_milliseconds, 2)
    Delta_time_minutes_round = round(Delta_time_minutes, 2)

    # Prints the time took for the program to run
    print(f'\nProgram took: {Delta_time_milliseconds_round}ms (~ {Delta_time_minutes_round}min).\n')
