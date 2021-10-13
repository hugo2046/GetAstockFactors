'''
Author: Hugo
Date: 2021-10-08 12:51:17
LastEditTime: 2021-10-13 20:22:55
LastEditors: Please set LastEditors
Description: 获取FactorWar的模型数据
             数据来源 https://www.factorwar.com/data/factor-models/
'''

from bs4 import BeautifulSoup
from collections import defaultdict
from typing import (List, Tuple, Dict, Callable, Union)
import requests
from urllib.parse import quote
import string

import pandas as pd


class Get_FactorWar_Data(object):
    '''
    获取factorWar的因子模型数据
    ------
    输入参数:
        model_name:CAPM模型,
                   Fama-French三因子模型,
                   Carhart四因子模型,
                   French五因子模型,Novy-Marx四因子模型,
                   Hou-Xue-Zhang四因子模型,
                   Stambaugh-Yuan四因子模型,
                   Daniel-Hirshleifer-Sun三因子模型,
                   BetaPlusA股混合四因子模型,
                   全部多因子模型basisportfolios月均收益率

        model_type:模型算法:1.经典算法 2.极简算法
        freq:因子数据频率:1.日频-daily 2.月频-monthly
    '''

    def __init__(self) -> None:

        self.MODEL_NAME_DIC = {
            'CAPM模型': 0,
            'Fama-French三因子模型': 1,
            'Carhart四因子模型': 2,
            'Fama-French五因子模型': 3,
            'Novy-Marx四因子模型': 4,
            'Hou-Xue-Zhang四因子模型': 5,
            'Stambaugh-Yuan四因子模型': 6,
            'Daniel-Hirshleifer-Sun三因子模型': 7,
            'BetaPlusA股混合四因子模型': 8,
            '全部多因子模型basisportfolios月均收益率': 9
        }

        url_model = 'https://www.factorwar.com/data/factor-models/'
        url_index = 'https://www.factorwar.com/data/betaplus-1000-index/'

        soup_model = self._get_soup(url_model)

        self.soup_index = self._get_soup(url_index)

        self.soups_model: List = soup_model.select(
            'div.entry-content > p.has-normal-font-size')[4:]

    @staticmethod
    def _get_soup(url: str) -> BeautifulSoup:
        '''获取网页'''
        response = requests.get(url)

        html_str = response.text
        soup = BeautifulSoup(html_str, "lxml")

        return soup

    def get_betaplus1000(self) -> pd.DataFrame:
        '''获取betaplus指数'''

        e = self.soup_index.select_one(
            '#post-153 > div > div.wp-block-group > div > p:nth-child(3) > a')
        csv_url = e['href']

        return pd.read_csv(csv_url, encoding='gbk', index_col=[0], parse_dates=[0])

    def get_model_data(self, model_name: str, model_type: str, freq: str) -> pd.DataFrame:
        '''
        model_type:模型算法:1.经典算法 2.极简算法
        freq:因子数据频率:1.日频-daily 2.月频-monthly
        '''

        select_model = self.MODEL_NAME_DIC[model_name]

        soups = self.soups_model[select_model]

        self.urls: Dict = self._get_urls(soups)
        url = self.urls[model_name][model_type][freq]

        return pd.read_csv(url)

    @staticmethod
    def _get_urls(children_soup: BeautifulSoup) -> Dict:

        dic: Dict = defaultdict(dict)

        for i, e in enumerate(children_soup.children):

            if i == 0:

                k = e.string
                k = k.string
                k = k.replace(' ', '')

                dic[k] = {
                    '经典算法': {
                        'daily': None,
                        'monthly': None
                    },
                    '极简算法': {
                        'daily': None,
                        'monthly': None
                    }
                }

            elif i == 3:

                dic[k]['经典算法']['daily'] = quote(e['href'],
                                                safe=string.printable)

            elif i == 5:

                dic[k]['经典算法']['monthly'] = quote(e['href'],
                                                  safe=string.printable)

            elif i == 8:

                dic[k]['极简算法']['daily'] = quote(e['href'],
                                                safe=string.printable)

            elif i == 10:

                dic[k]['极简算法']['monthly'] = quote(e['href'],
                                                  safe=string.printable)

        return dic


# if __name__ == '__main__':

#     gfd = Get_FactorWar_Data()

#     ff_model_data: pd.DataFrame = gfd.get_model_data(
#         'Fama-French三因子模型', '经典算法', 'monthly')

#     print(ff_model_data.tail())

#     betaplus1000_index: pd.DataFrame = gfd.get_betaplus1000()

#     print(betaplus1000_index.tail())
