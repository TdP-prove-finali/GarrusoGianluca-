from database.DB_connect import DBConnect
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