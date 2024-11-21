import os

def clear_screen():
    os.system("cls")

def rename_file(old_name, new_name):
    try:
        os.rename(old_name, new_name)
        print(f"[提示] 已重命名文件至 {new_name}")
    except FileNotFoundError:
        print(f"[错误] 文件不存在: {old_name}")
    except PermissionError:
        print(f"[错误] 无法重命名文件，权限不足: {old_name}")
    except Exception as e:
        print(f"[错误] 未知错误: {e}")

# Read or create the configuration file
try:
    with open("禁用助手配置文件.txt", "x", encoding="utf-8") as f:
        f.writelines(['\\\\\t\t    使用说明\n', '\\\\\n', '\\\\\t"\\\\"开始为注释(为啥配置文件要注释?)\n', '\\\\\t"."开始为直接输出，最后一个"."为读取输入\n', '\\\\\t类似"input$file"的内容为声明操作\n', '\\\\\t当输入"$"前面的内容时操作"$"后面的文件\n', '\\\\\t"$"的内容下面的"^"为同时操作的文件\n', '\\\\\t\t哦对了, 还有op~~~\n', '\n', '\n', '.禁用助手 Beta 2.1.2 - LIB临时工作室出品\n', '.---------------------------------\n', '.使用方法\n', '.- 输入功能前面的数字然后按回车\n', '.---------------------------------\n', '.功能列表:\n', '.1\t开关重锤\n', '1$assets\\minecraft\\models\\item\\mace.json\n', '\n', '.2\t开关泥土类\n', '2$assets\\minecraft\\blockstates\\podzol.json\n', '^assets\\minecraft\\blockstates\\dirt_path.json\n', '^assets\\minecraft\\blockstates\\grass_block.json\n', '^assets\\minecraft\\blockstates\\mycelium.json\n', '\n', '.3\t开关枯木白骨\n', '3$assets\\minecraft\\blockstates\\dead_bush.json\n', '^assets\\minecraft\\models\\block\\dead_bush1.json\n', '^assets\\minecraft\\models\\block\\dead_bush2.json\n', '^assets\\minecraft\\models\\block\\dead_bush3.json\n', '.---------------------------------\n', '.选择功能:'])
except FileExistsError:
    pass

# Read the configuration file
with open("禁用助手配置文件.txt", "r", encoding="utf-8") as f:
    rawdata = f.readlines()

clear_screen()

input_prompt = ""
last_key_add = "\n"
display_data = []
file_data = {}

# Process configuration file
for line in range(len(rawdata)):
    if rawdata[line][0] == ".":
        display = rawdata[line][1:]
        display_data.append(display)
    elif "^" in rawdata[line][0]:
        file = rawdata[line].split("^")[-1][:-1]
        if last_key_add == "\n":
            input(f"[错误] 配置文件第{line + 1}行错误, 错误的内容\n\n{rawdata[line]}\n文件内容: {rawdata}\n显示内容: {display_data}\n文件数据: {file_data}\n\n识别的内容:\n^{file}\n\n尝试删除配置文件可能会解决此问题")
            exit()
        file_data[last_key_add].append(file)
    elif rawdata[line][:1] == "\\" or rawdata[line][:1] == "\n":
        pass
    elif "$" in rawdata[line]:
        get_input = rawdata[line].split("$")[0]
        file = rawdata[line].split("$")[-1][:-1]
        if f"{get_input}${file}\n" != rawdata[line]:
            input(f"[错误] 配置文件第{line + 1}行错误, 错误的内容\n\n{rawdata[line]}\n文件内容: {rawdata}\n显示内容: {display_data}\n文件数据: {file_data}\n\n识别的内容: {get_input}${file}\n\n尝试删除配置文件可能会解决此问题")
            exit()
        else:
            if get_input not in file_data:
                file_data[get_input] = []
            file_data[get_input].append(file)
            last_key_add = get_input
    else:
        input(f"[错误] 配置文件第{line + 1}行无法识别, 错误的内容\n\n{rawdata[line]}\n文件内容: {rawdata}\n显示内容: {display_data}\n文件数据: {file_data}\n\n尝试删除配置文件可能会解决此问题")
        exit()

# Set prompt for user input
input_prompt = display_data.pop(-1)[:]

# Main loop to process user input
while True:
    for dis in display_data:
        print(dis, end="")
    inp = input(input_prompt)

    if inp in file_data:
        for file in file_data[inp]:
            if os.path.exists(file):
                rename_file(file, file + ".disabled")
            elif os.path.exists(file + ".disabled"):
                rename_file(file + ".disabled", file)
            else:
                print(f"[错误] 文件不存在{file}")
        input()
        clear_screen()
    else:
        input("无效输入，请重新选择功能。")
        clear_screen()
