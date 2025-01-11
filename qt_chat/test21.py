import markdown2  

def convert_markdown_to_html(markdown_text):  
    # 转换Markdown到HTML，并使用mathjax进行LaTeX渲染  
    html_output = markdown2.markdown(markdown_text, extras=["fenced-code-blocks", "tables", "mathjax"])  
    return html_output  

# 定义Markdown文本，确保LaTeX公式中的反斜杠不会被删掉  
markdown_text = r"""  
# 指数函数的导数  

在这里，我们展示了指数函数的导数:  

$$\frac{d}{dx} e^x = e^x$$
"""  

# 调用转换函数  
html_output = convert_markdown_to_html(markdown_text)  

# 打印转换后的HTML  
print(html_output) 