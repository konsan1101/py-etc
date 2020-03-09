#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd

def pd2fields(pandas_df=None):

        # pandas_df → fields_df
        columns   = ['フィールド', 'タイプ', '最小値', '最大値', '合計値', '最大桁数', '小数桁数', 'サンプル', ]
        fields_df = pd.DataFrame(columns=columns, )

        # フィールド
        for col in pandas_df.columns:
            series = pd.Series([col], index=['フィールド'], )
            fields_df = fields_df.append(series, ignore_index=True, )
        fields_df['最大桁数'] = 0
        fields_df['小数桁数'] = 0

        # タイプ
        df_dtypes = pandas_df.dtypes
        for i in range(len(df_dtypes)):
            フィールド = df_dtypes.index[i]
            タイプ     = df_dtypes.iloc[i]
            row = fields_df[fields_df['フィールド'] == フィールド]
            if (len(row) != 1):
                pass # あり得ない内部エラー
            else:
                # タイプ
                index = row.index[0]
                fields_df.loc[index, 'タイプ'] = str(タイプ)

        # 作業用 df
        work_df = pandas_df.copy()

        # 数値項目　最小、最大、合計、最大桁数、小数桁数
        for f in range(len(fields_df)):
            フィールド = fields_df.loc[f, 'フィールド']
            タイプ     = fields_df.loc[f, 'タイプ']
            if (タイプ[:3] == 'int') \
            or (タイプ[:5] == 'float'):
                work_df = work_df.fillna({フィールド:0})
                最小値 = work_df[フィールド].min()
                最大値 = work_df[フィールド].max()
                合計値 = work_df[フィールド].sum()
                fields_df.loc[f, '最小値'] = 最小値
                fields_df.loc[f, '最大値'] = 最大値
                fields_df.loc[f, '合計値'] = 合計値

                桁数1 = len(str(abs(int(最小値))))
                fields_df.loc[f, '最大桁数'] = 桁数1
                桁数2 = len(str(abs(int(最大値))))
                if (桁数2 > 桁数1):
                    fields_df.loc[f, '最大桁数'] = 桁数2

                小数桁数 = 0
                for i in range(len(work_df)):
                    if (i == 0):
                        fields_df.loc[f, 'サンプル'] = "'" + str(pandas_df.loc[i, フィールド]) + "'"
                    内容値 = abs(work_df.loc[i, フィールド])
                    整数値 = int(内容値)
                    if (内容値 != 整数値):
                        小数値 = 内容値 - 整数値
                        桁数 = len(str(小数値)) - 2  # 0.の2文字
                        if (桁数 > 小数桁数):
                            小数桁数 = 桁数                        
                fields_df.loc[f, '小数桁数'] = 小数桁数

        # 文字項目　最大桁数
        for f in range(len(fields_df)):
            フィールド = fields_df.loc[f, 'フィールド']
            タイプ     = fields_df.loc[f, 'タイプ']
            if  (タイプ[:3] != 'int') \
            and (タイプ[:5] != 'float'):
                work_df = work_df.fillna({フィールド:''})

                最大桁数 = 0
                for i in range(len(work_df)):
                    内容値 = str(work_df.loc[i, フィールド])
                    if (i == 0):
                        fields_df.loc[f, 'サンプル'] = "'" + 内容値 + "'"
                    桁数 = len(内容値)
                    if (桁数 > 最大桁数):
                        最大桁数 = 桁数
                fields_df.loc[f, '最大桁数'] = 最大桁数

        print('')
        print(fields_df)
        print('')

        return fields_df



if __name__ == '__main__':

    excel_file = '工程テスト.xlsx'
    inp_df = pd.read_excel(excel_file, sheet_name=0)

    fields_df = pd2fields(inp_df)

    # 関連マスタ抽出
    関連マスタ項目 = {}
    search_point    = 0
    while (search_point < len(fields_df)):

        # コード探索
        for f in range(search_point, len(fields_df)):
            フィールド = fields_df.loc[f, 'フィールド']
            search_point = f
            if (フィールド[-3:] == 'コード'):
                マスタ = フィールド[:-3]

                # コード追加
                #print(マスタ)
                関連マスタ項目[マスタ] = [フィールド]

                # フィールド追加
                for m in range(search_point + 1, len(fields_df)):
                    マスタ項目 = fields_df.loc[m, 'フィールド']
                    if (search_point == 0) \
                    or (マスタ項目[:len(マスタ)] == マスタ):
                        #print(マスタ名,マスタ項目)
                        関連マスタ項目[マスタ].append(マスタ項目)

            # 続きから探索
            search_point += 1

    # テーブル中のマスタ項目
    for マスタ in 関連マスタ項目.keys():
        マスタ項目 = 関連マスタ項目[マスタ]
        #print(マスタ, マスタ項目)

        out_df = pd.DataFrame(index=[], columns=マスタ項目, )
        for i in range(len(inp_df)):
            コード = inp_df.loc[i, マスタ項目[0]]
            out_df = out_df[out_df[マスタ項目[0]] != コード]
            out_df = out_df.append(inp_df.loc[i, マスタ項目], ignore_index=True, )

        print(out_df)


