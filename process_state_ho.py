import json
import argparse
prefix = "<TOKENS_UNUSED_1>"

system_prompt_1 = """你是一个能够理解对话过程，并从中抽取对话意图和对应槽位的助手。我定义了两个字段：'用户输入'和'历史状态', 其中'用户输入'表示用户的输入话术；'历史状态'表示你基于'用户输入'字段抽取出来的意图和槽位结果，并按照固定格式组合。其中'历史状态'字段格式要符合以下要求: 
1. 句法格式为: 意图名称(槽位类型1=槽位值1, 槽位类型2=槽位值2, 槽位类型3=槽位值3, ...)；
2. 句法格式中的意图名称是根据'用户输入'理解生成的具体意图名。槽位类型1、槽位类型2、槽位类型3等，是该意图可能存在的槽位类型，槽位值1、槽位值2、槽位值3等是从原文中抽取出来的符合该槽位类型的具体值，并且该值一定是在'用户输入'字段原文中，如果某个槽位类型没有具体值，则槽位值用None字符表示；
3. 槽位类型不仅仅只有3个，最少可能是0个，也可能是多于3个；
现在我将给你用户当前的'用户输入', 那么基于最新的'用户输入'，你要帮我抽取生成最新的'历史状态'。"""

system_prompt_2 = """你是一个能够理解对话过程，并从中抽取对话意图和对应槽位的助手。我会给你一轮的历史对话内容和抽取结果，分别用'用户输入', '历史状态', '助理答复'这三个字段表示历史信息，其中'用户输入'表示用户的输入话术；'历史状态'表示你基于'用户输入'字段抽取出来的意图和槽位结果，并按照固定格式组合；'助理答复'表示基于'用户输入'和'历史状态'两个字段，展示给用户的回答。其中'历史状态'字段格式要符合以下要求: 
1. 句法格式为: 意图名称(槽位类型1=槽位值1, 槽位类型2=槽位值2, 槽位类型3=槽位值3, ...)；
2. 句法格式中的意图名称是根据'用户输入'理解生成的具体意图名。槽位类型1、槽位类型2、槽位类型3等，是该意图可能存在的槽位类型，槽位值1、槽位值2、槽位值3等是从原文中抽取出来的符合该槽位类型的具体值，并且该值一定是在'用户输入'字段原文中，如果某个槽位类型没有具体值，则槽位值用None字符表示；
3. 槽位类型不仅仅只有3个，最少可能是0个，也可能是多于3个；
现在我将给你一轮的'用户输入', '历史状态', '助理答复'，以及用户当前最新一轮的'用户输入', 那么基于最新的'用户输入'，你要帮我抽取生成最新的'历史状态'。"""

system_prompt_3 = """你是一个能够理解对话过程，并从中抽取对话意图和对应槽位的助手。我会给你两轮的历史对话内容和抽取结果，分别用'用户输入', '历史状态', '助理答复'这三个字段表示历史信息，其中'用户输入'表示用户的输入话术；'历史状态'表示你基于'用户输入'字段抽取出来的意图和槽位结果，并按照固定格式组合；'助理答复'表示基于'用户输入'和'历史状态'两个字段，展示给用户的回答。其中'历史状态'字段格式要符合以下要求: 
1. 句法格式为: 意图名称(槽位类型1=槽位值1, 槽位类型2=槽位值2, 槽位类型3=槽位值3, ...)；
2. 句法格式中的意图名称是根据'用户输入'理解生成的具体意图名。槽位类型1、槽位类型2、槽位类型3等，是该意图可能存在的槽位类型，槽位值1、槽位值2、槽位值3等是从原文中抽取出来的符合该槽位类型的具体值，并且该值一定是在'用户输入'字段原文中，如果某个槽位类型没有具体值，则槽位值用None字符表示；
3. 槽位类型不仅仅只有3个，最少可能是0个，也可能是多于3个；
现在我将给你两轮的'用户输入', '历史状态', '助理答复'，以及用户当前最新一轮的'用户输入', 那么基于最新的'用户输入'，你要帮我抽取生成最新的'历史状态'。"""

suffix = "\n\n<TOKENS_UNUSED_2>\n"

seq="<|im_start|>"
rseq="<|im_end|>"

k2cn={
    'user':'用户输入',
    'state':'历史状态',
    'assistant':'助理答复'
}

def process():
    processed_data = []
    with open(args.file, 'r') as f:
        data = json.load(f)
        for i in data:
            d = i['dialog']
            if len(d) == 1:
                system_prompt = system_prompt_1
            elif len(d) ==2 :
                system_prompt = system_prompt_2
            elif len(d) == 3:
                system_prompt = system_prompt_3
            else:
                continue
                raise ValueError(f"length of dialog is wrong: {d}")
            try:
                entry = prefix + system_prompt + '\n'
                
                for message in d[:-1]:
                    for k, v in message.items():
                        if not v:
                            v = '好的'
                        entry += k2cn[k] + ': ' + v + '\n'
                entry += k2cn['user'] + ': ' + d[-1]['user'] + '\n'
                entry += k2cn['state'] + ': ' + suffix

                if args.test:
                    new_data = {
                    'input': entry,
                    'output': d[-1]['state'],
                    'label': i['label']
                }
                else:
                    new_data = {
                    'input': entry,
                    'output': d[-1]['state']
                }
                processed_data.append(new_data)
            except:
                print(i)
                raise

    with open(args.output_dir, 'w') as f:
        json.dump(processed_data, f, ensure_ascii=False, indent=4)
    print(processed_data[0])
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', default="/home/jovyan/end_mid_control/On-edge-moss2/data/honor/train_0715_trainset.json")
    parser.add_argument('--output_dir', default="/home/jovyan/end_mid_control/On-edge-moss2/data/honor/train_0715_trainset_prefix.json")
    parser.add_argument('--test', default=False)
    args = parser.parse_args()
    
    process()