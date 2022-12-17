import sys
from extractTxt import extractTxt

specName = sys.argv[1]  # 仕様書の名前(実行時に指定)
outPath = "\\Users\\ksk\\sync\\lab\\research\\2021\\GVA3\\Source\\createDataset\\loadTxt\\" + \
    sys.argv[2] + "_load.txt"
inputPath = "\\Users\\ksk\\sync\\lab\\research\\2021\\GVA3\\specification\\" + specName
extractTxt = extractTxt(outPath)

if '.pdf' in specName:
    extractTxt.extractPdf(inputPath)
elif '.docx' in specName:
    extractTxt.extractWord(inputPath)
    print("yes")
