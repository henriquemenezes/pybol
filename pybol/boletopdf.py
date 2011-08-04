#!/usr/bin/python
# -*- coding: utf-8 -*-

from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.colors import black, white
from reportlab.lib.pagesizes import landscape, A4


class BoletoPDF:

    def __init__(self, fileName):
        self.width = 190 * mm
        self.heightLine = 6.5 * mm
        self.space = 2
        self.fontSizeTitle = 6
        self.fontSizeValue = 9
        self.deltaTitle = self.heightLine - (self.fontSizeTitle + 1)
        self.deltaFont = self.fontSizeValue + 1;

        self.pdfCanvas = canvas.Canvas(fileName, pagesize=A4)
        self.pdfCanvas.setStrokeColor(black)
    
    def drawReciboSacado(self, boletoDados, x, y):
        self.pdfCanvas.saveState();
        self.pdfCanvas.translate(x*mm, y*mm);

        linhaInicial = 16

        # Horizontal Lines
        self.pdfCanvas.setLineWidth(1)
        self.__hLine(0, linhaInicial*self.heightLine, self.width)
        self.__hLine(0, (linhaInicial+1)*self.heightLine, self.width)
        self.pdfCanvas.setLineWidth(2)
        self.__hLine(0, (linhaInicial+2)*self.heightLine, self.width)

        # Vertical Lines
        self.pdfCanvas.setLineWidth(1)
        self.__vLine(self.width-(45*mm), (linhaInicial+0)*self.heightLine, 
                     2*self.heightLine)
        self.__vLine(self.width-(45*mm)-(30*mm), 
                     (linhaInicial+0)*self.heightLine, 2*self.heightLine)
        self.__vLine(self.width-(45*mm)-(30*mm)-(30*mm), 
                     (linhaInicial+0)*self.heightLine, 2*self.heightLine)

        # Head
        self.pdfCanvas.setLineWidth(2)
        self.__vLine(40*mm, (linhaInicial+2)*self.heightLine, self.heightLine)
        self.__vLine(60*mm, (linhaInicial+2)*self.heightLine, self.heightLine)

        logoImagePath = boletoDados.logo
        if logoImagePath:
            self.pdfCanvas.drawImage(boletoDados.logo, 0, 
                                     (linhaInicial+2)*self.heightLine+3,
                                     40*mm, self.heightLine, 
                                     preserveAspectRatio=True, anchor='sw')
        self.pdfCanvas.setFont('Helvetica-Bold', 18)
        self.pdfCanvas.drawCentredString(50*mm, 
                                         (linhaInicial+2)*self.heightLine+3, 
                                         boletoDados.codigo_banco_dv)
        self.pdfCanvas.setFont('Helvetica-Bold', 10)
        self.pdfCanvas.drawRightString(self.width, 
                                       (linhaInicial+2)*self.heightLine+3,
                                       'Recibo do Sacado')

        # Titles
        self.pdfCanvas.setFont('Helvetica', 6 )
        self.deltaTitle = self.heightLine - (6 + 1)

        self.pdfCanvas.drawRightString(self.width, self.heightLine,
                                       'Autenticação Mecânica')

        self.pdfCanvas.drawString(0, (((linhaInicial+1)*self.heightLine))+
                                  self.deltaTitle, 'Cedente')
        self.pdfCanvas.drawString(self.width-(45*mm)-(30*mm)-(30*mm)+self.space,
                                  (((linhaInicial+1)*self.heightLine))+
                                  self.deltaTitle, 'Agência/Código Cedente')
        self.pdfCanvas.drawString(self.width-(45*mm)-(30*mm)+self.space, 
                                  (((linhaInicial+1)*self.heightLine))+
                                  self.deltaTitle, 'Data Documento')
        self.pdfCanvas.drawString(self.width-(45*mm)+self.space,
                                  (((linhaInicial+1)*self.heightLine))+
                                  self.deltaTitle, 'Vencimento')

        self.pdfCanvas.drawString(0, (((linhaInicial+0)*self.heightLine))
                                  +self.deltaTitle, 'Sacado')
        self.pdfCanvas.drawString(self.width-(45*mm)-(30*mm)-(30*mm)+self.space,
                                  (((linhaInicial+0)*self.heightLine))+
                                  self.deltaTitle, 'Nosso Número')
        self.pdfCanvas.drawString(self.width-(45*mm)-(30*mm)+self.space, 
                                  (((linhaInicial+0)*self.heightLine))
                                  +self.deltaTitle, 'N. do documento')
        self.pdfCanvas.drawString(self.width-(45*mm)+self.space, 
                                  (((linhaInicial+0)*self.heightLine))+
                                  self.deltaTitle, 'Valor Documento')

        self.pdfCanvas.drawString(0, (((linhaInicial-1)*self.heightLine))
                                  +self.deltaTitle, 'Demonstrativo')

        # Values
        self.pdfCanvas.setFont('Helvetica', 9)
        heighFont = 9 + 1;

        self.pdfCanvas.drawString(0+self.space, 
                                  (((linhaInicial+1)*self.heightLine))+
                                  self.space, boletoDados.cedente)
        self.pdfCanvas.drawString(self.width-(45*mm)-(30*mm)-(30*mm)+self.space,
                                  (((linhaInicial+1)*self.heightLine))+
                                  self.space, boletoDados.agencia)
        self.pdfCanvas.drawString(self.width-(45*mm)-(30*mm)+self.space,
                                  (((linhaInicial+1)*self.heightLine))+
                                  self.space, boletoDados.data_processamento)
        self.pdfCanvas.drawString(self.width-(45*mm)+self.space, 
                                  (((linhaInicial+1)*self.heightLine))+
                                  self.space, boletoDados.data_vencimento)

        valorDocumento = self._formatarValor(boletoDados
                                                      .valor_documento)

        self.pdfCanvas.drawString(0+self.space, 
                                  (((linhaInicial+0)*self.heightLine))+
                                  self.space, boletoDados.sacado[0])
        self.pdfCanvas.drawString(self.width-(45*mm)-(30*mm)-(30*mm)+self.space,
                                  (((linhaInicial+0)*self.heightLine))+
                                  self.space, boletoDados.nosso_numero)
        self.pdfCanvas.drawString(self.width-(45*mm)-(30*mm)+self.space,
                                  (((linhaInicial+0)*self.heightLine))+
                                  self.space, boletoDados.numero_documento)
        self.pdfCanvas.drawString(self.width-(45*mm)+self.space, 
                                  (((linhaInicial+0)*self.heightLine))+
                                  self.space, valorDocumento)

        demonstrativo = boletoDados.demonstrativo[0:25]
        for i in range(len(demonstrativo)):
            self.pdfCanvas.drawString(2*self.space, 
                                      (((linhaInicial-1)*self.heightLine))-
                                      (i*heighFont), demonstrativo[i])

        self.pdfCanvas.restoreState();

        return (self.width/mm, ((linhaInicial+2)*self.heightLine)/mm);

    def drawHorizontalCorteLine(self, x, y, width):
        self.pdfCanvas.saveState();
        self.pdfCanvas.translate(x*mm, y*mm)

        self.pdfCanvas.setLineWidth(1)
        self.pdfCanvas.setDash(1,2)
        self.__hLine(0, 0, width*mm)

        self.pdfCanvas.restoreState()

    def drawReciboCaixa(self, boletoDados, x, y):
        self.pdfCanvas.saveState()

        self.pdfCanvas.translate(x*mm, y*mm)

        # De baixo para cima posicao 0,0 esta no canto inferior esquerdo
        self.pdfCanvas.setFont('Helvetica', self.fontSizeTitle)

        y = 1.5 * self.heightLine
        self.pdfCanvas.drawRightString(self.width, 
                                       (1.5*self.heightLine)+self.deltaTitle-1,
                                       'Autenticação Mecânica / '
                                       'Ficha de Compensação')


        # Primeira linha depois do codigo de barra
        y += self.heightLine;
        self.pdfCanvas.setLineWidth(2)
        self.__hLine(0, y, self.width)
        self.pdfCanvas.drawString(self.width-(45*mm)+self.space, y+self.space,
                                  'Código de baixa' )
        self.pdfCanvas.drawString(0, y+self.space, 'Sacador / Avalista')

        y += self.heightLine
        self.pdfCanvas.drawString(0, y+self.deltaTitle, 'Sacado')
        sacado = boletoDados.sacado


        # Linha grossa dividindo o Sacado
        y += self.heightLine
        self.pdfCanvas.setLineWidth(2)
        self.__hLine(0, y, self.width)
        self.pdfCanvas.setFont('Helvetica', self.fontSizeValue)
        for i in range(len(sacado)):
            self.pdfCanvas.drawString(15*mm, (y-10)-(i*self.deltaFont), 
                                      sacado[i])
        self.pdfCanvas.setFont('Helvetica', self.fontSizeTitle)


        # Linha vertical limitando todos os campos da direita
        self.pdfCanvas.setLineWidth(1)
        self.__vLine(self.width-(45*mm), y, 9*self.heightLine)
        self.pdfCanvas.drawString(self.width-(45*mm)+self.space, 
                                  y+self.deltaTitle, '(=) Valor cobrado')


        # Campos da direita
        y += self.heightLine
        self.__hLine(self.width-(45*mm), y, 45*mm)
        self.pdfCanvas.drawString(self.width-(45*mm)+self.space, 
                                  y+self.deltaTitle, '(+) Outros acréscimos')

        y += self.heightLine
        self.__hLine(self.width-(45*mm), y, 45*mm)
        self.pdfCanvas.drawString(self.width-(45*mm)+self.space, 
                                  y+self.deltaTitle, '(+) Mora/Multa')

        y += self.heightLine
        self.__hLine(self.width-(45*mm), y, 45*mm)
        self.pdfCanvas.drawString(self.width-(45*mm)+self.space,
                                  y+self.deltaTitle, '(-) Outras deduções')

        y += self.heightLine
        self.__hLine(self.width-(45*mm), y, 45*mm)
        self.pdfCanvas.drawString(self.width-(45*mm)+self.space, 
                                  y+self.deltaTitle,
                                  '(-) Descontos/Abatimentos')
        self.pdfCanvas.drawString(0, y+self.deltaTitle, 'Instruções')

        self.pdfCanvas.setFont('Helvetica', self.fontSizeValue)
        instrucoes = boletoDados.instrucoes
        for i in range(len(instrucoes)):
            self.pdfCanvas.drawString(2*self.space, y-(i*self.deltaFont), 
                                      instrucoes[i])
        self.pdfCanvas.setFont('Helvetica', self.fontSizeTitle)


        # Linha horizontal com primeiro campo Uso do Banco
        y += self.heightLine
        self.__hLine(0, y, self.width)
        self.pdfCanvas.drawString(0, y+self.deltaTitle, 'Uso do banco')

        self.__vLine((30)*mm, y, 2*self.heightLine)
        self.pdfCanvas.drawString((30*mm)+self.space, y+self.deltaTitle, 
                                  'Carteira')

        self.__vLine((30+20)*mm, y, self.heightLine)
        self.pdfCanvas.drawString(((30+20)*mm)+self.space, y+self.deltaTitle, 
                                  'Espécie')

        self.__vLine((30+20+20)*mm, y, 2*self.heightLine)
        self.pdfCanvas.drawString(((30+40)*mm)+self.space, y+self.deltaTitle,
                                  'Quantidade')

        self.__vLine((30+20+20+20+20)*mm, y, 2*self.heightLine)
        self.pdfCanvas.drawString(((30+40+40)*mm)+self.space, y+self.deltaTitle,
                                  'Valor')

        self.pdfCanvas.drawString(self.width-(45*mm)+self.space, 
                                  y+self.deltaTitle, '(=) Valor documento')

        self.pdfCanvas.setFont('Helvetica', self.fontSizeValue)
        self.pdfCanvas.drawString((30*mm)+self.space, y+self.space, 
                                  boletoDados.carteira)
        self.pdfCanvas.drawString(((30+20)*mm)+self.space, y+self.space, 
                                  boletoDados.especie)
        self.pdfCanvas.drawString(((30+20+20)*mm)+self.space, y+self.space, '')
        valor = self._formatarValor(boletoDados.valor)
        self.pdfCanvas.drawString(((30+20+20+20+20)*mm)+self.space, 
                                  y+self.space, valor)
        valorDocumento = self._formatarValor(boletoDados.valor_documento)
        self.pdfCanvas.drawRightString(self.width-2*self.space, y+self.space,
                                       valorDocumento)
        self.pdfCanvas.setFont('Helvetica', self.fontSizeTitle)


        # Linha horizontal com primeiro campo Data documento
        y += self.heightLine
        self.__hLine(0, y, self.width)
        self.pdfCanvas.drawString(0, y+self.deltaTitle, 'Data do documento')
        self.pdfCanvas.drawString((30*mm)+self.space, y+self.deltaTitle,
                                  'N. do documento')
        self.pdfCanvas.drawString(((30+40)*mm)+self.space, y+self.deltaTitle,
                                  'Espécie doc')
        self.__vLine((30+20+20+20)*mm, y, self.heightLine)
        self.pdfCanvas.drawString(((30+40+20)*mm)+self.space, y+self.deltaTitle,
                                  'Aceite')
        self.pdfCanvas.drawString(((30+40+40)*mm)+self.space, y+self.deltaTitle,
                                  'Data processamento')
        self.pdfCanvas.drawString(self.width-(45*mm)+self.space,
                                  y+self.deltaTitle, 'Nosso número')

        self.pdfCanvas.setFont('Helvetica', self.fontSizeValue )
        self.pdfCanvas.drawString(0, y+self.space, 
                                  boletoDados.data_processamento)
        self.pdfCanvas.drawString((30*mm)+self.space, y+self.space,
                                  boletoDados.numero_documento)
        self.pdfCanvas.drawString(((30+40)*mm)+self.space, y+self.space,
                                  boletoDados.especie_documento)
        self.pdfCanvas.drawString(((30+40+20)*mm)+self.space, y+self.space,
                                  boletoDados.aceite)
        self.pdfCanvas.drawString(((30+40+40)*mm)+self.space, y+self.space,
                                  boletoDados.data_processamento)
        self.pdfCanvas.drawRightString(self.width-2*self.space, y+self.space, 
                                  boletoDados.nosso_numero)
        self.pdfCanvas.setFont('Helvetica', self.fontSizeTitle)


        # Linha horizontal com primeiro campo Cedente
        y += self.heightLine
        self.__hLine(0, y, self.width)
        self.pdfCanvas.drawString(0, y+self.deltaTitle, 'Cedente')
        self.pdfCanvas.drawString(self.width-(45*mm)+self.space, 
                                  y+self.deltaTitle, 'Agência/Código cedente')

        self.pdfCanvas.setFont('Helvetica', self.fontSizeValue)
        self.pdfCanvas.drawString(0, y+self.space, boletoDados.cedente)
        self.pdfCanvas.drawRightString(self.width-2*self.space, y+self.space, 
                                       boletoDados.agencia)
        self.pdfCanvas.setFont('Helvetica', self.fontSizeTitle)


        # Linha horizontal com primeiro campo Local de Pagamento
        y += self.heightLine
        self.__hLine(0, y, self.width)
        self.pdfCanvas.drawString(0, y+self.deltaTitle, 'Local de pagamento')
        self.pdfCanvas.drawString(self.width-(45*mm)+self.space, 
                                  y+self.deltaTitle, 'Vencimento')

        self.pdfCanvas.setFont('Helvetica', self.fontSizeValue)
        self.pdfCanvas.drawString(0, y+self.space, boletoDados.local_pagamento)
        self.pdfCanvas.drawRightString(self.width-2*self.space, y+self.space, 
                                       boletoDados.data_vencimento)
        self.pdfCanvas.setFont('Helvetica', self.fontSizeTitle)


        # Linha grossa com primeiro campo logo tipo do banco
        self.pdfCanvas.setLineWidth(3)
        y += self.heightLine
        self.__hLine(0, y, self.width)
        self.pdfCanvas.setLineWidth(2)
        self.__vLine(40*mm, y, self.heightLine) # Logo Tipo
        self.__vLine(60*mm, y, self.heightLine) # Numero do Banco

        logoImagePath = boletoDados.logo
        if logoImagePath:
            self.pdfCanvas.drawImage(boletoDados.logo, 0,
                                     y+self.space+1, 40*mm, self.heightLine,
                                     preserveAspectRatio=True, anchor='sw')
        self.pdfCanvas.setFont('Helvetica-Bold', 18)
        self.pdfCanvas.drawCentredString(50*mm, y+2*self.space, 
                                         boletoDados.codigo_banco_dv)
        self.pdfCanvas.setFont('Helvetica-Bold', 10)
        self.pdfCanvas.drawRightString(self.width, y+2*self.space, 
                                       boletoDados.linha_digitavel)


        # Codigo de barras
        self._codigoBarraI25(boletoDados.codigo_barras, 2*self.space, 0)

        self.pdfCanvas.restoreState();

        return (self.width, (y+self.heightLine)/mm)

    def drawBoleto(self, boletoDados):
        x = 10
        y = 40
        self.drawHorizontalCorteLine(x, y, self.width/mm)
        y += 5
        d = self.drawReciboCaixa(boletoDados, x, y)
        y += d[1] + 10
        self.drawHorizontalCorteLine(x, y, self.width/mm)
        y += 10
        d = self.drawReciboSacado(boletoDados, x, y)
        return (self.width,y)

    def nextPage(self):
        self.pdfCanvas.showPage()

    def save(self):
        self.pdfCanvas.save()

    def __hLine( self, x, y, width ):
        self.pdfCanvas.line(x, y, x+width, y)

    def __vLine( self, x, y, width ):
        self.pdfCanvas.line(x, y, x, y+width)
    
    def __centreText(self, x, y, text):
        self.pdfCanvas.drawCentredString(self.refX+x, self.refY+y, text)

    def __rightText(self, x, y, text ):
        self.pdfCanvas.drawRightString(self.refX+x, self.refY+y, text)

    def _formatarValor(self, nfloat):
        if nfloat:
            txt = "%.2f" % nfloat
            txt = txt.replace('.', ',')
        else:
            txt = ""
        return txt

    def _codigoBarraI25(self, num, x, y):
        # http://thiagosm.wordpress.com/2008/06/07/codigo-de-barra-em-python/
        # http://en.wikipedia.org/wiki/Interleaved_2_of_5

        altura      = 40
        tracoFino   = 1
        tracoGrosso = 3

        padroes = (
          '00110', #0
          '10001', #1
          '01001', #2
          '11000', #3
          '00101', #4
          '10100', #5
          '01100', #6
          '00011', #7
          '10010', #8
          '01010', #9
        )

        # Parametro num deve ter a quantidade de caracters par
        # se for impar, acrescenta um 0 no incio para que fique par
        if (len(num) % 2) != 0:
            num = '0' + num

        # Intercalando os pares numericos de acordo com os padroes
        # 0 = 00110,  1 = 10001, 01 = 00110 10001, 01 Intercalado = 0100101001
        barra = ""
        for i in range(0,len(num),2):
            a1 = int(num[i])
            a2 = int(num[i+1])
            padrao1 = padroes[a1]
            padrao2 = padroes[a2]
            for j in range(0,len(padrao1)):
                barra += "%1s%1s" % (padrao1[j],padrao2[j])

        # Marca inicial
        barra = "0000" + barra

        # Marca final
        barra = barra + "1000"

        self.pdfCanvas.setLineWidth(1)
        self.pdfCanvas.scale(0.8, 1)

        # A barra deve ser pintado com barras pretas e brancas
        # sem nesse ordem preto,branco,preto,banco,...
        # Numero 0 representa um traco fino
        # Numero 1 representa um traco grosso
        cores = [black,white]
        iCores = 0
        for digito in barra:
            if digito == '0':
                traco = tracoFino
            else:
                traco = tracoGrosso

            self.pdfCanvas.setStrokeColor( cores[iCores] )
            self.pdfCanvas.setFillColor( cores[iCores] )
            self.pdfCanvas.rect(x, y, traco, altura, stroke = 1, fill = 1)

            x += traco

            iCores += 1
            if iCores >= len(cores):
                iCores = 0

        self.pdfCanvas.scale(1, 1)
