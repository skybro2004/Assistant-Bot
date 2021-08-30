def returnPath(fileName):
    #궁예
    if fileName.startswith("궁예"):
        return f"궁예/{fileName}.png"

    #달걀콘
    if fileName=="갈":
        return f"달걀/갈.png"
    elif fileName=="뇌절":
        return f"달걀/뇌절.png"
    elif fileName=="마참내":
        return f"달걀/마참내.png"
    elif fileName=="손도깔끔":
        return f"달걀/손도깔끔.png"
    elif fileName=="시간절약":
        return f"달걀/시간절약.png"
    elif fileName=="즐겁다":
        return f"달걀/즐겁다.png"

    #메탈슬러그 키
    if fileName=="f":
        return f"메탈슬러그/F.gif"
    elif fileName=="h":
        return f"메탈슬러그/H.gif"
    elif fileName=="l":
        return f"메탈슬러그/L.gif"
    elif fileName=="r":
        return f"메탈슬러그/R.gif"
    elif fileName=="s":
        return f"메탈슬러그/S.gif"

    #앵무
    if fileName.endswith("앵무"):
        return f"앵무/{fileName}.gif"

    #야인시대
    if fileName=="말도안돼":
        return f"야인시대/말도안돼.png"
    elif fileName=="사딸라" or fileName=="4딸라" or fileName=="4달라" or fileName=="사달라":
        return f"야인시대/사딸라.png"
    elif fileName=="상하이조" or fileName=="심영발사" or fileName=="프린세스메이커":
        return f"야인시대/상하이조.gif"
    elif fileName=="심영박수":
        return f"야인시대/심영박수.gif"
    elif fileName=="심영박수2":
        return f"야인시대/심영박수2.gif"
    elif fileName=="연막" or fileName=="심영연막":
        return f"야인시대/연막.gif"
    elif fileName=="오케이땡큐":
        return f"야인시대/오케이땡큐.png"
    elif fileName=="폭발" or fileName=="심영폭발":
        return f"야인시대/폭발.gif"

    #에펙
    if "눈물" in fileName:
        return f"에펙/{fileName}.png"
    elif fileName=="뱀부즐":
        return f"에펙/뱀부즐.png"
    elif fileName=="뱀뱀부즐":
        return f"에펙/뱀뱀부즐.png"
    elif fileName=="고뱀부즐":
        return f"에펙/고뱀부즐.png"
    elif fileName=="뱀부맘":
        return f"에펙/뱀부맘.png"
    
    #우리핵
    if fileName.startswith("우리핵"):
        return f"우리핵/{fileName}.gif"

    #인공지능
    if fileName.startswith("딥러닝"):
        return f"인공지능/{fileName}.png"

    #잼민
    if fileName=="미국잼민" or fileName=="지건":
        return f"잼민이/미국잼민.png"
    elif fileName=="잼민":
        return f"잼민이/잼민.png"
    elif fileName=="잼민2":
        return f"잼민이/잼민2.png"
    elif fileName=="잼민3":
        return f"잼민이/잼민3.png"
    elif fileName=="잼민4":
        return f"잼민이/잼민4.png"

    #ㅊㅈㅇ
    if fileName=="최재원" or fileName=="아갈하트" or fileName=="입하트":
        return "최재원.png"
    elif fileName=="청정원":
        return "청정원.png"

    #코주부
    elif fileName=="코주부한심":
        return "코주부/코주부한심.png"
    elif fileName=="코주부놀람" or fileName=="코주부화남":
        return "코주부/코주부놀람.png"

    #~풍당당
    if fileName.startswith("문풍당당"):
        return f"풍당당/{fileName}.gif"
    elif fileName.startswith("이풍당당"):
        return f"풍당당/{fileName}.gif"
    elif fileName=="예풍당당":
        return "풍당당/예풍당당.gif"

    #프밍
    if fileName=="스택플로" or fileName=="스택오버플로":
        return f"프밍/스택플로.png"
    elif fileName=="타이핑":
        return f"프밍/타이핑.gif"
    elif fileName=="프밍" or fileName=="프로그래밍":
        return f"프밍/프로그래밍.gif"
    
    #핫산
    if fileName.startswith("핫산"):
        return f"핫산/{fileName}.png"

    #그 외
    if fileName=="광클":
        return "광클.gif"
    elif fileName=="댄스로이":
        return f"댄스로이.gif"
    elif fileName=="뇌혼란":  
        return "뇌혼란.gif"
    elif fileName=="무지개엿":
        return f"무지개엿.png"
    elif fileName=="발작":
        return "발작.gif"
    elif fileName=="벽박이" or fileName=="꼴박":
        return f"벽박이.png"
    elif fileName=="산" or fileName=="수화":
        return f"산.png"
    elif fileName=="좌절":
        return f"좌절.gif"
    elif fileName=="짜라빠빠":
        return f"짜라빠빠.png"
    elif fileName=="하수구토":
        return "하수구토.png"
    elif fileName=="회전잇님":
        return f"회전잇님.gif"

    return "Notfound"