# Estado inicial -> duas jarras de 3 Litros e 4 Litros, inicialmente vazia.
# Estado final -> jarra de 4 Litros com 2 Litros e jarra de 3 Litros vazia.

# Ações:
#   1. Encher a jarra totalmente
#   2. Mover a agua de uma jarra para outra
#   3. Esvaziar jarra

def encherJarra(jar):
    return jar['limite']

def moverAgua(jar_fonte, jar_destino):
    # se fonte está vazia ou destino esta cheio, apenas retorne.
    if( jar_fonte['conteudo'] == 0 or jar_destino['limite'] == jar_destino['conteudo'] ):
        fonte = jar_fonte['conteudo']
        destino = jar_destino['conteudo']
    # quantidade de volume disponivel.
    espaco_disponivel = jar_destino['limite'] - jar_destino['conteudo']
    # agua disponivel para ser movida.
    if( jar_fonte['conteudo'] > espaco_disponivel ):
        fonte = jar_fonte['conteudo'] - espaco_disponivel
        destino = jar_destino['limite']
    # se a fonte é menor ou igual ao espaço disponivel, subtrai da fonte e soma no destino.
    else:
        destino = jar_destino['conteudo'] + jar_fonte['conteudo']
        fonte = 0
    if(jar_fonte['limite'] > jar_destino['limite']):
        return [fonte, destino]
    else:
        return [destino, fonte]

def esvaziarJarra(jar):
    return 0

def checarEstadoFinal(volume):
    """
    Funcao recebe objeto da jarra maior e retorna se está no estado final (Com 2 litros de água).
    Se sim, retorna True. Senão retorna False.
    """
    if(volume == 2):
        return True
    return False

class NodoArvore():
    def __init__(self, estado, pai=None):
        self.estado = estado  # lista de duas posições com [ conteúdo da jarra maior, conteúdo da jarra menor ].
        self.filhos = []  # lista apontando para mais instancias de NodoArvore    
        self.pai = pai

    def __repr__(self):
        return f'Estado = {self.estado}'

class ArvoreManager():
    def __init__(self, raiz):
        self.raiz = raiz

    def verificarEstadoRepetido(self, estado):
        """
        Recebe um estado e verifica se ele ja existe na árvore. Retorna True caso exista.
        """
        return self.__verificarEstado(raiz, estado)
    
    def __verificarEstado(self, nodo, estado):
        if(nodo.estado == estado):
            return True
        if(len(nodo.filhos) > 0):
            for filho in nodo.filhos:
                if(self.__verificarEstado(filho, estado)):
                    return True
        return False

    def printarRamoArvore(self, nodo):
        if(nodo.pai is not None):            
            self.printarRamoArvore(nodo.pai)
        print(nodo)


if __name__ == '__main__':
     # comporta 4 litros de agua
    jarra_maior = {
        'conteudo': 0,
        'limite': 4
    }

    # comporta 3 litros de agua
    jarra_menor = {
        'conteudo': 0,
        'limite': 3
    }
    
    raiz = NodoArvore([jarra_maior['conteudo'], jarra_menor['conteudo']])
    am = ArvoreManager(raiz)
    nodos_execucao = [raiz]  # Lista de Nodos a serem executados na geração de filhos

    for nodo_atual in nodos_execucao:
        # o estado final foi alcançado, sair do loop.
        if(checarEstadoFinal(nodo_atual.estado[0])):            
            no = nodo_atual
            am.printarRamoArvore(no)
            break
        
        j_maior = {
            'conteudo': nodo_atual.estado[0],
            'limite': 4
        }
        j_menor = {
            'conteudo': nodo_atual.estado[1],
            'limite': 3
        }

        # gerar possiveis estados
        filhos_candidatos = []

        # encher jarra grande
        filhos_candidatos.append([
            encherJarra(j_maior),
            j_menor['conteudo']
        ])
        # esvaziar jarra grande
        filhos_candidatos.append([
            esvaziarJarra(j_maior),
            j_menor['conteudo']
        ])
        # mover jarra grande para pequena
        filhos_candidatos.append(moverAgua(j_maior, j_menor))

        # encher jarra pequena
        filhos_candidatos.append([
            j_maior['conteudo'],
            encherJarra(j_menor)
        ])

        # esvaziar jarra pequena
        filhos_candidatos.append([
            j_maior['conteudo'],
            esvaziarJarra(j_menor)
        ])

        # mover jarra pequena para grande 
        filhos_candidatos.append(moverAgua(j_menor, j_maior))

        ## TODO -> JA TEMOS CANDIDATOS. AGORA ANALISAR QUAIS SAO VALIDOS
        for filho_candidato in filhos_candidatos:
            # verifica se o estado ja apareceu na árvore. se sim, retorna True.
            is_repetido = am.verificarEstadoRepetido(filho_candidato)
            if(not is_repetido):
                filho = NodoArvore(filho_candidato, nodo_atual)
                nodo_atual.filhos.append(filho)
                nodos_execucao.append(filho)

