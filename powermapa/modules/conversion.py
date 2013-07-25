# -*- coding: utf-8 -*-
__author__ = 'Evolutiva'

def convert_latin_chars(alias):
    return alias.replace(' ','_').replace('á','a').replace('é','e').replace('í','i')\
    .replace('ó','o').replace('ú','u').replace('ñ','n').replace('.','-').replace('Á','A')\
    .replace('É','E').replace('Í','I').replace('Ó','O').replace('Ú','U')


