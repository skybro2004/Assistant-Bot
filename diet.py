import datetime
import json
from time import daylight
import urllib.request as ul
import urllib.parse as parse

#api키
key = "Your open api key"
#visit https://open.neis.go.kr/ to get api key

def schlInfo(schlName):
    schlUrl = f"https://open.neis.go.kr/hub/schoolInfo?KEY={key}&Type=json"
    schlUrl += f"&SCHUL_NM={parse.quote(schlName)}"
    #print(schlUrl)
    request = ul.Request(schlUrl)
    response = ul.urlopen(request)

    if response.getcode()==200:
        #print(response.getcode())
        responseData = response.read()
        responseData = json.loads(responseData)
        try:
            schlCount = responseData["schoolInfo"][0]["head"][0]["list_total_count"]
            if 5<schlCount:
                return {"code":0}
            #print(schlCount)
            responseData = responseData["schoolInfo"][1]["row"]
            #print(schlCount)
            schools = []
            for i in range(schlCount):
                schools.append({"schlName":responseData[i]["SCHUL_NM"], "schlCode":responseData[i]["SD_SCHUL_CODE"], "office":responseData[i]["LCTN_SC_NM"], "officeCode":responseData[i]["ATPT_OFCDC_SC_CODE"]})
            #print('\n'.join(map(str, schools)))
            return {"code":1, "schlCount":schlCount, "schools":schools}
        except:
            #print(None)
            return {"code":-1}
        

    else:
        print(response.getcode())

    

def loadMeal(date, OfficeCode, SchoolCode):

    #url 정하기
    mealUrl = f"https://open.neis.go.kr/hub/mealServiceDietInfo?KEY={key}&Type=json&pIndex=1&pSize=31"
    mealUrl += f"&ATPT_OFCDC_SC_CODE={OfficeCode}"
    mealUrl += f"&SD_SCHUL_CODE={SchoolCode}"
    mealUrl += f"&MLSV_FROM_YMD={date}&MLSV_TO_YMD={date}"

    #요청
    request = ul.Request(mealUrl)
    response = ul.urlopen(request)

    if response.getcode()==200:
        #읽기
        responseData = response.read()
        #디코드
        responseData = json.loads(responseData)
        #데이터 정제
        
        try:
            responseData = responseData["mealServiceDietInfo"][1]["row"][0]
        except KeyError:
            return {"Code":-1, "Meal":"급식이 없어요!"}
        
        #급식
        Meal = responseData["DDISH_NM"]
        #조개기
        Meal = list(Meal.split("<br/>"))

        #칼로리
        Calorie = responseData["CAL_INFO"]
        
        return {"Code":200, "Meal":Meal, "Cal":Calorie}
    else:
        return {"Code":response.getcode()}


if __name__=="__main__":
    print(loadMeal("2021", "08", "18", "J10", "7530081"))
    #convertSchoolCode("서현고", "J10")
    #schlInfo("서당")

    #https://open.neis.go.kr/hub/schoolInfo?KEY=028278aaacd242438668d46a5464e934&Type=json&SCHUL_NM=%EC%84%9C%ED%98%84%EB%B0%A9%ED%86%B5
