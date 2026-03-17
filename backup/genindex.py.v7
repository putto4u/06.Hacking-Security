import os
import markdown
from datetime import datetime

def generate_index():
    # 제외할 폴더 및 파일 설정 (새로 생성될 목차 파일 toc.html 추가)
    exclude_dirs = {'.git', '.github', '.pytest_cache', '__pycache__', 'assets'}
    exclude_files = {'index.html', 'generate_index.py', 'genindex.py', 'README.md', 'toc.html'}
    
    # ---------------------------------------------------------------------------
    # [1] 마크다운 변환 및 목차(TOC)용 최소 HTML(HyperText Markup Language, 웹페이지 구조 언어) 헤더/푸터
    # ---------------------------------------------------------------------------
    doc_html_header = """<!DOCTYPE html>
<html lang="ko" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.tailwindcss.com?plugins=typography"></script>
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
    <script>tailwind.config = { darkMode: 'class' }</script>
</head>
<body class="p-6 md:p-10">
"""
    doc_html_footer = "</body></html>"

    # ---------------------------------------------------------------------------
    # [2] 메인 인덱스 전용 HTML 헤더 (스플릿 뷰 레이아웃)
    # ---------------------------------------------------------------------------
    index_html_header = f"""<!DOCTYPE html>
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
            color: #f8fafc; 
            background-image: linear-gradient(to bottom, rgba(2, 6, 23, 0.85), rgba(2, 6, 23, 0.98)), 
                              url('image_1a3201.jpg');
            background-size: cover;
            background-attachment: fixed;
            background-position: center center;
            height: 100vh;
            overflow: hidden; 
        }}

        .list-hover {{ transition: all 0.2s ease; }}
        .list-hover:hover {{
            color: #22d3ee; padding-left: 0.75rem; 
            background-color: rgba(15, 23, 42, 0.8); border-left-color: #0ea5e9;
        }}
        .text-glow {{ text-shadow: 0 2px 10px rgba(0, 0, 0, 0.8); }}
        .neon-glow {{ text-shadow: 0 0 8px rgba(34, 211, 238, 0.6); }}
        
        ::-webkit-scrollbar {{ width: 6px; height: 6px; }}
        ::-webkit-scrollbar-track {{ background: rgba(15, 23, 42, 0.5); border-radius: 4px; }}
        ::-webkit-scrollbar-thumb {{ background: #334155; border-radius: 4px; }}
        ::-webkit-scrollbar-thumb:hover {{ background: #0ea5e9; }}
    </style>
    <script>tailwind.config = {{ darkMode: 'class' }}</script>
</head>
<body class="flex flex-col">
    <header class="py-10 px-6 relative flex-shrink-0">
        <a href="toc.html" target="content-frame" class="absolute top-6 left-6 md:left-10 z-20 group cursor-pointer block">
            <div class="flex items-center space-x-2 bg-slate-900/80 py-2 px-4 rounded-xl border border-cyan-900/50 backdrop-blur-md shadow-[0_0_15px_rgba(8,145,178,0.2)] transition-all duration-300 group-hover:border-cyan-400/60 group-hover:shadow-[0_0_20px_rgba(34,211,238,0.4)]">
                <div class="relative flex h-3 w-3 mr-1">
                    <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-cyan-400 opacity-75"></span>
                    <span class="relative inline-flex rounded-full h-3 w-3 bg-cyan-500"></span>
                </div>
                <span class="font-mono text-[10px] md:text-xs text-slate-400 tracking-wider">CHIEF SYSTEM ARCHITECT <span class="text-cyan-500 ml-1">❯</span></span>
                <span class="font-black text-cyan-300 tracking-widest font-mono text-sm md:text-base neon-glow ml-1">PUTTO</span>
                <span class="font-bold text-slate-200 tracking-widest font-mono text-sm md:text-base">'S LECTURES</span>
            </div>
        </a>

        <div class="max-w-6xl mx-auto relative z-10 text-center mt-4">
            <h1 class="text-3xl md:text-4xl lg:text-5xl font-black tracking-tight mb-2 pb-1 bg-clip-text text-transparent bg-gradient-to-r from-cyan-300 via-blue-400 to-indigo-400 drop-shadow-[0_5px_5px_rgba(0,0,0,0.8)]">
                Cloud Security & Hacking Lab
            </h1>
            <p class="text-slate-300 font-medium text-sm md:text-base max-w-2xl mx-auto text-glow">
                실전 클라우드 인프라 보안 및 모의 해킹 시나리오 연구 자료 저장소
            </p>
        </div>
    </header>

    <main class="flex-grow w-full max-w-screen-2xl mx-auto px-4 pb-6 flex gap-4 min-h-0">
        
        <aside class="w-80 flex-shrink-0 flex flex-col bg-slate-900/60 rounded-2xl border border-slate-700/80 backdrop-blur-md shadow-2xl overflow-hidden">
            <div class="p-4 border-b border-slate-700/80 bg-slate-950/50 flex justify-between items-center flex-shrink-0">
                <span class="text-slate-200 font-bold tracking-widest text-sm font-mono"><i class="fas fa-network-wired mr-2 text-cyan-500"></i>DIRECTORY</span>
                <button onclick="toggleAllFolders()" class="group flex items-center space-x-1 hover:text-cyan-400 text-slate-400 transition-colors text-xs font-mono">
                    <i class="fas fa-folder-open" id="global-toggle-icon"></i>
                    <span id="global-toggle-text">COLLAPSE</span>
                </button>
            </div>
            
            <div class="p-4 overflow-y-auto flex-grow h-full space-y-4 pb-10">
"""

    index_html_middle = """
            </div>
        </aside>

        <section class="flex-grow flex flex-col bg-slate-950/90 rounded-2xl border border-slate-700/80 backdrop-blur-xl shadow-2xl relative overflow-hidden">
            <iframe name="content-frame" id="content-frame" class="w-full h-full border-none relative z-20 bg-transparent rounded-2xl" src="toc.html"></iframe>
        </section>
    </main>
"""

    index_html_footer = """
    <footer class="border-t border-slate-800/80 py-3 text-center text-slate-500 text-xs bg-slate-950/90 backdrop-blur-md flex-shrink-0">
        <p class="font-mono">&copy; 2026 Putto's Lectures. <span class="text-cyan-800 font-bold ml-1">| ACCESS SECURED.</span></p>
    </footer>

    <script>
        let isAllExpanded = true;

        function toggleFolder(element) {
            const section = element.closest('.folder-section');
            const listContainer = section.querySelector('.list-container');
            const folderIcon = element.querySelector('.folder-icon');
            const chevronIcon = element.querySelector('.chevron-icon');
            
            const baseIcon = element.getAttribute('data-base-icon');
            const isExpanded = listContainer.classList.contains('grid-rows-[1fr]');

            if (isExpanded) {
                listContainer.classList.remove('grid-rows-[1fr]', 'opacity-100');
                listContainer.classList.add('grid-rows-[0fr]', 'opacity-0');
                chevronIcon.classList.add('rotate-180');
                if (baseIcon !== 'fa-server') {
                    folderIcon.classList.remove('fa-folder-open');
                    folderIcon.classList.add('fa-folder');
                }
            } else {
                listContainer.classList.remove('grid-rows-[0fr]', 'opacity-0');
                listContainer.classList.add('grid-rows-[1fr]', 'opacity-100');
                chevronIcon.classList.remove('rotate-180');
                if (baseIcon !== 'fa-server') {
                    folderIcon.classList.remove('fa-folder');
                    folderIcon.classList.add('fa-folder-open');
                }
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
                const isCurrentlyExpanded = listContainer.classList.contains('grid-rows-[1fr]');

                if (isAllExpanded !== isCurrentlyExpanded) {
                    toggleFolder(header);
                }
            });

            if (isAllExpanded) {
                globalBtnIcon.classList.remove('fa-folder');
                globalBtnIcon.classList.add('fa-folder-open');
                globalBtnText.innerText = 'COLLAPSE';
            } else {
                globalBtnIcon.classList.remove('fa-folder-open');
                globalBtnIcon.classList.add('fa-folder');
                globalBtnText.innerText = 'EXPAND';
            }
        }
    </script>
</body>
</html>
"""

    content_body = ""
    structure = {}
    
    # ---------------------------------------------------------------------------
    # [3] 마크다운 변환 및 저장
    # ---------------------------------------------------------------------------
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

    # ---------------------------------------------------------------------------
    # [4] 디렉토리 구조화, 좌측 사이드바 생성 및 중앙 화면용 목차(TOC) 생성
    # ---------------------------------------------------------------------------
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        rel_path = os.path.relpath(root, '.')
        html_files = sorted([f for f in files if f.endswith('.html') and f not in exclude_files])
        if html_files:
            structure[rel_path] = html_files

    # Iframe(내부 프레임)의 첫 화면으로 보여질 목차 마크다운 텍스트 구성
    toc_md = "# 📚 전체 목차 (Table of Contents)\n\n"

    for folder in sorted(structure.keys()):
        files = structure[folder]
        is_root = folder == "."
        display_folder = "Root Directory" if is_root else folder
        
        base_icon = "fa-server" if is_root else "fa-folder-open"
        closed_icon = "fa-server" if is_root else "fa-folder"
        
        # 좌측 트리 뷰 구성
        content_body += f"""
        <div class="folder-section bg-slate-950/40 rounded-xl border border-slate-800/60 transition-all duration-300">
            <div class="folder-header flex items-center p-3 cursor-pointer group hover:bg-slate-800/50 rounded-t-xl transition-colors" 
                 onclick="toggleFolder(this)" 
                 data-base-icon="{base_icon}" 
                 data-closed-icon="{closed_icon}">
                <i class="folder-icon fas {base_icon} text-cyan-600 w-5 text-center transition-transform duration-300 group-hover:scale-110"></i>
                <h2 class="text-sm font-bold text-slate-300 ml-2 group-hover:text-cyan-300 truncate">{display_folder}</h2>
                <i class="fas fa-chevron-up ml-auto text-slate-600 text-xs transition-transform duration-300 chevron-icon"></i>
            </div>
            
            <div class="list-container grid transition-all duration-300 ease-in-out grid-rows-[1fr] opacity-100 border-t border-slate-800/60">
                <div class="overflow-hidden bg-slate-900/20 rounded-b-xl">
                    <ul class="py-1">
        """
        
        # 우측 Iframe 초기 화면용 목차(TOC) 추가
        toc_md += f"### 📂 {display_folder}\n"

        for file in files:
            file_path = os.path.join(folder, file) if not is_root else file
            display_name = file.replace('.html', '').replace('_', ' ').replace('-', ' ')
            
            # 우측 프레임용 목록 추가
            toc_md += f"- [{display_name}]({file_path})\n"
            
            # 좌측 메뉴 링크 구성
            content_body += f"""
                        <li>
                            <a href="{file_path}" target="content-frame" class="list-hover flex items-center py-2 px-4 border-l-2 border-transparent group text-sm">
                                <i class="fas fa-file-code text-slate-600 mr-2 group-hover:text-cyan-400 text-xs"></i>
                                <span class="text-slate-400 font-medium group-hover:text-cyan-100 truncate">{display_name}</span>
                            </a>
                        </li>
            """
            
        content_body += """
                    </ul>
                </div>
            </div>
        </div>
        """
        toc_md += "\n"

    # ---------------------------------------------------------------------------
    # [5] 우측 Iframe 용 toc.html(목차 파일) 렌더링 및 저장
    # ---------------------------------------------------------------------------
    toc_html_content = doc_html_header + f'''
    <div class="prose prose-invert prose-slate max-w-none prose-img:rounded-xl prose-a:text-cyan-400 hover:prose-a:text-cyan-300 prose-headings:text-slate-100 prose-strong:text-cyan-100 bg-slate-900/40 p-8 rounded-2xl border border-slate-700/50 shadow-xl">
        {markdown.markdown(toc_md, extensions=['fenced_code', 'tables'])}
    </div>
    ''' + doc_html_footer
    
    with open('toc.html', 'w', encoding='utf-8') as f:
        f.write(toc_html_content)

    # ---------------------------------------------------------------------------
    # [6] 최종 병합 및 메인 인덱스 파일 작성
    # ---------------------------------------------------------------------------
    full_html = index_html_header + content_body + index_html_middle + index_html_footer
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(full_html)
    
    print(f"System Log: {datetime.now().strftime('%H:%M:%S')} - Multi-frame layout with TOC(Table of Contents) auto-generation complete.")

if __name__ == "__main__":
    generate_index()
