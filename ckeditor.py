import os, shutil
from PyQt5 import QtGui, QtCore, QtWebKit, QtWebKitWidgets, QtWidgets

class jsObject(QtCore.QObject):
    filePath = ''
    def __init__(self):
        QtCore.QObject.__init__(self)
        self.editorHtml = ''

    @QtCore.pyqtSlot(str)
    def getHtml(self, text):
        self.editorHtml = text

    def insertHtml(self):
        return self.editorHtml

    html = QtCore.pyqtProperty(str, fget=insertHtml)

class WebPage(QtWebKitWidgets.QWebPage):
    def __init__(self, parent=None):
        QtWebKitWidgets.QWebPage.__init__(self, parent)

    def javaScriptConsoleMessage(self, msg, line, source):
        print('JS ERROR: %s line %d: %s' % (source, line, msg))

class WebView(QtWebKitWidgets.QWebView):
    def __init__(self, parent=None):
        QtWebKitWidgets.QWebView.__init__(self, parent)

        self.parent = parent
        web_page = WebPage(self)
        self.disableDrop = 0

        web_page.setLinkDelegationPolicy(QtWebKitWidgets.QWebPage.DelegateAllLinks)

        self.setPage(web_page)
        self.page().mainFrame().javaScriptWindowObjectCleared.connect(self.addjsObject)
        self.linkClicked.connect(self.urlClicked)

        self.editorJS = jsObject()
        self.page().mainFrame().addToJavaScriptWindowObject('pythonjs', self.editorJS)

    def urlClicked(self,url):
        self.parent.urlClicked(url)

    def addjsObject(self):
        self.editorJS = jsObject()
        self.page().mainFrame().addToJavaScriptWindowObject('pythonjs', self.editorJS)

    def addEditor(self,ckeditorPath,editor='editor1',**kargs):
        headHtml = """
            <html>
              <head>
                <script type="text/javascript" src=\""""+ ckeditorPath +"""\"></script>
              </head>
              <body>
                <form >
                  <textarea id=\""""+ editor +"""\" name=\""""+ editor +"""\"></textarea>
                </form>
                <script type="text/javascript">
                  CKEDITOR.replace( '"""+ editor +"""');
                </script>
              </body>
            </html>
            """

        baseurl = QtCore.QUrl("file:///") if 'baseurl' not in kargs else kargs['baseurl']

        self.setHtml(headHtml,baseurl)
        QtWidgets.QApplication.processEvents()

        ckEditorHtml = """
        CKEDITOR.on('instanceReady', function(ev) {
            var editor = ev.editor;
            editor.execCommand('maximize');
        });
        """
        self.page().mainFrame().evaluateJavaScript(ckEditorHtml)

    def getEditorHtml(self, editor="editor1"):
        self.page().mainFrame().evaluateJavaScript("pythonjs.getHtml(CKEDITOR.instances."+ editor +".getData());")
        return self.editorJS.editorHtml

    def setEditorHtml(self, html='', editor="editor1"):
        self.editorJS.editorHtml = html
        self.page().mainFrame().evaluateJavaScript(
        '''var txt =  pythonjs.html;
        CKEDITOR.instances.'''+ editor +'''.setData(txt)''')

    def insertEditorHtml(self, html, editor="editor1"):
        self.editorJS.editorHtml = html
        self.page().mainFrame().evaluateJavaScript(
        '''var txt =  pythonjs.html;
        CKEDITOR.instances.'''+ editor +'''.insertHtml(txt)''')

    def keyPressEvent(self,event):
        handled = False

        if event.modifiers() & QtCore.Qt.ControlModifier:
            if event.key() == QtCore.Qt.Key_V:
                clip = QtWidgets.QApplication.clipboard()
                if clip.mimeData().hasImage():
                    self.paste(clip.mimeData())
                elif clip.mimeData().urls():
                    pth = unicode(clip.mimeData().urls()[0].toString()).split('\n')[0]
                    ext = pth.split('.')[-1].lower()
                    if ext in ['png','jpg','jpeg','bmp','gif','svg']:
                        self.paste(clip.mimeData())
                        handled=True
                    else:
                        clip.setText(pth)
            elif event.key() == QtCore.Qt.Key_S:
                handled = True

        # if event.modifiers() & QtCore.Qt.ShiftModifier:
        #     if event.key() == QtCore.Qt.Key_Tab:
        #         self.insertEditorHtml("&nbsp;"*5)
        #         handled = True

        if handled:
            event.accept()
            return
        else:
            QtWebKitWidgets.QWebView.keyPressEvent(self, event)

    def dropEvent(self, event):
        handled=False
        if not self.disableDrop:
            if (event.mimeData().hasImage() or event.mimeData().urls()):
                self.paste(event.mimeData())
                handled=True

            if not handled:
                QtWebKitWidgets.QWebView.dropEvent(self,event)

    def dragEvent(self, event):
        pass

    def mouseMoveEvent(self, event):
        QtWebKitWidgets.QWebView.mouseMoveEvent(self,event)

    def mousePressEvent(self, event):
        ht = self.page().mainFrame().hitTestContent(event.pos())
        if ht.pixmap().isNull():
            self.disableDrop=0
        else:
            self.disableDrop=1

        QtWebKitWidgets.QWebView.mousePressEvent(self, event)

    def canInsertFromMimeData(self, mimeData):
        # Thanks to Windows
        if mimeData.hasImage() | mimeData.hasUrls():
            return True
        elif mimeData.hasText():
            return True

    def paste(self, mimeData):
        if mimeData == None:
            clipboard = QtWidgets.QApplication.clipboard()
            mimeData = clipboard.mimeData()
        ptxt = unicode(mimeData.text()).replace("\n","<br>").replace(u'\u2028','<br>').replace(u'\xa0','&nbsp;')

        if mimeData.hasImage() and mimeData.hasUrls():
            ext = unicode(mimeData.urls()[0].path()).split('.')[-1].lower()
            self.insertPicture(picData= mimeData.imageData(),ext=ext)
        elif mimeData.hasImage():
            self.insertPicture(picData= mimeData.imageData(),ext='png')
        elif mimeData.hasUrls():
            filepastetype = None
            for url in mimeData.urls():
                pth = unicode(url.toLocalFile())

                if pth.startswith('file:///'):
                    pth = pth[8:]
                if pth == '' or pth=='/':
                    pth = unicode(url.toString())

                ext = pth.split('.')[-1].lower()
                if ext in ['jpg','png','gif','bmp','svg']:
                    self.insertPicture(pth)
        else:
            self.insertEditorHtml(ptxt)
