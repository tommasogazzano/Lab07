from database.DB_connect import DBConnect
from model.situazione import Situazione


class MeteoDao():

    @staticmethod
    def get_all_situazioni():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT s.Localita, s.Data, s.Umidita
                        FROM situazione s 
                        ORDER BY s.Data ASC"""
            cursor.execute(query)
            for row in cursor:
                result.append(Situazione(row["Localita"],
                                         row["Data"],
                                         row["Umidita"]))
            cursor.close()
            cnx.close()
        return result


    @staticmethod
    def get_umidita(mese):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT s.Localita, AVG(s.Umidita)as media
                        from meteo.situazione s 
                        where month(s.`Data`) = %s
                        group by Localita """
            cursor.execute(query, (mese,))
            for row in cursor:
                result.append((row["Localita"],row["media"]))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_situazioni_meta_mese(mese):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT s.Localita, s.Umidita, s.`Data`
                            from meteo.situazione s 
                            where month(s.Data) = %s AND DAY(s.Data) <= 15
                            order by s.Data ASC """
            cursor.execute(query, (mese,))
            for row in cursor:
                result.append(Situazione(row["Localita"], row["Data"], row["Umidita"]))
            cursor.close()
            cnx.close()
        return result
