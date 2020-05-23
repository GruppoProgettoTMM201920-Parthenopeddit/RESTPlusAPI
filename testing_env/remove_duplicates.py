if __name__ == "__main__":

    esami_univoci = []
    with open('esami_ordinati.txt', 'r') as in_file:
        line = in_file.readline()
        esami_univoci.append(line)

        done = False
        while not done:
            new_line = in_file.readline()
            while new_line != "" and new_line == line:
                new_line = in_file.readline()

            print(new_line)

            if new_line != "":
                line = new_line
                esami_univoci.append(line)
            else:
                done = True

    with open('esami_univoci.txt', 'w') as out_file:
        for esame in esami_univoci:
            print(esame, file=out_file)


