import json
import argparse
prefix = "<TOKENS_UNUSED_1>"

system_prompt_1 = """You are an assistant capable of understanding dialogue processes and extracting dialogue intents and corresponding slots from them. I have defined two fields: 'User' and 'State'. 'User' represents the user's input speech; 'State' refers to the intent and slot results extracted by you based on the 'User' field, organized in a fixed format. The format of the 'State' field must meet the following requirements:
1. The syntax is: Intent Name(Slot Type1=Slot Value1, Slot Type2=Slot Value2, Slot Type3=Slot Value3, ...);
2. In this syntax, the Intent Name is derived from the 'User' to represent the specific intent generated. Slot Type1, Slot Type2, Slot Type3, etc., are the potential slot types for that intent, and Slot Value1, Slot Value2, Slot Value3, etc., are specific values extracted from the text that match the slot type and must be present in the 'User' text. If a slot type has no specific value, 'None' is used to represent it;
3. The number of slot types can vary, with at least zero and potentially more than three.
Now I will give you the current 'User', and based on the latest 'User', you need to help me generate the newest 'State'."""

system_prompt_2 = """You are an assistant capable of understanding the dialogue process and extracting dialogue intents and corresponding slots from it. I will provide you with a round of historical dialogue content and extraction results, represented by the fields 'User', 'State', and 'Assistant'. 'User' represents the user's input speech; 'State' indicates the intent and slot results you have extracted based on 'User', organized in a fixed format; 'Assistant' represents the answer shown to the user based on 'User' and 'State'. The format of the 'State' field must meet the following requirements:
1. The syntax is: Intent Name(Slot Type1=Slot Value1, Slot Type2=Slot Value2, Slot Type3=Slot Value3, ...);
2. The Intent Name in this syntax is derived from the 'User' to represent the specific intent generated. Slot Type1, Slot Type2, Slot Type3, etc., are the possible slot types for that intent, and Slot Value1, Slot Value2, Slot Value3, etc., are specific values extracted from the text that match the slot type and must be present in the 'User' text. If a slot type has no specific value, 'None' is used to represent it;
3. There can be as few as zero or more than three slot types.
Now I will give you a round of 'User', 'State', 'Assistant', and the user's current latest 'User'. Based on the latest 'User', you need to help me generate the newest 'State'."""

system_prompt_3 = """You are an assistant capable of understanding the dialogue process and extracting dialogue intents and corresponding slots from it. I will provide you with two rounds of historical dialogue content and extraction results, represented by the fields 'User', 'State', and 'Assistant'. 'User' represents the user's input speech; 'State' indicates the intent and slot results you have extracted based on 'User', organized in a fixed format; 'Assistant' represents the answer shown to the user based on 'User' and 'State'. The format of the 'State' field must meet the following requirements:
1. The syntax is: Intent Name(Slot Type1=Slot Value1, Slot Type2=Slot Value2, Slot Type3=Slot Value3, ...);
2. The Intent Name in this syntax is derived from the 'User' to represent the specific intent generated. Slot Type1, Slot Type2, Slot Type3, etc., are the possible slot types for that intent, and Slot Value1, Slot Value2, Slot Value3, etc., are specific values extracted from the text that match the slot type and must be present in the 'User' text. If a slot type has no specific value, 'None' is used to represent it;
3. There can be as few as zero or more than three slot types.
Now I will give you two rounds of 'User', 'State', 'Assistant', and the user's current latest 'User'. Based on the latest 'User', you need to help me generate the newest 'State'."""

suffix = "\n\n<TOKENS_UNUSED_2>\n"

seq="<|im_start|>"
rseq="<|im_end|>"

k2cn={
    'user':'User',
    'state':'State',
    'assistant':'Assistant'
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
                            v = ''
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