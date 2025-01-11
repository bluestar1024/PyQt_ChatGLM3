import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView  
import mistune
import commonmark
import markdown2

# 定义 Markdown 内容
markdown_content = """
# 一级标题
## 二级标题
这是一个段落，包含一些 *Markdown* 语法。
## LaTeX公式：
这是一个行内公式 $E=mc^2$ 的示例。
质能公式：$E = mc^2$
$$\sum_{i=1}^n a_i$$
$$\\frac{a}{b} = c$$
积分公式：
$$\int_{a}^{b} f(x) \ dx = F(b) - F(a)$$
求导公式：
$$\\frac{d}{dx} e^x = e^x$$
"""

# 使用 mistune 将 Markdown 转换为 HTML
#markdown = mistune.create_markdown(escape=False, renderer='html')
#html_content = markdown(markdown_content)

#html_content = pymarkdown.markdown(markdown_content)

parser = commonmark.Parser()
renderer = commonmark.HtmlRenderer()
ast = parser.parse(markdown_content)
html_content = renderer.render(ast)

#html_content = markdown2.markdown(markdown_content)

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
full_html_content = f"{mathjax_cdn}<body>\n{html_content}\n</body>\n</html>\n"

# 打印生成的 HTML 内容（在实际应用中，你可以将这段 HTML 加载到 QWebEngineView 中）
print(full_html_content)

# 如果要使用 PyQt 显示这段 HTML，可以取消以下代码的注释，并添加必要的设置
app = QApplication(sys.argv)
web_view = QWebEngineView()
web_view.setHtml(str(full_html_content))
web_view.show()
sys.exit(app.exec_())
