from rouge_chinese import Rouge
import jieba
import multiprocessing
from functools import partial

# 初始化操作
jieba.initialize()
rouge = Rouge()

def get_rouge_l_score(new_entry, other_entry):
    new_entry = ' '.join(jieba.cut(new_entry))
    other_entry = ' '.join(jieba.cut(other_entry))
    scores = rouge.get_scores(new_entry, other_entry)
    return scores[0]['rouge-l']['f']

def is_entry_diverse_based_on_rouge(new_entry, entry_pool, thr):
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as p:
        rouge_scores = p.map(
            partial(get_rouge_l_score, new_entry), entry_pool
        )
    
    if max(rouge_scores) > thr:
        return False
    else:
        return True