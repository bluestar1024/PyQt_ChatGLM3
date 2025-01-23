import sys
import markdown  
import mistune
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTextBrowser  
from PyQt5.QtWebEngineWidgets import QWebEngineView

# 定义 Markdown 内容
markdown_content = """
一级标题
========
二级标题
--------
------------------
# 一级标题
## 二级标题
### 三级标题
这是一个段落，包含一些 *Markdown* 语法。  
*斜体文本*  
_斜体文本_  
**粗体文本**  
__粗体文本__  
***粗斜体文本***  
___粗斜体文本___  
~~删除线文本~~  
<u>带下划线文本</u>  
苹果10$，梨子20$，香蕉30$，橘子40$。  
苹果10\$，梨子20\$，香蕉30\$，橘子40\$。  
创建脚注格式类似这样 [^RUNOOB]。  
[^RUNOOB]: 菜鸟教程 -- 学的不仅是技术，更是梦想！！！  

******************
### 特殊字符

******************
### 无序列表
* 第一项
* 第二项
* 第三项

+ 第一项
+ 第二项
+ 第三项

- 第一项
- 第二项
- 第三项

### 有序列表
1. 第一项
2. 第二项
3. 第三项

### 列表嵌套
1. 第一项
    - 第一项嵌套的第一个元素
    - 第一项嵌套的第二个元素
2. 第二项
    1. 第二项嵌套的第一个元素
    2. 第二项嵌套的第二个元素
******************
### 区块
> 菜鸟教程
> 学的不仅是技术更是梦想

> 最外层
> > 第一层嵌套
> > > 第二层嵌套

> 区块中使用列表
> 1. 第一项
> 2. 第二项
> + 第一项
> + 第二项
> + 第三项

列表中使用区块
* 第一项
    > 菜鸟教程
    > 学的不仅是技术更是梦想
* 第二项
******************
### 代码
`printf()`函数

    def printHelloWorld():
        print('hello world')

```python:
def printHelloWorld():
    print('hello world')
```
******************
### 链接
这是一个链接 [菜鸟教程](https://www.runoob.com)  
这个链接用 1 作为网址变量 [Baidu][1]  
这个链接用 runoob 作为网址变量 [Runoob][runoob]  
然后在文档的结尾为变量赋值（网址）  

[1]: http://www.baidu.com/  
[runoob]: http://www.runoob.com/  
******************
### 图片
![RUNOOB 图标](https://static.jyshare.com/images/runoob-logo.png "RUNOOB")

这个链接用 1 作为网址变量 [RUNOOB][2]  
然后在文档的结尾为变量赋值（网址）  

[2]: https://static.jyshare.com/images/runoob-logo.png

<img src="https://static.jyshare.com/images/runoob-logo.png" width="25%">

******************
### 表格
| 表头1| 表头2|表头3  |  
|:---- |----: | :----:|  
|单元格1  | 单元格2|单元格3  |  
| 单元格4|  单元格5| 单元格6|  
"""

class MyWebEngineView(QWebEngineView):  
    def __init__(self):  
        super(MyWebEngineView, self).__init__()  
        self.setFocus()

    def mousePressEvent(self, event):  
        print("Mouse pressed at: ", event.pos())  
        super(MyWebEngineView, self).mousePressEvent(event) 

class MarkdownViewer(QMainWindow):  
    def __init__(self):  
        super().__init__()  

        self.mainWidget = QWidget()
        self.mainVLayout = QVBoxLayout()
        self.setCentralWidget(self.mainWidget)
        self.mainWidget.setLayout(self.mainVLayout)
        self.text_browser = QTextBrowser()
        self.web_view = MyWebEngineView()
        #self.mainVLayout.addWidget(self.text_browser)
        self.mainVLayout.addWidget(self.web_view)
        self.mainWidget.resize(600, 400)
        self.resize(600, 400)

        tableText, tableItemList, tableAlignList, row, column = self.getTable(markdown_content)
        self.content = markdown_content.replace(tableText, '')

        # 使用 mistune 将 Markdown 转换为 HTML
        markdown = mistune.create_markdown()
        html_content = markdown(self.content)

        # 添加 MathJax CDN 链接到 HTML 头部
        mathjax_cdn = """
        <!DOCTYPE html>
        <html lang="zh">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Markdown with MathJax</title>
            <script type="text/javascript">
                MathJax = {
                    tex: {
                        inlineMath: [["$", "$"], ["\\(", "\\)"]],
                        displayMath: [["$$", "$$"], ["\\[", "\\]"]]
                    },
                    svg: {
                        fontCache: 'global'
                    }
                };
            </script>
            <script type="text/javascript" async
                src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/3.1.2/es5/tex-mml-chtml.js">
            </script>
            <style>  
                table {  
                    width: 50%;  
                    border-collapse: collapse;
                    margin: 10px 0;  
                }  
                th, td {  
                    border: 1px solid #ccc;  
                    padding: 8px;  
                }  
                th {  
                    background-color: #f2f2f2;  
                }
                .left-align { text-align: left; }  
                .center-align { text-align: center; }  
                .right-align { text-align: right; }  
            </style>  
        </head>
        """

        if tableItemList:
            html_content += """
            <table>  
                <thead>  
                    <tr>  
            """  
            # 添加表头  
            for i in range(column):  
                html_content += f"<th class='{self.getAlignmentClass(tableAlignList[i])}'>{tableItemList[i]}</th>"  
            html_content += """  
                    </tr>  
                </thead>  
                <tbody>  
            """  
            # 添加数据行
            for i in range(1, row):  # 共有6个单元格，每行3个  
                html_content += "<tr>"  
                for j in range(column):  
                    html_content += f"<td class='{self.getAlignmentClass(tableAlignList[j])}'>{tableItemList[i * column + j]}</td>"  
                html_content += "</tr>"  
            html_content += """  
                </tbody>  
            </table>  
            """

        # 将转换后的 HTML 内容添加到 body 中
        full_html_content = f"{mathjax_cdn}<body>\n{html_content}\n</body>\n</html>\n"

        # 打印生成的 HTML 内容（在实际应用中，你可以将这段 HTML 加载到 QWebEngineView 中）
        print(full_html_content)

        #self.text_browser.setMarkdown(str(markdown_content))
        #self.text_browser.show()
        self.web_view.setHtml(str(full_html_content))
        self.web_view.show()

    def showText(self, text):
        backslashInFront = False
        i = 0
        while(i < len(text)):
            if text[i] == '\\':
                if text[i + 1] == '$':
                    backslashInFront = True
                else:
                    backslashInFront = False
            elif text[i] == '$':
                if backslashInFront:
                    #渲染文本
                    backslashInFront = False
                else:
                    if text[i + 1] == '$':
                        for j in range(i + 2, len(text)):
                            if text[j] == '$' and text[j + 1] == '$':
                                if '\frac' in text[i + 2 : j]:
                                    latexFormula = text[i + 2 : j].replace('\frac', '\\frac')
                                i = j + 1
                                break
                        #渲染文本
                    else:
                        for j in range(i + 2, len(text)):
                            if text[j] == '$' and text[j + 1] != '$':
                                latexFormula = text[i + 1 : j]
                                i = j
                                break
                        #渲染文本
            else:
                #渲染文本
                return
            i += 1

    def getAlignmentClass(self, format_string):  
        """根据对齐格式返回相应的class名"""  
        if ':-' in format_string and '-:' in format_string:  
            return 'center-align'  # 居中对齐  
        elif ':-' in format_string:
            return 'left-align'   # 左对齐  
        elif '-:' in format_string:  
            return 'right-align'  # 右对齐  
        else:  
            return ''

    def getTable(self, text):
        tableText = ''
        tableItemList = []
        tableItemList1 = []
        tableAlignList = []
        i = 0
        r = 0
        row = 0
        row_full = 0
        column = 0
        while(i < len(text)):
            if text[i] == '|':
                tableText += '|'
                j = i
                k = j + 1
                while(k < len(text)):
                    if text[k] == '|':
                        tableText += text[j + 1 : k] + '|'
                        tableItemList.append(text[j + 1 : k].strip(' '))
                        j = k
                    k += 1
                break
            i += 1
        for tableItem in tableItemList:
            if '\n' in tableItem:
                row_full += 1
            else:
                if row_full == 0:
                    column += 1
                if tableItem == tableItemList[-1]:
                    row_full += 1
        if row_full > 1:
            row = row_full - 1
        else:
            row = row_full
        if row >= 1:
            tableItemList1 = tableItemList1 + tableItemList[0 : column]
        if row_full >= 2:
            tableAlignList = tableItemList[column + 1 : 2 * (column + 1) - 1]
        if row >= 2:
            for r in range(1, row):
                tableItemList1 = tableItemList1 + tableItemList[(r + 1) * (column + 1) : (r + 2) * (column + 1) - 1]
        return tableText, tableItemList1, tableAlignList, row, column

    def showImage(self, text):
        #渲染图片
        return

    def showCode(self, text):
        #渲染代码
        return

    def showList(self, text):
        #渲染列表
        return

    def showLink(self, text):
        #渲染链接
        return

    def showBlockquote(self, text):
        #渲染引用
        return

    def showHorizontalRule(self, text):
        #渲染水平线
        return

if __name__ == '__main__':  
    app = QApplication(sys.argv)  
    viewer = MarkdownViewer()  
    viewer.show()  
    sys.exit(app.exec_())  
