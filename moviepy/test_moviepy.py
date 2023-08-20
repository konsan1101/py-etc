#!/usr/bin/env python
# -*- coding: utf-8 -*-

from moviepy.editor import VideoFileClip

def convert_to_gif(video_path, gif_path):
    clip = VideoFileClip(video_path)
    clip.write_gif(gif_path)

if __name__ == '__main__':

    convert_to_gif("input.mp4", "output.gif")

