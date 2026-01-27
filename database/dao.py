from database.DB_connect import DBConnect
from model.album import Album

class DAO:

    @staticmethod
    def get_album_validi():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)

        query="""
        select al.id as id_album, al.title as nome_album, (sum(t.milliseconds)/(1000*60)) as durata_album
        from track t, album al
        where al.id=t.album_id 
        group by al.id
        """

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
        select distinct t1.album_id as id_album1, t2.album_id as id_album2
        from track t1, track t2, playlist_track pt1, playlist_track pt2
        where t1.id=pt1.track_id and t2.id=pt2.track_id
                and t1.album_id<t2.album_id and pt1.playlist_id=pt2.playlist_id 
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