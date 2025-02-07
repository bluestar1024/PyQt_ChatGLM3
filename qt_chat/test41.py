from PyQt5.QtCore import QUrl, QFile, Qt
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtGui import QContextMenuEvent

class NoContextMenuPage(QWebEnginePage):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def acceptNavigationRequest(self, url, type_, isMainFrame):
        """拦截所有导航请求"""
        return True  # 允许所有导航，但可以通过此方法控制特定类型
    
    def createWindow(self, _type):
        """完全禁止新窗口/标签页创建"""
        return None
    
    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceID):
        """可选：捕获JS控制台消息"""
        print(f"[JS {level.name}] {sourceID}:{lineNumber} {message}")

class LatexView(QWebEngineView):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # 设置自定义Page（关键步骤）
        self.setPage(NoContextMenuPage(self))
        
        # 加载HTML模板
        self.template = self.load_template()
        
        # 初始化JS禁用脚本
        self.js_disable_script = """
            document.addEventListener('contextmenu', function(e) {
                e.preventDefault();
                e.stopPropagation();
                return false;
            });
            
            // 可选：禁用文本选择
            // document.styleSheets[0].insertRule('* { user-select: none !important; }', 0);
            
            // 监听动态内容变化（针对异步渲染的公式）
            new MutationObserver(function(mutations) {
                mutations.forEach(function(mutation) {
                    if (mutation.addedNodes.length) {
                        mutation.addedNodes.forEach(function(node) {
                            if (node.nodeType === 1) { // ELEMENT_NODE
                                node.addEventListener('contextmenu', function(e) {
                                    e.preventDefault();
                                });
                            }
                        });
                    }
                });
            }).observe(document.body, { childList: true, subtree: true });
        """
        
        # 连接页面加载完成信号
        self.page().loadFinished.connect(self.on_page_loaded)
    
    def load_template(self):
        """加载嵌入式HTML模板"""
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
            <style>
                body { 
                    font-family: Arial;
                    margin: 20px;
                    line-height: 1.6;
                }
            </style>
        </head>
        <body>
            <div id="content"><!-- Content will be inserted here --></div>
            
            <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
            <script src="qrc:/katex/contrib/auto-render.min.js"></script>
            <script>
                function renderContent(content) {
                    document.getElementById('content').innerHTML = content;
                    renderMathInElement(document.body, {
                        delimiters: [
                            {left: '$$', right: '$$', display: true},
                            {left: '$', right: '$', display: false}
                        ],
                        throwOnError: false
                    });
                }
            </script>
        </body>
        </html>
        """
        return html
    
    def on_page_loaded(self, ok):
        """页面加载完成后注入禁用脚本"""
        if ok:
            self.page().runJavaScript(self.js_disable_script)
    
    def contextMenuEvent(self, event: QContextMenuEvent):
        """完全禁用Qt层面的右键菜单"""
        event.ignore()  # 必须调用
    
    def render_latex(self, content):
        """渲染LaTeX内容"""
        # 转义特殊字符
        safe_content = content.replace('\\', '\\\\').replace("'", "\\'")
        
        # 构建完整HTML
        full_html = self.template.replace(
            "<!-- Content will be inserted here -->",
            f"<script>document.addEventListener('DOMContentLoaded', function() {{ renderContent('{safe_content}'); }});</script>"
        )
        
        self.setHtml(full_html, QUrl("qrc:/"))

if __name__ == "__main__":
    import sys
    
    app = QApplication(sys.argv)
    
    # 示例使用
    view = LatexView()
    view.resize(800, 600)
    view.render_latex(
        "行内公式：$E = mc^2$\n\n"
        "块级公式：\n"
        "$$\\int_{a}^{b} x^2 dx$$\n\n"
        "带颜色的公式：\n"
        "$$\\color{blue}{\\sum_{n=1}^\\infty \\frac{1}{n^2}} = \\frac{\\pi^2}{6}$$"
    )
    view.show()
    
    sys.exit(app.exec_())