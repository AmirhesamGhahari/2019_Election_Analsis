import psycopg2
import requests


class PopulatingTables:
    HOST = "hiring-quiz-database.cztyxuc8pfkm.ca-central-1.rds.amazonaws.com"
    PORT = 5432
    DB = "postgres"
    USER = "aghahari"
    PASSWORD = "QJdYWGAA6XqqU7bnF"

    @classmethod
    def create_connection(cls):
        connection = None
        try:
            connection = psycopg2.connect(host=PopulatingTables.HOST, user=PopulatingTables.USER,
                                          password=PopulatingTables.PASSWORD, port=PopulatingTables.PORT,
                                          database=PopulatingTables.DB)
        except Exception as error:
            print("making connection was not successful", error)
            exit()
        finally:
            return connection

    @classmethod
    def closing_connection(cls, con):
        try:
            con.close()
        except Exception as error:
            print("closing connection was not successful", error)
            exit()

    @classmethod
    def create_tables(cls):
        con = PopulatingTables.create_connection()

        table_1_query = '''CREATE TABLE vote_share
        (RidingNumber INT PRIMARY KEY NOT NULL,
        RidingNameInEnglish VARCHAR(50) NOT NULL,
        RidingNameInFrench VARCHAR(50) NOT NULL,
        TotalVotes INT NOT NULL,
        Turnout REAL NOT NULL,
        ConservativeVoteShare INT NOT NULL,
        LiberalVoteShare INT NOT NULL,
        NDPVoteShare INT NOT NULL,
        GreenVoteShare INT NOT NULL,
        BlocQuebecoisVoteShare INT NOT NULL,
        PeoplesPartyVoteShare INT NOT NULL);'''

        table_2_query = '''CREATE TABLE candidates
        (RidingNumber INT PRIMARY KEY NOT NULL,
        LiberalCandidate VARCHAR(100),
        ConservativeCandidate VARCHAR(100),
        NDPCandidate VARCHAR(100),
        GreenCandidate VARCHAR(100),
        BlocQuebecoisCandidate VARCHAR(100),
        PeoplesPartyCandidate VARCHAR(100));'''

        try:
            cursor = con.cursor()

            cursor.execute("DROP TABLE IF EXISTS vote_share")
            con.commit()
            cursor.execute("DROP TABLE IF EXISTS candidates")
            con.commit()

            cursor.execute(table_1_query)
            con.commit()
            cursor.execute(table_2_query)
            con.commit()

            cursor.close()
            PopulatingTables.closing_connection(con)

        except Exception as error:
            print("creating tables was not successful", error)
            cursor.close()
            PopulatingTables.closing_connection(con)
            exit()

    @classmethod
    def populate_candidates_table(cls):
        con = PopulatingTables.create_connection()
        cursor = con.cursor()
        endpoint = "https://electionsapi.cp.org/api/federal2019/Candidates_For_Riding"

        for i in range(1, 339):
            try:
                lib_can = ""
                cons_can = ""
                ndp_can = ""
                green_can = ""
                bloc_can = ""
                peop_can = ""
                resp = requests.get(endpoint, params={"ridingnumber": i})
                if resp.status_code != 200:
                    print("access to rigid number " + str(i) + " was not successful.")
                    continue
                for t in resp.json():
                    if t["PartyShortName_En"] == "CON":
                        cons_can = t["First"] + " " + t["Last"]
                        continue
                    if t["PartyShortName_En"] == "LIB":
                        lib_can = t["First"] + " " + t["Last"]
                        continue
                    if t["PartyShortName_En"] == "NDP":
                        ndp_can = t["First"] + " " + t["Last"]
                        continue
                    if t["PartyShortName_En"] == "GRN":
                        green_can = t["First"] + " " + t["Last"]
                        continue
                    if t["PartyShortName_En"] == "BQ":
                        bloc_can = t["First"] + " " + t["Last"]
                        continue
                    if t["PartyShortName_En"] == "PPC":
                        peop_can = t["First"] + " " + t["Last"]
                        continue
            except Exception as error:
                print("API calls for rigid " + str(i) + " was not successful", error)
                cursor.close()
                PopulatingTables.closing_connection(con)
                exit()
            else:
                try:
                    query = '''INSERT INTO candidates (RidingNumber, LiberalCandidate,
                    ConservativeCandidate, NDPCandidate, GreenCandidate, BlocQuebecoisCandidate,
                    PeoplesPartyCandidate) VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (RidingNumber)
                    DO NOTHING'''
                    val = (i, lib_can, cons_can, ndp_can, green_can, bloc_can, peop_can)
                    cursor.execute(query, val)
                    con.commit()

                except Exception as error:
                    print("inserting was unsuccessful at rigid" + str(i), error)
                    cursor.close()
                    PopulatingTables.closing_connection(con)
                    exit()
        cursor.close()
        PopulatingTables.closing_connection(con)

    @classmethod
    def populate_voteshare_table(cls):

        endpoint1 = "https://electionsapi.cp.org/api/federal2019/Candidates_For_Riding"
        endpoint2 = "https://electionsapi.cp.org/api/federal2019/Ridings"

        try:
            info = requests.get(endpoint2)
            if info.status_code != 200:
                print("access to ridings information API was unsuccessful")
                exit()
            else:
                data = info.json()
        except Exception as error:
            print("request to riding API was unsuccessful.", error)
            exit()
        else:
            con = PopulatingTables.create_connection()
            cursor = con.cursor()

            # for i in range(len(data)):
            for i in data:
                rid_num = i["RidingNumber"]
                rid_name_en = i["Name_En"]
                rid_name_fr = i["Name_Fr"]
                tot_vot = i["TotalVotes"]
                turn = i["TotalVotes"]/i["TotalVoters"]
                lib_sha = 0
                cons_sha = 0
                ndp_sha = 0
                green_sha = 0
                bloc_sha = 0
                peop_sha = 0

                try:
                    resp = requests.get(endpoint1, params={"ridingnumber": rid_num})
                    if resp.status_code != 200:
                        print("access to rigid number " + str(rid_num) + " was not successful.")
                        continue
                    for t in resp.json():
                        if t["PartyShortName_En"] == "CON":
                            cons_sha = t["Votes"]
                            continue
                        if t["PartyShortName_En"] == "LIB":
                            lib_sha = t["Votes"]
                            continue
                        if t["PartyShortName_En"] == "NDP":
                            ndp_sha = t["Votes"]
                            continue
                        if t["PartyShortName_En"] == "GRN":
                            green_sha = t["Votes"]
                            continue
                        if t["PartyShortName_En"] == "BQ":
                            bloc_sha = t["Votes"]
                            continue
                        if t["PartyShortName_En"] == "PPC":
                            peop_sha = t["Votes"]
                            continue
                except Exception as error:
                    print("API calls for rigid " + str(rid_num) + " was not successful", error)
                    cursor.close()
                    PopulatingTables.closing_connection(con)
                    exit()
                else:
                    try:
                        query = '''INSERT INTO vote_share (RidingNumber, RidingNameInEnglish,
                        RidingNameInFrench, TotalVotes, Turnout, ConservativeVoteShare,
                        LiberalVoteShare, NDPVoteShare, GreenVoteShare,
                        BlocQuebecoisVoteShare, PeoplesPartyVoteShare) VALUES (%s, %s, %s, %s,
                         %s, %s, %s, %s, %s, %s, %s)  ON CONFLICT (RidingNumber)
                        DO NOTHING'''
                        val = (rid_num, rid_name_en, rid_name_fr, tot_vot, turn, cons_sha, lib_sha,
                               ndp_sha, green_sha, bloc_sha, peop_sha)
                        cursor.execute(query, val)
                        con.commit()

                    except Exception as error:
                        print("inserting was unsuccessful at rigid" + str(rid_num) , error)
                        cursor.close()
                        PopulatingTables.closing_connection(con)
                        exit()
                #if rid_num == 10:
                    #break

            cursor.close()
            PopulatingTables.closing_connection(con)

    @classmethod
    def testing_voteshare(cls):
        con = PopulatingTables.create_connection()
        cursor = con.cursor()
        cursor.execute("SELECT * FROM vote_share")
        res = cursor.fetchall()
        i = 0
        for t in res:
            i = i+1
        cursor.close()
        PopulatingTables.closing_connection(con)
        return i

    @classmethod
    def testing_candidates(cls):
        con = PopulatingTables.create_connection()
        cursor = con.cursor()
        cursor.execute("SELECT * FROM candidates")
        res = cursor.fetchall()
        i = 0
        for t in res:
            i = i + 1
        cursor.close()
        PopulatingTables.closing_connection(con)
        return i


if __name__ == '__main__':
    PopulatingTables.create_tables()

    size = 0
    while size != 338:
        PopulatingTables.populate_candidates_table()
        size = PopulatingTables.testing_candidates()
        print("Number of added Ridings to table--> " + str(size))
        if size == 338:
            print("candidate table is fully populated.")
    print("-----------------------------------")
    print("-----------------------------------")
    print("-----------------------------------")
    print("-----------------------------------")
    size = 0
    while size != 338:
        PopulatingTables.populate_voteshare_table()
        size = PopulatingTables.testing_voteshare()
        print("Number of added Ridings to table--> " + str(size))
        if size == 338:
            print("vote_share table is fully populated.")

    '''con = PopulatingTables.create_connection()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM candidates")
    res = cursor.fetchall()
    i = 0
    for t in res:
        i = i + 1
        print(t)
    print(i)
    cursor.close()
    PopulatingTables.closing_connection(con)'''

    '''con = PopulatingTables.create_connection()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM vote_share")
    res = cursor.fetchall()
    i = 0
    for t in res:
        i = i + 1
        print(t)
    print(i)
    cursor.close()
    PopulatingTables.closing_connection(con)'''