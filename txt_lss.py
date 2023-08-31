# Convert txt file to lss file
import sys
import traceback
from xml.dom import minidom


def createFile(save_path, game, category, splits, emu="False"):
    """
    Creates the lss file at save_path for the given game, category, and splits
    :param save_path: The file to save to
    :param game: The name of the game
    :param category: The name of the category (ex: Any%)
    :param splits: The list of split names
    :param emu: True if using emulator, False otherwise. Default value is False
    """

    root = minidom.Document()

    # Run
    run = root.createElement("Run")
    run.setAttribute("version", "1.7.0")
    root.appendChild(run)

    # GameIcon
    gameicon = root.createElement("GameIcon")
    run.appendChild(gameicon)

    # GameName
    gamename = root.createElement("GameName")
    game = root.createTextNode(game)
    gamename.appendChild(game)
    run.appendChild(gamename)

    # CategoryName
    categoryname = root.createElement("CategoryName")
    category = root.createTextNode(category)
    categoryname.appendChild(category)
    run.appendChild(categoryname)

    # Metadata
    metadata = root.createElement("Metadata")
    # Run (id)
    runid = root.createElement("Run")
    runid.setAttribute("id", "")
    metadata.appendChild(runid)
    # Platform
    platform = root.createElement("Platform")
    platform.setAttribute("usesEmulator", emu)
    metadata.appendChild(platform)
    # Region
    metadata.appendChild(root.createElement("Region"))
    # Variables
    metadata.appendChild(root.createElement("Variables"))

    run.appendChild(metadata)

    # Offset
    offset = root.createElement("Offset")
    offsetText = root.createTextNode("00:00:00")
    offset.appendChild(offsetText)
    run.appendChild(offset)

    # AttemptCount
    attcnt = root.createElement("AttemptCount")
    cnt = root.createTextNode("0")
    attcnt.appendChild(cnt)
    run.appendChild(attcnt)

    # AttemptHistory
    run.appendChild(root.createElement("AttemptHistory"))

    # Segments
    segments = root.createElement("Segments")

    for split in splits:
        segment = root.createElement("Segment")
        # Name
        name = root.createElement("Name")
        name.appendChild(root.createTextNode(split))
        segment.appendChild(name)
        # Icon
        segment.appendChild(root.createElement("Icon"))
        # SplitTimes
        splitTimes = root.createElement("SplitTimes")
        pb = root.createElement("SplitTime")
        pb.setAttribute("name", "Personal Best")
        splitTimes.appendChild(pb)
        segment.appendChild(splitTimes)
        # BestSegmentTime
        segment.appendChild(root.createElement("BestSegmentTime"))
        # SegmentHistory
        segment.appendChild(root.createElement("SegmentHistory"))

        segments.appendChild(segment)

    run.appendChild(segments)

    # AutoSplitterSettings
    run.appendChild(root.createElement("AutoSplitterSettings"))

    # Convert to xml string
    xml_str = root.toprettyxml(indent="  ", encoding="UTF-8")

    with open(save_path, "wb") as f:
        f.write(xml_str)


def getSplitsFromFile(file):
    """
    From a file of split names on each line, returns a list of those names.
    Ignores empty lines or all spaces.
    :param file: The path of the file
    :return: An array where each element is a line of the file
    """
    ret = []
    with open(file) as f:
        for line in f:
            if not line.isspace():
                ret.append(line.removesuffix("\n"))
    return ret


def main(args):
    if len(args) != 4:
        print("USAGE: python txt_lss.py <game> <category> <txt_path> <lss_path>")
        sys.exit(-1)
    else:
        game = args[0]
        category = args[1]
        txt_path = args[2]
        lss_path = args[3]
        try:
            splits = getSplitsFromFile(txt_path)
        except Exception:
            print("Error getting txt file.")
            traceback.print_exc()
            sys.exit(1)

        try:
            createFile(lss_path, game, category, splits)
        except Exception:
            print("Error creating lss file.")
            traceback.print_exc()
            sys.exit(1)

        print("Successfully created file " + lss_path)
        sys.exit(0)


if __name__ == "__main__":
    main(sys.argv[1:])
