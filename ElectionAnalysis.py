from PopulatingTables import PopulatingTables
import numpy as np


class ElectionAnalysis:

    @classmethod
    def part_a(cls):
        con = PopulatingTables.create_connection()
        cursor = con.cursor()

        cons_riding = 0
        lib_riding = 0
        ndp_riding = 0
        green_riding = 0
        bloc_riding = 0
        peop_riding = 0
        my_list = [cons_riding, lib_riding, ndp_riding, green_riding, bloc_riding, peop_riding]
        parties_names = ["Conservative", "Liberal", "NDP", "Green", "Bloc Quebecois", "Peoples Party"]

        for i in range(1, 339):
            query = '''SELECT ConservativeVoteShare, LiberalVoteShare, NDPVoteShare, GreenVoteShare,
            BlocQuebecoisVoteShare, PeoplesPartyVoteShare FROM vote_share WHERE RidingNumber = %s '''

            cursor.execute(query, (i,))
            k = cursor.fetchone()
            won_party = np.argmax(k)
            my_list[won_party] = my_list[won_party] + 1
            con.commit()

        cursor.close()
        PopulatingTables.closing_connection(con)
        print("Parties have earned following number of Ridings: \nConservativeVoteShare ---> " + str(my_list[0])
              + "\nLiberalVoteShare ---> " + str(my_list[1])
              + "\nNDPVoteShare ---> " + str(my_list[2])
              + "\nGreenVoteShare ---> " + str(my_list[3])
              + "\nBlocQuebecoisVoteShare ---> " + str(my_list[4])
              + "\nPeoplesPartyVoteShare ---> " + str(my_list[5]))
        print("*******")
        result = np.argmax(my_list)
        print("And the winner of election is ---> " + parties_names[result])

    @classmethod
    def part_b(cls):
        con = PopulatingTables.create_connection()
        cursor = con.cursor()

        max_ratio = 0
        winner_party = -1
        winner_riding = -1
        parties_names = ["Conservative", "Liberal", "NDP", "Green", "Bloc Quebecois", "Peoples Party"]

        for i in range(1, 339):
            query = '''SELECT ConservativeVoteShare, LiberalVoteShare, NDPVoteShare, GreenVoteShare,
                BlocQuebecoisVoteShare, PeoplesPartyVoteShare FROM vote_share WHERE RidingNumber = %s '''
            query2 = '''SELECT TotalVotes FROM vote_share WHERE RidingNumber = %s'''

            cursor.execute(query, (i,))
            k = cursor.fetchone()
            won_party = np.argmax(k)

            cursor.execute(query2, (i,))
            k1 = cursor.fetchone()
            cur_ratio = k[won_party]/k1[0]
            if cur_ratio > max_ratio:
                max_ratio = cur_ratio
                winner_party = won_party
                winner_riding = i

            con.commit()

        query3 = '''SELECT ConservativeCandidate, LiberalCandidate, NDPCandidate,
              GreenCandidate, BlocQuebecoisCandidate, PeoplesPartyCandidate 
              FROM candidates WHERE RidingNumber = %s'''

        cursor.execute(query3, (winner_riding,))
        q = cursor.fetchone()
        won_candidate = q[winner_party]

        cursor.close()
        PopulatingTables.closing_connection(con)
        print("Candidate --" + won_candidate + "-- earned the biggest share(ratio) of votes in" +
                                             " their riding with vote ration of --" + str(max_ratio)
              + "-- and this happened in riding number --" + str(winner_riding) +
              "-- and this candidate is in --" + parties_names[winner_party] + "-- party.")

    @classmethod
    def part_c(cls):
        con = PopulatingTables.create_connection()
        cursor = con.cursor()

        won_ridings = list()

        for i in range(1, 339):
            query = '''SELECT ConservativeVoteShare, LiberalVoteShare, NDPVoteShare, GreenVoteShare,
                BlocQuebecoisVoteShare, PeoplesPartyVoteShare FROM vote_share WHERE RidingNumber = %s '''

            cursor.execute(query, (i,))
            k = cursor.fetchone()
            won_party = np.argmax(k)

            query2 = '''SELECT ConservativeCandidate, LiberalCandidate, NDPCandidate,
              GreenCandidate, BlocQuebecoisCandidate, PeoplesPartyCandidate 
              FROM candidates WHERE RidingNumber = %s'''
            cursor.execute(query2, (i,))
            d = cursor.fetchone()
            won_candidate = d[won_party]

            tot = won_candidate.split(" ")
            if tot[0] == "John":
                won_ridings.append(i)

            con.commit()

        cursor.close()
        PopulatingTables.closing_connection(con)
        print("There are --" + str(len(won_ridings)) + " --Ridings with a winner candidate named John and those are "
                                             "as such:")
        for j in won_ridings:
            print("Riding number--> " + str(j))

    @classmethod
    def part_d(cls):
        con = PopulatingTables.create_connection()
        cursor = con.cursor()

        cons_riding = 0
        lib_riding = 0
        ndp_riding = 0
        green_riding = 0
        bloc_riding = 0
        peop_riding = 0
        my_list = [cons_riding, lib_riding, ndp_riding, green_riding, bloc_riding, peop_riding]
        parties_names = ["Conservative", "Liberal", "NDP", "Green", "Bloc Quebecois", "Peoples Party"]

        for i in range(1, 339):
            query = '''SELECT ConservativeVoteShare, LiberalVoteShare, NDPVoteShare, GreenVoteShare,
                BlocQuebecoisVoteShare, PeoplesPartyVoteShare FROM vote_share WHERE RidingNumber = %s '''

            cursor.execute(query, (i,))
            k = cursor.fetchone()
            won_party = np.argmax(k)
            my_list[won_party] = my_list[won_party] + 1
            con.commit()

        cursor.close()
        PopulatingTables.closing_connection(con)

        min_party = np.argmin(my_list)
        print("The party with lowest number of won ridings is --" + parties_names[min_party]
              + " --and the number of ridings it's won is--> " + str(my_list[min_party]))
        print("*****")

        result = list()
        for i in range(len(my_list)):
            if my_list[i] >= 1:
                result.append(i)

        print("The parties that have won at least one riding are as such:")
        for k in result:
            print(parties_names[k])


if __name__ == '__main__':
    print("FOR PART A:")
    ElectionAnalysis.part_a()
    print("-----------------------------------")
    print("-----------------------------------")
    print("-----------------------------------")
    print("-----------------------------------")

    print("FOR PART B:")
    ElectionAnalysis.part_b()
    print("-----------------------------------")
    print("-----------------------------------")
    print("-----------------------------------")
    print("-----------------------------------")

    print("FOR PART C:")
    ElectionAnalysis.part_c()
    print("-----------------------------------")
    print("-----------------------------------")
    print("-----------------------------------")
    print("-----------------------------------")

    print("FOR PART D:")
    ElectionAnalysis.part_d()