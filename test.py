import os
import shutil

def move_and_rename_txt_files(source_dir, target_dir):
    # 创建目标目录（如果不存在）
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    # 遍历源目录及其子目录
    for dirpath, _, filenames in os.walk(source_dir):
        for filename in filenames:
            if filename.endswith('.txt'):
                # # 提取新的文件名
                # base_name = filename.split('-')[0] if '-' in filename else filename.split('_')[0]
                # base_name = base_name.strip()
                # new_filename = f"{base_name}.txt"  # 追加后缀
                new_filename = filename.replace('.txt', '')
                new_filename += '.txt'

                # 构建完整的源文件路径和目标文件路径
                source_file = os.path.join(dirpath, filename)
                target_file = os.path.join(target_dir, new_filename)

                # 移动并重命名文件
                shutil.move(source_file, target_file)
                print(f'Moved: {source_file} to {target_file}')

# 示例使用
source_directory = "C:\\Users\\shackleslay\\Downloads\\DetectiveNovels"  # 替换为你的源目录路径
target_directory = "C:\\Users\\shackleslay\\Downloads\\DetectiveNovels\\txt_files_nospace"  # 替换为你的目标目录路径
move_and_rename_txt_files(source_directory, target_directory)
