
def invertPath(path):
    inverted_path = []
    for pathsegment in path:
        if pathsegment[0] == "u":
            reverse_dir = "d"
        elif pathsegment[0] == "d":
            reverse_dir = "u"
        elif pathsegment[0] == "l":
            reverse_dir = "r"
        else:
            reverse_dir = "l"
        inverted_path.insert(0, [reverse_dir, pathsegment[1], pathsegment[2]])
    return inverted_path

def oppositeDirection(Segment1, Segment2):
    if (
        (Segment1[0] == "u" and Segment2[0] == "d")
        or (Segment1[0] == "d" and Segment2[0] == "u")
        or (Segment1[0] == "l" and Segment2[0] == "r")
        or (Segment1[0] == "r" and Segment2[0] == "l")
    ):
        return True
    else:
        return False


def mergePaths(path1, path2):
    # function for merging two paths

    if oppositeDirection(path1[-1], path2[0]):
        while oppositeDirection(path1[-1], path2[0]) and path1[-1][2] == path2[0][2] and (len(path1) > 1 and len(path2) > 1):
            if path1 == [] or path1 == [[]]:
                if path2 == [] or path2 == [[]]:
                    return []
                else:
                    return path2
            elif path2 == [] or path2 == [[]]:
                print(path1)
                return path1
            else:
                # try:
                path2.pop(0)
                del path1[-1]
                # except:
                #     print("error in merge Paths")

    if oppositeDirection(path1[-1], path2[0]):
        if path1[-1][2] == path2[0][2]:
            path2.pop(0)
            del path1[-1]
        elif path1[-1][2] > path2[0][2]:
            path1[-1][2] = path1[-1][2] - path2[0][2]
            path2.pop(0)
        else:
            path2[0][2] = path2[0][2] - path1[-1][2]
            del path1[-1]

    # if path1[-1][0] == path2[0][0]:
    #     path1[-1][2] = path1[-1][2] + path2[0][2]
    #     path2.pop(0)

    path = [*path1, *path2]
    if len(path) == 1:
        path = path[0]
    return path

