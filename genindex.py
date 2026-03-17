import os
import markdown
from datetime import datetime

def generate_index():
    exclude_dirs = {'.git', '.github', '.pytest_cache', '__pycache__', 'assets'}
    exclude_files = {'index.html', 'generate_index.py', 'genindex.py', 'README.md', 'toc.html'}
    
    # ---------------------------------------------------------------------------
    # [1] 마크다운 변환 문서용 기본 HTML 헤더/푸터
    # ---------------------------------------------------------------------------
    doc_html_header = """<!DOCTYPE html>
<html lang="ko" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.tailwindcss.com?plugins=typography"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap');
        body { 
            font-family: 'Noto Sans KR', sans-serif; 
            background-color: transparent; 
            color: #f8fafc; 
            margin: 0; padding: 0;
        }
        ::-webkit-scrollbar { width: 8px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: #334155; border-radius: 4px; }
        ::-webkit-scrollbar-thumb:hover { background: #0ea5e9; }
    </style>
</head>
<body class="p-6 pt-20 md:p-10 md:pt-24 max-w-5xl mx-auto">
"""
    doc_html_footer = "</body></html>"

    # ---------------------------------------------------------------------------
    # [2] TOC(Table of Contents, 목차) 전용 HTML 헤더
    # ---------------------------------------------------------------------------
    toc_html_header = """<!DOCTYPE html>
<html lang="ko" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.tailwindcss.com?plugins=typography"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap');
        body { 
            font-family: 'Noto Sans KR', sans-serif; 
            background-color: transparent; 
            color: #f8fafc; 
            margin: 0; padding: 0;
        }
        .list-hover { transition: all 0.2s ease; }
        .list-hover:hover {
            color: #22d3ee; padding-left: 0.75rem; 
            background-color: rgba(15, 23, 42, 0.8); border-left-color: #0ea5e9;
        }
        ::-webkit-scrollbar { width: 8px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: #334155; border-radius: 4px; }
        ::-webkit-scrollbar-thumb:hover { background: #0ea5e9; }
        .text-glow { text-shadow: 0 2px 10px rgba(0, 0, 0, 0.8); }
    </style>
</head>
<body class="p-6 pt-20 md:p-12 md:pt-24">
    <div class="max-w-6xl mx-auto text-center mb-10 md:mb-14">
        <h1 class="text-3xl md:text-4xl lg:text-5xl font-black tracking-tight mb-2 pb-1 bg-clip-text text-transparent bg-gradient-to-r from-cyan-300 via-blue-400 to-indigo-400 drop-shadow-[0_5px_5px_rgba(0,0,0,0.8)]">
            Cloud Security & Hacking Lab
        </h1>
        <p class="text-slate-300 font-medium text-sm md:text-base max-w-2xl mx-auto text-glow">
            실전 클라우드 인프라 보안 및 모의 해킹 시나리오 연구 자료 저장소
        </p>
    </div>

    <div class="max-w-4xl mx-auto">
        <div class="flex justify-between items-center mb-8 border-b border-slate-700/80 pb-4">
            <h1 class="text-2xl md:text-3xl font-black text-slate-100 tracking-wide">
                <i class="fas fa-network-wired text-cyan-500 mr-3"></i>DIRECTORY INDEX
            </h1>
            <button onclick="toggleAllFolders()" class="group flex items-center space-x-2 bg-slate-800/80 hover:bg-slate-700 text-cyan-400 py-2 px-4 rounded-lg border border-cyan-900/50 transition-all duration-300 shadow-md">
                <i class="fas fa-folder-open" id="global-toggle-icon"></i>
                <span class="font-mono text-xs font-bold tracking-widest" id="global-toggle-text">EXPAND ALL</span>
            </button>
        </div>
        <div class="space-y-6">
"""

    toc_html_footer = """
        </div>
    </div>
    
    <script>
        let isAllExpanded = false;
        
        // 부모 창의 Hash(해시) 업데이트 함수
        function updateParentHash(path) {
            if (window.parent) {
                window.parent.location.hash = path;
            }
        }

        function toggleFolder(element) {
            const section = element.closest('.folder-section');
            const listContainer = section.querySelector('.list-container');
            const folderIcon = element.querySelector('.folder-icon');
            const chevronIcon = element.querySelector('.chevron-icon');
            const baseIcon = element.getAttribute('data-base-icon');
            
            const isExpanded = listContainer.style.gridTemplateRows === '1fr';

            if (isExpanded) {
                listContainer.style.gridTemplateRows = '0fr';
                listContainer.classList.remove('opacity-100', 'border-slate-700/80');
                listContainer.classList.add('opacity-0', 'border-transparent');
                chevronIcon.classList.replace('fa-chevron-up', 'fa-chevron-down');
                if (baseIcon !== 'fa-server') folderIcon.classList.replace('fa-folder-open', 'fa-folder');
            } else {
                listContainer.style.gridTemplateRows = '1fr';
                listContainer.classList.remove('opacity-0', 'border-transparent');
                listContainer.classList.add('opacity-100', 'border-slate-700/80');
                chevronIcon.classList.replace('fa-chevron-down', 'fa-chevron-up');
                if (baseIcon !== 'fa-server') folderIcon.classList.replace('fa-folder', 'fa-folder-open');
            }
        }

        function toggleAllFolders() {
            isAllExpanded = !isAllExpanded;
            const headers = document.querySelectorAll('.folder-header');
            const globalBtnIcon = document.getElementById('global-toggle-icon');
            const globalBtnText = document.getElementById('global-toggle-text');

            headers.forEach(header => {
                const section = header.closest('.folder-section');
                const listContainer = section.querySelector('.list-container');
                const isCurrentlyExpanded = listContainer.style.gridTemplateRows === '1fr';
                if (isAllExpanded !== isCurrentlyExpanded) toggleFolder(header);
            });

            if (isAllExpanded) {
                globalBtnIcon.classList.replace('fa-folder-open', 'fa-folder');
                globalBtnText.innerText = 'COLLAPSE ALL';
            } else {
                globalBtnIcon.classList.replace('fa-folder', 'fa-folder-open');
                globalBtnText.innerText = 'EXPAND ALL';
            }
        }
    </script>
</body>
</html>
"""

    # ---------------------------------------------------------------------------
    # [3] 메인 레이아웃 (주소창 Hash 제어 스크립트 포함)
    # ---------------------------------------------------------------------------
    index_html = f"""<!DOCTYPE html>
<html lang="ko" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Security & Cloud Hacking Lab</title>
    <script src="https://cdn.tailwindcss.com?plugins=typography"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap');
        body {{ 
            font-family: 'Noto Sans KR', sans-serif; 
            background-color: #020617; 
            background-image: linear-gradient(to bottom, rgba(2, 6, 23, 0.85), rgba(2, 6, 23, 0.98)), 
                              url('image_1a3201.jpg');
            background-size: cover;
            background-attachment: fixed;
            background-position: center center;
            margin: 0; padding: 0;
            height: 100vh;
            width: 100vw;
            overflow: hidden; 
        }}
        .neon-glow {{ text-shadow: 0 0 8px rgba(34, 211, 238, 0.6); }}
    </style>
</head>
<body class="relative">
    <!-- 저자 박스: 클릭 시 목차로 이동하며 Hash도 초기화 -->
    <a href="#toc.html" onclick="setFrameSource('toc.html')" class="absolute top-5 right-5 md:top-6 md:right-8 z-50 group cursor-pointer block">
        <div class="flex items-center space-x-1.5 bg-slate-900/80 py-1.5 px-3 rounded-lg border border-cyan-900/50 backdrop-blur-md shadow-[0_0_10px_rgba(8,145,178,0.2)] transition-all duration-300 group-hover:border-cyan-400/60 group-hover:shadow-[0_0_15px_rgba(34,211,238,0.4)]">
            <div class="relative flex h-2 w-2 mr-0.5">
                <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-cyan-400 opacity-75"></span>
                <span class="relative inline-flex rounded-full h-2 w-2 bg-cyan-500"></span>
            </div>
            <span class="font-mono text-[8px] md:text-[10px] text-slate-400 tracking-wider uppercase">Chief System Architect <span class="text-cyan-500 ml-0.5">❯</span></span>
            <span class="font-black text-cyan-300 tracking-widest font-mono text-xs md:text-sm neon-glow ml-0.5">PUTTO</span>
            <span class="font-bold text-slate-200 tracking-widest font-mono text-xs md:text-sm">'S LECTURES</span>
        </div>
    </a>

    <iframe name="content-frame" id="content-frame" class="absolute inset-0 w-full h-full border-none z-10 bg-transparent" src="toc.html"></iframe>

    <script>
        const frame = document.getElementById('content-frame');

        // 프레임 소스 변경 및 Hash 업데이트 함수
        function setFrameSource(path) {
            frame.src = path;
            window.location.hash = path;
        }

        // 초기 로드 시 또는 새로고침 시 Hash를 읽어 프레임 소스 설정
        function handleHash() {
            const currentHash = window.location.hash.replace('#', '');
            if (currentHash && currentHash !== 'toc.html') {
                frame.src = currentHash;
            } else {
                frame.src = 'toc.html';
            }
        }

        // 주소창의 Hash가 수동으로 변경될 때 감지
        window.addEventListener('hashchange', handleHash);
        
        // 페이지 로드 시 실행
        window.addEventListener('load', handleHash);
    </script>
</body>
</html>
"""

    structure = {}
    toc_body = ""
    
    # [4] 마크다운 변환 및 개별 HTML 파일 생성
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for file in files:
            if file.endswith('.md') and file.lower() != 'readme.md':
                md_path = os.path.join(root, file)
                html_filename = file.replace('.md', '.html')
                html_path = os.path.join(root, html_filename)

                with open(md_path, 'r', encoding='utf-8') as f:
                    md_text = f.read()

                md_html = markdown.markdown(md_text, extensions=['fenced_code', 'tables'])
                doc_content = f'''
                <div class="prose prose-invert prose-slate max-w-none prose-img:rounded-xl prose-a:text-cyan-400 hover:prose-a:text-cyan-300 prose-headings:text-slate-100 prose-strong:text-cyan-100 bg-slate-900/40 p-8 rounded-2xl border border-slate-700/50 shadow-xl">
                    {md_html}
                </div>
                '''
                full_doc_html = doc_html_header + doc_content + doc_html_footer
                with open(html_path, 'w', encoding='utf-8') as f:
                    f.write(full_doc_html)

    # [5] 디렉토리 탐색 및 목차 생성
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        rel_path = os.path.relpath(root, '.')
        html_files = sorted([f for f in files if f.endswith('.html') and f not in exclude_files])
        if html_files:
            structure[rel_path] = html_files

    for folder in sorted(structure.keys()):
        files = structure[folder]
        is_root = folder == "."
        display_folder = "Root Directory" if is_root else folder
        base_icon = "fa-server" if is_root else "fa-folder-open"
        initial_folder_icon = "fa-server" if is_root else "fa-folder"
        
        toc_body += f"""
        <div class="folder-section bg-slate-900/60 rounded-xl border border-slate-700/80 shadow-lg">
            <div class="folder-header flex items-center p-4 cursor-pointer group hover:bg-slate-800/80 rounded-t-xl transition-colors" 
                 onclick="toggleFolder(this)" data-base-icon="{base_icon}">
                <i class="folder-icon fas {initial_folder_icon} text-cyan-500 w-6 text-center text-lg transition-transform duration-300 group-hover:scale-110"></i>
                <h2 class="text-base font-bold text-slate-200 ml-3 group-hover:text-cyan-300 tracking-wide">{display_folder}</h2>
                <span class="text-cyan-600/80 text-[10px] font-mono ml-3 font-bold bg-slate-950/50 px-2 py-1 rounded-md">[{len(files)}]</span>
                <i class="fas fa-chevron-down ml-auto text-slate-500 text-sm transition-transform duration-300 chevron-icon"></i>
            </div>
            <div class="list-container grid transition-all duration-300 ease-in-out opacity-0 border-t border-transparent" style="grid-template-rows: 0fr;">
                <div class="overflow-hidden bg-slate-950/40 rounded-b-xl">
                    <ul class="py-2">
        """
        
        for file in files:
            # 파일 경로 계산 (경로 구분자 '/'로 통일)
            file_path = (os.path.join(folder, file) if not is_root else file).replace('\\', '/')
            display_name = file.replace('.html', '').replace('_', ' ').replace('-', ' ')
            
            # 링크 클릭 시 updateParentHash 호출하여 주소창 동기화
            toc_body += f"""
                        <li>
                            <a href="{file_path}" target="content-frame" onclick="updateParentHash('{file_path}')"
                               class="list-hover flex items-center py-3 px-5 border-l-2 border-transparent group text-sm">
                                <i class="fas fa-file-code text-slate-600 mr-3 group-hover:text-cyan-400"></i>
                                <span class="text-slate-300 font-medium group-hover:text-cyan-100">{display_name}</span>
                            </a>
                        </li>
            """
        toc_body += "</ul></div></div></div>"

    # [6] 파일 저장
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(index_html)
    with open('toc.html', 'w', encoding='utf-8') as f:
        f.write(toc_html_header + toc_body + toc_html_footer)
    
    print(f"System Log: {datetime.now().strftime('%H:%M:%S')} - Hash-based navigation enabled. URLs are now persistent.")

if __name__ == "__main__":
    generate_index()
