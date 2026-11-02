#!/usr/bin/env python3
#coding:utf-8
"""
test_core.py - Tests unitaires de validation du socle COVI-SCRABBLE et OpenSpec.
"""

import unittest
import os
import sys

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(TESTS_DIR)
SRC_DIR = os.path.join(PROJECT_DIR, 'src')
OPENSPEC_DIR = os.path.join(PROJECT_DIR, 'openspec')

sys.path.insert(0, SRC_DIR)
sys.path.insert(0, OPENSPEC_DIR)

from utils import sha256
from database import USERS
from dico.dictionary import Dictionary
from openspec_parser import get_openspec_data

class TestCoviScrabbleCore(unittest.TestCase):

    def test_sha256_passwords(self):
        """Vérifie que les mots de passe de test correspondent aux hachages SHA-256."""
        self.assertEqual(sha256('toto'), USERS['toto'])
        self.assertEqual(sha256('titi'), USERS['titi'])

    def test_dictionary_fr(self):
        """Vérifie le chargement et la recherche lexicale en français."""
        dico_fr = Dictionary('dico_fr')
        self.assertTrue(dico_fr.search('MAISON'))
        self.assertTrue(dico_fr.search('JOUER'))
        self.assertFalse(dico_fr.search('XYZABCDE'))

    def test_dictionary_en(self):
        """Vérifie le chargement et la recherche lexicale en anglais."""
        dico_en = Dictionary('dico_en')
        self.assertTrue(dico_en.search('SCRABBLE'))
        self.assertTrue(dico_en.search('HELLO'))
        self.assertFalse(dico_en.search('XYZABCDE'))

    def test_openspec_specifications(self):
        """Vérifie la conformité de l'arbre OpenSpec et l'intégrité des exigences vivantes."""
        data = get_openspec_data(PROJECT_DIR)
        self.assertIsNotNone(data)
        self.assertEqual(data['config']['name'], 'coviscrabble')
        self.assertEqual(data['total_requirements'], 8)
        self.assertEqual(data['total_changes'], 1)
        self.assertEqual(data['global_progress'], 100)

if __name__ == '__main__':
    unittest.main()
