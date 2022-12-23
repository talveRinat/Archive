#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Rinat Mahmutov'
__version__ = '1.0.0'
import os
try:
    import click
    import pandas
except ImportError:
    os.system('pip install --upgrade pip')
    os.system('pip install click')
    os.system('pip install pandas')

import click
import pandas as pd
import csv
import sys
from pathlib import Path


def calc_mean_cv(column):
    """calculate Mean and Coefficient of variation
    :param column: pd.Serial
    :return: (float|float)
    """
    return column.mean(), column.std() / column.mean() * 100


def python_script(filename):
    """Get csv file
    - calculates the average value and coefficient of variation of the percentage of the population A;
    - calculates the average value and coefficient of variation of the percentage of population B;
    - calculates the average value and coefficient of variation of the percentage of the population of cells
    that are not included in either population A or population B;
    :param filename
    :return pd.Dataframe
    """
    try:
        with open(filename, "r") as csvfile:
            df = pd.read_csv(csvfile, sep=';', encoding="UTF-8")
    except csv.Error as err:
        raise ValueError(err)

    # вычисляет среднее значение и коэффициент вариации процентного содержания популяции А
    A_mean, A_cv = calc_mean_cv(df['SubA'])

    # вычисляет среднее значение и коэффициент вариации процентного содержания популяции В
    B_mean, B_cv = calc_mean_cv(df['SubB'])

    # вычисляет среднее значение и коэффициент вариации процентного содержания популяции C
    df['SubC'] = df['Total'] - df['SubA'] - df['SubB']
    C_mean, C_cv = calc_mean_cv(df['SubC'])

    # создаем таблицу для записи результатов
    data = [[A_mean, A_cv], [B_mean, B_cv], [C_mean, C_cv]]
    final_df = pd.DataFrame(data,
                            columns=['mean', 'coefficient_of_variation'],
                            index=['SubA', 'SubB', 'SubC'])

    return final_df.round(4)


def save(df):
    """save as csv-file"""
    filepath = Path(os.path.join(os.path.dirname(__file__), 'out.csv'))
    filepath.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(filepath)
    print(f'File save in {filepath}')


@click.command()
@click.argument('filename', type=click.Path(exists=True))
def main(filename):
    """Run script
        :param filename
        :return csv file with results
    """
    # открываем файл и проверяем формат и корректность csv-файла
    if filename.split('.')[-1].lower() == 'csv':
        # запускаем скрипт
        print("Start python script...")
        df = python_script(filename)
        print("Script finish")
    else:
        print("File is not in csv format")
        sys.exit()

    # запись в csv
    save(df)


if __name__ == '__main__':
    main()
