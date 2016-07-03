#!/usr/bin/env python

def main():
    with open("wumpus_rules.txt", "wb") as rule_file:
        rule_file.write("# rule 1\n")

        for i in range(1, 5):
            for j in range(1, 5):
                line = "({} {} ({}".format("if", "M_" + str(i) + "_" + str(j)
                    , "and")

                if not (i-1 < 1):
                    line += " S_" + str(i-1) + "_" + str(j)
                if not (j+1 > 4):
                    line += " S_" + str(i) + "_" + str(j+1)
                if not (j-1 < 1):
                    line += " S_" + str(i) + "_" + str(j-1)
                if not (i+1 > 4):
                    line += " S_" + str(i+1) + "_" + str(j)
                line += "))\n"

                rule_file.write(line)

        rule_file.write("\n# rule 2\n")
        for i in range(1, 5):
            for j in range(1, 5):
                line = "({} {} ({}".format("if", "S_" + str(i) + "_" + str(j)
                    , "xor")

                if not (i-1 < 1):
                    line += " M_" + str(i-1) + "_" + str(j)
                if not (j+1 > 4):
                    line += " M_" + str(i) + "_" + str(j+1)
                if not (j-1 < 1):
                    line += " M_" + str(i) + "_" + str(j-1)
                if not (i+1 > 4):
                    line += " M_" + str(i+1) + "_" + str(j)
                line += "))\n"

                rule_file.write(line)

        rule_file.write("\n# rule 3\n")
        for i in range(1, 5):
            for j in range(1, 5):
                line = "({} {} ({}".format("if", "P_" + str(i) + "_" + str(j)
                    , "and")

                if not (i-1 < 1):
                    line += " B_" + str(i-1) + "_" + str(j)
                if not (j+1 > 4):
                    line += " B_" + str(i) + "_" + str(j+1)
                if not (j-1 < 1):
                    line += " B_" + str(i) + "_" + str(j-1)
                if not (i+1 > 4):
                    line += " B_" + str(i+1) + "_" + str(j)
                line += "))\n"

                rule_file.write(line)

        rule_file.write("\n# rule 4\n")
        for i in range(1, 5):
            for j in range(1, 5):
                line = "({} {} ({}".format("if", "B_" + str(i) + "_" + str(j)
                    , "or")

                if not (i-1 < 1):
                    line += " P_" + str(i-1) + "_" + str(j)
                if not (j+1 > 4):
                    line += " P_" + str(i) + "_" + str(j+1)
                if not (j-1 < 1):
                    line += " P_" + str(i) + "_" + str(j-1)
                if not (i+1 > 4):
                    line += " P_" + str(i+1) + "_" + str(j)
                line += "))\n"

                rule_file.write(line)

        rule_file.write("\n# rule 5\n")

        x, y = 1, 1
        count = 0

        while True:
            count += 1
            if x == 5:
                break

            line = "({} {} ({}".format("if", "M_" + str(x) + "_" + str(y)
                , "and")

            for i in range(1, 5):
                for j in range(1, 5):
                    if i == x and j == y:
                        continue
                    else:
                        line += " (not M_" + str(i) + "_" + str(j) + ")"

            line += "))\n"
            rule_file.write(line)

            if count == 4:
                x = x + 1
                count = 0
            y = (y % 4) + 1

        rule_file.write("\n# rule 6\n")
        for i in range(1, 3):
            for j in range(1, 3):
                line = "(not"

                line += " M_" + str(i) + "_" + str(j)
                line += ")\n"

                rule_file.write(line)

            for j in range(1, 3):
                line = "(not"

                line += " P_" + str(i) + "_" + str(j)
                line += ")\n"

                rule_file.write(line)

        rule_file.write("\n# rule 7 not needed, because it is not possible to have 12 pits due to previous rules\n")

if __name__ == "__main__":
    main()
