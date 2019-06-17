@ECHO OFF

SET PATH=%PATH%;C:\pdf2img\poppler-0.68.0\bin;

pdfinfo.exe  -listenc
PAUSE

python test.py
