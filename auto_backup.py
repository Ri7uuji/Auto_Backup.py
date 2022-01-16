import sys
import os
import datetime


def printHelp():
    """
        Outputs help.
    """
    print("flags:")
    print('[-t=time_in_min]       interval of backup')
    print('[-p=path]            str of file/folder path')
    print('[-tp=path]           backup folder')
    print('[-n=int]             number of backups b4 deletion, if undefined no backups will be deleted. 2 is the minimum.')


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

    # if numberOfBkUps < 2:
        #numberOfBkUps = 2

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

    lines = []

    with open("backupcount.autobkup", "r") as f:
        lines = f.readlines()
        f.close()

    if n_argpos != 0 and len(lines) >= numberOfBkUps:
        os.remove(lines[0].replace("\n", ""))
        os.remove("backupcount.autobkup")
        os.mknod("backupcount.autobkup")

        with open("backupcount.autobkup", "r+") as f:
            lines.remove(lines[0])
            f.writelines(lines)

    if os.path.exists("callme.sh"):
        os.remove("callme.sh")
    os.system(
        f'tar -czf {bkupdestination}{splitPath[len(splitPath)-1]}_{datetime.datetime.now().strftime("%d-%m-%Y_%H-%M")}.tar.gz {path}')

    with open("backupcount.autobkup", "w") as f:
        f.write(
            f'{bkupdestination}{splitPath[len(splitPath)-1]}_{datetime.datetime.now().strftime("%d-%m-%Y_%H-%M")}.tar.gz\n')
        f.close()

    os.mknod("callme.sh")

    with open("callme.sh", "w") as f:
        f.write("#!/bin/bash\n")
        f.write("cd "+os.path.realpath(__file__).replace("auto_backup.py", "")+"\n")
        combinedArgs = ''
        for eachArg in arguments:
            combinedArgs += eachArg + " "
        f.write(f'python3 {combinedArgs}')

    os.system(f'chmod +x callme.sh')
    os.system(f'at now + {interval} minute -f callme.sh')
