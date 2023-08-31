# Scrape quests from final bastion into txt file

from bs4 import BeautifulSoup
import requests
import sys

# URLs
WC_URL = "https://finalbastion.com/wizard101-guides/w101-quest-guides/main-quest-line-wizard-city/"
KT_URL = "https://finalbastion.com/wizard101-guides/w101-quest-guides/main-quest-line-krokotopia/"
MB_URL = "https://finalbastion.com/wizard101-guides/w101-quest-guides/marleybone-main-quest-line-guide/"
MS_URL = "https://finalbastion.com/wizard101-guides/w101-quest-guides/mooshu-main-quest-line-guide/"
DS_URL = "https://finalbastion.com/wizard101-guides/w101-spell-guides/dragonspyre-main-quest-line-guide/" # Uses OL
CS_URL = "https://finalbastion.com/wizard101-guides/w101-quest-guides/celestia-main-quest-line/" # Uses OL
ZF_URL = "https://finalbastion.com/wizard101-guides/w101-quest-guides/zafaria-main-quest-line-guide/" # Uses OL
AV_URL = "https://finalbastion.com/wizard101-guides/w101-quest-guides/avalon-main-quest-line-guide/" # Uses nested OL
AZ_URL = "https://finalbastion.com/wizard101-guides/w101-quest-guides/azteca-main-quest-line/"
KR_URL = "https://finalbastion.com/wizard101-guides/w101-quest-guides/khrysalis-main-quest-line-guide/"
PL_URL = "https://finalbastion.com/wizard101-guides/w101-quest-guides/polaris-main-quest-line-guide/" # Uses OL
MR_URL = "https://finalbastion.com/wizard101-guides/w101-quest-guides/mirage-main-quest-line/"
EM_URL = "https://finalbastion.com/wizard101-guides/w101-quest-guides/empyrea-main-quest-line/"
KM_URL = "https://finalbastion.com/wizard101-guides/w101-quest-guides/karamelle-main-quest-line-guide/" # No infobox
LM_URL = "https://finalbastion.com/wizard101-guides/w101-quest-guides/lemuria-main-quest-line-guide/" # No infobox
NV_URL = "https://finalbastion.com/wizard101-guides/w101-quest-guides/novus-main-quest-line-guide/" # No infobox

# Side areas
GZ_URL = "https://finalbastion.com/wizard101-guides/w101-quest-guides/grizzleheim-main-quest-line-guide/" # Uses OL
WT_URL = "https://finalbastion.com/wizard101-guides/w101-quest-guides/wintertusk-main-quest-line-guide/"
WY_URL = "https://finalbastion.com/wizard101-guides/w101-quest-guides/wysteria-main-quest-line-guide/"
WCUG_URL = "https://finalbastion.com/wizard101-guides/w101-quest-guides/wizard-city-underground-quest-line/" # No infobox


# URL Lists
ALL_WORLDS = [WC_URL, KT_URL, MB_URL, MS_URL, DS_URL, CS_URL, ZF_URL, AV_URL, AZ_URL, KR_URL, PL_URL, MR_URL, EM_URL, KM_URL, LM_URL, NV_URL, GZ_URL, WT_URL, WY_URL, WCUG_URL]
ARC_1 = ALL_WORLDS[:5]
ARC_2 = ALL_WORLDS[5:10]
ARC_3 = ALL_WORLDS[10:13]
ARC_4 = ALL_WORLDS[13:16]
MAINLINE = ALL_WORLDS[:16]
SIDE_WORLDS = ALL_WORLDS[16:]


def get_quests(url):
    headers = {"User-Agent": "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Googlebot/2.1; +http://www.google.com/bot.html) Chrome/W.X.Y.Z Safari/537.36"}
    site = requests.get(url, headers=headers)
    soup = BeautifulSoup(site.content, "html.parser")

    box = soup.select(".et-box, et-info")
    if not box:
        box = [soup.find("h3")]

    names = []

    def getQuests(list):
        for quest in list:
            try:
                # extract quest name
                try:
                    dot = quest.index(".")
                except ValueError:
                    dot = -1
                try:
                    dash = quest.index("–") # WC, KM-NV
                except ValueError:
                    dash = quest.index("(") # KR-EM, GR-WCUG
                name = quest[dot+1:dash].strip().replace("’", "'").replace("‘", "'").replace("…", "...")
                names.append(name)
            except ValueError:
                continue

    # Deal with ol

    cur = box[0].find_next_sibling("ol")
    if cur is not None:
        ol = cur.get_text().split("\n")
        getQuests(ol)

    # Do ps
    cur = box[0].find_next_sibling("p")

    while cur is not None:
        section_list = cur.get_text().split("\n")
        getQuests(section_list)
        # Find next quest section
        try:
            cur = cur.find_next_sibling("p")
            if not cur.findChild("strong") and not cur.findChild("span"):
                cur = cur.find_next_sibling("p")
        except Exception:
            continue

    return names


def to_txt_file(path, list):
    with open(path, "w") as f:
        for quest in list:
            f.write(quest + "\n")


def print_usage():
    print("USAGE: python quest_scraper.py <txt_path> <# of worlds>")
    print("       python quest_scraper.py <txt_path> <# starting world> <# ending world (inclusive)>")
    print("       python quest_scraper.py -worlds")
    print("Values must be 1 to 20")


def print_worlds():
    print("1  - Wizard City\n"
          "2  - Krokotopia\n"
          "3  - Marleybone\n"
          "4  - MooShu\n"
          "5  - Dragonspyre\n"
          "6  - Celestia\n"
          "7  - Zafaria\n"
          "8  - Avalon\n"
          "9  - Azteca\n"
          "10 - Khrysalis\n"
          "11 - Polaris\n"
          "12 - Mirage\n"
          "13 - Empyrea\n"
          "14 - Karamelle\n"
          "15 - Lemuria\n"
          "16 - Novus\n"
          "17 - Grizzleheim\n"
          "18 - Wintertusk\n"
          "19 - Wysteria\n"
          "20 - Wizard City Underground")



def main(args):
    if len(args) == 1:
        if args[0] == "-worlds":
            print_worlds()
            sys.exit(0)
        else:
            print_usage()
            sys.exit(-1)

    if len(args) == 2:
        num = args[1]
        if not num.isnumeric():
            print("Not a number.")
            print_usage()
            sys.exit(-1)

        num = int(num)
        if num > len(ALL_WORLDS) or num <= 0:
            print("Number our of range.")
            print_usage()
            sys.exit(-1)

        lst = []
        for i in range(0, num):
            print("Parsing world {i}...".format(i=i+1))
            quests = get_quests(ALL_WORLDS[i])
            lst.extend(quests)
        to_txt_file(args[0], lst)
        print("Created file at {file}".format(file=args[0]))
        sys.exit(0)

    if len(args) == 3:
        path = args[0]
        start = args[1]
        end = args[2]

        if not start.isnumeric() or not end.isnumeric():
            print("Not a number.")
            print_usage()
            sys.exit(-1)

        start = int(start)
        end = int(end)

        if start <= 0 or end > len(ALL_WORLDS) or end < start:
            print("Invalid range or sequence.")
            print_usage()
            sys.exit(-1)

        lst = []
        for i in range(start-1, end):
            print("Parsing world {i}".format(i=i+1))
            lst.extend(get_quests(ALL_WORLDS[i]))
        to_txt_file(path, lst)
        print("Created file at {file}".format(file=path))
        sys.exit(0)

    else:
        print_usage()

if __name__ == "__main__":
    main(sys.argv[1:])