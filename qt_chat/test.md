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
苹果10\\$，梨子20\\$，香蕉30\\$，橘子40\\$。  
$\alpha$ $\beta$ $\gamma$ $\delta$ $\epsilon$ $\zeta$ $\eta$ $\theta$ $\iota$ $\kappa$ $\lambda$ $\mu$ $\nu$ $\xi$ $\omicron$ $\pi$ $\rho$ $\sigma$ $\tau$ $\upsilon$ $\phi$ $\chi$ $\psi$ $\omega$ $\Gamma$ $\Delta$ $\Theta$ $\Lambda$ $\Xi$ $\Pi$ $\Sigma$ $\Upsilon$ $\Phi$ $\Psi$ $\Omega$  
创建脚注格式类似这样 [^RUNOOB]。  
[^RUNOOB]: 菜鸟教程 -- 学的不仅是技术，更是梦想！！！  

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
`printHelloWorld()`函数

    def printHelloWorld():
        print('hello world')

```python
def printHelloWorld():
    print('hello world')
```
******************
### 链接
这是一个链接 [菜鸟教程](https://www.runoob.com)  
这个链接用 1 作为网址变量 [Google][1]  
这个链接用 runoob 作为网址变量 [Runoob][runoob]  
然后在文档的结尾为变量赋值（网址）  

[1]: http://www.google.com/
[runoob]: http://www.runoob.com/
******************
### 图片
![RUNOOB 图标](https://static.jyshare.com/images/runoob-logo.png "RUNOOB")

这个链接用 2 作为网址变量 [RUNOOB][2]  
然后在文档的结尾为变量赋值（网址）  

[2]: https://static.jyshare.com/images/runoob-logo.png

<img src="https://static.jyshare.com/images/runoob-logo.png" width="25%">

******************
### 表格
|  表头  |  表头  |  表头  |
| :----- | -----: | :----: |
| 单元格 | 单元格 | 单元格 |
| 单元格 | 单元格 | 单元格 |
******************
### LaTeX公式：
这是一个行内公式 $E=mc^2$ 的示例。  
行间公式：
$$\sum_{i=1}^n a_i$$
$$\frac{a}{b} = c$$
积分公式：
$$\int_{a}^{b} {f(x)} \, \mathrm{d}x = F(b) - F(a)$$
微分公式：
$$\frac{d}{dx} e^x = e^x$$