#!/usr/bin/env python2

import re
import sys
import datetime

categories = ["essence", "regulier", "nourriture", "loisir", "autres", "recettes"]

if len (sys.argv) != 2:
    print >> sys.stderr, "Usage: %s file.csv\n    Analyse depenses et recettes" % sys.argv[0]
    sys.exit (0)

now = datetime.datetime.now()

try:
    f = open (sys.argv[1], 'r')
    entries = []
    curEntry = None

    for line in f:
        if curEntry is None:
            d, l = line.split (';', 1)
            curEntry = {'date': datetime.date (*map(int, d.split('/'))[::-1])}
            libelle = l[1:].replace ("\r\n", "")
        else:
            if line[0] == '"':
                curEntry['libelle'] = libelle
                a = line[2:].split (';')
                if len (a) > 2:
                    curEntry['amount'] = float (a[1].replace (',', '.'))
                else:
                    curEntry['amount'] = -1*float (a[0].replace (',', '.'))
                entries.append (curEntry)
                curEntry = None
            else:
                libelle += line.replace ("\r\n", "")

    n = int (raw_input ("How many months to analyse ? "))
    nn = n
    end = now
    while nn > 0:
        m = end.month
        if m == 1:
            end = datetime.date (end.year-1, 12, end.day)
        else:
            end = datetime.date (end.year, end.month-1, end.day)
        nn -= 1

    sortedEntries = {}
    for c in categories:
        sortedEntries[c] = []

    for e in entries:
        if (end-e['date']).days > 0:
            break
        if e['amount'] > 0:
            categ = "recettes"
        elif "Amazon" in e['libelle']:
            categ = "loisir"
        elif "Subway" in e['libelle']:
            categ = "loisir"
        elif "Aides" in e['libelle']:
            categ = "regulier"
        elif "Escot" in e['libelle']:
            categ = "essence"
        elif "Dac" in e['libelle']:
            categ = "essence"
        elif "Biot Distribution" in e['libelle']:
            categ = "nourriture"
        elif "Satoriz" in e['libelle']:
            categ = "nourriture"
        elif "Philosophie" in e['libelle']:
            categ = "regulier"
        elif "Cotisation" in e['libelle']:
            categ = "regulier"
        elif "Pub" in e['libelle']:
            categ = "loisir"
        elif "Decathlon" in e['libelle']:
            categ = "loisir"
        elif "Intermarche" in e['libelle']:
            categ = "nourriture"
        elif "Autoroute" in e['libelle']:
            categ = "essence"
        elif "Prelevmnt" in e['libelle']:
            categ = "regulier"
        elif "Carrefour" in e['libelle']:
            categ = "nourriture"
        else:
            print >> sys.stderr, ", ".join (["%d: %s" % (i,s) for i,s in enumerate (categories[:-1])])
            print >> sys.stderr, "%02d:%02d:%02d %f" % (e['date'].day, e['date'].month, e['date'].year, e['amount'])
            print >> sys.stderr, e['libelle']
            while True:
                s = raw_input (">> ")
                try:
                    categ = categories[int(s)]
                    break
                except:
                    pass

        sortedEntries[categ].append (e)

    print "\nTotal par mois :"

    totDepense = 0
    for c in categories:
        tot = [0]
        end = now
        m = end.month
        if m == 1:
            end = datetime.date (end.year-1, 12, end.day)
        else:
            end = datetime.date (end.year, end.month-1, end.day)

        for e in sortedEntries[c]:
            if (end-e['date']).days > 0:
                tot.append (0)
                m = end.month
                if m == 1:
                    end = datetime.date (end.year-1, 12, end.day)
                else:
                    end = datetime.date (end.year, end.month-1, end.day)

            if c == 'recettes':
                tot[-1] += e['amount']
            else:
                tot[-1] -= e['amount']

        if c != 'recettes':
            totDepense += sum(tot)/n
        else:
            print ""

        print "    %s: %.2f" % (c, sum(tot)/n)

    print "    depenses: %.2f" % totDepense


except IOError:
    print >> sys.stderr, "Could not open file %s..." % sys.argv[1]
    sys.exit (-1)

