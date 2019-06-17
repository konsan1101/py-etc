from pdf2image import convert_from_path, convert_from_bytes

images = convert_from_path('test.pdf')
images[0].save('test0.png', 'png')
images[1].save('test1.png', 'png')


