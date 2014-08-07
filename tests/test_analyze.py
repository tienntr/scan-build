# -*- coding: utf-8 -*-
#                     The LLVM Compiler Infrastructure
#
# This file is distributed under the University of Illinois Open Source
# License. See LICENSE.TXT for details.

import analyzer.driver as sut
import unittest
import tests.fixtures as fixtures


class AnalyzerTest(unittest.TestCase):

    def test_set_language(self):
        def test(expected, input):
            spy = fixtures.Spy()
            self.assertEqual(spy.success, sut.set_language(input, spy.call))
            self.assertEqual(expected, spy.arg)

        l = 'language'
        f = 'file'
        i = 'is_cxx'
        test({f: 'file.c', l: 'c'}, {f: 'file.c', l: 'c'})
        test({f: 'file.c', l: 'c++'}, {f: 'file.c', l: 'c++'})
        test({f: 'file.c', l: 'c++', i: True}, {f: 'file.c', i: True})
        test({f: 'file.c', l: 'c'}, {f: 'file.c'})
        test({f: 'file.cxx', l: 'c++'}, {f: 'file.cxx'})
        test({f: 'file.i', l: 'c-cpp-output'}, {f: 'file.i'})
        test({f: 'f.i', l: 'c-cpp-output'}, {f: 'f.i', l: 'c-cpp-output'})
        test(None, {f: 'file.java'})

    def test_filter_dict_insert_works(self):
        input = {'key': 1}
        expected = {'key': 1, 'value': 2}
        self.assertEqual(expected,
                         sut.filter_dict(input, frozenset(), {'value': 2}))

    def test_filter_dict_delete_works(self):
        input = {'key': 1, 'value': 2}
        expected = {'value': 2}
        self.assertEqual(expected,
                         sut.filter_dict(input, frozenset(['key', 'other']),
                                         dict()))

    def test_filter_dict_modify_works(self):
        input = {'key': 1}
        expected = {'key': 2}
        self.assertEqual(
            expected, sut.filter_dict(input, frozenset(['key']), {'key': 2}))
        self.assertEqual(1, input['key'])

    def test_filter_dict_does_strip(self):
        input = {
            'good': 'has value',
            'bad': None,
            'another bad': None,
            'normal': 'also'}
        expected = {'good': 'has value', 'normal': 'also'}
        self.assertEqual(expected, sut.filter_dict(input, frozenset(), {}))

    def test_arch_loop_default_forwards_call(self):
        spy = fixtures.Spy()
        input = {'key': 'value'}
        self.assertEqual(spy.success, sut.arch_loop(input, spy.call))
        self.assertEqual(input, spy.arg)

    def test_arch_loop_specified_forwards_call(self):
        spy = fixtures.Spy()
        input = {'archs_seen': ['-arch', 'i386', '-arch', 'ppc']}
        self.assertEqual(spy.success, sut.arch_loop(input, spy.call))
        self.assertEqual({'arch': 'i386'}, spy.arg)

    def test_arch_loop_stops_on_failure(self):
        spy = fixtures.Spy()
        input = {'archs_seen': ['-arch', 'sparc', '-arch', 'i386']}
        self.assertNotEqual(spy.success, sut.arch_loop(input, spy.fail))
        self.assertEqual({'arch': 'i386'}, spy.arg)