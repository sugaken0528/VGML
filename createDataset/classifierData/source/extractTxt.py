from pdfminer.high_level import extract_pages
from pdfminer.layout import LAParams, LTTextBox
import collections
import MeCab
from docx import Document


class extractTxt:
    def __init__(self, outPath):
        self.outPath = outPath

    def extractWord(self, inputPath):
        text = ''
        document = Document(inputPath)
        for i, p in enumerate(document.paragraphs):
            text += p.text + '\n'
        self.textAnalysis(text)

    def extractPdf(self, inputPath):
        laparams = LAParams()
        start_page1 = 7
        last_page1 = 13
        start_page2 = 24
        last_page2 = 30
        footer = 50
        header = 795

        # 対象ページを読み、テキスト抽出する。（maxpages：0は全ページ）
        text = ''
        for page_layout in extract_pages(inputPath, maxpages=0, laparams=laparams):    #
            # 抽出するページの選別。extract_pagesの引数では、開始ページだけの指定に対応できないため
            if page_layout.pageid < start_page1:
                continue                   # 指定開始ページより前は飛ばす
            if last_page1 < page_layout.pageid < start_page2:
                continue                   # 指定開始ページより前は飛ばす
            if last_page2 < page_layout.pageid:
                break    # 指定終了ページ以降は中断

            # 要素のイテレータをたどり入れ子の要素を1次元に取り出す。戻るイテレータはLTTextBox型のみ
            # 要素の行の上側y1で降順、行の左側x0で昇順にソートする。
            for element in sorted(self.flatten_lttext(page_layout, LTTextBox), key=lambda x: (-x.y1, x.x0)):
                if element.y1 < footer:
                    continue  # フッター位置の文字は抽出しない
                if element.y0 > header:
                    continue  # ヘッダー位置の文字は抽出しない
                text += element.get_text()
        self.textAnalysis(text)

    def textAnalysis(self, text):
        sentenceList = []
        newText = ''
        textList = []
        for i in range(len(text)):
            textList.append(text[i])
        replaceDic = ['：', ':', '（', '）',
                      '(', ')', '.', '「', '」', '→', '【', '】', '、', '[', ']', '=','・']
        for i in range(len(textList)):
            if textList[i] == '⚫' or textList[i] == '➢':
                newText += '　'
            elif textList[i] in replaceDic:
                newText += '　'
            elif textList[i] != ' ':
                newText += textList[i]

        NoSymTextList = newText.splitlines()

        NoCapTextList = []
        for i in range(len(NoSymTextList)):
            if len(NoSymTextList[i]) >= 1 and NoSymTextList[i][0] != '図' and NoSymTextList[i][0] != '表' and NoSymTextList[i][0] != '数式' and NoSymTextList[i][0] != ' ':
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

        joshi = "助詞"
        jodoshi = "助動詞"
        setsuzokushi = "接続詞"
        hukushi = "副詞"
        dokuten = "記号-句点"
        kuten = "記号-読点"
        kuhaku = "記号-空白"
        doshi = "動詞"
        kakujoshi = "格助詞"
        rentai = "助詞-連体化"
        meishi = "名詞"

        textList = []
        for i in range(len(sentenceList)):
            str = ''
            m = MeCab.Tagger("-Ochasen")
            nouns = m.parse(sentenceList[i]).splitlines()
            for j in range(len(nouns)-1):
                if kuhaku in nouns[j].split()[0]:
                    str += ' '
                elif len(nouns[j].split()) >= 2 and (kakujoshi in nouns[j].split()[3] and nouns[j].split()[0] != 'と' and nouns[j].split()[0] != 'が' and nouns[j].split()[0] != 'に' and nouns[j].split()[0] != 'へ' and nouns[j].split()[0] != 'を')or rentai in nouns[j].split()[3]:
                    pass
                elif len(nouns[j].split()) >= 2 and joshi in nouns[j].split()[3] or jodoshi in nouns[j].split()[3] or setsuzokushi in nouns[j].split()[3] or hukushi in nouns[j].split()[3] or kuten in nouns[j].split()[3] or dokuten in nouns[j].split()[3]:
                    str += ' '
                elif len(nouns[j].split()) >= 2 and doshi in nouns[j].split()[3] and not meishi in nouns[j].split()[3]:
                    str += '  ' + nouns[j].split()[0] + ' '
                else:
                    str += ' ' + nouns[j].split()[0]
            textList.append(str)

        connectList = []
        for i in range(len(textList)):
            str = ''
            brankCount = 0
            strId = 0
            countId = 0
            while countId < len(textList[i]) and strId != len(textList[i])-1:
                countId += brankCount
                brankCount = 0
                if textList[i][countId] != ' ':
                    str += textList[i][countId]
                    countId += 1
                elif textList[i][countId] == ' ':
                    strId = countId
                    while textList[i][strId] == ' ':
                        if strId < len(textList[i])-1:
                            brankCount += 1
                            strId += 1
                        else:
                            break
                    if brankCount >= 2 and countId != 0:
                        str += ' '
                    elif brankCount == 1:
                        pass
            connectList.append(str)
        for i in range(len(connectList)):
            if len(connectList[i]) != 0 and connectList[i][-1] != ' ':
                connectList[i] += ' '
        for i in range(len(connectList)):
            print(connectList[i])
            print("------------------------------------------------------------")

        f = open(self.outPath, 'w', encoding='UTF-8')
        for i in range(len(connectList)):
            if len(connectList[i]) > 4:
                f.write(connectList[i]+'\n')
        f.close()

        """
            for i in range(len(nouns)-1):
            print(nouns[i].split()[0])
            print(nouns[i].split()[-1])
        """

    def flatten_lttext(self, l, _type):
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
                    yield from self.flatten_lttext(el, _type)
                else:
                    continue
