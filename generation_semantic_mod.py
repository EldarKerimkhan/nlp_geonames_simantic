#!/usr/bin/env python
# coding: utf-8

import torch

class GenSearch():

    # функция для генерации подходящего названия
    def gen_sim_mbart(self, city, tokenizer, model, table):
        
        device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
        model.to(device)
        # токенезирует название города
        city_tokens = tokenizer(city, return_tensors="pt", padding=True, truncation=True).to(device)
        # генерируем название города на основе обученных данных
        outputs = model.generate(city_tokens.input_ids)
        # декодируем название города
        output_str = tokenizer.batch_decode(outputs, skip_special_tokens=True, clean_up_tokenization_spaces=True)
        
        # вывод в виде словаря
        if output_str[0] in table['asciiname'].values:
            res_dict = {}
            res_dict['geonameid'] = table.loc[table['asciiname'] == output_str[0], 'geonameid'].values[0]
            res_dict['asciiname'] = output_str[0]
            res_dict['region'] = table.loc[table['asciiname'] == output_str[0], 'region'].values[0]
            res_dict['country'] = table.loc[table['asciiname'] == output_str[0], 'country'].values[0]
        else:
            res_dict = {"error": {output_str[0]}}
    
        return res_dict
