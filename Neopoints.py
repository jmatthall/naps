#!/usr/bin/env python3
'''
Various methods to check and insure a certain amount of neopoints is on-hand

Part of naps (neopets automation program suite)
'''


from NeoSession import NeoSession


class Neopoints(NeoSession):

    def __init__(self):
        pass


def main():
    NeoSession()
    Neopoints()


if __name__ == '__main__':
    main()
