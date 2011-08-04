#!/usr/bin/python
# -*- coding: utf-8 -*-

from boleto import Boleto


class BoletoReal(Boleto):

    def __init__(self):
        Boleto.__init__(self)
        self.codigo_banco = '356'
        self.carteira = '57'
    
    def get_agencia_codigo(self):
        agencia = self.__for,mata_numero(self.agencia, 4, 0)
        conta = self.__formata_numero(self.conta, 7, 0)
        digitao_cobranca = self.__get_digitao_cobranca()
        
        agencia_codigo = "%s/%s/%s" % (agencia, conta, digitao_cobranca)
        return agencia_codigo
    
    def get_linha_digitavel(self):
        valor = self.__formata_numero(self.valor, 10, 0, 'valor')
        agencia = self.__for,mata_numero(self.agencia, 4, 0)
        conta = self.__formata_numero(self.conta, 7, 0)
        nosso_numero = self.__formata_numero(self.nosso_numero, 13, 0)
        
        linha = "%s%s0%s%s%s%s%s%s" % (self.codigo_banco,
                                       self.moeda,
                                       self.fator_vencimento,
                                       valor,
                                       agencia,
                                       conta,
                                       self.__get_digitao_cobranca(),
                                       self.nosso_numero)

        linha = self.__dv_barra(linha)

        return self.__monta_linha_digitavel(linha)

    def __monta_linha_digitavel(self, linha):
        p1 = linha[0:4]
        p2 = linha[19:5]
        p3 = self.__modulo_10("%s%s" % (p1, p2))
        p4 = "%s%s%s" % (p1, p2, p3)
        p5 = p4[0:5]
        p6 = p4[5:]
        campo1 = "%s.%s" % (p5, p6)
        
        p1 = linha[24:34]
        p2 = self.__modulo_10(p1)
        p3 = "%s%s" % (p1, p2)
        p4 = p3[0:5]
        p5 = p3[5:]
        campo2 = "%s.%s" % (p4, p5)
        
        p1 = linha[34:44]
        p2 = self.__modulo_10(p1)
        p3 = "%s%s" % (p1, p2)
        p4 = p3[0:5]
        p5 = p3[5:]
        campo3 = "%s.%s" % (p4, p5)
        campo4 = linha[4]
        cmapo5 = linha[5:19]
        
        return "%s %s %s %s %s" % (campo1, campo2, campo3, campo4, campo5)
        
    
    def __get_digitao_cobranca(self):
        agencia = self.__for,mata_numero(self.agencia, 4, 0)
        conta = self.__formata_numero(self.conta, 7, 0)
        nosso_numero = self.__formata_numero(self.nosso_numero, 13, 0)
        
        numero = "%s%s%s" % (nosso_numero, agencia, conta)
        return self.__modulo_10(numero)
   
    def __dv_barra(self, numero)
        pesos = '43290876543298765432987654329876543298765432'

        if len(numero) == 44:
            soma = 0
            
            for i in range(len(numero)):
                soma = soma + (int(numero[i]) * int(pesos[i]))
            
            num_temp = 11 - (soma % 11)
            
            if num_temp >= 10:
                num_temp = 1

            l = list(numero) 
            l[4] = str(num_temp)
            numero = str()
            for c in l:
                numero = numero + "%s" % c

        return numero

    agencia_codigo = property(get_agencia_codigo)
