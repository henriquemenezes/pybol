#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import date, timedelta
from boletopdf import BoletoPDF
from boletosantander import BoletoSantander


if __name__ == "__main__":
    listaDados = []

    for i in range(2):
        d = BoletoSantander()
        d.cedente = 'Coloque a Razão Social da sua empresa aqui'
        d.agencia = '1333'
        d.conta = '0707077'

        d.data_vencimento = date.today() + timedelta(days=5)
        d.data_processamento = date.today()

        d.instrucoes = ['- Sr. Caixa, cobrar multa de 2% após o vencimento',
                        '- Receber até 10 dias após o vencimento',
                        '- Em caso de dúvidas entre em contato conosco:'
                        ' progeste@gmail.com']
        
        d.demonstrativo = ['Pagamento de Aforo da Diocese',
                           'Referente ao terreno de codigo X-X',
                           'Sistema Progeste']
        
        d.valor = float(2950.00)    
        d.valor_documento = d.valor

        d.nosso_numero = '1234567'
        d.numero_documento = '12345'
        d.sacado = ["Cliente Teste",
                    "Rua Desconhecida, 00/0000 - Não Sei - Cidade - "
                    "Cep. 00000-000",
                    ""]
        
        listaDados.append(d)

    # Formato normal - uma pagina por folha A4
    print "Normal"
    boleto = BoletoPDF('boleto-formato-normal-teste.pdf')
    for i in range(len(listaDados)):
        print i
        boleto.drawBoleto(listaDados[i])
        boleto.nextPage()
    boleto.save()

    print "Ok"
