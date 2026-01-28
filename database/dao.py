from database.DB_connect import DBConnect
from model.album import Album

class DAO:

    @staticmethod
    def get_album_validi():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)

        query="""
        select al.id as id_album, al.title as nome_album, (sum(t.milliseconds)/(60000.0)) as durata_album
        from track t, album al
        where al.id=t.album_id 
        group by al.id
        """
        # Metto 60000.0 per essere sicura si float
        cursor.execute(query)

        for row in cursor:
            result.append(Album(**row))

        cursor.close()
        conn.close()
        return result # Lista di oggetti album

    @staticmethod
    def get_album_connessi():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)

        query="""
        SELECT DISTINCT T1.album_id as id_album1, T2.album_id as id_album2
        FROM 
            (SELECT DISTINCT pt.playlist_id, t.album_id
             FROM playlist_track pt, track t 
             WHERE pt.track_id = t.id) T1,
            (SELECT DISTINCT pt.playlist_id, t.album_id
             FROM playlist_track pt, track t 
             WHERE pt.track_id = t.id) T2
        WHERE T1.playlist_id = T2.playlist_id AND T1.album_id < T2.album_id
        """
        cursor.execute(query)

        for row in cursor:
            result.append((row['id_album1'], row['id_album2']))

        cursor.close()
        conn.close()
        return result # Lista di tuple

# Verifica primo metodo: ok
# risultato1=DAO.get_album()
# print(risultato1)

# Verifica secondo metodo: ok
# risultato2=DAO.get_album_validi()
# print(risultato2)

# Verifica terzo metodo
# risultato3=DAO.get_album_connessi()
# print(risultato3)