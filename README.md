# CQU 时间冲突检查

指定周、星期、时间的范围，检查该时间范围与一批学工号中的上课时间的冲突。

应用场景：用于社团活动时间安排、考试时间安排等需要兼顾一群同学的场景

## 依赖

依赖于 [pymycqu](https://github.com/Hagb/pymycqu)，用以下命令安装
```bash
pip install -r requirements.txt
```

## 使用

用
```bash
python cqu_find_idle_time.py
```
来运行，之后根据提示输入时间范围、登录凭据、学号列表。

注意，其中时间范围的写法中，开头的减号代表整行的范围都用于反选；非开头的减号代表用范围选择，如 `1-5` 代表 1、2、3、4、5 ；逗号表示并列，如 `1-4,7,9-11` 指 1、2、3、4、7、9、10、11。

```
请输入需要使用的周次
> 14

请输入排除或使用的星期，正选直接以数字开头（只使用指定星期），反选以减号开头（排除指定星期），留空全选。
数字 1 表示周一，数字 7 表示周日。例：工作日 1-5 或 -6,7 或 -6-7，周末 6,7 或 6-7
>     

请输入排除或使用的节次，正选直接以数字开头（只使用指定节次），反选以减号开头（排除指定节次），留空全选。
例：-1-2,5,10-12 表示排除早上（1-2）、中午（5）、晚上（10-12）的课，10-12 表示只选择晚上的课，
> -1-2,5

14 周，星期 1,2,3,4,5,6,7，第 3,4,6,7,8,9,10,11,12 节课
统一身份认证号: 2019xxxx
统一身份认证密码: password12345
登陆成功！输入学生学号，一行一个（可直接将 excel 等表格软件中一列学号复制下来）
>>>
2020xxxx
2021xxxx
2021xxxx
2021xxxx
2021xxxx
2021xxxx
2021xxxx
2021xxxx
2021xxxx
2021xxxx
2021xxxx
2021xxxx
2021xxxx
2021xxxx
2021xxxx
2021xxxx
DZ21xxxx

<<<

2020xxxx 获得 22条记录
2021xxxx 获得 36条记录
2021xxxx 获得 46条记录
2021xxxx 获得 32条记录
2021xxxx 获得 32条记录
2021xxxx 获得 33条记录
2021xxxx 获得 28条记录
2021xxxx 获得 28条记录
2021xxxx 获得 28条记录
2021xxxx 获得 33条记录
2021xxxx 获得 28条记录
2021xxxx 获得 29条记录
2021xxxx 获得 30条记录
2021xxxx 获得 28条记录
2021xxxx 获得 27条记录
2021xxxx 获得 29条记录
DZ21xxxx 获得 21条记录
按一次回车输出一次


0 冲突：
14 周星期 2 第 12 节
14 周星期 4 第 8 节
14 周星期 4 第 9 节
14 周星期 7 第 3 节
14 周星期 7 第 4 节
14 周星期 7 第 10 节
14 周星期 7 第 11 节
14 周星期 7 第 12 节


1 冲突：
14 周星期 6 第 9 节
    数字逻辑×1
14 周星期 6 第 10 节
    数字逻辑×1
14 周星期 6 第 11 节
    数字逻辑×1
14 周星期 6 第 12 节
    数字逻辑×1
14 周星期 7 第 6 节
    Java程序开发×1
14 周星期 7 第 7 节
    Java程序开发×1
14 周星期 7 第 8 节
    Java程序开发×1
14 周星期 7 第 9 节
    Java程序开发×1


2 冲突：
14 周星期 5 第 12 节
    Java程序开发×1 大学化学实验Ⅰ×1
14 周星期 6 第 6 节
    数字逻辑×1 大学化学实验Ⅰ×1
14 周星期 6 第 7 节
    数字逻辑×1 大学化学实验Ⅰ×1
14 周星期 6 第 8 节
    数字逻辑×1 大学化学实验Ⅰ×1


5 冲突：
14 周星期 2 第 3 节
    工程原理×1 思想道德与法治×1 工程制图×1 程序设计基础×1 汇编语言程序设计×1
14 周星期 2 第 4 节
    工程原理×1 思想道德与法治×1 工程制图×1 程序设计基础×1 汇编语言程序设计×1
14 周星期 4 第 6 节
    自然与设计×1 文明经典系列B×4
14 周星期 4 第 7 节
    自然与设计×1 文明经典系列B×4
14 周星期 4 第 12 节
    数据结构×1 文明经典系列B×4
14 周星期 5 第 8 节
    数学分析（1）×1 中国近现代史纲要×1 工程制图×3
14 周星期 5 第 9 节
    数学分析（1）×1 中国近现代史纲要×1 工程制图×3
14 周星期 6 第 3 节
    中国共产党简史×1 中国改革开放史×2 社会主义发展史×2
14 周星期 6 第 4 节
    中国共产党简史×1 中国改革开放史×2 社会主义发展史×2

...
```

## TODO

- 代码重构（急忙中写就的代码糟糕透了，捂着鼻子写）
- 对考试时间和选定时间的冲突也纳入检查范围
- 相邻节次合并输出（如 6,7,8 节输出为 6-8）

## 许可

AGPLv3
