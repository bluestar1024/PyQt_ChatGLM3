import sys  
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QToolBar, QAction  
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage  
from PyQt5.QtCore import QUrl, Qt
import mistune

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

class CustomWebEngineView(QWebEngineView):  
    """ windows = [] #创建一个容器存储每个窗口，不然会崩溃，因为是createwindow函数里面的临时变量 """
    def __init__(self, parent=None):  
        super().__init__(parent)  

    def createWindow(self, _type):  
        print('createWindow')
        # 创建新的QWebEngineView窗口  
        self.newView = CustomWebEngineView(self)  
        self.newView.setAttribute(Qt.WA_DeleteOnClose)  
        """ self.newView.urlChanged.connect(self.on_url_changed) """
        self.newView.resize(1024, 600)
        """ new_view.show()  # 显示新窗口   """

        newWindow= MainWindow()
        newWindow.setWindowTitle("窗口")  
        newWindow.setCentralWidget(self.newView)
        newWindow.show()
        """ self.windows.append(newWindow) """
        return self.newView  

    """ def on_url_changed(self,url):
        self.newView.setUrl(url) """

class MainWindow(QMainWindow):  
    def __init__(self):  
        super().__init__()  
        self.setWindowTitle("主窗口")  

        # 布局  
        central_widget = QWidget()  
        layout = QVBoxLayout(central_widget)  

        # 创建定制的QWebEngineView  
        self.web_view = CustomWebEngineView(self)  

        layout.addWidget(self.web_view)  
        self.setCentralWidget(central_widget)   

        self.content = markdown_content
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
        # 将转换后的 HTML 内容添加到 body 中
        full_html_content = f"{mathjax_cdn}<body>\n{html_content}\n</body>\n</html>\n"

        self.web_view.setUrl(QUrl("https://www.baidu.com"))
        """ self.web_view.setHtml(str(full_html_content)) """

        self.web_view.resize(800, 600)
        central_widget.resize(800, 600)
        self.resize(800, 600)

if __name__ == "__main__":  
    app = QApplication(sys.argv)  
    window = MainWindow()  
    window.show()  
    sys.exit(app.exec_())
