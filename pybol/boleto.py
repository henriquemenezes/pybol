#!/usr/bin/python
# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractproperty
from datetime import date


class Boleto(object):

    __metaclass__ = ABCMeta

    def __init__(self):
        # Banco
        self.__codigo_banco = ''
        self.__carteira = ''
        self.__logo = ''
        self.__local_pagamento = 'Pagável em qualquer banco até o vencimento'

        # Cedente
        self.__cedente = ''
        self.__agencia = ''
        self.__conta = ''

        # Cliente
        self.__sacado = []

        # Boleto
        self.__aceite = 'N'
        self.__moeda = '9'
        self.__especie = 'R$'
        self.__especie_documento = ''
        self.__nosso_numero = ''
        self.__numero_documento = ''
        self.__valor = None
        self.__valor_documento = None
        self.__data_processamento = ''
        self.__data_vencimento = ''
        self.__demonstrativo = []
        self.__instrucoes = []

    def get_codigo_banco(self):
        return self.__codigo_banco

    def set_codigo_banco(self, v):
        self.__codigo_banco = v

    def get_carteira(self):
        return self.__carteira

    def set_carteira(self, v):
        self.__carteira = v

    def get_logo(self):
        return self.__logo

    def set_logo(self, v):
        self.__logo = v

    def get_local_pagamento(self):
        return self.__local_pagamento

    def set_local_pagamento(self, v):
        self.__local_pagamento = v

    def get_cedente(self):
        return self.__cedente

    def set_cedente(self, v):
        self.__cedente = v

    def get_agencia(self):
        return self.__agencia

    def set_agencia(self, v):
        self.__agencia = v

    def get_conta(self):
        return self.__conta

    def set_conta(self, v):
        self.__conta = v

    def get_sacado(self):
        return self.__sacado

    def set_sacado(self, v):
        self.__sacado = v

    def get_aceite(self):
        return self.__aceite

    def set_aceite(self, v):
        self.__aceite = v

    def get_moeda(self):
        return self.__moeda

    def get_especie(self):
        return self.__especie

    def get_especie_documento(self):
        return self.__especie_documento

    def set_especie_documento(self, v):
        self.__especie_documento = v

    def get_nosso_numero(self):
        return self.__nosso_numero

    def set_nosso_numero(self, v):
        self.__nosso_numero = v

    def get_numero_documento(self):
        return self.__numero_documento

    def set_numero_documento(self, v):
        self.__numero_documento = v

    def get_valor(self):
        return self.__valor

    def set_valor(self, v):
        self.__valor = v

    def get_valor_documento(self):
        return self.__valor_documento

    def set_valor_documento(self, v):
        self.__valor_documento = v

    def get_data_processamento(self):
        return self.__data_processamento.strftime("%d/%m/%Y")

    def set_data_processamento(self, v):
        self.__data_processamento = v

    def get_data_vencimento(self):
        return self.__data_vencimento.strftime("%d/%m/%Y")

    def set_data_vencimento(self, v):
        self.__data_vencimento = v

    def get_linha_digitavel(self):
        pass
        
    def get_codigo_barras(self):
        pass

    def get_demonstrativo(self):
        return self.__demonstrativo

    def set_demonstrativo(self, v):
        self.__demonstrativo = v

    def get_instrucoes(self):
        return self.__instrucoes

    def set_instrucoes(self, v):
        self.__instrucoes = v

    def get_codigo_banco_dv(self):
        return '%s-%s' % (self.codigo_banco, 
                          self._modulo_11(self.codigo_banco))

    def get_fator_vencimento(self):
        return self._fator_vencimento(self.data_vencimento)

    def _modulo_10(self, num):
        soma = 0
        peso = 2

        for i in range(len(num)-1, -1, -1):
            parcial = int(num[i]) * peso
            if parcial > 9:
                s = "%d" % parcial
                parcial = int(s[0])+int(s[1])
            soma += parcial
            if peso == 2:
                peso = 1
            else:
                peso = 2

        resto10 = soma % 10
        if resto10 == 0:
            modulo10 = 0
        else:
            modulo10 = 10 - resto10

        return modulo10

    def _modulo_11(self, num, base=9, r=0):
        soma = 0
        peso = 2

        for i in range(len(num)-1, -1, -1):
            parcial = int(num[i]) * peso
            soma += parcial
            if peso == base:
                peso = 2
            else:
                peso += 1

        if r == 0:
            soma *= 10
            digito = soma % 11
            return 0 if digito == 10 else digito
        else:
            return soma % 11

    def _fator_vencimento(self, data):
        data = data.split('/')
        ano = int(data[2])
        mes = int(data[1])
        dia = int(data[0])

        delta = abs(date(1997, 10, 7) - date(ano, mes, dia))

        return delta.days

    def _formata_numero(self, numero, loop, insert, tipo="geral"):
        if tipo == "geral":
            numero = numero.replace(",","").replace('.','')
            while len(numero) < loop:
                numero="%s%s" %(insert,numero)

        if tipo == "valor":
            numero = numero.replace(",","").replace('.','')
            while len(numero) < loop:
                numero = "%s%s" %(insert,numero)

        if tipo == "convenio":
            while len(numero) < loop:
                numero = "%s%s" %(numero,insert)

        return numero

    codigo_banco = property(get_codigo_banco, set_codigo_banco)
    carteira = property(get_carteira, set_carteira)
    logo = property(get_logo, set_logo)
    local_pagamento = property(get_local_pagamento, set_local_pagamento)
    cedente = property(get_cedente, set_cedente)
    agencia = property(get_agencia, set_agencia)
    conta = property(get_conta, set_conta)
    sacado = property(get_sacado, set_sacado)
    aceite = property(get_aceite, set_aceite)
    moeda = property(get_moeda)
    especie = property(get_especie)
    especie_documento = property(get_especie_documento, set_especie_documento)
    nosso_numero = property(get_nosso_numero, set_nosso_numero)
    numero_documento = property(get_numero_documento, set_numero_documento)
    valor = property(get_valor, set_valor)
    valor_documento = property(get_valor_documento, set_valor_documento)
    data_processamento = property(get_data_processamento,
                                  set_data_processamento)
    data_vencimento = property(get_data_vencimento, set_data_vencimento)
    linha_digitavel = abstractproperty(get_linha_digitavel)
    codigo_barras = abstractproperty(get_codigo_barras)
    demonstrativo = property(get_demonstrativo, set_demonstrativo)
    instrucoes = property(get_instrucoes, set_instrucoes)
    codigo_banco_dv = property(get_codigo_banco_dv)
    fator_vencimento = property(get_fator_vencimento)
