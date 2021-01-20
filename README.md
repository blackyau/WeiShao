# WeiShao

# 警告:该项目仅供个人研究所用，微哨打卡信息需保证是账号本人填写，账号本人需对信息内容的真实性和完整性负责。

适用于 [四川轻化工大学](http://www.suse.edu.cn/) 微哨 - 健康打卡

## 快速开始

### 下载安装Python与依赖

下载并安装 Python 3.X https://www.python.org/

安装依赖库 requests ,在 `cmd` 中执行以下命令

```shell
pip install -i https://opentuna.cn/pypi/web/simple requests
```

### 下载源码

https://github.com/blackyau/WeiShao/archive/main.zip

将压缩包中所有文件全部解压出来

### 修改配置文件

按照格式修改配置文件 `userinfo.csv`

> 请使用记事本、Notepad++ 或 Visual Studio Code 编辑 csv 格式文件，不要使用 Excel 进行编辑

csv 格式：

学号,姓名,密码

例如：

```csv
12345678901,张三,123456
12345678902,李四,123456
12345678903,王五,123456
12345678904,孙七,123456
12345678905,周八,123456
12345678906,吴九,123456
```

如果你只填写学号、姓名、密码的话，打卡的信息就是**在校**。如果需要打卡**未在校**的话，请看后面的内容。

### 运行程序

执行代码中的 `运行.bat` 就可以运行程序。

## 未在校

如果需要提交的状态为**未在校**，直接在 `userinfo.csv` 中多加一项，那一项就是你的当前位置。其他选项则会自动选择。如下例，张三同学在成都，而李四同学在学校（因为他没有填写地址信息）。

```csv
12345678901,张三,123456,四川省成都市高新区天环街680号凯丽滨江花园
12345678902,李四,123456
```

## 运行参数

运行时可带参数运行，目前支持指定数据文件，例如数据文件名为 `userinfoall.csv`，那么运行的时候就可以使用以下参数运行。

```
python main.py userinfoall.csv
```

# License

```
This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <https://unlicense.org>
```
