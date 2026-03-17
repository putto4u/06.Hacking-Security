## Markdown 파일을 HTML로 자동 변환 및 통합하는 아키텍처 구성

현재 작성하신 Python(파이썬) 기반의 정적 페이지 생성 로직은 매우 훌륭한 접근입니다. 여기에 외부 프레임워크를 도입하지 않고, 기존 스크립트만 수정하여 **Markdown(마크다운)** 파일을 직접 **HTML(하이퍼텍스트 마크업 언어)**로 렌더링(Rendering)하는 기능을 추가했습니다.

아래 코드는 `.md` 파일을 스캔하여 HTML로 변환한 뒤, 기존 파일들과 함께 `index.html`에 예쁘게 나열하도록 수정한 최종 버전입니다.

---

### 1. `update_index.yml` 수정본

Python이 마크다운을 변환할 수 있도록 라이브러리를 설치하는 단계를 추가하고, 새로 생성된 HTML 파일들까지 모두 저장소에 반영(Commit)되도록 `git add .`으로 범위를 넓혔습니다.

```yaml
name: Generate Index HTML

on:
  push:
    branches:
      - main  # 또는 사용하는 기본 브랜치 명

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.x'

      - name: Install Dependencies
        run: pip install markdown

      - name: Run Index Generator
        run: python genindex.py

      - name: Commit and Push Changes
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add .  
          git diff --quiet && git diff --staged --quiet || (git commit -m "Update index.html and generate HTML from MD [skip ci]" && git push)

```

---

### 2. `genindex.py` 수정본

스크립트 상단에 `markdown` 모듈을 추가했습니다. 마크다운이 HTML로 변환되었을 때 텍스트가 깨지지 않고 깔끔한 문서 형태로 보이도록, Tailwind CSS(테일윈드 씨에스에스)의 `typography` Plugin(플러그인)을 헤더에 삽입하고 적용했습니다.

```python
import os
import markdown
from datetime import datetime

def generate_index():
    # 제외할 폴더 및 파일 설정
    exclude_dirs = {'.git', '.github', '.pytest_cache', '__pycache__', 'assets'}
    exclude_files = {'index.html', 'generate_index.py', 'genindex.py'}
    
    # 현대적인 디자인을 위한 CSS 및 HTML 구조 정의 (typography 플러그인 추가)
    html_header = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Putto's Lectures - 학습 콘텐츠 목록</title>
    <script src="https://cdn.tailwindcss.com?plugins=typography"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&display=swap');
        body {{ font-family: 'Noto Sans KR', sans-serif; background-color: #f8fafc; }}
        .hero-gradient {{
            background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        }}
        .card-hover {{
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        .card-hover:hover {{
            transform: translateY(-4px);
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1);
        }}
    </style>
</head>
<body class="text-slate-800">
    <header class="hero-gradient text-white py-12 px-6 shadow-lg mb-10">
        <div class="max-w-5xl mx-auto">
            <div class="flex items-center space-x-4 mb-4">
                <i class="fas fa-graduation-cap text-4xl text-blue-400"></i>
                <h1 class="text-4xl font-bold tracking-tight">Putto's Lectures</h1>
            </div>
            <p class="text-slate-300 text-lg">공용 클라우드 및 IT 기술 교육 자료 저장소</p>
            <div class="mt-6 flex items-center text-sm text-slate-400">
                <i class="far fa-clock mr-2"></i>
                <span>마지막 업데이트: {datetime.now().strftime('%Y-%m-%d %H:%M')}</span>
            </div>
        </div>
    </header>

    <main class="max-w-5xl mx-auto px-6 pb-20">
"""

    html_footer = """
    </main>
    <footer class="border-t border-slate-200 py-10 text-center text-slate-500 text-sm">
        <p>&copy; 2026 Putto's Lectures. 모든 권리 보유.</p>
    </footer>
</body>
</html>
"""

    content_body = ""
    structure = {}
    
    # 1. 마크다운(.md) 파일을 찾아 HTML 파일로 사전 변환
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for file in files:
            if file.endswith('.md') and file.lower() != 'readme.md':
                md_path = os.path.join(root, file)
                html_filename = file.replace('.md', '.html')
                html_path = os.path.join(root, html_filename)

                # 파일 읽기
                with open(md_path, 'r', encoding='utf-8') as f:
                    md_text = f.read()

                # 마크다운을 HTML 태그로 변환 (코드 블록 및 표 지원 확장 기능 포함)
                md_html = markdown.markdown(md_text, extensions=['fenced_code', 'tables'])

                # 개별 문서용 HTML 구성 (Tailwind prose 클래스로 자동 스타일링)
                doc_content = f'<div class="bg-white p-8 rounded-xl shadow-sm prose prose-slate max-w-none prose-img:rounded-xl">{md_html}</div>'
                full_doc_html = html_header + doc_content + html_footer

                # 변환된 HTML 저장
                with open(html_path, 'w', encoding='utf-8') as f:
                    f.write(full_doc_html)

    # 2. 저장소 탐색 및 데이터 구조화 (생성된 HTML 포함)
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        rel_path = os.path.relpath(root, '.')
        html_files = sorted([f for f in files if f.endswith('.html') and f not in exclude_files])
        
        if html_files:
            structure[rel_path] = html_files

    # 3. 정렬된 키(폴더명) 순으로 루트 인덱스 생성
    for folder in sorted(structure.keys()):
        files = structure[folder]
        display_folder = "루트 디렉터리" if folder == "." else folder
        folder_icon = "fa-folder-open" if folder != "." else "fa-house"
        
        content_body += f"""
        <section class="mb-12">
            <div class="flex items-center space-x-3 mb-6 border-b border-slate-200 pb-2">
                <i class="fas {folder_icon} text-blue-500"></i>
                <h2 class="text-2xl font-bold text-slate-700">{display_folder}</h2>
                <span class="bg-slate-200 text-slate-600 text-xs font-bold px-2 py-1 rounded-full">{len(files)}개 파일</span>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        """
        
        for file in files:
            file_path = os.path.join(folder, file) if folder != "." else file
            display_name = file.replace('.html', '').replace('_', ' ').replace('-', ' ')
            
            content_body += f"""
                <a href="{file_path}" target="_blank" class="card-hover bg-white p-5 rounded-xl border border-slate-100 shadow-sm flex items-start space-x-4">
                    <div class="bg-blue-50 p-3 rounded-lg text-blue-600">
                        <i class="far fa-file-code text-xl"></i>
                    </div>
                    <div class="overflow-hidden">
                        <h3 class="font-semibold text-slate-800 truncate" title="{display_name}">{display_name}</h3>
                        <p class="text-xs text-slate-400 mt-1 truncate">{file}</p>
                    </div>
                </a>
            """
            
        content_body += """
            </div>
        </section>
        """

    # 최종 파일 작성
    full_html = html_header + content_body + html_footer
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(full_html)
    
    print(f"성공: {datetime.now().strftime('%H:%M:%S')} - index.html 생성 및 마크다운 변환 완료.")

if __name__ == "__main__":
    generate_index()

```

---

### 💡 전문 용어 및 주석

* **Rendering (렌더링):** 원시 코드(마크다운 등)를 사용자가 브라우저에서 볼 수 있는 형태의 그래픽이나 텍스트(HTML)로 변환해 화면에 뿌려주는 과정입니다.
* **Commit (커밋):** 코드의 변경 사항을 로컬 저장소에 영구적으로 기록하는 Git(깃) 명령어입니다. 여기서는 Actions(액션즈)가 변환한 결과를 저장합니다.
* **Plugin (플러그인):** 소프트웨어에 특정 기능을 추가하기 위해 결합하는 보조 프로그램입니다. 여기서는 Tailwind의 `typography` 플러그인을 사용하여 마크다운이 변환된 밋밋한 HTML에 교재처럼 예쁜 서식을 입혔습니다.
* **`fenced_code` / `tables`:** 파이썬 `markdown` 모듈의 확장 기능으로, 백틱(```)을 이용한 코드 블록이나 마크다운 표(Table)를 정상적으로 변환해주는 역할을 합니다.

---

Next Step: Python Syntax Highlighting(구문 강조) 적용, index.html 검색 창 추가, GitHub Actions 빌드 캐시 최적화
