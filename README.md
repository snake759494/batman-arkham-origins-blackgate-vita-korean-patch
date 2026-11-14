# 배트맨: 아캄 오리진 블랙게이트 PS Vita 한글패치

PS Vita 일본판 **バットマン：アーカム・ビギンズ ブラックゲート (PCSG00261)**용 비공식 한국어 패치입니다. 메뉴·일시정지·옵션, 배트컴퓨터(지도·아이템·수사 사건), 탐정 분석기, 팝업·튜토리얼·목표 안내, 컷신 동영상과 인게임 대사 자막까지 게임 안의 일본어 문장 **1,320항목 전체**를 한국어로 바꿨습니다. 게임 글꼴 6종에 한글 848자를 넣었습니다. 현재 배포판은 **v1.0 (2026-11-14)**입니다.

[패치 다운로드](https://github.com/snake759494/batman-arkham-origins-blackgate-vita-korean-patch/releases/latest) · [기술 설명](docs/TECHNICAL.md) · [재빌드](docs/BUILD.md) · [용어집](docs/GLOSSARY.md) · [변경 기록](CHANGELOG.md) · [권리 안내](RIGHTS.md)

릴리즈 첨부 파일은 한글패치 **Batman_Arkham_Origins_Blackgate_Vita_KO_v1.0.xdelta** 1개뿐입니다. 저장소에는 제작 소스와 한국어 번역만 공개합니다. 원본·완성 게임 파일, 추출한 게임 데이터, 일본어 원문, 글꼴 파일, 외부 실행 파일은 포함하지 않습니다. GitHub가 자동으로 만드는 Source code ZIP/TAR는 저장소 소스를 압축한 것이며 게임 파일이 아닙니다.

## 게임 소개 및 대상 버전

『배트맨: 아캄 오리진 블랙게이트』는 Armature Studio가 개발하고 워너 브라더스 인터랙티브가 2013년에 낸 PS Vita·3DS용 액션 어드벤처입니다. 『아캄 오리진』 3개월 뒤, 폭동이 일어난 블랙게이트 교도소에 들어간 배트맨이 조커·펭귄·블랙 마스크를 쫓는 이야기로, 2.5D 메트로배니아식 탐색과 탐정 모드 수사가 특징입니다. 일본판 제목은 『バットマン：アーカム・ビギンズ ブラックゲート』이며, 이 패치는 국내 정식 제목인 『아캄 오리진』 표기를 따릅니다.

이 패치는 **PS Vita 일본판(PCSG00261)의 게임 데이터 파일 `ozzy.psp2arc`**에 적용합니다. 복호화된 게임 폴더(`ux0:app/PCSG00261/`)에 있는 파일이어야 합니다. 파일 이름보다 아래 크기와 해시가 일치하는지가 중요합니다.

## 적용할 원본

| 파일 | 크기 (바이트) | **MD5** | SHA-256 |
| --- | --- | --- | --- |
| 원본 `ozzy.psp2arc` | 1,249,975,136 | `e692f4c12b1b4182f1da0e04ca487918` | `5a607c8522473fb467991c0851271b6817664854f33cdeedd25a4f0375ae5ecc` |
| 적용 결과 `ozzy.psp2arc` | 1,251,429,476 | `7bf0ef68cf31a6e1def0c2f55194d05a` | `dbcbed0832ee83d46c7dba4a22a8af480c2da6ce920015c1f376b61e57184b15` |
| `Batman_Arkham_Origins_Blackgate_Vita_KO_v1.0.xdelta` | 1,779,410 | `5475e5e3420c0ccae55c1cdf7ca62d97` | `138ba4b4d04e62bf4da5fd4faa3c0ad33a966491a1e4c945de30444290d97804` |

SHA-1은 [release_manifest.json](release_manifest.json)에 있습니다. 원본 게임 파일은 사용자가 직접 준비해야 합니다. `eboot.bin` 등 다른 파일은 바꾸지 않습니다.

## 패치 적용 방법

### Windows에서 원본 확인

```powershell
Get-FileHash -Algorithm MD5 -LiteralPath '.\ozzy.psp2arc'
```

위 표와 다르면 적용을 중단하세요.

### xdelta UI 사용

1. 릴리즈에서 `Batman_Arkham_Origins_Blackgate_Vita_KO_v1.0.xdelta`를 받습니다.
2. xdelta3 패치를 지원하는 도구에서 **Apply Patch** 기능을 엽니다.
3. **Patch**에는 xdelta 파일을, **Source File**에는 해시가 일치하는 원본 `ozzy.psp2arc`를 선택합니다.
4. **Output File**에는 새 파일 이름을 지정합니다(예: `ozzy_ko.psp2arc`). 다 만든 뒤 이름을 `ozzy.psp2arc`로 바꿔 아래 위치에 넣습니다.

xdelta는 호환성을 위해 압축·2차 압축·파일 경로 헤더 없이 만들었습니다. xdelta 자체는 [공식 프로젝트](https://github.com/jmacd/xdelta)를 참고하세요.

### 명령줄 사용

```powershell
.\xdelta3.exe -d -s '.\ozzy.psp2arc' '.\Batman_Arkham_Origins_Blackgate_Vita_KO_v1.0.xdelta' '.\ozzy_ko.psp2arc'
```

해시를 자동으로 검사하는 도구도 있습니다. Python 3과 xdelta3가 필요하며, 같은 이름의 출력 파일이 이미 있으면 덮어쓰지 않습니다.

```powershell
python tools/apply_release.py --xdelta '.\xdelta3.exe' --source '.\ozzy.psp2arc' --patch '.\Batman_Arkham_Origins_Blackgate_Vita_KO_v1.0.xdelta' --output '.\ozzy_ko.psp2arc'
```

### 게임에 넣기

- **PS Vita 실기(rePatch, 권장)**: 결과 파일을 `ux0:rePatch/PCSG00261/ozzy.psp2arc`로 복사합니다. 원본 게임 폴더는 그대로 둡니다.
- **PS Vita 실기(직접 교체)**: `ux0:app/PCSG00261/ozzy.psp2arc`를 백업한 뒤 결과 파일로 덮어씁니다.
- **Vita3K**: 설치된 게임 폴더(`<Vita3K 데이터 폴더>/ux0/app/PCSG00261/`)의 `ozzy.psp2arc`를 결과 파일로 바꿉니다.

일본판이므로 **✕ 버튼이 결정, ○ 버튼이 취소**입니다. 세이브 데이터 형식은 바꾸지 않았습니다.

## 작업 내용과 범위

| 구분 | 작업량 및 내용 |
| --- | --- |
| 메뉴·시스템 | 타이틀·세이브 선택·메인 메뉴·옵션·일시정지·조작 방법·콘셉트/무비 갤러리 해금 조건·확인창 |
| 배트컴퓨터 | 지도 목표·지역 이름, 아이템 이름·설명, 수사 사건 14건의 단서·해결 설명·사건 이름 |
| 탐정 분석기 | 분석 대상 이름·설명 254항목 |
| 안내·팝업 | 버튼 안내·튜토리얼·획득 팝업·목표 힌트·배트슈트 부품·엔딩 메모 |
| 자막 | 컷신 동영상 31편과 인게임 무전·대사 자막(음성 타이밍은 일본판 그대로) |
| 게임 글꼴 | 6종 글꼴(`bm_game`, `linefeed`, `chainprinter_small`, `chainprinter`, `voxbold`, `bm_header`)의 가나·한자 자리를 비우고 한글 **848자**를 그림(나눔스퀘어네오 Rg/Bd/Eb) |

텍스트 파일 52개(`ozzy/loc/_vta/*.cloc`)와 글꼴 12개(`*.cfon`·`*.ctxr`)를 바꿨고, 바꾼 파일은 원본 아카이브 끝에 덧붙였습니다. 원본 데이터는 그대로 남으므로 문장 길이 제한이 없습니다. 자세한 내용은 [docs/TECHNICAL.md](docs/TECHNICAL.md)를 참고하세요.

### 번역 원칙

- 기계 번역 없이 일본어·영어 원문과 문맥을 보고 직접 번역했습니다. 일본어판의 오역·오기는 영어 원문을 기준으로 바로잡았습니다.
- 인명·장비·장소는 한 가지 표기로 통일했습니다([용어집](docs/GLOSSARY.md)). 배트맨과 악당은 반말, 교도관·인질은 배트맨에게 존댓말을 씁니다.
- 화면별 어미를 통일했습니다(확인창 「~습니다」, 설명문 「~한다」, 목표 「~하라」, 메뉴는 명사형).

### 번역하지 않은 것

- 음성
- 원래 영어 전용인 스태프 크레디트
- 그림으로 된 로고(「BATMAN: ARKHAM ORIGINS BLACKGATE」 등 원래 영문)

## 알려진 한계

- 모든 장면을 게임으로 직접 플레이하며 확인하지는 못했습니다. Vita3K에서 타이틀·메뉴·옵션·일시정지·조작 방법·갤러리·배트컴퓨터·탐정 분석기·프롤로그 전투와 컷신 자막을 확인했고, 진행 후반의 수사 사건·보스 컷신 문장은 같은 화면에 넣은 시험 빌드로 표시를 확인했습니다.
- 「BEWARE THE BATMAN」 배트슈트 해금 화면은 PSN 연동이 필요해 확인하지 못했습니다.
- 실기에서의 동작은 확인하지 못했습니다. 문제가 있으면 이슈로 알려 주세요.

## 저장소 구성

| 경로 | 내용 |
| --- | --- |
| `tools/build.py` | 원본 `ozzy.psp2arc`에서 한글판을 빌드(텍스트 재구성, 글꼴 생성, 아카이브 덧붙이기) |
| `tools/` | 빌드·검증 도구(Python). `psarc.py` 아카이브 읽기, `psarc_patch.py` 바꾼 파일 덧붙이기, `cloc.py`·`locbuild.py` 텍스트 파일, `cfon.py` 글꼴 정보, `ctxr.py`·`fontbuild.py` 글꼴 텍스처(DXT5·스위즐), `preview.py` 글꼴 미리보기, `emu.py` 에뮬레이터 조작, `apply_release.py` 해시 검사 후 적용 |
| `text/ko.json` | 번역. 파일 이름 → 문자열 키 → 한국어(자막은 구간별 배열) |
| `docs/` | 기술 설명, 재빌드 방법, 용어집, 글꼴 출처 |

권리 관련 내용은 [RIGHTS.md](RIGHTS.md)를 참고하세요.
