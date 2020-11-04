# WeiShao

# 警告:该项目仅供个人研究所用，微哨打卡信息需保证是账号本人填写，账号本人需对信息内容的真实性和完整性负责。

适用于 [四川轻化工大学](http://www.suse.edu.cn/) 微哨 - 健康打卡

## 快速开始

下载并安装 Python 3.X https://www.python.org/

安装依赖库 requests

```shell
pip install -i https://opentuna.cn/pypi/web/simple requests
```

csv 格式：

学号,姓名,密码

```csv
12345678901,张三,123456
12345678902,李四,123456
12345678903,王五,123456
12345678904,孙七,123456
12345678905,周八,123456
12345678906,吴九,123456
```

将数据命名为 `userinfo.csv` 放在与 `main.py` 同一目录下，运行 `main.py` 即可。

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
