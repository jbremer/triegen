#!/usr/bin/env python
"""Triegen    (C) Jurriaan Bremer 2013

Utility to generate a Trie from a set of strings.

"""
import RBTree
import sys


class Node:
    """Represents a single, light-weight, node of a tree."""
    def __init__(self, left, value, right):
        self.left = left
        self.value = value
        self.right = right

    def count(self):
        """Returns the count of values, including its own."""
        ret = 1
        if self.left:
            ret += self.left.count()
        if self.right:
            ret += self.right.count()
        return ret


def trie(l):
    """Function which translates a list into a balanced trie."""
    def node(n):
        return Node(node(n.left), n.value, node(n.right)) if n else None

    # there's some serious stuff going on in the Garbage Collector,
    # effectively unlinking the _entire_ tree when omitting a temporary
    # storage of the tree object (due to an aggressive __del__ in RBTree)
    tree = RBTree.RBList(l)
    return node(tree.root)


def calcdiff(n):
    """Calculates the difference between a Nodes value, left, and right.

    This function has no return value, it only adds some fields to the Nodes.

    """


def triegen_C_int(n, fmt):
    """Trie Generator for C.

    Returns a list of C code, which represent the generated Trie.

    """
    lines = []

    if n.left:
        if n.left.count() == 1:
            lines += triegen_C_int(n.left, fmt)
        else:
            lines += ['if(x < %s) {' % n.value]
            lines += [' ' + x for x in triegen_C_int(n.left, fmt)]
            lines += ['}']

    if n.right:
        if n.right.count() == 1:
            lines += triegen_C_int(n.right, fmt)
        else:
            lines += ['%sif(x > %s) {' % ('else ' if n.left else '', n.value)]
            lines += [' ' + x for x in triegen_C_int(n.right, fmt)]
            lines += ['}']

    lines += [
        '%sif(%s == x) {' % ('else ' if n.left or n.right else '', n.value),
        ' return ' + fmt.format(n.value) + ';',
        '}']

    return lines


def triegen_C(n, fn, fmt):
    lines = ['#include <stdio.h>', 'const char *%s(int x)' % fn, '{']
    lines += [' ' + x for x in triegen_C_int(n, fmt)]
    return lines + [' return NULL;', '}']

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print 'Usage: %s <infile> <funcname> <fmt>' % sys.argv[0]
        exit(0)

    root = trie(int(x.strip()) for x in open(sys.argv[1]))

    calcdiff(root)

    print '\n'.join(triegen_C(root, sys.argv[2], sys.argv[3]))
