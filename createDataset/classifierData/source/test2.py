from pdfminer.high_level import extract_pages
from pdfminer.layout import LAParams, LTTextBox
import collections
import MeCab


def flatten_lttext(l, _type):
    """
    ツリー状になっているイテレータをフラットに返すイテレータ
    返る要素の型を指定
    pdfminerのextract_pagesで使用するのを想定
    要素の型が引数で指定した型を継承したもののみを返す

    Args:
        l:      pdfminerのextract_pages()の戻り値
        _type:  戻したい値の型
    """
    for el in l:
        if isinstance(el, (_type)):
            yield el
        else:
            if isinstance(el, collections.abc.Iterable) and not isinstance(el, (str, bytes)):
                yield from flatten_lttext(el, _type)
            else:
                continue


laparams = LAParams()
input_path = "\\Users\\ksk\\sync\\lab\\research\\2021\\GVA3\\specification\\kyogi_rules(sim)_1.0.1.pdf"
start_page1 = 7
last_page1 = 13
start_page2 = 24
last_page2 = 30
footer = 50
header = 795

# 対象ページを読み、テキスト抽出する。（maxpages：0は全ページ）
text = ''
for page_layout in extract_pages(input_path, maxpages=0, laparams=laparams):    #
    # 抽出するページの選別。extract_pagesの引数では、開始ページだけの指定に対応できないため
    if page_layout.pageid < start_page1:
        continue                   # 指定開始ページより前は飛ばす
    if last_page1 < page_layout.pageid < start_page2:
        continue                   # 指定開始ページより前は飛ばす
    if last_page2 < page_layout.pageid:
        break    # 指定終了ページ以降は中断

    # 要素のイテレータをたどり入れ子の要素を1次元に取り出す。戻るイテレータはLTTextBox型のみ
    # 要素の行の上側y1で降順、行の左側x0で昇順にソートする。
    for element in sorted(flatten_lttext(page_layout, LTTextBox), key=lambda x: (-x.y1, x.x0)):
        if element.y1 < footer:
            continue  # フッター位置の文字は抽出しない
        if element.y0 > header:
            continue  # ヘッダー位置の文字は抽出しない
        text += element.get_text()

sentenceList = []
newText = ''
textList = []
for i in range(len(text)):
    textList.append(text[i])

for i in range(len(textList)):
    if textList[i] == '⚫' or textList[i] == '➢':
        pass
    elif textList[i] == '：' or textList[i] == '（' or textList[i] == '）' or textList[i] == '(' or textList[i] == ')':
        newText += '　'
    elif textList[i] != ' ' and textList[i] != '.':
        newText += textList[i]

NoSymTextList = newText.splitlines()

NoCapTextList = []
for i in range(len(NoSymTextList)):
    if len(NoSymTextList[i]) >= 1 and NoSymTextList[i][0] != '図' and NoSymTextList[i][0] != '表' and NoSymTextList[i][0] != ' ' and len(NoSymTextList[i]) > 10:
        NoCapTextList.append(NoSymTextList[i])

count = 0
while count <= len(NoCapTextList)-2:
    str = NoCapTextList[count]
    if len(NoCapTextList[count]) >= 25 and NoCapTextList[count][-1] != '。':
        while len(NoCapTextList[count]) >= 25 and NoCapTextList[count][-1] != '。' and count <= len(NoCapTextList)-2:
            str += NoCapTextList[count+1]
            count += 1
    count += 1
    sentenceList.append(str)
sentenceList.append(NoCapTextList[len(NoCapTextList)-1])

for i in range(len(sentenceList)):
    print(sentenceList[i])

joshi = "助詞"
jodoshi = "助動詞"
setsuzokushi = "接続詞"
hukushi = "副詞"
dokuten = "記号-句点"
kuten = "記号-読点"
kuhaku = "記号-空白"
textList = []
for i in range(len(sentenceList)):
    str = ''
    m = MeCab.Tagger("-Ochasen")
    nouns = m.parse(sentenceList[i]).splitlines()
    for j in range(len(nouns)-1):
        if kuhaku in nouns[j].split()[0]:
            str += ' '
        elif len(nouns[j].split()) >= 2 and joshi in nouns[j].split()[3] or jodoshi in nouns[j].split()[3] or setsuzokushi in nouns[j].split()[3] or hukushi in nouns[j].split()[3] or kuten in nouns[j].split()[3] or dokuten in nouns[j].split()[3]:
            str += ' '
        else:
            str += ' ' + nouns[j].split()[0]
    textList.append(str)
    print(textList[i])
    print("--------------------------------------------------------------------------------------------")

"""
    for i in range(len(nouns)-1):
    print(nouns[i].split()[0])
    print(nouns[i].split()[-1])
"""
