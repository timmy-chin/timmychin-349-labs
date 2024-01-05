# Tests 2-approximations of the Metric Traveling Salesperson Problem.
# CSC 349, Assignment 8
# Given tests, Fall '19

import re
import os
import tempfile
import subprocess
import unittest
import weighted_graph as graph


class TestTSP(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        compile()

    def test01_in1(self):
        out, err = run("in1.txt")
        msg = "Testing \"in1.txt\"; output to stderr, if any:\n%s" % err
        self.assertTrue(self.assertCycle(out, "in1.txt", msg) <= 42, msg)

    def test02_in2(self):
        out, err = run("in2.txt")
        msg = "Testing \"in2.txt\"; output to stderr, if any:\n%s" % err
        self.assertTrue(self.assertCycle(out, "in2.txt", msg) <= 6, msg)

    def test03_in3(self):
        out, err = run("in3.txt")
        msg = "Testing \"in3.txt\"; output to stderr, if any:\n%s" % err
        self.assertTrue(self.assertCycle(out, "in3.txt", msg) <= 16, msg)

    def assertCycle(self, out, graph_fname, msg):
        try:
            with open(graph_fname, "r") as graph_file:
                return parse(out, graph.read_graph(graph_file))
        except Exception as e:
            raise AssertionError(msg) from e


def compile():
    """
    Compile the approximation and discard its output.
    NOTE: This assumes a Unix-like runtime environment.
    """
    with open(os.devnull, "r+") as dev_null:
        subprocess.call(
         "./compile.sh",
         stdout = dev_null, stderr = dev_null,
         stdin = dev_null, shell = True)


def run(input_fname, _outs = {}, _errs = {}):
    """
    Run the approximation and capture its output.
    NOTE: This assumes a Unix-like runtime environment.
    :param input_fname: An input file's name
    :return: The outputs to stdout and stderr
    """
    if input_fname not in _outs:
        try:
            with tempfile.TemporaryFile(mode = "w+") as out_file,\
                 tempfile.TemporaryFile(mode = "w+") as err_file,\
                 open(os.devnull, "r") as dev_null:

                subprocess.call(
                 "./run.sh %s" % input_fname,
                 stdout = out_file, stderr = err_file,
                 stdin = dev_null, shell = True)

                out_file.seek(0)
                _outs[input_fname] = out_file.read()
                err_file.seek(0)
                _errs[input_fname] = err_file.read()

        except Exception as e:
            if input_fname not in _outs:
                _outs[input_fname] = ""
            if input_fname not in _errs:
                _errs[input_fname] = "%s: %s" % (type(e).__name__, str(e))

    return (_outs[input_fname], _errs[input_fname])


def parse(raw_out, graph_g):
    """
    Parse a Hamiltonian cycle from raw output.
    :param raw_out: An approximation's raw output
    :param graph_g: A graph in which the approximation was found
    :return: The weight of the cycle
    :raise: A RuntimeError if the cycle cannot be parsed
    :raise: A ValueError if the cycle is not Hamiltonian
    """
    raw_cycle = re.match(
     "^Hamiltonian cycle of weight (\d+):\s+([\d\s,]+)\s+$", raw_out)

    try:
        weight = int(raw_cycle.group(1))
        cycle = re.split(",\s*", raw_cycle.group(2))
        explored = set()
    except Exception as e:
        raise RuntimeError("Failed to parse output.") from e

    for i in range(1, len(cycle)):
        if cycle[i] in explored:
            raise ValueError("Cycle passes through vertices multiple times.")
        elif cycle[i] not in graph_g:
            raise ValueError("Cycle passes through nonexistent vertices.")
        else:
            explored.add(cycle[i])
            weight -= graph_g[cycle[i - 1]][cycle[i]]

    if cycle[0] != cycle[-1]:
        raise ValueError("Cycle does not begin and end at the same vertex.")
    elif len(explored) != len(graph_g.matrix):
        raise ValueError("Cycle does not pass through every vertex.")
    elif weight != 0:
        raise ValueError("Cycle does not traverse edges matching its weight.")
    else:
        return int(raw_cycle.group(1))


if __name__ == "__main__":
    unittest.main()
