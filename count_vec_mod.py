#!/usr/bin/env python
# coding: utf-8

import torch
from sklearn.metrics.pairwise import cosine_similarity

class CountVec():
    
    # Разделяем каждую строку на отдельные слова и векторизуем каждое слово        
    
    def get_cos(self, word_to_compare, table, vectorizer, num=5):
        results = []
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        # Разделяем каждую строку на отдельные слова и векторизуем каждое слово
        for idx in range(len(table['alternatenames'])):
            alternatenames = table['alternatenames'][idx]
            if isinstance(alternatenames, str):  # Проверяем, является ли значение строкой
                city_names_list = alternatenames.split(',')  # Разделение строки на отдельные слова
                cosine_sim_max = 0
                city_max = ''
                for city_name in city_names_list:
                    word_vector = torch.tensor(vectorizer.fit_transform([word_to_compare]).toarray(), 
                                               device=device)
                    city_vector = torch.tensor(vectorizer.transform([city_name]).toarray(), 
                                               device=device)
                    # Вычисление косинусного расстояния на GPU
                    cosine_sim = torch.nn.functional.cosine_similarity(word_vector.float(),
                                                                       city_vector.float(),).item()           

                    if (cosine_sim > 0) and (cosine_sim > cosine_sim_max):
                        cosine_sim_max = cosine_sim
                        city_max = city_name

                res_dict = {}
                res_dict['geonameid'] = table['geonameid'][idx]
                res_dict['asciiname'] = table['asciiname'][idx]
                res_dict['region'] = table['region'][idx]
                res_dict['country'] = table['country'][idx]
                res_dict['cosine_sim'] = cosine_sim_max
                results.append(res_dict) 

        unique_results = [dict(t) for t in {tuple(d.items()) for d in results}]
        sorted_results = sorted(unique_results, key=lambda x: x['cosine_sim'], reverse=True)[:num]
    
        return sorted_results     
