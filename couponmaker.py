#사전 설치 pip install - pillow, opencv, numpy, qrcode,matplotlib
import cv2
import numpy as np
import qrcode
from PIL import Image
from matplotlib import pyplot as plt
import glob
import os
from cryptography.fernet import Fernet

key = Fernet.generate_key()

key = '4OvZjUh5ZRDnc3Fmo3OIy_mLxz3gF07h6wEyiG0zoNQ='


fernet = Fernet(key)
png = ".jpg"
back_img = 'coupon.png'


qrcode_size = 250
location_x = 15
location_y = 15

def coupondev():
    with open('code.txt', 'r') as f:#쿠폰 리스트 한줄씩 읽기
        data = f.read()
    couponlist = data.splitlines()#쿠폰 리스트 한줄씩 추가

    i=0

    for i in range(len(couponlist)):
        img = qrcode.make(couponlist[i])#쿠폰번호 qr코드로 변환
        resize_img = img.resize((qrcode_size,qrcode_size))
        resize_img.save("coupon_"+str(i)+png)#쿠폰번호 qr코드 png이미지로 저장

        src1 = cv2.imread(back_img,1) #쿠폰 이미지 삽입
        src2 = cv2.imread("coupon_"+str(i)+png,1) #QR코드 번호
        rows, cols, channels = src2.shape #QR코드 파일 픽셀값 저장
        
        roi = src1[location_x:rows+location_x,location_y:cols+location_y] #QR코드 파일 픽셀값을 관심영역(ROI)으로 저장함.
        
        gray = cv2.cvtColor(src2, cv2.COLOR_BGR2GRAY) #로고파일의 색상을 그레이로 변경
        
        ret, mask = cv2.threshold(gray, 160, 255, cv2.THRESH_BINARY) #배경은 흰색으로, 그림을 검정색으로 변경
        mask_inv = cv2.bitwise_not(mask)

         
        src1_bg = cv2.bitwise_and(roi,roi,mask=mask) #배경에서만 연산 = src1 배경 복사

        src2_fg = cv2.bitwise_and(src2,src2, mask = mask_inv) #QR코드에서만 연산

        dst = cv2.bitwise_or(src1_bg, src2_fg) #src1_bg와 src2_fg를 합성

        src1[location_x:rows+location_x,location_y:cols+location_y] = dst #src1에 dst값 합성
        

        cv2.imwrite("coupon_"+str(i)+png, src1)



def combineImage(full_width,full_height,image_key,image_list,index):
    canvas = Image.new('RGB', (full_width, full_height), 'white')
    output_height = 0
    
    for im in image_list:
        width, height = im.size
        canvas.paste(im, (0, output_height))
        output_height += height
    
    print('출력 결과로 다음을 출력합니다.'+image_key+'_'+str(index)+'.jpg')

    canvas.save('out//'+image_key+'_'+str(index)+'.jpg')


def listImage(image_key,image_value):
    full_width, full_height,index = 0, 0, 1
    image_list = []
    
    for i in image_value:
        im = Image.open(image_key+"_"+str(i)+".jpg")
        print('합성'+image_key+"_"+str(i)+".jpg")
        width, height = im.size

        if full_height+height > 4500:
            combineImage(full_width,full_height,image_key,image_list,index)
            index = index + 1
            image_list = []
            full_width, full_height = 0, 0
        
        image_list.append(im)
        full_width = max(full_width, width)
        full_height += height

    combineImage(full_width,full_height,image_key,image_list,index)


def mk_code(n):
    f = open("code.txt",'wb')
    for i in range(0, n):
        data = str(i)+"_ComputerEngine"+"\n"
        i=i+1
        encrypted_data = fernet.encrypt(b"data")
        f.write(encrypted_data)
        f.write(b"\n")
    f.close()

def image_size():
    image1 = Image.open('coupon.png')
    image1.show()
    imag1_size = image1.size
    print("사진의 사이즈는"+str(imag1_size)+"px(픽셀)입니다.")

def main():
    print("암호화 한 키 값을 출력합니다.\n")
    print(f'대칭키 :{key}\n')
    image_size()
    n = input("생성할 쿠폰 코드의 개수를 입력하세요 : ")
    n = int(n)
    print("쿠폰 코드를 생성합니다.")
    mk_code(n)
    coupondev()
    print("쿠폰 합성을 시작합니다")



main()

if __name__ == '__main__' :# 쿠폰 파일 새 파일로 합성
    
    print('')
    target_dir = "./"
    files = glob.glob(target_dir + "*.jpg")

    name_list = {} 

    # Make Directory
    
    try:
        if not(os.path.isdir('out')):
            os.makedirs(os.path.join('out'))
    except OSError as e:
        if e.errno != errno.EEXIST:
            print("Failed to create directory!!!!!")
            raise

    for f in files:
        name = f.split('\\')[1]
        key = name.split('_')[0]
        value = name.split('_')[1].split('.')[0]

        if key in name_list.keys():
            name_list[key].append(int(value))
        else:
            name_list[key] = [int(value)]

        name_list[key].sort()
    
    for key,value in name_list.items():
        listImage(key,value)
    
    print('쿠폰 합성에 성공하였습니다.')

