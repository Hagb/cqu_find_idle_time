from mycqu.auth import login, IncorrectLoginCredentials, NeedCaptcha
from mycqu.mycqu import access_mycqu
from mycqu.course import CourseTimetable, Course
# from mycqu.exam import Exam
from requests import Session
from typing import List, Set, Dict, Iterable, Tuple
from functools import reduce
from itertools import product
from time import sleep


def captcha_callback(image: bytes, image_type: str) -> str:
    with open("captcha.jpg", "wb") as file:
        file.write(image)
    print("输入 captcha.jpg 处的验证码并回车")
    return(input("> "))


CLASSES: Set[int] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12}
WEEKDAYS: Set[int] = {1, 2, 3, 4, 5, 6, 7}


def parse_weekdays_or_classes(string: str, set_: Set[int]) -> Set[int]:
    string = string.strip().replace("，", ",")
    if not string:
        return set_
    inverse: bool = string[0] == "-"
    result: set = set_.copy() if inverse else set()
    if string[0] == "-":
        string = string[1:]
    for i in string.split(","):
        a = i.split("-")
        assert len(a) == 1 or len(a) == 2
        tmp_classes: set = set((int(a[0]),)) \
            if len(a) == 1 else set(range(int(a[0]), int(a[1])+1))
        if inverse:
            result.difference_update(tmp_classes)
        else:
            result.update(tmp_classes)
    return result


def parse_classes(string: str) -> Set[int]:
    return parse_weekdays_or_classes(string, CLASSES)


def parse_weeks(string) -> Set[int]:
    string = string.strip().replace("，", ",")
    assert string
    weeks: set = set()
    for i in string.split(","):
        a = i.split("-")
        assert len(a) == 1 or len(a) == 2
        tmp_classes: set = set((int(a[0]),)) \
            if len(a) == 1 else set(range(int(a[0]), int(a[1])+1))
        weeks.update(tmp_classes)
    return weeks


def parse_weekdays(string) -> Set[int]:
    return parse_weekdays_or_classes(string, WEEKDAYS)


def tuples2set(tuples: Iterable[Tuple[int, int]]) -> Set[int]:
    return reduce(lambda x, y: x.union(y),
                  map(lambda a: set(range(a[0], a[1]+1)),
                      tuples)
                  )


if __name__ == "__main__":
    print("请输入需要使用的周次")
    while(True):
        weeks: Set[int] = parse_weeks(input("> "))
        break
    print()
    print("请输入排除或使用的星期，正选直接以数字开头（只使用指定星期），反选以减号开头（排除指定星期），留空全选。")
    # 在程序中数字 0 表示周一，数字 6 表示周日
    print("数字 1 表示周一，数字 7 表示周日。例：工作日 1-5 或 -6,7 或 -6-7，周末 6,7 或 6-7")
    while(True):
        weekdays: Set[int] = set(
            map(lambda x: x-1, parse_weekdays(input("> "))))
        break
    print()
    print("请输入排除或使用的节次，正选直接以数字开头（只使用指定节次），反选以减号开头（排除指定节次），留空全选。")
    print("例：-1-2,5,10-12 表示排除早上（1-2）、中午（5）、晚上（10-12）的课，10-12 表示只选择晚上的课，")
    while(True):
        classes: Set[int] = parse_classes(input("> "))
        break
    print()
    print(f"{','.join(map(str, weeks))} 周，星期 {','.join(str(d+1) for d in weekdays)}，第 {','.join(map(str, classes))} 节课")
    allclasses: Dict[Tuple[int, int, int], Dict[str, int]] = {
        index: {"": 0} for index in product(weeks, weekdays, classes)
    }

    session = Session()
    while(True):
        try:
            login(session, input("统一身份认证号: "), input("统一身份认证密码: "),
                  captcha_callback=captcha_callback)
            access_mycqu(session)
        except IncorrectLoginCredentials:
            print("用户名或密码错误")
        except NeedCaptcha:
            print("验证码错误")
        else:
            break

    stu_ids: List[int] = []
    print("登陆成功！输入学生学号，一行一个（可直接将 excel 等表格软件中一列学号复制下来）")
    print(">>>")
    while i := input().strip():
        stu_ids.append(i)
    print("<<<")

    print("")
    for stu_id in stu_ids:
        sleep(0.1)
        tts = CourseTimetable.fetch(session, stu_id)
        # exam = Exam.fetch(stu_id)
        # sleep(0.1)
        if not tts:
            print(f"{stu_id} 无记录")
        else:
            print(f"{stu_id} 获得 {len(tts)}条记录")
        for tt in tts:
            course_weeks = tuples2set(tt.weeks).intersection(weeks)
            if tt.whole_week:
                for index in product(course_weeks, weekdays, classes):
                    allclasses[index][tt.course.name] = \
                        allclasses[index].get(tt.course.name, 0) + 1
                    allclasses[index][""] += 1
                continue
            if not tt.day_time:
                continue
            weekday = tt.day_time.weekday
            if weekday not in weekdays:
                continue
            course_classes = tuples2set(
                [tt.day_time.period]).intersection(classes)
            for index in product(course_weeks, (weekday,), course_classes):
                allclasses[index][tt.course.name] = \
                    allclasses[index].get(tt.course.name, 0) + 1
                allclasses[index][""] += 1

    sorted_record = sorted(allclasses.items(), key=lambda x: x[1][""])
    print("按一次回车输出一次")
    old_count = -1
    for index, record in sorted_record:
        if record[""] != old_count:
            print()
            input()
            print(f"{record['']} 冲突：")
            old_count = record[""]
        print(f'{index[0]} 周星期 {index[1]+1} 第 {index[2]} 节')
        if record[""]:
            del record[""]
            string = ' '.join(map(
                lambda x: f"{x[0]}×{x[1]}",
                sorted(record.items(), key=lambda x: x[1])
            ))
            print(" "*4, end = "")
            if len(string) >= 80-4:
                print(string[:76-4], '...')
            else:
                print(string)
