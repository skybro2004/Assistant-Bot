import datetime
import json
from time import daylight
import urllib.request as ul
import urllib.parse as parse

#api키
key = "Your open api key"
#visit https://open.neis.go.kr/ to get api key

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
    mealUrl = f"https://open.neis.go.kr/hub/mealServiceDietInfo?KEY={key}&Type=json&pIndex=1&pSize=31"
    mealUrl += f"&ATPT_OFCDC_SC_CODE={OfficeCode}"
    mealUrl += f"&SD_SCHUL_CODE={SchoolCode}"
    mealUrl += f"&MLSV_FROM_YMD={date}&MLSV_TO_YMD={date}"

    #요청
    request = ul.Request(mealUrl)
    #응답
    response = ul.urlopen(request)

    if response.getcode()==200:
        #응답 읽기
        responseData = response.read()
        #json 디코드
        responseData = json.loads(responseData)

        #데이터 정제
        try:
            responseData = responseData["mealServiceDietInfo"][1]["row"][0]
        except KeyError: #급식 없는날. 왜 응답코드가 에러가 아닌 정상으로 해놨는지 모르겠음
            return {"Code":-1, "Meal":"급식이 없어요!"}
        
        #급식 값 불러오기
        Meal = responseData["DDISH_NM"]
        #줄바꿈 기준으로 쪼개기
        Meal = list(Meal.split("<br/>"))

        #총 칼로리 불러오기
        Calorie = responseData["CAL_INFO"]
        
        #리턴
        return {"Code":200, "Meal":Meal, "Cal":Calorie}
    else:
        #에러코드 리턴
        return {"Code":response.getcode()}

#디버그용
if __name__=="__main__":
    print(loadMeal("2021", "08", "18", "J10", "7530081"))
    print(schlInfo("서당"))
