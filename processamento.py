import threading
import time
import random


class Caixa:
    def __init__(self, id_caixa):
        self.id_caixa = id_caixa
        self.lista_requisicoes = []
        self.ws = WebService(self.id_caixa)

    def adicionar_requisicao_venda(self, id_produto, preco_produto, taxa_produto):
        # print(f'\nCaixa {self.id_caixa}\n')
        # print(f'Venda do produto {id_produto}\n{preco_produto = }\n{taxa_produto = }')
        # adiciona a requisicao no final da fila
        self.lista_requisicoes.append([id_produto, preco_produto, taxa_produto])

    def visualizar_requisicoes(self):
        print(f'Vendas do caixa {self.id_caixa}')

        for requisicao in self.lista_requisicoes:
            print(requisicao)

    def enviar_requisicoes(self):
        while True:
            if len(self.lista_requisicoes):
                # enviar requisicao da posicao 0 e tira ela da fila
                # print(f'enviando requisicao do caixa {self.id_caixa}')
                self.ws.receber_requisicao(self.lista_requisicoes.pop(0))


class WebService:
    def __init__(self, id):
        self.id = id
        self.lista_requisicoes = []
        self.lista_rp = [[RP(self.id, i), True] for i in range(1, 10+1)]
        self.thread_enviar_requisicao = threading.Thread(target=self.enviar_requisicoes_processamento)
        self.thread_enviar_requisicao.start()

    def receber_requisicao(self, requisicao):
        # print(f'requisicao recebida do caixa {self.id}')
        self.lista_requisicoes.append(requisicao)

    def enviar_requisicoes_processamento(self):
        while True:
            if len(self.lista_requisicoes):
                # enviar requisicao da posicao 0 para algum Rp disponivel
                # self.lista_rp[0].receber_requisicao()
                r = False
                while True:
                    for rp in range(len(self.lista_rp)):
                        if self.lista_rp[rp][1]:
                            self.lista_rp[rp][1] = False
                            threading.Thread(target=self.enviar_requisicao, args=(rp,)).start()
                            r = True
                            break
                    if r:
                        break

    def enviar_requisicao(self, num_rp):
        self.lista_rp[num_rp][0].receber_requisicao(self.lista_requisicoes.pop(0))
        time.sleep(10)
        self.lista_rp[num_rp][1] = True


class RP:
    def __init__(self, num_caixa, id):
        self.num_caixa = num_caixa
        self.id = id

    def receber_requisicao(self, requisicao):
        print(f'Requisicao {requisicao} do caixa {self.num_caixa} processada pelo RP {self.id}')


def gerar_requisicoes(caixa):
    while True:
        caixa.adicionar_requisicao_venda(random.randint(0, 9), round(random.random()*1000, 2), round(random.random()*100))
        # caixa.visualizar_requisicoes()
        time.sleep(1)


if __name__ == '__main__':
    lista_caixas = [Caixa(i) for i in range(1, 10+1)]
    # lista_caixas[0].adicionar_requisicao_venda(1, 10.5, 5)
    # lista_caixas[0].adicionar_requisicao_venda(2, 50, 2)
    # lista_caixas[0].visualizar_requisicoes()
    threads_enviar_requisicoes = [threading.Thread(target=lista_caixas[i].enviar_requisicoes) for i in range(len(lista_caixas))]
    threads_requisicoes = [threading.Thread(target=gerar_requisicoes, args=(lista_caixas[i],)) for i in range(len(lista_caixas))]
    # threads_requisicoes[0].start()

    for thread in threads_enviar_requisicoes:
        thread.start()

    # iniciando as threads dos caixas
    for thread in threads_requisicoes:
        thread.start()

    # ws = WebService(1)
    #
    # ws.lista_requisicoes = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
