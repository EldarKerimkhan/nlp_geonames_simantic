#!/usr/bin/env python
# coding: utf-8

from spellchecker import SpellChecker
import random

# Создаем экземпляр SpellChecker
spell = SpellChecker()

class AugTypo():
    # Функция принимает один из 6 языков - 
        # возвращает букву из соответствующего алфавита
    def get_random_letter(self, language_code):
        alphabets = {
            'Russia': 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя',
            'Kazakhstan': ' ғәқңұүһійөһшч',
            'Belarus': 'абвгдежзiйклмнопрстуўфхцчшыьэюя',
            'Armenia': 'աբգդեւզէըթժիլխծկհձղճմյնշոչպջռսվտրցւփ',
            'Kyrgyzstan': 'абдежийклмноптуфхцчшыъэюя',
            'Serbia': 'абвгдђежзијклљмнњопрстћуфхцчџш',
            'Turkey': 'abcçdefgğhıijklmnoöprsştuüvyz'
        }
        
        if language_code in alphabets:
            alphabet = alphabets[language_code]
            return random.choice(alphabet)
        else:
            raise ValueError('Unsupported language code')

    # Функция для создания случайной опечатки в слове
    def add_typo(self, word, country):
        word_length = len(word)
        replace_idx = random.randint(0, word_length - 1)
        typo = word
        while typo == word:
            replace_idx = random.randint(0, word_length - 1)
            typo = word[:replace_idx] + self.get_random_letter(country) + word[replace_idx + 1:]
        return typo
