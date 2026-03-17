16GB USB 드라이브에 Kali Linux Live 부팅 환경을 만드는 방법을 순서대로 안내합니다. 이 과정은 \*\*지속성 저장 공간(Persistence)\*\*을 포함하지 않는 기본적인 Live USB 생성 방법입니다.

## 🛠️ 준비물

1.  **16GB 이상의 USB 드라이브:** (모든 데이터가 삭제되므로, 중요한 자료는 미리 백업해야 합니다.)
2.  **Kali Linux ISO 이미지 파일:** [Kali Linux 공식 웹사이트](https://www.google.com/search?q=https://www.kali.org/get-kali/%23kali-platforms)에서 다운로드합니다.
3.  **이미지 쓰기 도구 (이미저):** **Rufus** 또는 **Etcher (balenaEtcher)** 사용을 권장합니다.

-----

## 📝 Kali Linux Live USB 생성 순서

### 단계 1: ISO 파일 다운로드

1.  **Kali Linux 공식 다운로드 페이지**에서 자신의 시스템 아키텍처(대부분 **64-bit Installer** 또는 **Live** 버전)에 맞는 최신 ISO 파일을 다운로드합니다.
      * *실전 팁:* **Live** 이미지를 다운로드해야 부팅 시 설치 없이 바로 운영체제를 사용할 수 있습니다.

### 단계 2: 이미지 쓰기 도구 실행 (Rufus 사용 권장)

Windows 환경에서는 **Rufus**가 안정성과 다양한 옵션 지원 면에서 좋습니다.

1.  Rufus를 다운로드하여 실행합니다. (설치 없이 실행 가능한 포터블 버전입니다.)
2.  **USB 드라이브를 PC에 연결**합니다.

### 단계 3: Rufus 설정 및 이미지 쓰기

Rufus 화면에서 다음 설정들을 순서대로 지정합니다.

| 설정 항목 | 설정 값 | 설명 |
| :--- | :--- | :--- |
| **장치 (Device)** | 연결된 **16GB USB 드라이브** 선택 | **⚠️ 드라이브 문자를 반드시 확인하세요.** |
| **부트 선택 (Boot selection)** | **Disk or ISO image (Please select)** | 오른쪽 **'선택'** 버튼을 눌러 다운로드한 **Kali Linux ISO 파일**을 지정합니다. |
| **이미지 옵션 (Image option)** | **ISO Image** 또는 **DD Image** (ISO 모드 권장) | Rufus가 묻는 창이 뜨면 \*\*'ISO Image 모드'\*\*를 선택하세요. |
| **파티션 구성표 (Partition scheme)** | **GPT** | 최신 UEFI 시스템과의 호환성을 위해 **GPT**를 선택하는 것이 좋습니다. |
| **대상 시스템 (Target system)** | **UEFI (non CSM)** | GPT 선택 시 자동으로 선택됩니다. |
| **볼륨 레이블 (Volume label)** | 기본값 유지 (예: `KALI-LIVE`) | 필요에 따라 이름을 지정합니다. |

USB 라이브 부팅 디스크 제작 도구인 **Rufus**를 사용하여 Kali Linux Live USB를 만들 때, 영속성(Persistence)을 설정하는 방법에는 몇 가지 중요한 점이 있습니다.

Rufus는 Kali Linux ISO 파일이 선택되면 **자동으로 영속성 설정 슬라이더를 활성화**시키는 것이 일반적입니다. 하지만 이 옵션이 보이지 않거나 제대로 작동하지 않는 경우를 대비한 팁을 알려드립니다.

## 🔑 Rufus에서 영속성(Persistence) 설정 찾기

Kali Linux ISO를 선택하고 나면, Rufus의 주요 옵션 영역에 **"지속성 파티션 크기(Persistence partition size)"** 또는 이와 유사한 이름의 **슬라이더 바**가 나타납니다.

1.  **ISO 파일 선택:** Rufus 상단의 '부트 선택'에서 다운로드한 Kali Linux ISO 파일을 선택합니다.
2.  **슬라이더 확인:** 파일을 선택하면 보통 아래쪽 레이아웃 옵션 부분에 **파티션 크기를 조절하는 슬라이더**가 나타나는데, 이 슬라이더를 오른쪽으로 움직여 USB 드라이브에 저장할 영속성 공간의 크기를 지정할 수 있습니다.
    * `0`으로 설정하면 일반적인 Live 모드(재부팅 시 초기화)로 작동합니다.
    * `0`보다 큰 값으로 설정하면 해당 용량만큼 영속성 공간이 확보됩니다.

### ❗ 주의 사항 및 고급 팁

Rufus에서 영속성 슬라이더가 보이지 않거나, 영속성 기능이 제대로 작동하지 않는 경우가 있습니다. 특히 최신 버전의 Kali Linux Live ISO 이미지나 "Everything" 버전 이미지에서 이러한 문제가 발생할 수 있습니다.

**이 경우, Kali Linux에서 공식적으로 권장하는 방식은 Rufus의 내장 기능을 사용하는 것이 아닙니다.**

#### 공식 권장 방법 (더 전문적이고 확실함)

IT 전문가의 관점에서, Rufus의 기능에 의존하기보다, **직접 파티션을 생성하여 영속성을 확보**하는 방식이 훨씬 안정적이고 유연합니다.

1.  **Rufus로 기본 Live USB 생성:**
    * Rufus에서 ISO 파일만 구동할 수 있도록 Live USB를 만듭니다. (이때, 영속성 크기를 0으로 두거나 슬라이더가 없어도 됩니다.)
    * **주의:** Rufus의 "이미지 기록 모드"를 **`ISO Image 모드`**로 선택해야 합니다. DD 모드로 기록하면 USB의 모든 공간이 ISO 이미지로 덮어씌워져 추가 파티션을 만들기 어려워집니다.

2.  **Kali Live로 부팅 및 파티션 생성:**
    * 방금 만든 Live USB로 PC를 부팅합니다.
    * 부팅된 Kali Linux 환경에서 **`gparted`**와 같은 파티션 도구를 사용하여 USB 드라이브의 **남은 공간**에 새로운 파티션을 만듭니다.
    * 새로 만든 파티션에 **`persistence`**라는 **레이블(Label)**을 지정하고, 파일 시스템은 **`ext3`** 또는 **`ext4`**로 설정합니다.

3.  **영속성 설정 파일 생성 (핵심):**
    * 새 파티션을 마운트하고, 그 안에 영속성을 위한 설정 파일(`persistence.conf`)을 만듭니다.

$$\text{kali@kali:} \sim\$ \text{sudo mkdir -p /mnt/persistence}$$
$$\text{kali@kali:} \sim\$ \text{sudo mount /dev/sdXN /mnt/persistence} \quad\quad (\text{N은 새로 만든 파티션 번호})$$
$$\text{kali@kali:} \sim\$ \text{echo "/ union" | sudo tee /mnt/persistence/persistence.conf}$$
$$\text{kali@kali:} \sim\$ \text{sudo umount /dev/sdXN}$$

4.  **영속성 모드로 재부팅:**
    * 이제 USB를 뽑고 다시 꽂아 재부팅합니다. Kali 부트 메뉴에서 **"Live USB Persistence"** 옵션을 선택하면 영속성이 활성화된 상태로 부팅됩니다.

이 방식은 수동으로 파티션을 분할하여 영속성 공간을 확실히 확보하므로, Rufus의 슬라이더 옵션에 의존하는 것보다 훨씬 안정적인 방법입니다.


### 단계 5: 부팅 테스트

1.  USB 쓰기 작업이 완료되면, Rufus를 닫고 USB를 제거하지 않은 상태로 PC를 **재부팅**합니다.
2.  PC 시작 시 **BIOS/UEFI 설정 진입 키** (삼성 노트북은 보통 **F2**) 또는 **부팅 메뉴 키** (보통 **F10, F12, ESC**)를 눌러 부팅 순서를 선택합니다.
3.  부팅 옵션에서 **생성한 USB 드라이브** (일반적으로 **UEFI: [USB 제조사 이름]** 형태)를 선택합니다.
4.  Kali Linux 부팅 메뉴가 나타나면 **"Live system"** 또는 \*\*"Live (forensic mode)"\*\*를 선택하여 Kali Linux를 사용합니다.

-----

**자주 오해하거나 실수하는 부분:**

Kali Linux Live USB를 생성한 후에도 부팅이 안 된다면, 바로 전 질문에서 해결했던 것처럼 **노트북의 BIOS 설정**에서 **Secure Boot를 비활성화**하고 **OS Mode Selection을 CSM and UEFI OS로 설정**했는지 다시 한번 확인해야 합니다. 이는 USB 제작 방식의 문제가 아닌, PC의 보안 설정 문제입니다.

Kali Linux의 로그인 정책이 최신 버전에서 변경되었기 때문에, 버전에 따라 기본 계정 정보가 달라집니다.

현재 사용하시는 **Kali Linux Live** 이미지의 버전에 맞춰 알려드립니다.

-----

## 📌 최신 Kali Linux Live의 기본 계정 (2020.1 버전 이후)

Kali Linux는 2020.1 버전부터 보안 강화를 위해 기본적으로 `root` 계정 대신 **일반 사용자 계정** 정책을 채택했습니다.

따라서, Live USB로 부팅했을 때의 기본 로그인 정보는 다음과 같습니다.

| 구분 | 사용자 이름 (Username) | 비밀번호 (Password) |
| :---: | :---: | :---: |
| **기본값** | `kali` | `kali` |

즉, **사용자 이름은 `kali`**, \*\*비밀번호도 `kali`\*\*로 입력하시면 됩니다.

-----

### 💡 실전 팁: `root` 권한 사용과 영속성

Live 세션에서 대부분의 해킹 도구는 `root` 권한을 필요로 합니다. `kali/kali`로 로그인한 후 터미널에서 `root` 권한으로 전환할 수 있습니다.

1.  **`root` 권한으로 전환:**
    터미널을 열고 다음 명령어를 입력한 후, 현재 사용자(`kali`)의 비밀번호인 \*\*`kali`\*\*를 입력하세요.

    ```bash
    sudo su -
    ```

    이제 프롬프트가 `#`로 바뀌면서 `root` 권한으로 모든 작업을 수행할 수 있습니다.

2.  **영속성(Persistence) 사용 시 주의점:**
    영속성 모드로 부팅한 경우, `root` 계정의 비밀번호를 안전하게 변경하여 사용하시는 것을 권장합니다.

    ```bash
    sudo passwd root
    ```

    이후 새로운 `root` 비밀번호를 설정하시면 됩니다. 영속성을 설정하셨다면, 이렇게 변경한 비밀번호가 재부팅 후에도 유지됩니다.
