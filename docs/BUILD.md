# 재빌드

## 준비물

- 원본 `ozzy.psp2arc` (PCSG00261 복호화 게임 폴더, MD5 `e692f4c12b1b4182f1da0e04ca487918`)
- Python 3.13, `Pillow`, `numpy`
- 글꼴: `fonts/NanumSquareNeo-bRg.ttf`, `fonts/NanumSquareNeo-cBd.ttf`, `fonts/NanumSquareNeo-dEb.ttf` (출처는 `docs/FONT_CREDITS.md`)
- xdelta3 (배포 파일을 만들 때만)

## 빌드

저장소 폴더에서 실행합니다.

```powershell
python tools/build.py "..\ozzy.psp2arc" "..\ozzy_ko.psp2arc"
```

원본에서 텍스트 52개와 글꼴 6종을 읽어 한글판을 만든 뒤, 원본 아카이브를 그대로 복사하고 바꾼 파일 65개를 끝에 덧붙입니다. 결과의 SHA-256을 `release_manifest.json`의 `output_sha256`과 비교하세요. 같은 원본과 글꼴이면 바이트 단위로 같은 결과가 나옵니다.

## 배포 파일

```powershell
xdelta3 -e -0 -S none -A -s "..\ozzy.psp2arc" "..\ozzy_ko.psp2arc" Batman_Arkham_Origins_Blackgate_Vita_KO_v1.0.xdelta
```

## 번역 수정

- `text/ko.json`: `{텍스트 파일 이름: {문자열 키: [구간, ...]}}`. 자막 파일(`vo_anim_*`)은 컷신 하나가 키 하나이고, 배열의 각 구간이 화면에 한 번씩 나오는 자막입니다. 구간 수는 원본과 같아야 하며 표시 타이밍은 일본판 것을 그대로 씁니다.
- `%FACEUP%`, `%CASE_NAME%`, `%RED%` 같은 `%…%` 자리표시자는 그대로 둡니다. `%%`는 `%` 한 글자입니다.
- 원문을 보려면 `tools/psarc.py`로 원본에서 `ozzy/loc/_vta/`를 추출하고 `tools/cloc.py`로 읽습니다(언어 표 0 = 영어, 1 = 일본어).
- 새 한글 글자는 빌드 때 자동으로 글꼴에 들어갑니다. 글꼴마다 가나·한자 자리 수만큼(최소 약 1,100자) 넣을 수 있습니다.
- 글자 크기·간격은 `tools/build.py`의 `FONTS`(글자 간격 보정, 띄어쓰기 폭)에서 조정합니다.

## 에뮬레이터 확인

`tools/emu.py`는 저장소 옆 `emu/`에 설치한 Vita3K(Qt 프런트엔드, Vulkan)를 백그라운드로 띄우고 키·터치 입력과 스크린샷(F12 단축키)을 보냅니다. `start`, `key x _2 down`, `shot out.png`, `stop` 순서로 씁니다.
