# 2022-2-OSSProj-No.1-1
### ๐Space War๐
Pygame์ ํ์ฉํ ์ํ๊ฒ์ 

![badges](https://img.shields.io/badge/OS-ubuntu-red)
![badges](https://img.shields.io/badge/IDE-VSCode-informational)
![badges](https://img.shields.io/badge/python-3.8-blue)
![badges](https://img.shields.io/badge/pygame-2.1.2-yellow)
![badges](https://img.shields.io/badge/license-MIT-green)


### ํ์ ์๊ฐ
* **ํ์ฅ : ๋๊ตญ๋ํ๊ต ์ ๋ณดํต์ ๊ณตํ๊ณผ** [**๊น์ ํ**](https://github.com/junghye01) yejjungxye@gmail.com
* **ํ์ : ๋๊ตญ๋ํ๊ต ๊ฒฝ์ ํ๊ณผ** [**๊นํ์**](https://github.com/seueooo) yds06206@gamail.com
* **ํ์ : ๋๊ตญ๋ํ๊ต ์ฐ์์์คํ๊ณตํ๊ณผ** [**๋ฐฑ์ฑ์ฐ**](https://github.com/codusl100) codusl0422@gmail.com


## ์คํ ๋ฐฉ๋ฒ
1. python, pygame, pymysql, grequests ์ค์น
```
sudo apt-get update
sudo apt install python3.8
pip3 install pygame==2.1.2
pip3 install pymysql
pip3 install grequests 
```

2. ์ ์ฅ์ ํด๋ก  ๋ฐ ์คํ
```
git clone https://github.com/CSID-DGU/2022-2-OSSProj-No.1-1
cd 2022-2-OSSProj-No.1-1
python3 shooting_game.py
```

## Game Controls
### Default
![default](https://user-images.githubusercontent.com/108131226/207036631-58cd3f2d-e7c0-4342-b452-fd6b7068d40e.jpeg)

### For PVP
![pvp](https://user-images.githubusercontent.com/108131226/207036656-e912655e-3f30-4746-bbb5-b1c67fc22c5b.jpeg)


## Sign up, Sign in
<img width="500" alt="แแณแแณแแตแซแแฃแบ 2022-12-13 แแฉแแฎ 9 07 00" src="https://user-images.githubusercontent.com/108131226/207313760-9915bef6-279a-474e-920b-48bd74c16d1f.png">

- ๊ฒ์์ ์์ํ๊ธฐ์ ์์, ํ์๊ฐ์ ๋ฐ ๋ก๊ทธ์ธ์ ์งํํฉ๋๋ค.



## In Game
### 1. Single Mode  
  - ๊ฒ์์ ๋ฒ ์ด์ค๊ฐ ๋๋ ๊ฒ์์๋๋ค. 


### 2. Extreme Mode
  - ์ ํ๋ ์๊ฐ ๋ด์์ ๋ชฌ์คํฐ๋ฅผ ์ฒ์นํ๊ณ  ๊ฐ์ฅ ๋ง์ ์ ์๋ฅผ ํ๋ํ ์ฌ๋์ด ๋ญํน ๋ณด๋์ ๋ฑ๋ก๋๋ ๋ชจ๋์๋๋ค. 
  - ์ ํ ์๊ฐ์ 60์ด๋ก, ๊ธฐ์กด ๋ชจ๋๋ค๊ณผ ๋ค๋ฅธ ์ ์ ๋ชฌ์คํฐ๋ค์ด ๊ฒ์ ์์์๋ง ๋ฑ์ฅํ๋ ๊ฒ์ด ์๋ ์ข์ฐ์์๋ ๋ฑ์ฅํฉ๋๋ค. 
  - ๊ทธ๋ฆฌ๊ณ  ๊ธฐ์กด๋ณด๋ค ๋น ๋ฅธ ์๋๋ก ์งํ๋๋ฉฐ, ์์ดํ ๋๋ ์๊ฐ ์ฆ๊ฐํฉ๋๋ค. 
  - ๋ ์ธ ๊ธฐ๋ฆฐํ์ time mode๋ฅผ ์ฐธ๊ณ ํ์ฌ ์ต์คํธ๋ฆผ ๋ชจ๋๋ฅผ ์ ์ํ์์ต๋๋ค.
  ์ฐธ๊ณ  ์์ค์ฝ๋ : https://github.com/CSID-DGU/2021-2-OSSProj-Lets_Kirin-8
 
  
### 3. PVP Mode
  - 2๋ช์ด์ ํ๋ ์ดํ  ์ ์๋ PVP ๋ชจ๋๋ฅผ ์ถ๊ฐํ์์ต๋๋ค. 
  - ํด๋น ๋ชจ๋๋ ๋ญํน ๋ชจ๋๊ฐ ์ ์ฉ๋์ง ์์ผ๋ฉฐ 2๋ช์ด์ ๊ฒ์์ ์งํ ํ ์ต์ข ๊ฒฐ๊ณผ๋ฅผ ๋น๊ตํด ์น์๋ฅผ ๊ฐ๋ฆฝ๋๋ค.   


## High Score
<img width="712" alt="แแณแแณแแตแซแแฃแบ 2022-12-13 แแฉแแฎ 9 08 58" src="https://user-images.githubusercontent.com/108131226/207314495-43461280-5baf-420f-b10d-ea2e91ced133.png">

 - high score ๋ฉ๋ด๋ฅผ ํตํด ๋ชจ๋ ๋ณ ์ ์ ๊ธฐ๋ก์ ๋ณผ ์ ์์ต๋๋ค. ๊ฒ์ ํ๋ ์ด๊ฐ ๋๋๊ณ  ENTER ํค ์๋ ฅ ํ ๋ฉ๋ด๋ก ๋์๊ฐ๋ฉด high score ๋ฉ๋ด์์ ๋ณธ์ธ์ ์ ์๊ฐ ๊ธฐ๋ก์ ๋ฐ์๋ ๊ฒ์ ํ์ธํ  ์ ์์ต๋๋ค.



## Ship shop

<img width="500" alt="แแณแแณแแตแซแแฃแบ 2022-12-13 แแฉแแฎ 8 36 09" src="https://user-images.githubusercontent.com/108131226/207307734-935c7302-8dcb-45ee-b9b2-589bbf4b6e60.png">

 - ๊ฒ์ํด์ ๋ชจ์ coin์ผ๋ก shop ๋ฉ๋ด์์ ์บ๋ฆญํฐ๋ฅผ ๊ตฌ๋งคํ  ์ ์์ต๋๋ค.
 - ๊ตฌ๋งคํ ์บ๋ฆญํฐ๋ค์ char setting ๋ฉ๋ด์์ ์ ํํ  ์ ์์ต๋๋ค.

 ### Items
<img width="456" alt="แแณแแณแแตแซแแฃแบ 2022-12-13 แแฉแแฎ 8 39 57" src="https://user-images.githubusercontent.com/108131226/207308719-1c858a16-cb26-4f4d-93ed-ccaa8fb007d5.png">

 - ์์ดํ์ ๋ค์๊ณผ ๊ฐ์ต๋๋ค.

### ๊ฒ์ ์์ฐ ์์
- https://youtu.be/NsPBna2KnSA

## References
- https://github.com/CSID-DGU/2021-2-OSSProj-BATONG-01
- https://github.com/CSID-DGU/2021-2-OSSProj-Lets_Kirin-8

## Image credit
- https://opengameart.org/
- https://textcraft.net/

## Sound credit
- https://opengameart.org/art-search-advanced?keys=&field_art_type_tid%5B%5D=12&sort_by=count&sort_order=DESC

