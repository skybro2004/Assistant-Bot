import discord
from discord.http import Route
import datetime, time, os, random, asyncio, logging, json, sqlite3

#파일 경로
path = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")

#디스코드 봇 토큰 받아오기
try:
    with open(path + '/token.txt') as token:
        token = token.readline()
except FileNotFoundError:
    from setup import setup
    token = setup()

#현재 실행중인 디바이스 이름 받아오기
try:
    with open(path + '/device.txt') as device:
        Running_in = device.readline()
except FileNotFoundError:
    Running_in = "Unknown Device"

#내가 만든 모듈
from modules import diet
from modules import hangang

#봇 선언
client = discord.Client()
http = client.http

#컴포넌트 메시지 보내는 함수
async def sendComponent(message, channel, components):
    r = Route('POST', f'/channels/{channel}/messages')
    payload = {
        "content":message,
        "components":components
    }
    responseTemp = await http.request(r, json=payload)
    return responseTemp

#DB
con = sqlite3.connect(f"{path}/data/database.db")
cursor = con.cursor()

#로그 작성
logger = logging.getLogger(__name__)
formatter = logging.Formatter("[%(levelname)s, line:%(lineno)s][%(asctime)s] >>> %(message)s")
streamHandler = logging.StreamHandler()
fileHandler = logging.FileHandler(f"{path}" + "/discordServer.log", encoding="utf-8")
fileHandler.setFormatter(formatter)
logger.addHandler(streamHandler)
logger.addHandler(fileHandler)
logger.setLevel(level=logging.INFO)

#마지막 수정시간
lastUpdateTime = datetime.datetime.fromtimestamp(os.path.getmtime(__file__)).strftime('%Y-%m-%d %H:%M:%S')

#업타임
startTime = datetime.datetime.now()

#투표
voteResult = {}

#main====================================================================

#로그인시 실행
@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game("Type !help or !도움말 for help"))
    logger.info(f"{'='*50}login as {client.user}{'='*50}")


@client.event
async def on_message(message):
    
    #메시지 로그
    logger.info(f"{message.author} : {message.content}")

    #봇 메시지 예외처리
    if message.author.bot:
        return


    #명령어====================================================================


    #핑
    if message.content=="!ping":
        await message.channel.send(f"pong! {round(round(client.latency, 4)*1000)}ms")
        return


    #현재 상태
    if message.content.startswith("!status"):
        status_embed = discord.Embed(title="status", description=f"log in as {client.user}", color=0xfe0405)
        status_embed.add_field(name="ping", value=f'{round(round(client.latency, 4)*1000)}ms')
        status_embed.add_field(name="last update", value=lastUpdateTime)
        status_embed.add_field(name="Uptime", value=f"{str(datetime.datetime.now() - startTime).split('.')[0]}")
        status_embed.set_footer(text=f"hosting by {Running_in}")
        await message.channel.send(embed=status_embed)
        return


    #도움말
    #TODO : 걍 싹 다 갈아엎기
    if message.content.startswith("!help") or message.content.startswith("!도움") or message.content.startswith("!도움말"):
        if len(message.content.split(" ")) == 1:
            help_embed = discord.Embed(title='!help', color=0xfe0405)
            help_embed.add_field(name="!status", value="현재 조교봇의 상태를 불러옵니다.", inline=False)
            help_embed.add_field(name="!help [기능]", value="입력한 기능의 도움말을 불러옵니다.", inline=False)
            help_embed.set_footer(text="(value):필수 입력값\n[value]:선택 입력값\n{value}:등록 시 생략가능")
            await message.channel.send(embed=help_embed)
        return

    #로드맵
    if message.content=="!로드맵":
        roadmap_embed = discord.Embed(title="조교봇 로드맵", color=0xfe0405)
        roadmap_embed.add_field(name="급식봇 날짜기능", value="이번달 안", inline=False)
        roadmap_embed.add_field(name="짤봇", value="(beta)다음달 안\n(Alpha)올해 안", inline=False)
        roadmap_embed.add_field(name="자가진단", value="미정(최대한 빠른 시일 내에)", inline=False)
        roadmap_embed.add_field(name="투표 리워크", value="급식봇 완성 후", inline=False)
        roadmap_embed.add_field(name="시간표", value="미정", inline=False)
        roadmap_embed.add_field(name="야추", value="예정 없음", inline=False)
        await message.channel.send(embed=roadmap_embed)
        return

    #급식
    if str(message.channel)=="밥" or str(message.channel)=="test": #밥 채널 혹은 test채널에서만 작동

        #사용자의 id 저장
        author = message.author.id

        #등록
        if message.content==("!등록"):
            #학교 이름 입력받기
            botMsg = await http.request(
                Route("POST", f"/channels/{message.channel.id}/messages"),
                json = {"content":"학교 이름을 입력해주세요"}
            )
            #botMsg = await sendComponent("학교 이름을 입력해주세요", message.channel.id, [])
            def check(m):
                return m.author.id == author and m.channel.id == int(botMsg["channel_id"])

            while 1:
                try:
                    #30초간 사용자 응답을 기다림
                    usrMsg = await client.wait_for('message', timeout=30.0, check=check)
                    
                except asyncio.TimeoutError: #30초간 응답을 하지 않았을시
                    await http.request(
                        Route('PATCH', f"/channels/{botMsg.get('channel_id')}/messages/{botMsg.get('id')}"),
                        json={"content":"시간 초과"}
                    )
                    return
                else:
                    #데이터 정제 및 메시지 삭제
                    schlName = usrMsg.content
                    await usrMsg.delete()

                    #예외처리
                    if schlName.startswith("!등록 "):
                        schlName = schlName.split()[1]

                    #검색결과 불러오기
                    data = diet.schlInfo(schlName)

                    #정상적으로 됐는지 판별
                    #코드 1 : 에러없음
                    if data["code"]==1:
                        #컴포넌트(버튼)
                        components = [{"type": 1,"components": []}]
                        #컴포넌트 리스트에 검색한 학교 추가
                        for i, school in enumerate(data["schools"]):
                            components[0]["components"].append({"type":2, "style":1, "label":f"{school['schlName']}({school['office']})", "custom_id":i})

                        #메시지 수정(버튼 추가)
                        botMsg = await http.request(
                            Route("PATCH", f"/channels/{botMsg.get('channel_id')}/messages/{botMsg.get('id')}"),
                            json={"content":"학교를 선택해주세요", "components":components}
                        )
                        
                        try:
                            
                            def buttonCheck(p):
                                try:

                                    #발생한 이벤트가 '버튼을 눌렀는가' 인가?
                                    cond1 = p["t"]=='INTERACTION_CREATE'
                                    cond2 = p["d"]["type"]==3
                                    #이 메시지에서 일어난 이벤트인가?
                                    cond3 = botMsg["id"]==p["d"]["message"]["id"]
                                    #이벤트를 발생시킨(버튼을 누른) 사용자가 현재 등록 진행중인 사용자인가?
                                    cond4 = author==int(p["d"]["member"]["user"]["id"])

                                    return cond1 and cond2 and cond3 and cond4
                                    
                                except KeyError: #다른 이벤트와 꼬여 발생하는 에러 대처
                                    return False
                            
                            #30초간 응답을 기다림
                            schlName = await client.wait_for("socket_response", timeout=30.0, check=buttonCheck)

                        except asyncio.TimeoutError: #30초간 응답없음
                            await http.request(
                                Route('PATCH', f"/channels/{botMsg.get('channel_id')}/messages/{botMsg.get('id')}"),
                                json={"content":"시간 초과", "components":[]}
                            )
                            return

                        else:

                            #선택한 데이터만 뽑아오기
                            data = data["schools"][int(schlName["d"]["data"]["custom_id"])]

                            try:
                                #DB에 저장
                                cursor.execute(
                                    "INSERT INTO meal(id, officeCode, schlCode) VALUES(?, ?, ?)",
                                    (author, data["officeCode"], data["schlCode"])
                                )

                            except sqlite3.IntegrityError: #이미 등록한 사용자의 경우
                                #정보업데이트
                                cursor.execute(
                                    "UPDATE meal SET officeCode=?, schlCode=? WHERE id=?",
                                    (data["officeCode"], data["schlCode"], author)
                                )

                            #DB 변경사항 적용
                            con.commit()
                            
                            #수정 완료!
                            await http.request(
                                Route('PATCH', f"/channels/{botMsg.get('channel_id')}/messages/{botMsg.get('id')}"),
                                json={"content":"등록 성공!", "components":[]}
                            )
                            return

                    #코드 -1 : 학교를 찾지 못함
                    elif data["code"]==-1:
                        botMsg = await http.request(
                            Route("PATCH", f"/channels/{botMsg.get('channel_id')}/messages/{botMsg.get('id')}"),
                            json={"content":"학교를 찿지 못했어요\n다시 입력해주세요"}
                        )
                        continue

                    #코드 0 : 학교가 5개를 넘어감
                    elif data["code"]==0:
                        botMsg = await http.request(
                            Route("PATCH", f"/channels/{botMsg.get('channel_id')}/messages/{botMsg.get('id')}"),
                            json={"content":"검색한 학교가 너무 많아요\n좀 더 자세하게 입력해주세요"}
                        )
                        continue

                    else:
                        botMsg = await http.request(
                            Route("PATCH", f"/channels/{botMsg.get('channel_id')}/messages/{botMsg.get('id')}"),
                            json={"content":f"에러가 발생했습니다\n에러 코드 : {data['code']}"}
                        )
                        return

                        
        #밥
        if "급식" in message.content or "밥" in message.content:

            #등록된 id 불러옴
            cursor.execute("SELECT id FROM meal")
            keys = []
            for item in cursor.fetchall():
                keys.append(item[0])

            #등록된 사용자인가?
            if author in keys:
                #사용자의 정보를 불러옴
                cursor.execute(f"SELECT * FROM meal WHERE id={author}")
                temp = cursor.fetchone()
                todayDiet = diet.loadMeal(datetime.datetime.today().strftime("%Y%m%d"), temp[1], temp[2])


                if todayDiet["Code"]==200: #정상작동

                    #급식 정보 전송
                    dietStr = '\n'.join(todayDiet['Meal'])
                    
                    diet_embed = discord.Embed(
                        title=f"{datetime.datetime.today().strftime('%m월 %d일')} (학교이름) 급식",
                        value=todayDiet,
                        color=0xfe0405
                    )

                    diet_embed.add_field(name="중식", value=dietStr, inline=True)
                    diet_embed.set_footer(text=todayDiet['Cal'])

                    await message.channel.send(embed=diet_embed)

                elif todayDiet["Code"]==-1: #api 불러오기는 정상적으로 작동했으나 급식을 불러오지 못함(대부분의 경우 그 날 급식이 없음)
                    await message.channel.send("오늘은 급식이 없습니다.")

                else: #에러
                    await message.channel.send(f"급식을 불러올 수 없어요\n에러코드 : {todayDiet['Code']}")

            else: #등록안된 사용자
                await message.channel.send("먼저 등록을 해주세요")
            return

    
    #가위바위보(조작됨)
    if message.content.startswith('!가위바위보'):
        rsp = ["가위","바위","보"]
        embed = discord.Embed(title="가위바위보",description="가위바위보를 합니다 3초내로 (가위/바위/보)를 써주세요!", color=0x00aaaa)
        channel = message.channel
        msg1 = await message.channel.send(embed=embed)
        def check(m):
            return m.author == message.author and m.channel == channel
        try:
            msg2 = await client.wait_for('message', timeout=3.0, check=check)
        except asyncio.TimeoutError:
            await msg1.delete()
            embed = discord.Embed(title="가위바위보",description="앗 3초가 지났네요...!", color=0x00aaaa)
            await message.channel.send(embed=embed)
            return
        else:
            await msg1.delete()
            bot_rsp = str(random.choice(rsp))
            user_rsp  = str(msg2.content)
            answer = ""
            if "가위" == user_rsp:
                answer = "저는 " + "바위" + "를 냈고, 당신은 " + user_rsp + "을 내셨내요.\n" + "제가 이겼습니다!"
            elif "바위" == user_rsp:
                answer = "저는 " + "보" + "를 냈고, 당신은 " + user_rsp + "을 내셨내요.\n" + "제가 이겼습니다!"
            elif "보" == user_rsp:
                answer = "저는 " + "가위" + "를 냈고, 당신은 " + user_rsp + "을 내셨내요.\n" + "제가 이겼습니다!"
            else:
                embed = discord.Embed(title="가위바위보",description="앗, 가위, 바위, 보 중에서만 내셔야죠...", color=0x00aaaa)
                await message.channel.send(embed=embed)
                return
            embed = discord.Embed(title="가위바위보",description=answer, color=0x00aaaa)
            await message.channel.send(embed=embed)
            return


    #투표
    if message.content.startswith("!투표"):
        #주제
        topic = ""
        #선택지
        options = []

        #메시지 쪼개기
        msgContent = message.content[3:]
        msgContent = msgContent.split(",")
        msgContent = [v.strip() for v in msgContent]

        #첫번째 요소가 "주제"로 시작하면 주제로 정함
        if msgContent[0].startswith("주제"):
            #"주제:밥 뭐먹을까" 형식일시
            if ":" in msgContent[0]:
                topic = msgContent[0].split(":")[1].strip()
            #"주제 밥 뭐먹을까" 형식일시
            else:
                topic = msgContent[0][2:].strip()

            msgContent.pop(0)

        #나머지 요소를 전부 투표 항목으로 설정
        options = msgContent
        if 5<len(options):
            await message.channel.send("선택지가 너무 많아요!")
            return

        #투표 메시지 임베드 설정
        vote_embed = discord.Embed(title="!투표", description=f"{topic}")
        components = [
            {
                "type":1,
                "components":[

                ]
            }
        ]

        #옵션이 주어지지 않았을 때, 찬반투표 진행
        if options==[''] or options==[]:
            components[0]["components"] = [
                {
                    "type":2,
                    "label":"👍(0)",
                    "style":3,
                    "custom_id":0
                },
                {
                    "type":2,
                    "label":"👎(0)",
                    "style":4,
                    "custom_id":1
                },
            ]
            options = ["y", "n"]

        #옵션이 주어졌을경우
        else:
            for i, option in enumerate(options):
                components[0]["components"].append({
                    "type":2,
                    "label":f"{option}(0)",
                    "style":1,
                    "custom_id":i
                })

        #투표 메시지 보냄
        botMsg = await http.request(
            Route("POST", f"/channels/{message.channel.id}/messages"),
            json={"embed":vote_embed.to_dict()}
        )

        #데이터베이스에 투표 데이터 저장
        #id(int), opt1(int), opt2(int), opt3(int), opt4(int), opt5(int), voted(str)
        #투표 메시지 id, 항목별 투표수, 투표한 사용자 id
        arr = [botMsg.get("id"), 0, 0, 0, 0, 0, '']
        cursor.execute(
            f"INSERT INTO vote VALUES(?, ?, ?, ?, ?, ?, ?)",
            arr
        )

        #데이터베이스 적용
        con.commit()

        #투표 메시지에 버튼 추가
        botMsg = await http.request(
            Route("PATCH", f"/channels/{message.channel.id}/messages/{botMsg.get('id')}"),
            json={"embed":vote_embed.to_dict(), "components":components}
        )



    #한강
    if message.content=="!한강":
        await message.channel.send(f"현재 한강 수온 : {hangang.hangang()}°C")
    


@client.event
#TODO : ListOutOfIndex 에러 잡기
#이벤트가 발생했을때
async def on_socket_response(payload):
    #print(payload)
    #버튼을 눌렀을때
    if payload.get("t", "") == "INTERACTION_CREATE" and payload.get("d", {}).get("type") == 3:

        #기본적인 정보 변수로 지정(데이터 정제)
        interaction_id = payload.get("d").get("id")
        interaction_token = payload.get("d").get("token")
        msgId = payload.get("d").get("message").get("id")
        channelId = payload.get("d").get("channel_id")
        selection = payload.get("d").get("data").get("custom_id")
        userId = payload.get("d").get("member").get("user").get("id")

        #투표
        if payload.get("d").get("message").get("embeds", [""])[0].get("title")=="!투표":
            
            selection = int(selection)

            #데이터베이스에서 투표한 사람들 데이터를 불러옴
            cursor.execute(
                f"SELECT voted FROM vote WHERE id=?",
                (msgId,)
            )

            #투표한 사람들
            voted = cursor.fetchone()[0]

            #데이터 정제
            votedArr = voted.split(",")

            #이미 투표했다면
            if userId in votedArr:
                await client.http.request(
                    Route("POST", f"/interactions/{interaction_id}/{interaction_token}/callback"),
                    json={"type": 4, "data": {
                        "content": "이미 투표했습니다!",
                        "flags": 64
                    }},
                )
                return
            
            #투표한 사람들 리스트에 현재 사용자 추가
            voted += userId + ","

            #투표 결과 불러옴
            cursor.execute(
                f"SELECT opt{selection + 1} FROM vote WHERE id=?",
                (msgId,)
            )
            value = cursor.fetchone()[0]
            
            #투표 결과에 1 추가
            value += 1
            #컴포넌트에 투표 결과 1추가 적용
            components = payload.get("d").get("message").get("components")
            components[0]["components"][selection]["label"] = components[0]["components"][selection]["label"][:-3] + f"({value})"

            #투표 결과, 투표한 사람 데이터베이스에 업로드
            cursor.execute(
                f"UPDATE vote SET opt{selection + 1}=?, voted=? WHERE id=?",
                (value, voted, msgId)
            )

            #데이터베이스 적용
            con.commit()

            #투표 메시지 업데이트
            await http.request(
                Route("PATCH", f"/channels/{channelId}/messages/{msgId}"),
                json={"components": components}
            )

            #응답
            await client.http.request(
                Route("POST", f"/interactions/{interaction_id}/{interaction_token}/callback"),
                json={"type": 6}
            )

    
client.run(token)
