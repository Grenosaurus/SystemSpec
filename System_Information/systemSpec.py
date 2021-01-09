"""CPU
 This program is used to check and get the operating systems spec information. These details can later be used 
 for illustrating benchmarking result of a specific program (Made: Jauaries).
"""


# Python packets
import psutil
import GPUtil
import platform
import speedtest

from tabulate import tabulate
from win32com.client import GetObject
from datetime import datetime


"""
 Due to a certain module the program can only identify NVIDIA GPU drivers and not AMD GPU drivers.
"""


# Converst large numbers of bytes into scaled Byte format
def ByteScale(bytes, suffix = 'B'):

    factor = 1024
    unit_Format = ["", "K", "M", "G", "T", "P"]

    for unit in unit_Format:
        if(bytes < factor):
            return f'{bytes :.2f}{unit}{suffix}'
        
        bytes = bytes / factor


# CPU details
def CPU_Information():
    print('CPU Information:')
    
    # CPU name
    root_winmgmts = GetObject('winmgmts:root\cimv2')
    cpu = root_winmgmts.ExecQuery('Select * from Win32_Processor')
    CPU_Name = cpu[0].name
    print(f'CPU: {CPU_Name}')

    # Number of physical and total cores
    core_Total = psutil.cpu_count(logical = True)
    core_Physical = psutil.cpu_count(logical = False)
    print(f'CPU Core Number (N)\nTotal: {core_Total}\nPhysical: {core_Physical}')

    # CPU frequency
    CPU_Freq = psutil.cpu_freq()
    Freq_Current = CPU_Freq.current # Shows actual frequency of the system
    print(f'CPU frequency: {Freq_Current :.2f}MHz')

    # Usege presentage of CPU cores (single and total)
    core_UsageTotal = psutil.cpu_percent()
    core_Percentage = psutil.cpu_percent(percpu = True, interval = 1)
    
    print(f'CPU total Core Usage: {core_UsageTotal}%')
    print('CPU Single Core Usage:')
    
    for i, percentage in enumerate(core_Percentage):
        core = i + 1
        core_UsagePresentage = percentage
        print(f' - Core {core}: {core_UsagePresentage}%')



# RAM details
def RAM_Information():
    print('\nRAM Information:')

    # Memory details
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
    print('GPU Information:')

    # Getting systems GPU details
    gpu = GPUtil.getGPUs()
    list





def main():
    CPU_Information()
    RAM_Information()
    Disk_Information()
    GPU_Information()
    
main()