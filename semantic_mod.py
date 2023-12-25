#!/usr/bin/env python
# coding: utf-8

import torch
import numpy as np
from sentence_transformers import util
from scipy.spatial import distance

class SemSearch():

    # функция для нахождения cosine-similarity
    def get_sim(self, city, names, embeddings,
            model, table, top=5):
        
        # если имеется возможность, подключаем gpu
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        model.to(device)
        # рассчитаем расстояние cosine-similarity        
        city_tensor = torch.tensor(model.encode([city])[0]).to(device)  # Convert city to PyTorch tensor
        embeddings_tensor = torch.tensor(embeddings).to(device)  # Convert embeddings to PyTorch tensor
        results = util.semantic_search(city_tensor, embeddings_tensor, top_k=top)
        result = []

        # вывод в виде словаря
        for idx in range(top):
            res_dict = {}
            asciiname_idx = results[0][idx]['corpus_id']
            res_dict['geonameid'] = table.loc[
                table['asciiname'] == names[asciiname_idx], 'geonameid'
                ].values[0]
            res_dict['asciiname'] = names[asciiname_idx]
            res_dict['region'] = table.loc[
                table['asciiname'] == names[asciiname_idx], 'region'
                ].values[0]
            res_dict['country'] = table.loc[
                table['asciiname'] == names[asciiname_idx], 'country'
                ].values[0]
            res_dict['score'] = results[0][idx]['score']
            result.append(res_dict)
        return result

    # функция для нахождения расстояния mahalanobis
    def get_mahalanobis(self, city, names, embeddings,
            model, table, cov_matrix, top=5):

        results = []
       
        for emb in embeddings:
            mahalanobis_dist = distance.mahalanobis(model.encode(city),
                                       emb,
                                       cov_matrix)
            results.append(mahalanobis_dist)

        indices = np.argsort(results)[:top]

        result = []
        for idx in indices:
            res_dict = {}
            asciiname_idx = idx
            res_dict['geonameid'] = table.loc[
                table['asciiname'] == names[asciiname_idx], 'geonameid'
                ].values[0]
            res_dict['asciiname'] = names[asciiname_idx]
            res_dict['region'] = table.loc[
                table['asciiname'] == names[asciiname_idx], 'region'
                ].values[0]
            res_dict['country'] = table.loc[
                table['asciiname'] == names[asciiname_idx], 'country'
                ].values[0]
            res_dict['mahalanobis_distance'] = results[idx]
            result.append(res_dict)
        return result
    
  
    
    
    