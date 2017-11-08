from generator import Generator

if __name__ == "__main__":    
    with open("names.txt", "r") as in_file:
        names = list(map(lambda s: s.rstrip(), in_file.readlines()))
    
    g = Generator(names, no_aliases = True, length_control = True)
    new_names = list()
    for i in range(25):
        s = g.generate()
        new_names.append(s)

    print("You could call your Ancient Roman kid:\n")
    for name in new_names:
        print(name)
    
