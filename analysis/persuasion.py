import pandas as pd

def Merge(dict1, dict2):
    dict1.update(dict2)
    dict3 = dict1
    return dict3

def gen_unigrams(corpus):
    unigrams_list = []
    for sent in corpus:
        for e in sent:
            unigrams_list.append(e)
    return unigrams_list

def bigram(l):
    bigram = []
    limit = len(l)-1
    for i, e in enumerate(l):
        if i < limit:
            bigram.append((l[i], l[i+1]))
    return bigram

def gen_bigrams(corpus):
    bigrams_list = []
    for sent in corpus:
        bigrams_list += bigram(sent)
    return bigrams_list

def trigram(l):
    trigram = []
    limit = len(l) - 2
    for i, e in enumerate(l):
        if i < limit:
            trigram.append((l[i], l[i+1], l[i+2]))
    return trigram

def gen_trigrams(corpus):
    trigrams_list = []
    for sent in corpus:
        trigrams_list += trigram(sent)
    return trigrams_list

def gen_n_grams(corpus, n=1):
    if i == 1:
        n_grams = gen_unigrams(corpus)
    elif i == 2:
        n_grams = gen_bigrams(corpus)
    elif i == 3:
        n_grams = gen_trigrams(corpus)
    else:
        n_grams = []  
    return n_grams

def n_gram_count(n_gram_list):
    count = {}
    for key in n_gram_list:
        if key not in count:
            count[key] = 1
        else:
            count[key] += 1 
    return count

def unigram_df(corpora):
    import pandas as pd
    unigram_set = []
    u_df_list = []
    
    p = gen_unigrams(corpora[0])
    n = gen_unigrams(corpora[1])
    unigram_set = sorted(set(p+n))

    pos = n_gram_count(p)
    neg = n_gram_count(n)
    
    for u in unigram_set:
        if u not in pos:
            pos_freq = 0
        else:
            pos_freq = pos[u]

        if u not in neg:
            ng_freq = 0
        else:
            neg_freq = neg[u]
        
        u_df_list.append({'N-Gram': u, 'Pos-Frequency': pos_freq, 'Neg-Frequency': neg_freq})

    return pd.DataFrame(u_df_list)

def bigram_df(corpora):
    import pandas as pd
    bigram_set = []
    b_df_list = []
    p = gen_bigrams(corpora[0])
    n = gen_bigrams(corpora[1])
    bigram_set = sorted(set(p+n))

    pos = n_gram_count(p)
    neg = n_gram_count(n)
    
    for b in bigram_set:
        if b not in pos:
            pos_freq = 0
        else:
            pos_freq = pos[b]

        if b not in neg:
            ng_freq = 0
        else:
            neg_freq = neg[b]
        
        b_df_list.append({'N-Gram': b, 'Pos-Frequency': pos_freq, 'Neg-Frequency': neg_freq})

    return pd.DataFrame(b_df_list)

def trigram_df(corpora):

    import pandas as pd

    trigram_set = []
    t_df_list = []

    p = gen_trigrams(corpora[0])
    n = gen_trigrams(corpora[1])

    trigram_set = sorted(set(p+n))

    pos = n_gram_count(p)
    neg = n_gram_count(n)
    
    for t in trigram_set:
        if t not in pos:
            pos_freq = 0
        else:
            pos_freq = pos[t]

        if t not in neg:
            ng_freq = 0
        else:
            neg_freq = neg[t]
        
        t_df_list.append({'N-Gram': t, 'Pos-Frequency': pos_freq, 'Neg-Frequency': neg_freq})

    return pd.DataFrame(t_df_list)

def n_gram_freq_df(corpora, n=1):
    if n == 1:
        df = unigram_df(corpora)
    elif n == 2:
        df = bigram_df(corpora)
    elif n == 3:
        df = trigram_df(corpora)
    else:
        df = []
    return df

def export_top_5(df, overlap=False, tail=False):

    # p_df is the positive n-gram dataframe
    # n_df is the negative n-gram dataframe
    # overlap is a bollean variable used to distinct between top 5 based solely on freq
    # or based on top 5 where pos and neg do not have the same
    # dir determines if it is the top 5 highest freq or the bottom 5 lowest freq

    p_df = df.sort_values('Pos-Frequency', ascending=tail)
    n_df = df.sort_values('Neg-Frequency', ascending=tail)
    
    p_list = [(row[1], row[2], row[3]) for row in p_df.itertuples()]
    n_list = [(row[1], row[2], row[3]) for row in n_df.itertuples()]
    
    count = 0
       
    for i, n in enumerate(p_list):
        p = p_list[i][0]; n = n_list[i][0]
        if overlap:
            p = p_list[i]; n = n_list[i]
            output = f'''N-Gram Number: {count+1:<3} 
Top Successful N-Gram: {str(p[0]):<52} Percentage of use: {p[1]/(p[1]+p[2])*100}%  
Top Unsuccessful N-Gram: {str(n[0]):<50} Percentage of use: {n[2]/(n[1]+n[2])*100}%'''   
            print(output + '\n')
            if count == 4:
                break
            count+=1
            
        else:     
            if p == n:
                continue 
            p = p_list[i]; n = n_list[i]
            output = f'''N-Gram Number: {count+1:<3} 
Top Successful N-Gram: {str(p[0]):<52} Percentage of use: {p[1]/(p[1]+p[2])*100}%  
Top Unsuccessful N-Gram: {str(n[0]):<50} Percentage of use: {n[2]/(n[1]+n[2])*100}%'''   
            print(output + '\n')
            if count == 4:
                break
            count+=1
            