# -*- coding: utf-8 -*-
from ..data import BoletoData, custom_property


class BoletoBanrisul(BoletoData):
    conta_cedente = custom_property('conta_cedente', 6)
    nosso_numero = custom_property('nosso_numero', 8)

    def __init__(self):
        BoletoData.__init__(self)
        self.codigo_banco = "041"
        self.logo_image = "logo_banrisul.jpg"
        self.disclaimer = '*** SAC BANRISUL 0800 646 1515 - '
        self.disclaimer += 'OUVIDORIA BANRISUL 0800 644 2200 ***'

    @property
    def campo_livre(self):
        content = '21%04d%07d%08d40' % (int(self.agencia_cedente),
                                        int(self.conta_cedente),
                                        int(self.nosso_numero))
        return '%s%s' % (content, self.calcula_dv(content))

    # From http://jrimum.org/bopepo/browser/trunk/src/br/com/nordestefomento/
    # jrimum/bopepo/campolivre/AbstractCLBanrisul.java
    def calcula_dv(self, seisPrimeirosCamposConcatenados):
        primeiroDV = self.modulo10(seisPrimeirosCamposConcatenados)
        digitos = seisPrimeirosCamposConcatenados + str(primeiroDV)
        restoMod11 = self.modulo11(digitos, 7, 1)

        while restoMod11 == 1:
            if primeiroDV == 9:
                primeiroDV = 0
            else:
                primeiroDV += 1

            digitos = seisPrimeirosCamposConcatenados + str(primeiroDV)
            restoMod11 = self.modulo11(digitos, 7, 1)

        if restoMod11 == 0:
            segundoDV = 0
        else:
            segundoDV = 11 - restoMod11
        return str(primeiroDV) + str(segundoDV)


    @property
    def agencia_conta_cedente(self):
        dv = self.calcula_dv(self.conta_cedente)
        s = "%s/%s.%s" % (self.agencia_cedente, self.conta_cedente, dv)
        return s

    def format_nosso_numero(self):
        dv = self.calcula_dv(self.nosso_numero)
        s = "%s-%s" % (self.nosso_numero, dv)
        return s
