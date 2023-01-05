#!/usr/bin/env python
# -*- coding: utf-8 -*-



import torch



if __name__ == '__main__':

    print('torch version        =', torch.__version__)
    print('torch cuda available =', torch.cuda.is_available())

    torch.cuda.is_available = lambda: False

    print('torch cuda available =', torch.cuda.is_available())


