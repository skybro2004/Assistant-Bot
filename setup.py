import os

#파일 경로
path = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")

def setup():
    while 1:
        token = input("디스코드 봇의 토큰을 입력해주세요 : ")
        
        if token=="":
            print("디스코드 봇의 토큰을 정확히 입력해주세요!")
        else:
            break

    with open(path + "/token.txt", "w") as tokenFile:
        tokenFile.write(token)

    while 1:
        key = input("나이스 api 키를 입력해주세요 : ")
        
        if key=="":
            print("api 키를 정확히 입력해주세요!")
        else:
            break

    with open(path + "/modules/key.txt", "w") as keyFile:
        keyFile.write(key)

    device = input("봇을 호스팅할 기기의 이름을 입력해주세요(선택) : ")

    if not(device==""):
        with open(path + "/device.txt", "w") as deviceFile:
            deviceFile.write(device)

    return token


if __name__=="__main__":
    setup()
