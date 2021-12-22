import json, os
import urllib.request as ul
import urllib.parse as parse

#파일 경로
path = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")

#api키
try:
    with open(path + '/key.txt') as key:
        key = key.readline()
except FileNotFoundError:
    from setup import setup
    setup()
    with open(path + '/key.txt') as key:
        key = key.readline()

#학교 검색
def schlInfo(schlName):
    #url 정하기
    schlUrl = f"https://open.neis.go.kr/hub/schoolInfo?KEY={key}&Type=json"
    schlUrl += f"&SCHUL_NM={parse.quote(schlName)}"
    #요청
    request = ul.Request(schlUrl)
    #응답
    response = ul.urlopen(request)

    #정상적으로 불러옴
    if response.getcode()==200:
        #응답 데이터 읽기
        responseData = response.read()
        #json으로 디코드
        responseData = json.loads(responseData)

        try:
            schlCount = responseData["schoolInfo"][0]["head"][0]["list_total_count"]
            #검색된 학교가 5개 이상이면 다시 검색
            if 5<schlCount:
                return {"code":0}
            #데이터 정제
            responseData = responseData["schoolInfo"][1]["row"]
            schools = []
            #필요한 데이터(학교 이름, 도,시 이름, 학교 코드, 도,시 코드)만 뽑아와서 school 배열 안에 정리
            for i in range(schlCount):
                schools.append({"schlName":responseData[i]["SCHUL_NM"], "schlCode":responseData[i]["SD_SCHUL_CODE"], "office":responseData[i]["LCTN_SC_NM"], "officeCode":responseData[i]["ATPT_OFCDC_SC_CODE"]})
            #리턴
            return {"code":1, "schlCount":schlCount, "schools":schools}

        except: #학교가 검색되지 않았을때
            return {"code":-1}
        
    #api 에러
    else:
        return {"code":response.getcode()}



#급식 불러오기
def loadMeal(date, OfficeCode, SchoolCode):

    #url 정하기
    mealUrl = f"https://api.skybro2004.com/meal"
    mealUrl += f"?officeCode={OfficeCode}"
    mealUrl += f"&schlCode={SchoolCode}"
    mealUrl += f"&date={date}"

    #요청
    request = ul.Request(mealUrl)
    #응답
    response = ul.urlopen(request)

    if response.getcode()==200:
        #응답 읽기
        responseData = response.read()
        #json 디코드
        responseData = json.loads(responseData)

        #급식 없는 날 판단
        if responseData["code"]==404:
            return {"code":-1, "Meal":"급식이 없어요!"}
        
        #급식 불러오기
        meals = responseData["meal"]

        mealList = []
        #급식 이름만 빼옴
        for meal in meals:
            mealList.append(meal["name"])
        #칼로리 불러옴
        cal = responseData["cal"]
        #리턴
        return {"code":200, "meal":mealList, "cal":cal}

        

    else:
        #알 수 없는 에러
        return {"code":response.getcode()}



#디버그용
if __name__=="__main__":
    print(loadMeal("20210818", "J10", "7530081"))
    print(schlInfo("서당"))
