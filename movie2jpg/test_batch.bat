
pause

    ffmpeg                          -i test_input.flv -filter:v "fps=fps=1:round=down, showinfo" temp/%04d.jpg
rem ffmpeg -init_hw_device qsv:hw   -i test_input.mp4 -filter:v "fps=fps=1:round=down, showinfo" temp/%04d.jpg
rem ffmpeg -filter_hw_device qsv:hw -i test_input.mp4 -filter:v "fps=fps=1:round=down, showinfo" temp/%04d.jpg

pause

    ffmpeg                          -i test_input.flv -filter:v "select=gt(scene\,0.1), scale=0:0, showinfo" temp/%04d.jpg
rem ffmpeg -init_hw_device qsv:hw   -i test_input.mp4 -filter:v "select=gt(scene\,0.1), scale=0:0, showinfo" temp/%04d.jpg
rem ffmpeg -filter_hw_device qsv:hw -i test_input.mp4 -filter:v "select=gt(scene\,0.1), scale=0:0, showinfo" temp/%04d.jpg

pause

