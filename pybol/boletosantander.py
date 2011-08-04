#!/usr/bin/python
# -*- coding: utf-8 -*-

from boleto import Boleto


class BoletoSantander(Boleto):

    def __init__(self):
        Boleto.__init__(self)
        self.codigo_banco = '033'
        self.carteira = '102'
        self.__fixo = '9'
        self.__ios = '0'
    
    def get_nosso_numero(self):
        nnum = self._formata_numero(self.__nosso_numero, 7, 0)
        dv_nosso_numero = self._modulo_11(nnum, 9, 0)        
        return '00000%s%s' % (nnum, dv_nosso_numero)

    def set_nosso_numero(self, v):
        self.__nosso_numero = v
    
    def get_fixo(self):
        return self.__fixo
        
    def get_ios(self):
        return self.__ios
    
    def get_linha_digitavel(self):
        valor = self._formata_numero('%.2f' % self.valor, 10, 0, 'valor')
        conta = self._formata_numero(self.conta, 7, 0)
        
        barra = '%s%s%s%s%s%s%s%s%s' % (self.codigo_banco,
                                        self.moeda,
                                        self.fator_vencimento,
                                        valor,
                                        self.fixo,
                                        conta,
                                        self.nosso_numero,
                                        self.ios,
                                        self.carteira)
        
        dv = self.__dv_barra(barra)
        
        linha = '%s%s%s' % (barra[0:4], dv, barra[4:])
        
        return self.__monta_linha_digitavel(linha)
    
    def get_codigo_barras(self):
        valor = self._formata_numero('%.2f' % self.valor, 10, 0, 'valor')
        conta = self._formata_numero(self.conta, 7, 0)
        
        barra = '%s%s%s%s%s%s%s%s%s' % (self.codigo_banco,
                                        self.moeda,
                                        self.fator_vencimento,
                                        valor,
                                        self.fixo,
                                        conta,
                                        self.nosso_numero,
                                        self.ios,
                                        self.carteira)
        
        dv = self.__dv_barra(barra)
        
        linha = '%s%s%s' % (barra[0:4], dv, barra[4:])
        
        return linha

    def __monta_linha_digitavel(self, codigo):
        campo1 = '%s%s%s%s' % (codigo[0:3], codigo[3], codigo[19],
                               codigo[20:24])
        campo1 = '%s%s' % (campo1, self._modulo_10(campo1))
        campo1 = '%s.%s' % (campo1[0:5], campo1[5:])

        campo2 = codigo[24:34]
        campo2 = '%s%s' % (campo2, self._modulo_10(campo2))
        campo2 = '%s.%s' % (campo2[0:5], campo2[5:])
        
        campo3 = codigo[34:44]
        campo3 = '%s%s' % (campo3, self._modulo_10(campo3))
        campo3 = '%s.%s' % (campo3[0:5], campo3[5:])
        
        campo4 = codigo[4]
        
        campo5 = '%s%s' % (codigo[5:9], codigo[9:19])
        
        return '%s %s %s %s %s' % (campo1, campo2, campo3, campo4, campo5)

    def __dv_nosso_numero(self, numero):
        resto2 = self._modulo_11(numero, 9, 1)
        digito = 11 - resto2
        if (digito == 10 or digito == 1):
            dv = 0
        else:
            dv = digito
        return dv
    
    def __dv_barra(self, numero):
        resto2 = self._modulo_11(numero, 9, 1)
        if (resto2 == 0 or resto2 == 1 or resto2 == 10):
            dv = 1
        else:
            dv = 11 - resto2
        return dv
    
    nosso_numero = property(get_nosso_numero, set_nosso_numero)
    codigo_barras = property(get_codigo_barras)
    linha_digitavel = property(get_linha_digitavel)
    fixo = property(get_fixo)
    ios = property(get_ios)
