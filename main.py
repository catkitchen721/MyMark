import os
import re
import markdown
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox, ttk
from typing import Callable, Dict
from tkhtmlview import HTMLLabel, HTMLScrolledText
from tkinterdnd2 import DND_FILES, TkinterDnD

class CustomMarkdownPreviewer:
    def __init__(self):
        self.custom_syntax: Dict[str, Callable] = {}
        self.symbol_syntax: Dict[str, str] = {}
        self.single_side_syntax: Dict[str, bool] = {}
        self.load_custom_syntax()
        self.load_default_syntax()
        self.create_gui()

    def load_custom_syntax(self):
        mod_folder = 'mod'
        if not os.path.exists(mod_folder):
            os.makedirs(mod_folder)
            messagebox.showinfo("資訊", f"已創建 '{mod_folder}' 資料夾。請在此資料夾中添加自定義語法檔案。")
            return

        for file in os.listdir(mod_folder):
            if file.endswith('.py'):
                syntax_name = os.path.splitext(file)[0]
                with open(os.path.join(mod_folder, file), 'r', encoding='utf-8') as f:
                    code = f.read()
                    # 添加編碼聲明
                    code = "# -*- coding: utf-8 -*-\n" + code
                    exec(code, globals())
                    self.custom_syntax[syntax_name] = globals()[syntax_name]
                    # 讀取符號定義和單側標記
                    symbol, is_single_side = self.get_symbol_and_side_from_docstring(code)
                    if symbol:
                        self.symbol_syntax[symbol] = syntax_name
                        self.single_side_syntax[syntax_name] = is_single_side

    def get_symbol_and_side_from_docstring(self, code):
        match = re.search(r'"""Symbol:\s*(\S+)\s*Single-side:\s*(True|False)\s*"""', code)
        if match:
            return match.group(1), match.group(2) == 'True'
        return None, False

    def load_default_syntax(self):
        default_syntax = {
            'bold': lambda text: f'<strong>{text}</strong>',
            'italic': lambda text: f'<em>{text}</em>',
            'underline': lambda text: f'<u>{text}</u>',
            'strikethrough': lambda text: f'<del>{text}</del>',
        }
        for name, func in default_syntax.items():
            if name not in self.custom_syntax:
                self.custom_syntax[name] = func

    def parse_custom_syntax(self, text: str) -> str:
        for syntax_name, syntax_func in self.custom_syntax.items():
            if self.single_side_syntax.get(syntax_name, False):
                pattern = r'\[' + syntax_name + r'\]'
                text = re.sub(pattern, lambda m: syntax_func(), text)
            else:
                pattern = r'\[' + syntax_name + r'\](.*?)\[/' + syntax_name + r'\]'
                text = re.sub(pattern, lambda m: syntax_func(m.group(1)), text, flags=re.DOTALL)
        return text

    def parse_symbol_syntax(self, text: str) -> str:
        for symbol, syntax_name in self.symbol_syntax.items():
            if self.single_side_syntax.get(syntax_name, False):
                text = text.replace(symbol, f'[{syntax_name}]')
            else:
                text = text.replace(symbol, f'[{syntax_name}]', 1)
                text = text.replace(symbol, f'[/{syntax_name}]', 1)
        return text

    def preview(self, text: str) -> str:
        symbol_parsed = self.parse_symbol_syntax(text)
        custom_parsed = self.parse_custom_syntax(symbol_parsed)
        html = markdown.markdown(custom_parsed)
        return html

    def create_gui(self):
        self.root = TkinterDnD.Tk()
        self.root.title("MyMark : 可自訂語法")

        # 創建左右分割的面板
        self.paned_window = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True)

        # 左側編輯區
        left_frame = ttk.Frame(self.paned_window)
        self.paned_window.add(left_frame)

        self.text_edit = scrolledtext.ScrolledText(left_frame, wrap=tk.WORD)
        self.text_edit.pack(fill=tk.BOTH, expand=True)
        self.text_edit.bind('<KeyRelease>', self.on_text_change)

        # 右側預覽區
        right_frame = ttk.Frame(self.paned_window)
        self.paned_window.add(right_frame)

        self.preview_html = HTMLLabel(right_frame, html="", background="white")
        self.preview_html.pack(fill=tk.BOTH, expand=True)

        # 按鈕區域
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill=tk.X, padx=10, pady=10)

        self.import_button = ttk.Button(button_frame, text="匯入文字檔", command=self.import_file)
        self.import_button.pack(side=tk.LEFT, padx=5)
        self.import_button_tips = ttk.Label(button_frame, text="提示: 你也可以拖拉檔案到視窗中進行匯入。")
        self.import_button_tips.pack(side=tk.LEFT, padx=5)

        self.save_button = ttk.Button(button_frame, text="保存文件", command=self.save_file)
        self.save_button.pack(side=tk.LEFT, padx=5)

        self.tutorial_button = ttk.Button(button_frame, text="自定義語法教學", command=self.show_tutorial)
        self.tutorial_button.pack(side=tk.LEFT, padx=5)

        self.loaded_mods_button = ttk.Button(button_frame, text="已載入的 Mods", command=self.show_loaded_mods)
        self.loaded_mods_button.pack(side=tk.LEFT, padx=5)

        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind('<<Drop>>', self.drop_file)

        self.root.mainloop()

    def on_text_change(self, event=None):
        content = self.text_edit.get("1.0", tk.END)
        preview_html = self.preview(content)
        self.preview_html.set_html(preview_html)

    def import_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("文字檔", "*.txt"), ("Markdown 檔", "*.md")])
        if file_path:
            self.load_file(file_path)

    def drop_file(self, event):
        file_path = event.data
        if file_path.endswith(('.txt', '.md')):
            self.load_file(file_path)

    def load_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            self.text_edit.delete("1.0", tk.END)
            self.text_edit.insert(tk.END, content)
            self.on_text_change()

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".md", filetypes=[("Markdown 檔", "*.md"), ("文字檔", "*.txt")])
        if file_path:
            content = self.text_edit.get("1.0", tk.END)
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            messagebox.showinfo("保存成功", f"文件已保存至 {file_path}")

    def show_tutorial(self):
        tutorial_window = tk.Toplevel(self.root)
        tutorial_window.title("自定義語法教學")
        tutorial_window.geometry("1200x600")

        tutorial_text = HTMLScrolledText(tutorial_window, html=self.get_tutorial_content())
        tutorial_text.pack(fill=tk.BOTH, expand=True)

    def get_tutorial_content(self):
        return '''
<h1>自定義語法教學</h1>

<h2>重要提示</h2>
<p>所有的自定義腳本檔案必須使用 UTF-8 編碼保存，以確保正確處理中文和其他特殊字符。</p>

<h2>步驟</h2>
<ol>
    <li>在 'mod' 資料夾中創建一個新的 Python 檔案，檔名格式為 [語法名稱].py。例如：<code>custom_highlight.py</code></li>
    <li>使用支持 UTF-8 編碼的文本編輯器（如 VS Code、Notepad++等）打開檔案。</li>
    <li>在檔案中定義一個與檔名相同的函數（不包括 .py 副檔名）。例如：
        <pre><code>"""Symbol: !! Single-side: False"""
def custom_highlight(text):
    return f'<span style="background-color: yellow;">{text}</span>'
        </code></pre>
    </li>
    <li>函數必須接受一個字串參數，並返回一個字串。
        <ul>
            <li><strong>輸入</strong>：包含在自定義標籤內的文字</li>
            <li><strong>輸出</strong>：處理後的 HTML 或純文字</li>
        </ul>
    </li>
    <li>如果要創建單側語法，請將 Single-side 設置為 True，並且函數不需要參數：
        <pre><code>"""Symbol: ## Single-side: True"""
def horizontal_line():
    return '&lt;hr&gt;'
        </code></pre>
    </li>
    <li>在 Markdown 文件中使用自定義語法：
        <ul>
            <li>雙側語法：<code>[custom_highlight]這是高亮文字[/custom_highlight]</code> 或 <code>!!這是高亮文字!!</code></li>
            <li>單側語法：<code>[horizontal_line]</code> 或 <code>##</code></li>
        </ul>
    </li>
    <li>重啟應用程式以載入新的自定義語法。</li>
</ol>

<h2>互動式示例</h2>
<p>讓我們一起創建一個將文字變為紅色的自定義語法和一個插入換行的單側語法！</p>
<ol>
    <li>創建檔案 <code>mod/red_text.py</code>（使用 UTF-8 編碼）</li>
    <li>在檔案中輸入以下代碼：
        <pre><code>"""Symbol: @@ Single-side: False"""
def red_text(text):
    return f'<span style="color: red;">{text}</span>'
        </code></pre>
    </li>
    <li>創建檔案 <code>mod/br.py</code>（使用 UTF-8 編碼）</li>
    <li>在檔案中輸入以下代碼：
        <pre><code>"""Symbol: -- Single-side: True"""
def br():
    return '&lt;br&gt;'
        </code></pre>
    </li>
    <li>保存檔案並重啟應用程式</li>
    <li>現在你可以在 Markdown 中使用：
        <ul>
            <li><code>[red_text]這是紅色文字[/red_text]</code> 或 <code>@@這是紅色文字@@</code></li>
            <li><code>[br]</code> 或 <code>--</code></li>
        </ul>
    </li>
</ol>
<p>試試看！創建你自己的自定義語法，然後在 Markdown 文件中使用它。記住，所有的自定義腳本都必須使用 UTF-8 編碼保存。</p>

<h2>預設語法</h2>
<ul>
    <li><strong>粗體</strong>：<code>[bold]粗體[/bold]</code></li>
    <li><em>斜體</em>：<code>[italic]斜體[/italic]</code></li>
    <li><u>底線</u>：<code>[underline]底線[/underline]</code></li>
    <li><del>刪除線</del>：<code>[strikethrough]刪除線[/strikethrough]</code></li>
</ul>

<h2>使用教學與用法</h2>

<h3>匯入文字檔</h3>
<ol>
    <li>點擊 "匯入文字檔" 按鈕。</li>
    <li>選擇一個 .txt 或 .md 檔案。</li>
    <li>檔案內容將會顯示在編輯區域。</li>
</ol>

<h3>保存文件</h3>
<ol>
    <li>點擊 "保存文件" 按鈕。</li>
    <li>選擇保存位置和檔案名稱。</li>
    <li>檔案將會以 .md 或 .txt 格式保存。</li>
</ol>

<h3>拖拉檔案</h3>
<ol>
    <li>你可以直接將 .txt 或 .md 檔案拖拉到視窗中。</li>
    <li>檔案內容將會自動顯示在編輯區域。</li>
</ol>

<h3>自定義語法</h3>
<ol>
    <li>在 'mod' 資料夾中創建自定義語法檔案。</li>
    <li>定義自定義函數並保存檔案。</li>
    <li>重啟應用程式以載入新的自定義語法。</li>
    <li>在 Markdown 文件中使用自定義語法標籤。</li>
</ol>

<p>希望這些教學能幫助你更好地使用這個應用程式！</p>
'''

    def show_loaded_mods(self):
        mods_window = tk.Toplevel(self.root)
        mods_window.title("已載入的 Mods")
        mods_window.geometry("400x300")

        mods_text = scrolledtext.ScrolledText(mods_window, wrap=tk.WORD)
        mods_text.pack(fill=tk.BOTH, expand=True)

        for symbol, syntax_name in self.symbol_syntax.items():
            is_single_side = self.single_side_syntax.get(syntax_name, False)
            mods_text.insert(tk.END, f"符號: {symbol}\n")
            mods_text.insert(tk.END, f"名稱: {syntax_name}\n")
            mods_text.insert(tk.END, f"單側標記: {'是' if is_single_side else '否'}\n\n")

        mods_text.config(state=tk.DISABLED)

if __name__ == "__main__":
    previewer = CustomMarkdownPreviewer()

