from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LAParams
from io import StringIO

# 標準組込み関数open()でモード指定をbinaryでFileオブジェクトを取得
fp = open("\\Users\\ksk\\sync\\lab\\research\\2021\\GVA3\\specification\\kyogi_rules(sim)_1.0.1.pdf", 'rb')
textList = []
# PDFファイルから1ページずつ解析(テキスト抽出)処理する
for page in PDFPage.get_pages(fp):
    rmgr = PDFResourceManager()  # PDFResourceManagerオブジェクトの取得
    outfp = StringIO()  # 出力先をPythonコンソールするためにIOストリームを取得
    lprms = LAParams()          # LAParamsオブジェクトの取得
    # TextConverterオブジェクトの取得
    device = TextConverter(rmgr, outfp, laparams=lprms)
    iprtr = PDFPageInterpreter(rmgr, device)  # PDFPageInterpreterオブジェクトの取得
    iprtr.process_page(page)
    text = outfp.getvalue()  # Pythonコンソールへの出力内容を取得
    textList.append(text)

outfp.close()  # I/Oストリームを閉じる
device.close()  # TextConverterオブジェクトの解放
fp.close()  # Fileストリームを閉じる

# print(textList[26])  # Jupyterの出力ボックスに表示する
text = textList[26]
newText = ''
for i in range(len(text)):
    if text[i] != ' ' and text[i] != '.' and text[i] != '⚫' and text[i] != '➢':
        newText += text[i]

print(newText)
