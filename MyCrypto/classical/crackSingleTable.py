import os
import random

def generateKey():
    table = [chr(ord('A')+i) for i in range(26)]
    random.shuffle(table)
    return table

def readFile(filepath):
    text = str()
    with open(filepath, 'r', encoding='utf-8') as f:
        context = f.read().lower()
        for c in context:
            if c == ' ' or c.islower():
                text += c
    return text

def singleTable(x, key, method='encrypt'):
    if method == 'encrypt':
        forward = {' ':' '}
        for i in range(26):
            forward[chr(ord('a')+i)] = key[i]
        code = str()
        for c in x:
            code += forward[c]
        return code
    elif method == 'decrypt':
        backward = {' ':' '}
        for i in range(26):
            backward[key[i]] = chr(ord('a')+i)
        code = str()
        for c in x:
            code += backward[c]
        return code
    else:
        return -1

def statistic(text):
    assert text.isupper()
    length = len(text)
    freq = dict()
    letters = [chr(ord('A')+i) for i in range(26)]
    for c in letters:
        freq[c] = 0
    for c in text:
        freq[c] += 1
    prob_stat = list()
    for k, v in freq.items():
        prob_stat.append((k, v/length))
    prob_stat.sort(key=lambda x:x[1], reverse=True)
    return prob_stat

def cracker(code, topK=30):
    prob_stat = statistic(code.replace(' ', ''))
    print(prob_stat)
    prob_table = ['e', 't', 'a', 'o', 'i', 'n', 's', 'h', 'r', 'd', 'l', 'c', 'u', 'm', 'w', 'f', 'g', 'y', 'p', 'b', 'v', 'k', 'j', 'x', 'q', 'z']
    candidates = [[dict(), prob_stat.copy(), 1.0]]
    while len(candidates[0][1]):
        newcandidates = list()
        for current in candidates:
            for i in range(len(current[1])):
                newobj = [current[0].copy(), current[1].copy(), current[2]] # copy
                newobj[2] *= 1 - (newobj[1][i][1] * (newobj[1][0][1] - newobj[1][i][1]))**0.1 # new_prob
                c, _ = newobj[1].pop(i) # new_map
                newobj[0][c] = prob_table[len(current[0])]
                if len(newcandidates) > topK and newobj[2] <= newcandidates[-1][2]:
                    break
                newcandidates.append(newobj)
                newcandidates.sort(key=lambda x:x[2], reverse=True)
            newcandidates = newcandidates[:topK]
        candidates = newcandidates
    for r in candidates:
        print(r)
        text = str()
        for c in code:
            text += r[0][c] if c != ' ' else ' '
        if not os.path.exists('result'):
            os.mkdir('result')
        with open('./result/result{:.6f}.txt'.format(r[2]), 'w', encoding='utf-8') as f:
            f.write(text)

if __name__ == '__main__':
    random.seed(114514)
    key = generateKey()
    text = readFile('story.txt')
    print(text)
    print('length:', len(text))
    print(statistic(text.replace(' ', '').upper()))
    code = singleTable(text, key)
    print(code)
    cracker(code)
