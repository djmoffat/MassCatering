#!/usr/bin/env python

import yaml
import re
import sys
from pint import UnitRegistry

ureg = UnitRegistry()
# Some definitions
ureg.define('carrot = 72 grams')
ureg.define('onion = 90 grams')
ureg.define('red_onion = 90 grams')
ureg.define('roll = 60 grams')
ureg.define('vege_burger = 125 grams')
ureg.define('leaf = 5 grams')
ureg.define('sprig = 5 grams')
ureg.define('turnip = 500 grams')
ureg.define('parsnip = 112 grams')
ureg.define('garlic_clove = 7 grams')
ureg.define('egg_large = 70 grams')
ureg.define('banana = 183 grams')
ureg.define('apple = 85 grams')
ureg.define('tea_bag = 2 grams')
ureg.define('leek = 200 grams')
ureg.define('can = 400 grams')
ureg.define('lettuce = 400 grams')
ureg.define('large_jar = 800 grams')
ureg.define('tomato = 62 grams')
ureg.define('slice = 10 grams')
ureg.define('unit = 1 grams')
ureg.define('potato = 150 grams')

def open_yaml(file):
    with open(file, 'r') as stream:
        try:
            data = yaml.load(stream)
            print(data)
        except yaml.YAMLError as exc:
            print(exc)
    return data
    
def amount_units(string):
    regex = r"(?P<number>\d+(\.\d+)?|(\.\d+)?)\s*(?P<unit>[a-zA-Z_]*)"

    test_str = ("0.4\n"
	".3 g\n"
	"0.3 g\n"
	"0.17\n"
	"0.3\n"
	"0.3\n"
	"0.2\n"
	"50ml\n"
	"50ml\n"
	"3.3 g\n"
	"5g")
#    try:
    matches = re.match(regex, str(string))
#    except:
#        import pdb; pdb.set_trace()

#    for matchNum, match in enumerate(matches):
#	matchNum = matchNum + 1
#	
#	print ("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))
#	
#	for groupNum in range(0, len(match.groups())):
#	    groupNum = groupNum + 1
#	    
#	    print ("Group {groupNum} found at {start}-{end}: {group}".format(groupNum = groupNum, start = match.start(groupNum), end = match.end(groupNum), group = match.group(groupNum)))
    
    gd = matches.groupdict()

    return (gd['number'], gd['unit'])


toget = dict()

class Ingredient():
    """A Class to store ingredients - hopefully also do unit conversions 
    if needed"""


    def __init__(self, name, value, unit):
        self.name = name

        if len(unit) > 0:
            self.value = value * ureg.parse_expression(unit)
        else:
            print "using name as unit"
            self.value = value * ureg.parse_expression(name)

    def add(self, value, unit):
        if len(unit) > 0:
            self.value = self.value + (value * ureg.parse_expression(unit))
        else:
            print "using name as unit"
            self.value = self.value + (value * ureg.parse_expression(self.name))

    def pr(self):
        return '{!s}'.format(self.value)

class Ingredients():
    """ All the ingredients """

    food = open_yaml("food.yaml")
    default_shop = "Tesco"
    shops = dict()

    def __init__(self):
        self.l = dict()

    def add(self, ingredient, value, unit):
        if ingredient in self.l.keys():
            #try:
            a = self.l[ingredient]
            a.add(value, unit)
            self.l[ingredient] = a
        #except:
        #        import pdb; pdb.set_trace()
        else:
            self.l[ingredient] = Ingredient(ingredient, value, unit)

    def all_byshop(self):
        output = ""
        for i in self.l.values():
            try:
              this_shop = self.food[i.name]['shop']
            except KeyError:
                this_shop = self.default_shop

            if this_shop in self.shops:
                self.shops[this_shop] = self.shops[this_shop] + "    [ ] {!s} {!s}\n".format(i.value, i.name)
            else:
                self.shops[this_shop] = "    [ ] {!s} {!s}\n".format(i.value, i.name)

        for shop in self.shops:
            output +=  "# %s\n" % (shop)
            output += self.shops[shop] + "\n"

        return output


ingredients = Ingredients()
menu = open_yaml(sys.argv[1])
for item in menu:
    skip = False
    try:
        people = int(menu[item]['people'])

        file = "recipe/" + item + ".yaml"
        recipe = open_yaml(file)
    except:
        print "Can't open %s as recipe... trying as single ingredient" % item
        (number, unit) = amount_units(menu[item])
        print "%20s: %8.2f %s" % (item, float(number), unit)
        ingredients.add(item, float(number), unit)
        print "skip ingredients"
        skip = True
        continue

    if not skip:
        f = open(item + ".md", "w")
        f.write("#{!s}\n".format(item))
        f.write("\n")

        # DO we have serves?
        serves = float(1)
        try:
            serves = float(recipe['serves'])
        except:
            pass

        for ingredient in recipe['ingredients']:
            amount = recipe['ingredients'][ingredient]
            (number, unit) = amount_units(amount)
            number = float(number) / serves
            f.write("%28s: %8.2f %s\n" % (ingredient, float(number) * people, unit))
            ingredients.add(ingredient, float(number) * people, unit)

    try:
        f.write("## Description\n")
        f.write(recipe['method'].encode('utf-8'))
        f.write("\n")
    except KeyError:
        pass

    f.close()

outfile = open("shoppinglist.md", "w")
outfile.write(ingredients.all_byshop())
outfile.close()


