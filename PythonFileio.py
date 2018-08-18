import random


#201811458 정종현 파이썬 전화번호 및 전화 시뮬레이션 프로젝트
#2018.05~2018.06

#파일에 등록
def file():
    file = open("전화부.txt",'a',encoding = "utf-8")

    name = input("이름을 입력하세요>>")
    number = input("번호를 입력하세요.(형식 : 010-xxxx-xxxx)>>")
    
    file.write(name+" ")
    file.write(number+"\n")

    file.close()

#검색

def fileall():
    
    file = open("전화부.txt",'r', encoding="utf-8")
    while True:
        line = file.readline()
        if not line: break
        print(line+"\n")
    file.close()
    
#파일에 있는 문자 비교 함수

def search(name):
    #저장되어있는 txt파일을 읽어서 이름과 폰을 스페이스바 기준으로 나눔
    with open("전화부.txt", "r", encoding="utf-8") as f:
        people = [{"name": line.split()[0], "phone": line.split()[1][:-1]}for line in f.readlines()]
    for person in people:
        if person["name"].find(name) >= 0:
            print(person["name"], person["phone"])

#통화기록 함수 
def write_history():
    with open("전화부.txt", "r", encoding="utf-8") as f:
        people = [{"name": line.split(" ")[0], "phone": str(line.split(" ")[1])[:-1]} for line in f.readlines()]#개행문자를 지워주기 위해 :-1 을 써줌.

    with open("통화기록.txt", "a", encoding="utf-8") as f:
        for _ in range(30):
            random_user = random.randint(0, len(people)-1)
            random_user = people[random_user]
            hour = random.randint(0, 23)
            minn = random.randint(0, 60)
            output_sentence = "%s %s %d:%d" % (random_user["name"], random_user["phone"], hour, minn)
            f.write(output_sentence + "\n")#파일에 있는 시간 정보 출력
            
#통화기록 파일에 넣어주는 함수
def show_history():
    history = {}
    #통화 기록 파일에 이름과 폰 번호를 등록 후 시간을 랜덤으로 집어 넣어줌 기록에서의 검색 
    with open("통화기록.txt", "r", encoding="utf-8") as f:
        for line in f.readlines():
            name = line.split()[0]
            phone = line.split()[1]
            time = line.split()[2][:-1]
            if phone not in history:
                history[phone] = {"name": name, "phone": phone, "time": [time], "count": 1}
            else:
                history[phone]["time"].append(time)
                history[phone]["count"] += 1

    for numbers in history.keys():
        print("%s님(%s)과 %d번 통화하셨습니다" % (history[numbers]["name"], history[numbers]["phone"], history[numbers]["count"]))

#기록을 검색하는 함수 name에 입력받기 

def search_history(name):
    history = {}
    with open("통화기록.txt", "r", encoding="utf-8") as f:
        for line in f.readlines():
            name = line.split()[0]
            phone = line.split()[1]
            time = line.split()[2][:-1]
            if phone not in history:
                history[phone] = {"name": name, "phone": phone, "time": [time], "count": 1}#이름에 해당하는 key 값은 파일 안에 있는 부분을 문자열을 분리하여 한 문자를 받아온다.
            else:
                history[phone]["time"].append(time)
                history[phone]["count"] += 1

    for numbers in history.keys():
        if history[numbers]["name"].find(name) >=0:
            print("%s님(%s)과 %d번 통화하셨습니다" % (history[numbers]["name"], history[numbers]["phone"], history[numbers]["count"]))



#연락 기록의 횟수를 정렬
def sort_window(data_add,stickcolor,color,size,xshift,yshift):
    import turtle
    t = turtle.Turtle()
    data = []
    i=1
    t.color(stickcolor)
    data.append(data_add)
    t.pensize(size)
    t.begin_fill()
    t.fillcolor(color)
    t.lt(90)
    t.fd(data[i-1])
    t.write(str(data))
    t.right(90)

    t.fd(40)
    t.rt(90)
    t.fd(data[i-1])
    t.lt(90)
    t.end_fill()
    t.fd(data[i-1])
    t.write(str(xshift))
    t.home()
    t.lt(90)
    t.fd(data[i-1])
    t.write(str(yshift))
    t.home()

#친밀도 정렬

#메인 창

while 1:
    select = int(input("=========================\n1. 파일에 저장 \n2. 파일 전체 출력\n3. 딕셔너리 전체 출력 \n4. 파일에서 이름 검색\n5. 통화기록 생성\n6. 통화기록 보여주기\n7. 통화기록 검색  \n=========================\n>>"))
    if select == 1:
        file()
    elif select == 2:
        fileall()
    elif select == 3:
        fileall()
    elif select == 4:
        search(input("검색할 이름을 입력해주세요 : "))
    elif select == 5:
        write_history()
        print("통화기록이 생성되었습니다...")
    elif select == 6:
        show_history()
    elif select == 7:
        search_history(input("이름을 입력하세요"))
 

