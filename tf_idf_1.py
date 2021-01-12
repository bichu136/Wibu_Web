import pickle
import os
import re
import math
import time
import pandas
class HyperParams:
    pass
class TfIdfIndex():
    def __init__(self):
        self.tf_idf_index, self.docs_length = self.__get_data_train()
    
    def __get_words_from_text(self,text):
    # text = StemSentence(text)
    # stop_words = set(stopwords.words('english'))
        processed_text = self.__preprocess_text(text)

        # xóa stopwords
        words = [
            w for w in processed_text.split()
        ]

        return words
    def __preprocess_text(self,text):
        processed_text = text.lower()
        processed_text = processed_text.replace("’", "'")
        processed_text = processed_text.replace("“", '"')
        processed_text = processed_text.replace("”", '"')
        non_words = re.compile(r"[^A-Za-z']+")
        processed_text = re.sub(non_words, ' ', processed_text)

        return processed_text
    def __n_gram(self,str,n):
        return [str[i:i+n] for i in range(len(str)-(n-1))]
    def __get_token_from_str(self,str):
        processed_str = self.__preprocess_text(str)
        tokens = self.__n_gram(processed_str,5)
        return tokens

    def __build_inverted_index(self,datasets):
        arr = dict()
        for index,row in datasets.iterrows():
            words = self.__get_words_from_text(row['title'])
            for word in words:
                if word not in arr.keys():
                    arr[word] = {'count': 1, 'num_doc': 1, 'index': []}
                    arr[word]['index'].append([row['anime_id'], 1])
                else:
                    arr[word]['count'] += 1
                    if arr[word]['index'][-1][0] == row['anime_id']:
                        arr[word]['index'][-1][1] += 1
                    else:
                        arr[word]['index'].append([row['anime_id'], 1])
                        arr[word]['num_doc'] += 1
        return arr


    def __calc_tf_idf(self,count, num_doc, tf):
        return math.log(tf * (1 + math.log2(count / num_doc)))


    def __convert_tf_idf_arr(self,arr):
        for keys, values in arr.items():
            arr[keys]['index'] = [
                [
                    item[0],
                    self.__calc_tf_idf(values['count'], values['num_doc'], item[1])
                ] for item in values['index']
            ]
        return arr


    def __get_vector_length_of_docs(self,tf_idf_index):
        docs_length = dict()
        for key, values in tf_idf_index.items():
            for value in values['index']:
                if value[0] not in docs_length.keys():
                    docs_length[value[0]] = math.pow(value[1], 2)
                else:
                    docs_length[value[0]] += math.pow(value[1], 2)
        for key in docs_length.keys():
            docs_length[key] = math.sqrt(docs_length[key])
        return docs_length


    def __get_data_train(self):
        try:
            pkl_file = open('inverted.pickle', 'rb')
            tf_idf_index = pickle.load(pkl_file)
            docs_length = pickle.load(pkl_file)
            pkl_file.close()
            # pkl_file = open('index.pickle', 'rb')
            # pkl_file.close()

        except:
            datasets = pandas.read_csv('./processed_data.csv')
            arr = self.__build_inverted_index(datasets)
            tf_idf_index = self.__convert_tf_idf_arr(arr)
            docs_length = self.__get_vector_length_of_docs(tf_idf_index)

            with open('./inverted.pickle', mode='wb') as f:
                pickle.dump(tf_idf_index, f)
                pickle.dump(docs_length, f)
            f.close()

        return tf_idf_index, docs_length


    def __get_relevant_ranking_for_query(self,query, tf_idf_index, docs_length):
        # lấy từ trong query
        
        q_words = self.__get_words_from_text(query)
        # đếm từ
        q_word_with_count = dict()
        for word in q_words:
            if word not in q_word_with_count.keys():
                q_word_with_count[word] = 1
            else:
                q_word_with_count[word] += 1

        # tính tf_idf cho các từ trong query
        tf_idf_for_querry = {
            word: self.__calc_tf_idf(
                tf_idf_index[word]['count'],
                tf_idf_index[word]['num_doc'],
                q_word_with_count[word]
            )
            for word in q_word_with_count.keys()
            if word in tf_idf_index.keys()
        }
        # find q length
        q_length = 0

        # nhân query vô index
        relevant_between_words = {
            word: [[
                item[0],
                item[1] * tf_idf_for_querry[word]
            ] for item in tf_idf_index[word]['index']
            ]
            for word in q_word_with_count.keys()
            if word in tf_idf_index.keys()
        }
        for key, value in tf_idf_for_querry.items():
            q_length += math.pow(value, 2)
        q_length = math.sqrt(q_length)

        # cộng các document có ở trên
        q_score = dict()
        for _, value in relevant_between_words.items():
            for i in value:
                if i[0] not in q_score.keys():
                    q_score[i[0]] = i[1]
                else:
                    q_score[i[0]] += i[1]
        
        for key in q_score.keys():
            q_score[key] = q_score[key] / 1+(docs_length[key] * (q_length + 0.01))

        # a = sorted(q_score.items(), key=lambda item: item[1], reverse=True)

        q_score_linked_with_files = {
            key: value
            for key, value in q_score.items()
        }
        a = sorted(q_score_linked_with_files.items(),
                key=lambda item: item[1], reverse=True)
        x_retrieved = []
        for i in a:
            x_retrieved.append(i[0])
        return a


    # def get_data_ground_truth():
    #     path = os.path.join('input', 'RES')
    #     data = dict()

    #     for file in os.listdir(path):
    #         filename = os.path.join(path, file)
    #         text = get_text_from_file(filename)
    #         text = text.rstrip('\n')
    #         cutLine = text.split('\n')
    #         for index, line in enumerate(cutLine):
    #             # cutTab[1] chua can quan tam toi do chua can dung
    #             cutTab = line.split('\t')
    #             cutSpace = cutTab[0].split(" ")
    #             if cutSpace[0] not in data.keys():
    #                 data[cutSpace[0]] = [cutSpace[1]]
    #             else:
    #                 data[cutSpace[0]].append(cutSpace[1])
    #     return data


    # def get_Average_Precision(x_retrieved, relevant_docs):
    #     # find R_Precision value
    #     R_TH = 20
    #     validation_result = {'R': [], 'P': []}
    #     c = 0
    #     for i in range(len(relevant_docs)):
    #         if x_retrieved[i] in relevant_docs:
    #             c += 1
    #         validation_result['R'].append((c / len(relevant_docs)))
    #         validation_result['P'].append((c / (i + 1)))
    #     return sum(validation_result['P']) / len(validation_result['P'])


# def validation():
    
#     queries = open_queries()
#     list_of_x_retrieved = dict()
#     for key, value in queries.items():
#         list_of_x_retrieved[key] = get_relevant_ranking_for_query(
#             value, tf_idf_index, docs_length)
#     # Bắt đầu đánh giá mô hình.
#     data_ground_truth = get_data_ground_truth()

#     Average_precision_of_all_x_retrieved = \
#         {
#             key: get_Average_Precision(value, data_ground_truth[key])
#             for key, value in list_of_x_retrieved.items()
#         }
#     MAP = 0
#     for key, value in Average_precision_of_all_x_retrieved.items():
#         MAP += value
#     MAP = MAP / len(Average_precision_of_all_x_retrieved)
#     print("MAP:", MAP)

    def Retrieve(self,query):
        return self.__get_relevant_ranking_for_query(query, self.tf_idf_index, self.docs_length)

