# 2022-2-OSSProj-No.1-1
### 🌌Space War🌌
Pygame을 활용한 슈팅게임 

![badges](https://img.shields.io/badge/OS-ubuntu-red)
![badges](https://img.shields.io/badge/IDE-VSCode-informational)
![badges](https://img.shields.io/badge/python-3.8-blue)
![badges](https://img.shields.io/badge/pygame-2.1.2-yellow)
![badges](https://img.shields.io/badge/license-MIT-green)

<img width="500" alt="스크린샷 2022-12-13 오후 6 27 25" src="https://user-images.githubusercontent.com/108131226/207305003-3f3b272a-1f43-4c1b-80fe-874c822221a3.png">

### 팀원 소개
* **팀장 : 동국대학교 정보통신공학과** [**김정혜**](https://github.com/junghye01)
* **팀원 : 동국대학교 경제학과** [**김한서**](https://github.com/seueooo)
* **팀원 : 동국대학교 산업시스템공학과** [**백채연**](https://github.com/codusl100)


## Original source
https://github.com/CSID-DGU/2021-2-OSSProj-BATONG-01


## 실행 방법
1. python 설치
```
sudo apt-get update
sudo apt install python3.8

```
2. 필요한 모듈 설치
```
sudo apt-get update
pip3 install -r requirements.txt

```


3. 저장소 클론 및 실행
```
git clone https://github.com/CSID-DGU/2022-2-OSSProj-No.1-1
cd 2022-2-OSSProj-No.1-1
python3 shooting_game.py
```

## Sign up, Sign in
<img width="600" alt="스크린샷 2022-12-13 오후 9 07 00" src="https://user-images.githubusercontent.com/108131226/207313760-9915bef6-279a-474e-920b-48bd74c16d1f.png">

- 게임을 시작하기에 앞서, 회원가입 및 로그인을 진행합니다.


## Game Controls
### Default
![default](https://user-images.githubusercontent.com/108131226/207036631-58cd3f2d-e7c0-4342-b452-fd6b7068d40e.jpeg)

### For PVP
![pvp](https://user-images.githubusercontent.com/108131226/207036656-e912655e-3f30-4746-bbb5-b1c67fc22c5b.jpeg)

## In Game
### 1. Single Mode  
<img width="500" alt="스크린샷 2022-12-13 오후 6 33 39" src="https://user-images.githubusercontent.com/108131226/207305306-1e7292e2-1295-47c3-8256-6ce6ebf18ffc.png">

  - 게임의 베이스가 되는 게임입니다. 


### 2. Extreme Mode
<img width="500" alt="스크린샷 2022-12-13 오후 8 25 57" src="https://user-images.githubusercontent.com/108131226/207306105-211b1621-0110-4512-916d-0f08b6ab4de3.png">

  - 제한된 시간 내에서 몬스터를 처치하고 가장 많은 점수를 획득한 사람이 랭킹 보드에 등록되는 모드입니다. 
  - 제한 시간은 60초로, 기존 모드들과 다른 점은 몬스터들이 게임 위에서만 등장하는 것이 아닌 좌우에서도 등장합니다. 
  - 그리고 기존보다 빠른 속도로 진행되며, 아이템 드랍 수가 증가합니다. 
  - 렛츠기린팀의 time mode를 참고하여 익스트림 모드를 제작하였습니다.
  - 참고 소스코드 : https://github.com/CSID-DGU/2021-2-OSSProj-Lets_Kirin-8
 
 
  
### 3. PVP Mode

<img width="500" alt="스크린샷 2022-12-13 오후 8 27 17" src="https://user-images.githubusercontent.com/108131226/207305964-48034a9d-e158-4956-b635-252b71ad3451.png">

  - 2명이서 플레이할 수 있는 PVP 모드를 추가하였습니다. 
  - 해당 모드는 랭킹 모드가 적용되지 않으며 2명이서 게임을 진행 후 최종 결과를 비교해 승자를 가립니다.  


## High Score
<img width="712" alt="스크린샷 2022-12-13 오후 9 08 58" src="https://user-images.githubusercontent.com/108131226/207314495-43461280-5baf-420f-b10d-ea2e91ced133.png">

 - high score 메뉴를 통해 모드 별 점수 기록을 볼 수 있습니다. 게임 플레이가 끝나고 ENTER 키 입력 후 메뉴로 돌아가면 high score 메뉴에서 본인의 점수가 기록에 반영된 것을 확인할 수 있습니다.



## Ship shop

<img width="500" alt="스크린샷 2022-12-13 오후 8 36 09" src="https://user-images.githubusercontent.com/108131226/207307734-935c7302-8dcb-45ee-b9b2-589bbf4b6e60.png">

 - 게임해서 모은 coin으로 shop 메뉴에서 캐릭터를 구매할 수 있습니다.
 - 구매한 캐릭터들은 char setting 메뉴에서 선택할 수 있습니다.

 ### Items
<img width="456" alt="스크린샷 2022-12-13 오후 8 39 57" src="https://user-images.githubusercontent.com/108131226/207308719-1c858a16-cb26-4f4d-93ed-ccaa8fb007d5.png">

 - 아이템은 다음과 같습니다.