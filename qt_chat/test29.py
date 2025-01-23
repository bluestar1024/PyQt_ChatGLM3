from flask import Flask  

app = Flask(__name__)  

@app.route('/')  
def home():  
    # 给定的数据  
    data = ['表头1', '表头2', '表头3', '单元格1', '单元格2', '单元格3', '单元格4', '单元格5', '单元格6']  
    
    # 将HTML内容作为多行字符串  
    html_content = f"""  
    <!DOCTYPE html>  
    <html lang="zh">  
    <head>  
        <meta charset="UTF-8">  
        <meta name="viewport" content="width=device-width, initial-scale=1.0">  
        <title>表格示例</title>  
        <style>  
            table {{  
                width: 50%;  
                border-collapse: collapse;  
                margin: 20px 0;  
            }}  
            th, td {{  
                border: 1px solid #ccc;  
                padding: 8px;  
                text-align: left;  
            }}  
            th {{  
                background-color: #f2f2f2;  
            }}  
        </style>  
    </head>  
    <body>  
        <h1>用户信息表格</h1>  
        <table>  
            <thead>  
                <tr>  
    """  
    
    # 添加表头  
    for header in data[:3]:  # 假设前3个元素为表头  
        html_content += f"<th>{header}</th>"  
    
    html_content += """  
                </tr>  
            </thead>  
            <tbody>  
    """  
    
    # 添加数据行：每行3个单元格  
    for i in range(3):  # 共有6个单元格，每行3个  
        html_content += "<tr>"  
        for j in range(3):  # 为了保证每行包含3个单元格  
            html_content += f"<td>{data[i * 3 + j + 3]}</td>"  
        html_content += "</tr>"  
    
    html_content += """  
            </tbody>  
        </table>  
    </body>  
    </html>  
    """  

    return html_content  

if __name__ == '__main__':  
    app.run(debug=True)