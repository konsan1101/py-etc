#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import psutil

# https://srbrnote.work/archives/1641

def main():
    """プロセスの優先度変更テスト"""
    print('start\n')


    # プロセスクラスのインスタンス作成
    p = psutil.Process()


    # 現在の「プロセスID」と「優先度」を表示
    print('PID: %s   優先度: %s\n' % (p.pid, p.nice()))
    os.system('PAUSE')


    # 優先度: 高 (ハイ・プライオリティ)
    p.nice(psutil.HIGH_PRIORITY_CLASS)
    print('PID: %s   優先度: %s\n' % (p.pid, p.nice()))
    os.system('PAUSE')


    # 優先度: 通常以上 (アボーブ・ノーマル・プライオリティ)
    p.nice(psutil.ABOVE_NORMAL_PRIORITY_CLASS)
    print('PID: %s   優先度: %s\n' % (p.pid, p.nice()))
    os.system('PAUSE')


    # 優先度: 通常 (ノーマル・プライオリティ)
    p.nice(psutil.NORMAL_PRIORITY_CLASS)
    print('PID: %s   優先度: %s\n' % (p.pid, p.nice()))
    os.system('PAUSE')


    # 優先度: 通常以下 (ビロウ・ノーマル・プライオリティ)
    p.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    print('PID: %s   優先度: %s\n' % (p.pid, p.nice()))
    os.system('PAUSE')


    # 優先度: 低 (アイドル・プライオリティ)
    p.nice(psutil.IDLE_PRIORITY_CLASS)
    print('PID: %s   優先度: %s\n' % (p.pid, p.nice()))
    os.system('PAUSE')


    del p

    # ここに実行したい処理を書く

    print('end')
    return

if __name__ == '__main__':
    main()


