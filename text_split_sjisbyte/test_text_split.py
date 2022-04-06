#!/usr/bin/env python
# -*- coding: utf-8 -*-

def text_split(txt, split_len, charset='shift_jis'):
    sl   = split_len
    cs   = charset
    head = ''
    tail = ''

    if (len(txt) <= split_len):
        head = txt
        return str(head), str(tail)

    try:
        text_bytes = txt.encode(cs)

        try:
            head = text_bytes[:split_len].decode(cs)
            tail = text_bytes[split_len:].decode(cs)
            return str(head), str(tail)
        except:
            pass

        try:
            head = text_bytes[:split_len-1].decode(cs)
            tail = text_bytes[split_len-1:].decode(cs)
            return str(head), str(tail)
        except:
            pass

    except:
        pass

    sl = int(sl/2)
    head = txt[:sl]
    tail = txt[sl:]
    return str(head), str(tail)



if __name__ == '__main__':

    txt = str('近藤光男')

    head,tail =text_split(txt,2) 
    print(head, tail, )

    head,tail =text_split(txt,3) 
    print(head, tail, )

    head,tail =text_split(txt,10) 
    print(head, tail, )
