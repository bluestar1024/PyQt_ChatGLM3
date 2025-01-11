def to_raw_string(original_string):  
    # 用repr获取字符串的表示形式，并去掉引号  
    return repr(original_string)[1:-1]  

# 示例  
regular_string = "这是一个字符串。\\n这里有两个反斜杠。"  
raw_string = to_raw_string(regular_string)  

print("普通字符串:", regular_string)  
print("模仿原始字符串:", raw_string)