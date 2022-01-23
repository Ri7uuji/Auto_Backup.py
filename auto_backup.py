import sys
import os
import datetime
import subprocess


def printHelp():
    """
        Outputs help.
    """
    print("flags:")
    print('[-t=time_in_min]     interval of backup')
    print('[-t2=<int><w/d/m>]   interval of secondary backup')
    print('[-p=path]            str of file/folder path')
    print('[-tp=path]           backup folder')
    print('[-tp2=path]          backup folder for 2ndary backups')
    print('[-n=int]             number of backups b4 deletion, if undefined no backups will be deleted')
    print('[-n2=int]            same as n just for secondary backups')


if __name__ == '__main__':
    arguments = sys.argv
    if len(arguments) < 2:
        printHelp()
        quit()

    count = len(arguments)-1
    t_argpos = int()
    t_argpos = 0
    p_argpos = int()
    p_argpos = 0
    tp_argpos = int()
    tp_argpos = 0
    n_argpos = int()
    n_argpos = 0
    t2_argpos = int()
    t2_argpos = 0
    n2_argpos = int()
    n2_argpos = 0
    tp2_argpos = int()
    tp2_argpos = 0
    tb_argpos = int()
    tb_argpos = 0

    while count >= 1:
        try:
            idx = arguments[count].index("-t=")
            t_argpos = count

        except Exception:
            try:
                idx = arguments[count].index("-p=")
                p_argpos = count
            except Exception:
                try:
                    idx = arguments[count].index("-n=")
                    n_argpos = count
                except Exception:
                    try:
                        idx = arguments[count].index("-tp=")
                        tp_argpos = count
                    except Exception:
                        try:
                            idx = arguments[count].index("-n2=")
                            n2_argpos = count
                        except Exception:
                            try:
                                idx = arguments[count].index("-t2=")
                                t2_argpos = count
                            except Exception:
                                try:
                                    idx = arguments[count].index("-tb=")
                                    tb_argpos = count     
                                except Exception:
                                    try:
                                        idx = arguments[count].index("-tp2=")
                                        tp2_argpos = count
                                    except Exception:
                                        None            
        count -= 1

    if t_argpos == 0:
        print("Interval not given.")
        printHelp()
        quit()

    if p_argpos == 0:
        print("Backup path is not given.")
        printHelp()
        quit()

    if tp_argpos == 0:
        print("Save dir for Backup is not given.")
        printHelp()
        quit()

    interval = arguments[t_argpos].replace("-t=", "")
    interval = interval.replace("m", "")

    try:
        interval = int(interval)
    except Exception:
        print(f'{interval} isnt a time. Format: -t=<int>.')
        printHelp()
        quit()

    path = arguments[p_argpos].replace("-p=", "")

    if not os.path.exists(path):
        print(f'{path} is not a path.')
        printHelp()
        quit()

    bkupdestination = arguments[tp_argpos].replace("-tp=", "")

    if not os.path.exists(bkupdestination):
        print(f'{bkupdestination} is not a path.')
        printHelp()
        quit()

    if not n_argpos == 0:
        numberOfBkUps = arguments[n_argpos].replace("-n=", "")
        try:
            numberOfBkUps = int(numberOfBkUps)
        except Exception:
            print(f'{numberOfBkUps} is not an int.')
            printHelp()
            quit()

    if not n2_argpos == 0:
        numberOf2ndBkUps = arguments[n2_argpos].replace("-n2=", "")
        try:
            numberOf2ndBkUps = int(numberOf2ndBkUps)
        except Exception:
            print(f'{numberOf2ndBkUps} is not an int.')
            printHelp()
            quit()

    if not t2_argpos == 0:
        t2Str = arguments[t2_argpos].replace("-t2=", "")
        week = False
        day = False
        minute = False 
        try:
            idx = t2Str.index("w")
            week = True
        except Exception:
            try:
                idx = t2Str.index("d")
                day = True
            except Exception:
                try:
                    idx = t2Str.index("m")
                    minute = True
                except Exception:
                    None
        if not week and not day and not minute:
            print("Wrong t2 format.")
            printHelp()
            quit()
        
        try:
            if week:
                t2Str = t2Str.replace("w", "")
                interval2Type = "week"
            elif day:
                t2Str = t2Str.replace("d", "")
                interval2Type = "day"
            elif minute:
                t2Str = t2Str.replace("m", "")
                interval2Type = "minute"
            
            t2int = int(t2Str)
        except Exception:
            print('Wrong t2 time format.')
            print(f'{t2Str} is not an int.')
            printHelp()
            quit()
        
    if not tb_argpos == 0:
        tbStr = arguments[tb_argpos].replace("-tb=","")
        try:
            tbBool = bool(tbStr == "True")
        except Exception:
            quit()

    if not t2_argpos == 0 and not n2_argpos == 0 and tp2_argpos == 0:
        print("Tp2 is missing.")
        printHelp()
        quit()

    if not tp2_argpos == 0:
        scndpath = arguments[tp2_argpos].replace("-tp2=", "")
        if not os.path.exists(scndpath):
            print(f'{scndpath} is not a path.')
            printHelp()
            quit()
        if  bkupdestination == scndpath:
            print(f'tp cant be the same as tp2.')
            printHelp()
            quit()
    
    if path[len(path)-1] == "/":
        newPath = ""
        i = 0
        for char in path:
            if not i == len(path)-1:
                newPath += char
            i += 1
        path = newPath

    if not bkupdestination[len(bkupdestination)-1] == "/":
        bkupdestination += "/"

    splitPath = path.split("/")
    if not os.path.exists("backupcount.autobkup"):
        os.mknod("backupcount.autobkup")

    if (not tb_argpos == 0 and tbBool) or tb_argpos == 0:
        if not os.path.exists("backupcount2.autobkup"):
            os.mknod("backupcount2.autobkup")
        
        lines2 = []

        with open("backupcount2.autobkup", "r") as f:
            lines2 = f.readlines(-1)
            f.close()

        if n2_argpos != 0 and len(lines2) >= numberOf2ndBkUps:
            os.remove(lines2[0].replace("\n", ""))
            os.remove("backupcount2.autobkup")
            os.mknod("backupcount2.autobkup")
            with open("backupcount2.autobkup", "r+") as f:
                lines2.remove(lines2[0])
                f.writelines(lines2)
                f.close()

        if os.path.exists("callmetwo.sh"):
            os.remove("callmetwo.sh")
        fileName =f'{scndpath}{splitPath[len(splitPath)-1]}_{datetime.datetime.now().strftime("%d-%m-%Y_%H-%M")}.tar.gz'
        os.system(
            f'tar -czf {fileName} {path}')

        with open("backupcount2.autobkup", "w") as f:
            f.writelines(lines2)
            f.write(
                f'{fileName}\n')
            f.close()

        os.mknod("callmetwo.sh")

        with open("callmetwo.sh", "w") as f:
            f.write("cd "+os.path.realpath(__file__).replace("auto_backup.py", "")+"\n")
            combinedArgs = ''
            for eachArg in arguments:
                combinedArgs += eachArg + " "

            if tb_argpos == 0:
                combinedArgs += "-tb=True "

            f.write(f'python3 {combinedArgs}')
            f.close()

        os.system(f'chmod +x callmetwo.sh')
        os.system(f'at now + {t2int} {interval2Type} -f callmetwo.sh')

        if not tb_argpos == 0 and tbBool:
         quit() 

          

    lines = []

    with open("backupcount.autobkup", "r") as f:
        lines = f.readlines(-1)
        f.close()

    if n_argpos != 0 and len(lines) >= numberOfBkUps:
        os.remove(lines[0].replace("\n", ""))
        os.remove("backupcount.autobkup")
        os.mknod("backupcount.autobkup")
        with open("backupcount.autobkup", "r+") as f:
            lines.remove(lines[0])
            f.writelines(lines)
            f.close()

    if os.path.exists("callme.sh"):
        os.remove("callme.sh")
    fileName =f'{bkupdestination}{splitPath[len(splitPath)-1]}_{datetime.datetime.now().strftime("%d-%m-%Y_%H-%M")}.tar.gz'
    os.system(
        f'tar -czf {fileName} {path}')

    with open("backupcount.autobkup", "w") as f:
        f.writelines(lines)
        f.write(
            f'{fileName}\n')
        f.close()

    os.mknod("callme.sh")

    with open("callme.sh", "w") as f:
        f.write("cd "+os.path.realpath(__file__).replace("auto_backup.py", "")+"\n")
        combinedArgs = ''
        for eachArg in arguments:
            combinedArgs += eachArg + " "
        if tb_argpos == 0:
            combinedArgs += "-tb=False "
        f.write(f'python3 {combinedArgs}')
        f.close()

    os.system(f'chmod +x callme.sh')
    os.system(f'at now + {interval} minute -f callme.sh')
