import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._edges_3 = []
        self._idMapNodes_3 = {}
        self._nodes_3 = []
        self._artista_cliente = {}
        self._idMapNodes_2 = {}
        self._edges_2 = []
        self._nodes_2 = []
        self._edges_1 = []
        self._idMapNodes_1 = {}
        self._nodes_1 = []
        self._graph1 = nx.Graph()
        self._graph2 = nx.Graph()
        self._graph3 = nx.Graph()



    def buildGraph1(self, genre, date1, date2):
        self._graph1.clear()
        self._nodes_1 = DAO.get_nodes_1(genre, date1, date2)
        self._idMapNodes_1 = {}
        for node in self._nodes_1:
            self._idMapNodes_1[node.TrackId] = node
        self._edges_1 = DAO.get_edges_1(genre, date1, date2, self._idMapNodes_1)
        self._graph1.add_nodes_from(self._nodes_1)
        for item in self._edges_1:
            self._graph1.add_edge(item[0], item[1], weight=item[2])

    def printGraph1(self):
        return f"Il grafo ha {len(self._graph1.nodes)} nodi e {len(self._graph1.edges)} archi."


    def buildGraph2(self, soglia, date1, date2):
        self._graph2.clear()
        self._nodes_2 = DAO.get_nodes_2(date1, date2)
        self._idMapNodes_2 = {}
        for node in self._nodes_2:
            self._idMapNodes_2[node. ArtistId] = node
        self._graph2.add_nodes_from(self._nodes_2)
        self._edges_2 = DAO.get_edges_2(soglia,date1, date2, self._idMapNodes_2)
        for edge in self._edges_2:
            self._graph2.add_edge(edge[0], edge[1], weight=edge[2])


    def printGraph2(self):
        return f"Il grafo ha {len(self._graph2.nodes)} nodi e {len(self._graph2.edges)} archi."


    def buildGraph3(self, soglia):
        self._graph3.clear()
        self._nodes_3 = DAO.get_nodes_3()
        self._idMapNodes_3 = {}
        for node in self._nodes_3:
            self._idMapNodes_3[node.CustomerId] = node
        self._graph3.add_nodes_from(self._nodes_3)
        self._edges_3 = DAO.get_edges_3(soglia,self._idMapNodes_3)
        for edge in self._edges_3:
            self._graph3.add_edge(edge[0], edge[1], weight=edge[2])

    def printGraph3(self):
        return f"Il grafo ha {len(self._graph3.nodes)} nodi e {len(self._graph3.edges)} archi."


    def get_optPath_coAcquisto(self,brano_start_id,k_brani):
        brano_start = self._idMapNodes_1[brano_start_id]
        correnti = [brano_start]
        self.bestScore1 = 0
        self.bestSolution_coAcquisto = []
        self.ricorsione_coAcquisto(correnti,k_brani)
        return self.bestSolution_coAcquisto, self.bestScore1

    def ricorsione_coAcquisto(self,correnti, k):
        if len(correnti) == k:
            score = self.calcolaScore1(correnti)
            if score > self.bestScore1:
                self.bestSolution_coAcquisto = copy.deepcopy(correnti)
                self.bestScore1 = score
            return
        ultimo = correnti[-1]
        vicini = list(self._graph1.neighbors(ultimo))
        for node in vicini:
            if node not in correnti:
                correnti.append(node)
                self.ricorsione_coAcquisto(correnti, k)
                correnti.pop()

    def calcolaScore1(self,correnti):
        score = 0
        for i in range(0,len(correnti)-1):
            if self._graph1.has_edge(correnti[i],correnti[i+1]):
                score += self._graph1[correnti[i]][correnti[i+1]]['weight']
        return score






    def get_optPath_Artisti(self,k_artisti,alfa):
        if k_artisti > len(self._nodes_2):
            return [], 0
        self._best_artists = []
        self._best_score2  = float('-inf')
        res_query = DAO.get_artista_clienti()
        self.calcola_clienti_per_artista(res_query)

        self.ricorsione_artisti(k_artisti, [], alfa,0)

        return self._best_artists, self._best_score2

    def ricorsione_artisti(self,k_artisti,parziale,alfa,start):
        if len(parziale) == k_artisti:
            score = self.calcolaScore2(parziale,alfa)
            if score > self._best_score2:
                self._best_artists = copy.deepcopy(parziale)
                self._best_score2 = score
            return
        for i in range(start,len(self._nodes_2)):
            node = self._nodes_2[i]
            if node not in parziale:
                parziale.append(node)
                self.ricorsione_artisti(k_artisti, parziale, alfa,i+1)
                parziale.pop()

    def calcola_clienti_per_artista(self,res_query):
        self._artista_cliente = {}
        for item in res_query:
            if item[0] not in self._artista_cliente:
                self._artista_cliente[item[0]] = set()
            self._artista_cliente[item[0]].add(item[1])
        return self._artista_cliente



    def calcolaScore2(self,parziale,alfa):
        copertura = self.calcolaCopertura2(parziale)
        sovrapposizione = self.calcolaSovrapposizione2(parziale)
        score = copertura - alfa*sovrapposizione
        return score

    def calcolaSovrapposizione2(self,parziale):
        sovrapposizione = 0
        for i in range(0,len(parziale)-1):
            for j in range(i+1, len(parziale)):
                n1 = parziale[i]
                n2 = parziale[j]
                if self._graph2.has_edge(n1,n2):
                    sovrapposizione += self._graph2[n1][n2]['weight']
        return sovrapposizione

    def calcolaCopertura2(self, parziale):
        clienti_coperti = set()

        for artista in parziale:
            clienti_coperti.update(self._artista_cliente[artista.ArtistId])
        return len(clienti_coperti)


    def getOpt_Path_Clienti(self,k_clienti,alfa):
        self._best_clients = []
        self._best_score_clients = float('-inf')

        self._ricorsione_clienti(k_clienti,[],alfa,0)

        return self._best_clients, self._best_score_clients

    def _ricorsione_clienti(self,k_clienti,parziale,alfa,start):
        if len(parziale) == k_clienti:
            score = self.calcolaScore_clienti(parziale,alfa)
            if score > self._best_score_clients:
                self._best_clients = copy.deepcopy(parziale)
                self._best_score_clients = score
            return
        nodes = list(self._graph3.nodes)
        for i in range(start,len(nodes)):
            node = nodes[i]
            if node not in parziale:
                parziale.append(node)
                self._ricorsione_clienti(k_clienti,parziale,alfa,i+1)
                parziale.pop()

    def calcolaScore_clienti(self,parziale,alfa):
        copertura = self.calcolaCoperturaClienti(parziale)
        sovrapposizione = self.calcolaSovrapposizioneClienti(parziale)
        score = copertura - alfa*sovrapposizione
        return score


    def calcolaCoperturaClienti(self,parziale):
        clienti_coperti = set()
        for client in parziale:
            clienti_coperti.add(client)
            clienti_coperti.update(self._graph3.neighbors(client))

        return len(clienti_coperti)

    def calcolaSovrapposizioneClienti(self,parziale):
        sovrapposizione = 0
        for i in range(0,len(parziale)-1):
            for j in range(i+1,len(parziale)):
                u = parziale[i]
                v = parziale[j]
                if self._graph3.has_edge(u,v):
                    sovrapposizione += self._graph3[u][v]['weight']

        return sovrapposizione


    def get_top_five_tracks(self):
        allTracks = DAO.get_Tracks()
        idMapAllTracks = {}
        for item in allTracks:
            idMapAllTracks[item.TrackId] = item
        top_five_tracks = []
        order_tracks = DAO.get_TopTracks()
        for i in range(0,5):
            top_five_tracks.append(idMapAllTracks[order_tracks[i]])

        return top_five_tracks
    #return lista di oggetti con dataclass

    def get_top_five_artists(self):
        return DAO.get_topArtists()
    #return lista di oggetti con dataclass


    def get_top_five_genres(self):
        return DAO.get_TopGenres()
    #return di oggetti con dataclass

    def get_num_tracks(self):
        return DAO.get_num_tracks()
    #return int

    def get_num_customers(self):
        return DAO.get_num_customers()
    #return int

    def get_num_fatture(self):
        return DAO.get_num_fatture()
    #return int


    def get_top_3_artist_with_more_different_clients(self):
        return DAO.get_artists_with_more_different_clients()
    #return una lista con 3 oggetti--> dataclass

    def get_top_3_spenders(self):
        return DAO.get_top3_spender()
    #return di una lista di tuple con ('name','surname')


    def get_name_genres(self):
        return DAO.get_name_genres()
    #return lista di stringhe con i nomi die generi



    def get_top_bridge_tracks(self):
        centrality = nx.betweenness_centrality(self._graph1, weight="weight")

        results = []

        for node in self._graph1.nodes:
            degree = self._graph1.degree(node)
            weighted_degree = self._graph1.degree(node, weight="weight")

            results.append({
                "track": node,
                "degree": degree,
                "weighted_degree": weighted_degree,
                "centrality": centrality[node]
            })

        results.sort(key=lambda x: x["centrality"], reverse=True)

        return results[:3]
    #funzione sul grafo 1 che dà completezza e mostra quelli che sono i brani piu centrali

    def get_top_artists(self):
        results = []
        centrality = nx.betweenness_centrality(self._graph2,weight="weight")

        for artist in self._graph2.nodes:
            degree = self._graph2.degree(artist)

            weighted_degree = self._graph2.degree(artist,weight="weight")
            results.append(
                (artist,
                 degree,
                 weighted_degree,
                 centrality[artist])
            )
        results.sort(key=lambda x: x[3],reverse=True)
        return results[:3]
    #vado ad inidividuare artisti maggiormente centarali all'interno del grafo:
    # che raggiungono un ampio segmento della clientela

    def get_nodes_graph1(self):
        return list(self._graph1.nodes)

    def analyze_customer_segments(self, outlier_threshold=1):
        representative_customers = []
        outlier_customers = []

        for customer in self._graph3.nodes:
            degree = self._graph3.degree(customer)
            weighted_degree = self._graph3.degree(customer, weight="weight")

            data = {
                "customer": customer,
                "degree": degree,
                "weighted_degree": weighted_degree
            }
            if degree <= outlier_threshold:
                outlier_customers.append(data)
            else:
                representative_customers.append(data)

        representative_customers.sort(key=lambda x: x["weighted_degree"], reverse=True)
        outlier_customers.sort(key=lambda x: x["degree"])
        return representative_customers[:3], outlier_customers





















