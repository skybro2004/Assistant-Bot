import subprocess

def status():
    status = subprocess.getstatusoutput("sudo systemctl is-active openvpn")
    status = status[1]
    return status

def turn_on():
    subprocess.call("sudo systemctl start openvpn", shell=True)

def turn_off():
    subprocess.call("sudo systemctl stop openvpn", shell=True)

if __name__=="__main__":
    try:
        while 1:
            print(status())
            command = input("1.turn on\n2. turn off\n")
            if command=="1" or command.replace(" ", "")=="turnon":
                turn_on()
            elif command=="2" or command.replace(" ", "")=="turnoff":
                turn_off()
            else:
                print("not found")
    except KeyboardInterrupt:
        print("shutdown...")
