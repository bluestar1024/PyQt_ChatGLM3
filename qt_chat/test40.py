from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtGui import QContextMenuEvent
import mistune

class NoContextMenuPage(QWebEnginePage):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def createWindow(self, _type):
        return None  # 阻止新窗口

class OnlineLatexView(QWebEngineView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setPage(NoContextMenuPage(self))
        
        # 基础HTML模板（使用CDN资源）
        self.template = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <!-- 在线KaTeX资源 -->
            <link rel="stylesheet" 
                  href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css"
                  integrity="sha384-n8MVd4RsNIU0tAv4ct0nTaAbDJwPJzDEaqSD1odI+WdtXRGWt2kTvGFasHpSy3SV"
                  crossorigin="anonymous">
            <script defer
                    src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"
                    integrity="sha384-XjKyOOlGwcjNTAIQHIpgOno0Hl1YQqzUOEleOLALmuqehneUG+vnGctmUb0ZY0l8"
                    crossorigin="anonymous"></script>
            <script defer
                    src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js"
                    integrity="sha384-+VBxd3r6XgURycqtZ117nYw44OOcIax56Z4dCRWbxyPt0Koah1uHoK0wo4/YF0AA"
                    crossorigin="anonymous"
                    onload="renderMathInElement(document.body);"></script>
            <style>
                body { 
                    font-family: Arial;
                    margin: 20px;
                    line-height: 1.6;
                }
            </style>
        </head>
        <body>
            <div id="content">{content}</div>
            <script>
                // 动态渲染函数
                function updateContent(newContent) {{
                    document.getElementById('content').innerHTML = newContent;
                    renderMathInElement(document.body, {{
                        delimiters: [
                            {{left: '$$', right: '$$', display: true}},
                            {{left: '$', right: '$', display: false}}
                        ],
                        throwOnError: false
                    }});
                }}

                // 禁用右键菜单
                document.addEventListener('contextmenu', e => e.preventDefault());
            </script>
        </body>
        </html>
        """
        
        # 初始化禁用脚本
        self.js_disable_script = """
            // 禁止文本选择（可选）
            document.styleSheets[0].insertRule(
                '* { user-select: none !important; }', 0
            );
        """
        
        self.page().loadFinished.connect(self.on_page_loaded)

    def on_page_loaded(self, ok):
        if ok:
            self.page().runJavaScript(self.js_disable_script)

    def contextMenuEvent(self, event):
        event.ignore()  # 禁用Qt层右键菜单

    def render_latex(self, content):
        # 转义特殊字符
        safe_content = (
            content.replace('\\', '\\\\')
                   .replace("'", "\\'")
                   .replace('\n', '<br>')
        )
        
        # 生成完整HTML
        full_html = self.template.format(content=f"<script>updateContent('{safe_content}')</script>")
        
        self.setHtml(full_html, QUrl())

if __name__ == "__main__":
    import sys
    
    app = QApplication(sys.argv)
    
    view = OnlineLatexView()
    view.resize(800, 600)
    view.render_latex(
        "行内公式：$E = mc^2$\n\n"
        "块级公式：\n"
        "$$\\int_{a}^{b} x^2 dx$$\n\n"
        "矩阵示例：\n"
        "$$\\begin{pmatrix} 1 & 2 \\\\ 3 & 4 \\end{pmatrix}$$\n"
    )
    view.show()
    
    sys.exit(app.exec_())