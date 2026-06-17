from database.DB_connect import DBConnect
from model.Artist import Artist
from model.Customer import Customer
from model.Genre import Genre
from model.Track import Track


class DAO():
    def __init__(self):
        pass


    @staticmethod
    def get_Tracks():
        cnx = DBConnect.get_connection()
        tracks = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)

            query = """select t.*
                        from Track t """
            cursor.execute(query)
            for row in cursor:
                tracks.append(Track(**row))

            cursor.close()
            cnx.close()
        return tracks


    @staticmethod
    def get_nodes_1(genre,date1,date2):
        cnx = DBConnect.get_connection()
        nodes = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)

            query = """select distinct t.*
                    from track t, Invoice i, InvoiceLine il, Genre g  
                    where i.InvoiceId = il.InvoiceId
                    and t.TrackId = il.TrackId
                    and g.GenreId = t.GenreId
                    and g.Name = %s
                    and i.InvoiceDate between %s and %s"""
            cursor.execute(query,(genre,date1,date2))
            for row in cursor:
                nodes.append(Track(**row))
            cursor.close()
            cnx.close()
        return nodes

    @staticmethod
    def get_edges_1(genre,date1,date2,idMap):
        cnx = DBConnect.get_connection()
        edges = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)

            query = """select t1.TrackId as n1, t2.TrackId as n2, count(*) as peso
                from Track t1, Track t2, Invoice i1, Invoice i2,
                InvoiceLine il1, InvoiceLine il2, Genre g1, Genre g2
                where t1.GenreId = g1.GenreId
                and t2.GenreId  = g2.GenreId
                and g1.Name = %s
                and g2.Name = %s
                and t1.TrackId = il1.TrackId
                and t2.TrackId = il2.TrackId
                and il1.InvoiceId = i1.InvoiceId
                and il2.InvoiceId = i2.InvoiceId
                and i1.InvoiceDate between %s and %s
                and i2.InvoiceDate between %s and %s
                and i1.InvoiceId = i2.InvoiceId
                and t1.TrackId < t2.TrackId
                group by t1.TrackId, t2.TrackId"""
            cursor.execute(query,(genre,genre,date1,date2, date1,date2))
            for row in cursor:
                edges.append((idMap[row['n1']], idMap[row['n2']], row['peso']))
            cursor.close()
            cnx.close()
        return edges


    @staticmethod
    def get_nodes_2(date1,date2):
        cnx = DBConnect.get_connection()
        nodes = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)

            query = """select distinct a.*
                    from Artist a, Album al, Track t , Invoice i , InvoiceLine il  
                    where a.ArtistId = al.ArtistId
                    and al.AlbumId = t.AlbumId
                    and t.TrackId = il.TrackId
                    and il.InvoiceId = i.InvoiceId
                    and i.InvoiceDate between %s and %s"""
            cursor.execute(query,(date1,date2))
            for row in cursor:
                nodes.append(Artist(**row))
            cursor.close()
            cnx.close()
        return nodes

    @staticmethod
    def get_edges_2(soglia,date1,date2,idMap):
        cnx = DBConnect.get_connection()
        edges = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)

            query = """select al1.ArtistId as n1, al2.ArtistId as n2, count(distinct c1.CustomerId) as peso
                from Album al1, Album al2, Track t1, Track t2,
                Invoice i1, Invoice i2, InvoiceLine il1, InvoiceLine il2,
                Customer c1, Customer c2
                where al1.AlbumId = t1.AlbumId
                and al2.AlbumId = t2.AlbumId
                and t1.TrackId = il1.TrackId
                and t2.TrackId = il2.TrackId
                and il1.InvoiceId = i1.InvoiceId
                and il2.InvoiceId = i2.InvoiceId
                and i1.CustomerId = c1.CustomerId
                and i2.CustomerId = c2.CustomerId
                and c1.CustomerId = c2.CustomerId
                and al1.ArtistId < al2.ArtistId
                and i1.InvoiceDate between %s and %s
                and i2.InvoiceDate between %s and %s
                group by al1.ArtistId , al2.ArtistId
                having count(distinct c1.CustomerId) >= %s"""
            cursor.execute(query,(date1,date2, date1,date2,soglia))
            for row in cursor:
                edges.append((idMap[row['n1']], idMap[row['n2']], row['peso']))
            cursor.close()
            cnx.close()
        return edges


    @staticmethod
    def get_nodes_3():
        cnx = DBConnect.get_connection()
        nodes = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)

            query = """select distinct c.*
                    from Customer c"""
            cursor.execute(query)
            for row in cursor:
                nodes.append(Customer(**row))
            cursor.close()
            cnx.close()
        return nodes

    @staticmethod
    def get_edges_3(soglia,idMap):
        cnx = DBConnect.get_connection()
        edges = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)

            query = """select c1.CustomerId as n1, c2.CustomerId as n2, count(distinct t1.TrackId) as peso
                from Customer c1, Track t1, Invoice i1, InvoiceLine il1,
                Customer c2, Track t2, Invoice i2, InvoiceLine il2
                where c1.CustomerId = i1.CustomerId
                and c2.CustomerId = i2.CustomerId
                and i1.InvoiceId = il1.InvoiceId
                and i2.InvoiceId = il2.InvoiceId
                and il1.TrackId = t1.TrackId
                and il2.TrackId = t2.TrackId
                and t1.TrackId = t2.TrackId
                and c1.CustomerId < c2.CustomerId
                group by c1.CustomerId, c2.CustomerId
                having count(distinct t1.TrackId) >= %s"""
            cursor.execute(query,(soglia,))
            for row in cursor:
                edges.append((idMap[row['n1']], idMap[row['n2']], row['peso']))
            cursor.close()
            cnx.close()
        return edges


    @staticmethod
    def get_copertura_artisti_clienti():
        cnx = DBConnect.get_connection()
        idMap = {}
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)

            query = """select ar.ArtistId as id, count(distinct(c.CustomerId)) as clienti
                from Artist ar, Album al, Track t, InvoiceLine il, Invoice i, Customer c 
                where ar.ArtistId = al.ArtistId
                and al.AlbumId = t.AlbumId
                and t.TrackId = il.TrackId
                and il.InvoiceId = i.InvoiceId
                and i.CustomerId = c.CustomerId
                group by ar.ArtistId"""
            cursor.execute(query)
            for row in cursor:
                idMap[row['id']] = row['clienti']
            cursor.close()
            cnx.close()
        return idMap


    @staticmethod
    def get_artista_clienti():
        cnx = DBConnect.get_connection()
        lista = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)

            query = """select distinct ar.ArtistId as id_art, c.CustomerId as id_cus
                    from Artist ar, Album al, Track t, InvoiceLine il, Invoice i, Customer c 
                    where ar.ArtistId = al.ArtistId
                    and al.AlbumId = t.AlbumId
                    and t.TrackId = il.TrackId
                    and il.InvoiceId = i.InvoiceId
                    and i.CustomerId = c.CustomerId"""
            cursor.execute(query)
            for row in cursor:
                lista.append((row['id_art'], row['id_cus']))
            cursor.close()
            cnx.close()
        return lista


    @staticmethod
    def get_TopTracks():
        cnx = DBConnect.get_connection()
        tracks = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)

            query = """select t.TrackId as id, count(*) as num
                    from Track t, InvoiceLine il 
                    where t.TrackId = il.TrackId
                    group by t.TrackId
                    order by num desc"""
            cursor.execute(query)
            for row in cursor:
                tracks.append(row['id'])

            cursor.close()
            cnx.close()
        return tracks

    @staticmethod
    def get_topArtists():
        cnx = DBConnect.get_connection()
        artists = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)

            query = """select ar.ArtistId as id, ar.Name as name, count(*) as num
                from Artist ar, Album al, Track t, InvoiceLine il
                where ar.ArtistId = al.ArtistId
                and al.AlbumId = t.AlbumId
                and t.TrackId = il.TrackId
                group by ar.ArtistId, ar.Name
                order by num desc"""
            cursor.execute(query)
            for row in cursor:
                artists.append(Artist(row['id'], row['name']))

            cursor.close()
            cnx.close()
        return artists[0:5]

    @staticmethod
    def get_TopGenres():
        cnx = DBConnect.get_connection()
        genres = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)

            query = """select g.GenreId as id, g.Name as name, count(*) as num
                from Genre g, Track t, InvoiceLine il 
                where g.GenreId = t.GenreId
                and t.TrackId = il.TrackId
                group by g.GenreId, g.Name
                order by num desc"""
            cursor.execute(query)
            for row in cursor:
                genres.append(Genre(row['id'], row['name']))

            cursor.close()
            cnx.close()
        return genres[0:5]

    @staticmethod
    def get_num_tracks():
        cnx = DBConnect.get_connection()
        if cnx is None:
            print("Connessione fallita")
        cursor = cnx.cursor(dictionary=True)

        query = """select count(*) as num
                        from Track t"""
        cursor.execute(query)
        row = cursor.fetchone()

        cursor.close()
        cnx.close()
        return row['num']

    @staticmethod
    def get_num_customers():
        cnx = DBConnect.get_connection()
        if cnx is None:
            print("Connessione fallita")
        cursor = cnx.cursor(dictionary=True)

        query = """select count(*) as num
                        from Customer c"""
        cursor.execute(query)
        row = cursor.fetchone()

        cursor.close()
        cnx.close()
        return row['num']

    @staticmethod
    def get_num_fatture():
        cnx = DBConnect.get_connection()
        if cnx is None:
            print("Connessione fallita")
        cursor = cnx.cursor(dictionary=True)

        query = """select count(*) as num
                        from Invoice i"""
        cursor.execute(query)
        row = cursor.fetchone()

        cursor.close()
        cnx.close()
        return row['num']


    @staticmethod
    def get_top3_spender():
        cnx = DBConnect.get_connection()
        spenders = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)

            query = """select c.CustomerId,c.FirstName as name, c.LastName as surname, sum(i.Total) as spesa
                from Customer c, Invoice i 
                where c.CustomerId = i.CustomerId
                group by c.CustomerId, c.FirstName, c.LastName
                order by spesa desc"""
            cursor.execute(query)
            for row in cursor:
                spenders.append((row['name'], row['surname']))

            cursor.close()
            cnx.close()
        return spenders[0:3]

    @staticmethod
    def get_artists_with_more_different_clients():
        cnx = DBConnect.get_connection()
        top_artists = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)

            query = """select ar.ArtistId as id, ar.Name as name, count(distinct c.CustomerId) as clienti
                    from Artist ar, Album al, Track t, InvoiceLine il,
                    Invoice i, Customer c
                    where ar.ArtistId = al.ArtistId
                    and al.AlbumId = t.AlbumId
                    and t.TrackId = il.TrackId
                    and il.InvoiceId = i.InvoiceId
                    and i.CustomerId = c.CustomerId
                    group by ar.ArtistId, ar.Name
                    order by clienti desc
                    """
            cursor.execute(query)
            for row in cursor:
                top_artists.append(Artist(row['id'], row['name']))

            cursor.close()
            cnx.close()
        return top_artists[0:3]

    @staticmethod
    def get_name_genres():
        cnx = DBConnect.get_connection()
        genres = []
        if cnx is None:
            print("Connessione fallita")
        cursor = cnx.cursor(dictionary=True)

        query = """select g.Name as name
                from Genre g """
        cursor.execute(query)
        for row in cursor:
            genres.append(row['name'])

        cursor.close()
        cnx.close()
        return genres























