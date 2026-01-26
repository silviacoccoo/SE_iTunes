from database.DB_connect import DBConnect
from model.album import Album

class DAO:

    # Album e sue canzoni all'interno
    @staticmethod
    def get_album():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ 
        select al.id as id_album, al.title as nome_album, t.id as id_canzone, t.name as nome_canzone
        from album al, track t
        where al.id=t.album_id
        group by al.id, t.id 
        """

        cursor.execute(query)

        for row in cursor:
            result.append((row['id_album'], row['nome_album'], row['id_canzone'], row['nome_canzone']))

        cursor.close()
        conn.close()
        return result # Lista di tuple con id e nome albu, id e nome canzone

    @staticmethod
    def get_album_validi():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)

        query="""
        select al.id as id_album, sum(t.milliseconds) as durata_album
        from track t, artist ar, album al
        where al.id=t.album_id and al.artist_id=ar.id
        group by al.id
        """

        cursor.execute(query)

        for row in cursor:
            result.append(row)

        cursor.close()
        conn.close()
        return result # Lista di dizionari
        # Ogni dizionario ha due chiavi: id album e sua durata complessiva

    @staticmethod
    def get_album_connessi():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)

        query="""
        select distinct a1.id as id_album1, a2.id as id_album2, pt1.playlist_id as id_playlist
        from album a1, album a2, track t1, track t2, playlist_track pt1, playlist_track pt2
        where a1.id=t1.album_id and a2.id=t2.album_id
                and t1.id=pt1.track_id and t2.id=pt2.track_id
                and a1.id!=a2.id and pt1.playlist_id=pt2.playlist_id 
        """
        cursor.execute(query)

        for row in cursor:
            result.append(row)

        cursor.close()
        conn.close()
        return result

# Verifica primo metodo: ok
risultato1=DAO.get_album()
# print(risultato1)

# Verifica secondo metodo: ok
risultato2=DAO.get_album_validi()
# print(risultato2)

# Verifica terzo metodo
risultato3=DAO.get_album_connessi()
print(risultato3)