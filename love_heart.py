import os

def clear_screen():
    """Clears the console screen."""
    os.system("cls")

def rename_file(old_name, new_name):
    """Renames a file and handles potential errors."""
    try:
        os.rename(old_name, new_name)
        print(f"[提示] 已重命名文件至 {new_name}")
    except FileNotFoundError:
        print(f"[错误] 文件不存在: {old_name}")
    except PermissionError:
        print(f"[错误] 无法重命名文件，权限不足: {old_name}")
    except Exception as e:
        print(f"[错误] 未知错误: {e}")

def create_default_config():
    """Creates a default configuration file if it doesn't exist."""
    config_content = ['\\\\\t\t\t\t使用说明\n', '\\\\\t"\\\\"开始为注释\n', '\\\\\t"."开始为直接输出，最后一个"."为读取输入\n', '\\\\\t输入"$"前的内容进行操作，操作"$"后的文件\n', '\\\\\t"$"后的文件下一行以"^"开头表示同时操作的文件\n', '\\\\\t"+"可以设置目录前缀，如果"+"后为空那么清空前缀\n', '\\\\\n', '\\\\\t所有闪退均为bug\n', '\\\\\t如发现请在https://pd.qq.com/s/1d83nni17\n', '\\\\\t@指令小蛇_Cbscfe\n', '\\\\\t程序出现问题如修改配置文件需一并发送\n', '\\\\\n', '\\\\\t做GUI之前永远Beta!!!\n', '\\\\\t\t\t\t\t\t----(一个一个不会用tkinter的人)\n', '\n', '+assets\\minecraft\\models\\item\\\n', '1$mace.json\n', '\n', '+assets\\minecraft\\blockstates\\\n', '2$podzol.json\n', '^dirt_path.json\n', '^grass_block.json\n', '^mycelium.json\n', '\n', '+assets\\minecraft\\blockstates\\\n', '3$dead_bush.json\n', '+assets\\minecraft\\models\\block\\\n', '^dead_bush1.json\n', '^dead_bush2.json\n', '^dead_bush3.json\n', '\n', '.禁用助手 Beta 2.1.3 - LIB临时工作室出品\n', '.---------------------------------\n', '.使用方法\n', '.- 输入功能前面的数字然后按回车\n', '.---------------------------------\n', '.功能列表:\n', '.1\t开关重锤\n', '.2\t开关泥土类\n', '.3\t开关枯木白骨\n', '.---------------------------------\n', '.选择功能:']
    try:
        with open("禁用助手配置文件.txt", "x", encoding="utf-8") as f:
            f.writelines(config_content)
    except FileExistsError:
        pass

def parse_config():
    """Parses the configuration file into a dictionary and a display list."""
    with open("禁用助手配置文件.txt", "r", encoding="utf-8") as f:
        raw_data = f.readlines()

    display_data = []
    file_data = {}
    current_key = None
    file_prefix = ""

    for line_num, line in enumerate(raw_data, start=1):
        line = line.strip()
        if not line or line.startswith("\\"):
            continue  # Skip empty or comment lines
        if line.startswith("."):
            display_data.append(line[1:] + "\n")
        elif line.startswith("+"):
            file_prefix = line[1:].strip()
        elif "$" in line:
            try:
                key, file = line.split("$", 1)
                key = key.strip()
                file = file_prefix + file.strip()
                if key not in file_data:
                    file_data[key] = []
                file_data[key].append(file)
                current_key = key
            except ValueError:
                raise ValueError(f"[错误] 配置文件第{line_num}行格式错误: {line}")
        elif line.startswith("^"):
            if not current_key:
                raise ValueError(f"[错误] 配置文件第{line_num}行没有主键用于关联: {line}")
            file = file_prefix + line[1:].strip()
            file_data[current_key].append(file)
        else:
            raise ValueError(f"[错误] 配置文件第{line_num}行无法识别: {line}")

    return display_data, file_data

def main():
    """Main function to drive the program."""
    create_default_config()
    try:
        display_data, file_data = parse_config()
    except Exception as e:
        input(f"{e}")
        exit()

    input_prompt = display_data.pop(-1)[:-1]

    while True:
        clear_screen()
        for line in display_data:
            print(line, end="")
        user_input = input(input_prompt)
        enabled_files_cnt = 0
        disabled_files_cnt = 0

        if user_input in file_data:
            for file in file_data[user_input]:
                if os.path.exists(file):
                    rename_file(file, file + ".disabled")        
                    disabled_files_cnt += 1
                elif os.path.exists(file + ".disabled"):
                    rename_file(file + ".disabled", file)
                    enabled_files_cnt += 1
                else:
                    print(f"[错误] 文件不存在: {file}")
            input(f"[提示] 操作完成，启用了{enabled_files_cnt}个文件，禁用了{disabled_files_cnt}个文件。按回车继续...")
        else:
            input("[提示] 无效输入，请重试...")

if __name__ == "__main__":
    main()
