import re
from difflib import SequenceMatcher
from datetime import datetime

def MyGreedySimilarityStrings(X, Y):
    total_similarity = 0
    
    for start_on in range(len(X)):
        similarity_count = 0
        
        str_ret = ""
        
        str_ret += str(start_on) + ","
        # find first similarity on the other str
        found_str_chunk = False
        index_on_str1 = start_on
        index_on_str2 = 0
        last_index_str2_equal = 0
        while not found_str_chunk:
            #print(X[index_on_str1], Y[index_on_str2])
            if index_on_str1 < len(X) and index_on_str2 < len(Y) and X[index_on_str1] == Y[index_on_str2]:
                index_on_str1 += 1
                similarity_count += 1
                
                last_index_str2_equal = index_on_str2
                str_ret = str_ret + str(Y[index_on_str2])
                
            index_on_str2 += 1
            
            if (index_on_str2 >= len(Y)):
                index_on_str2 = last_index_str2_equal + 1
                index_on_str1 += 1
            if (index_on_str1 >= len(X)):
                found_str_chunk = True

        str_ret += "," + str(similarity_count)
        #print(str_ret)
        
        total_similarity = max(total_similarity, similarity_count)
    return total_similarity

def RetError(str1, str2):
    useSequenceMatcher = True
    if useSequenceMatcher:
        s = SequenceMatcher(None, str1, str2)
        return 1 - s.ratio()
    
    a = MyGreedySimilarityStrings(str1, str2)
    return 1 - a / max(len(str1),len(str2))

def IsMatch(worker_id, output_queue, Part_D, RE, startIdx, endIdx):
    out = {}
    out['worker_id'] = worker_id
    out['time'] = datetime.now()
    p = re.compile(RE)
    for i in range(startIdx, endIdx):
        x = p.search(Part_D[i])
        if x:
            out['error'+str(i)] = 0 
        else:
            out['error'+str(i)] = RetError(Part_D[i], RE)
    
    out['deltatime'] = datetime.now() - out['time']
    output_queue.put(out)

def test(name, output):
    output.put('hello {0}'.format(name))
    return