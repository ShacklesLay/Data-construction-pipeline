latex_table = """
GPT-4-turbo & 20.4 & 20.4 & 28.0 & 8.2 & 19.0 & 23.9 & 17.8 & 34.4 & 34.0 & 12.9  & 21.9 \\
Qwen2-72b-Instruct & 28.7 & 19.4 & 29.0 & 20.4 & 43.5 & 17.4 & 31.1 & 30.5 & 58.8 & 25.8  & 30.5 \\
Claude-3.5-sonnet & 21.3 & 16.7 & 23.0 & 12.2 & 29.9 & 23.9 & 24.4 & 37.5 & 50.0 & 23.3  & 26.2 \\
Gemini-1.5-pro & 8.3 & 20.4 & 11.0 & 14.3 & 25.2 & 26.1 & 13.3 & 35.2 & 49.0 & 20.9  & 22.4 \\
Intern2.5-7b-chat & 29.6 & 18.5 & 21.0 & 12.2 & 23.1 & 28.3 & 24.4 & 25.0 & 61.0 & 21.5  & 26.5 \\
Llama3.1-70b-Instruct & 13.9 & 21.3 & 33.0 & 8.8 & 17.0 & 28.3 & 13.3 & 26.6 & 51.0 & 19.0  & 23.2 \\
Internlm2.5-7b-chat & 29.6 & 18.5 & 21.0 & 12.2 & 23.1 & 28.3 & 24.4 & 25.0 & 61.0 & 21.5  & 26.5 \\
Internlm2.5-7b-chat-sft-200 & 14.8 & 21.3 & 28.0 & 12.2 & 21.8 & 8.7 & 4.4 & 25.0 & 56.0 & 14.7  & 20.7 \\
Internlm2.5-7b-chat-sft-500 & 22.2 & 25.9 & 19.0 & 26.5 & 14.3 & 15.2 & 31.1 & 35.2 & 56.0 & 23.3  & 26.9 \\
Llama3-8b-chat & 8.3 & 26.9 & 18.0 & 10.9 & 14.3 & 37.0 & 20.0 & 27.3 & 63.0 & 19.0  & 24.5 \\
Llama3-8b-chat-sft-200 & 31.5 & 25.9 & 32.0 & 20.4 & 1.4 & 19.6 & 37.8 & 5.5 & 39.0 & 19.6  & 23.3 \\
Llama3-8b-chat-sft-500 & 29.6 & 25.9 & 30.0 & 13.6 & 0.7 & 30.4 & 44.4 & 34.4 & 54.0 & 35.0  & 29.8 \\
"""

# 分割行和列
rows = latex_table.strip().replace('\\','').split("\n")
data = [row.split("&") for row in rows]
# 转置数据以便按列处理
columns = list(zip(*data))
# 找到每列的最大值和第二大的值
formatted_columns = [columns[0]]
for col in columns[1:]:
    temp = [(float(x.strip()), x.strip()) for x in col]  # 转换为浮点数并保留原始格式
    temp.sort(reverse=True)  # 降序排序
    max_val = temp[0][1]  # 最大值
    second_max_val = temp[1][1] if len(temp) > 1 else None  # 第二大的值

    # 格式化列
    formatted_col = []
    for value in col:
        stripped_value = value.strip()
        if stripped_value == max_val:
            formatted_col.append(r"\textbf{" + stripped_value + "}")
        elif stripped_value == second_max_val:
            formatted_col.append(r"\underline{" + stripped_value + "}")
        else:
            formatted_col.append(stripped_value)
    formatted_columns.append(formatted_col)

# 转置回来
formatted_data = list(zip(*formatted_columns))

# 重构为 LaTeX 代码
output_latex = "\n".join([" & ".join(row) + r" \\" for row in formatted_data])
print(output_latex)
