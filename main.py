#!/usr/bin/python3
import EFrame as eframe
import sys
import logging

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    src_dir = sys.argv[1]
    f = eframe.EFrame(src_dir)

    if len(sys.argv) == 3:
        fileName = sys.argv[2]
        f.try_to_use(fileName)
    else:
        f.do_work()
