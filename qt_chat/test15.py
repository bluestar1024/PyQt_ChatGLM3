import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView  
import mistune
import markdown

# 定义 Markdown 内容
markdown_content = """
# 数学公式示例
 
这是一段包含LaTeX公式的Markdown文本。下面是一个简单的数学公式示例：
 
行内公式：这是一个勾股定理的公式 $$a^2 + b^2 = c^2$$。
 
块级公式：
 
\[
E = mc^2
\]
 
这是爱因斯坦的质能方程，表示能量（E）等于质量（m）乘以光速（c）的平方。

"""

test_text = """\[
E = mc^2
\]"""

# 使用 mistune 将 Markdown 转换为 HTML
#markdown = mistune.create_markdown()

html_content = markdown.markdown(markdown_content, extensions=['extra', 'smarty'])

# 添加 MathJax CDN 链接到 HTML 头部
mathjax_cdn = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Markdown with MathJax</title>
    <script type="text/javascript" async
        src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js">
    </script>
</head>
"""

# 将转换后的 HTML 内容添加到 body 中
full_html_content = f"{mathjax_cdn}<body>\n{html_content}<p>{test_text}</p>\n</body>\n</html>\n"

# 打印生成的 HTML 内容（在实际应用中，你可以将这段 HTML 加载到 QWebEngineView 中）
print(full_html_content)

# 如果要使用 PyQt 显示这段 HTML，可以取消以下代码的注释，并添加必要的设置
app = QApplication(sys.argv)
web_view = QWebEngineView()
web_view.setHtml(str(full_html_content))
web_view.show()
sys.exit(app.exec_())