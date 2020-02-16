#!/usr/bin/env python3

import yaml
import re
import sys
import os
import pdb
from pint import UnitRegistry

compile_pandoc = True

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
ureg.define('potato = 150 grams')
ureg.define('unit = 1 grams')


# 1 tsp smoked paprika = 3.3g
# 9 cloves garlic in a bulb

def open_yaml(file):
    with open(file, 'r') as stream:
        try:
            data = yaml.load(stream)
            # print(data)
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
            print("using " + name + " as unit")
            self.value = value * ureg.parse_expression(name)
            # self.value = value * ureg.parse_expression('unit')

    def add(self, value, unit):
        if len(unit) > 0:
            self.value = self.value + (value * ureg.parse_expression(unit))
        else:
            print("using " + self.name + " as unit")
            self.value = self.value + (value * ureg.parse_expression(self.name))
            # self.value = self.value + (value * ureg.parse_expression('unit'))

    def pr(self):
        return '{!s}'.format(self.value)

class Ingredients():
    """ All the ingredients """

    food = open_yaml("food.yaml")
    default_shop = "Supermarket"
    shops = dict()

    # Unit equivalents.
    equi = dict()
    equi['onions'] = ['onion']
    equi['celery'] = ['celery_sticks']
    equi['carrots'] = ['carrot']
    equi['garlic_cloves'] = ['garlic']
    equi['garlic_cloves'] = ['garlic_clove']
    equi['tomato'] = ['tomatoes']


    def __init__(self):
        self.list = dict()

    def add(self, ingredient, value, unit):
        ingredient = self.equivalent_check(ingredient)
        if ingredient in self.list:
            #try:
            a = self.list[ingredient]
            print("Adding %s %s: %s" % (value, unit, ingredient))
            a.add(value, unit)
            self.list[ingredient] = a
        else:
            print("Adding %s %s: %s" % (value, unit, ingredient))
            self.list[ingredient] = Ingredient(ingredient, value, unit)

    def equivalent_check(self, ingredient):
        for equivalent in self.equi:
            if ingredient in self.equi[equivalent]:
                return equivalent

        return ingredient

    def all_byshop(self):
        output = "# Shopping List\n\n"
        for item_ in sorted(self.list):
            item = self.list[item_]
            try:
              this_shop = self.food[item.name]['shop']
            except KeyError:
                this_shop = self.default_shop

            if this_shop in self.shops:
                self.shops[this_shop] = self.shops[this_shop] + "    [ ] {!s} {!s}\n".format(round(item.value,2), item.name)
            else:
                self.shops[this_shop] = "    [ ] {!s} {!s}\n".format(item.value, item.name)

        for shop in self.shops:
            output +=  "## %s\n" % (shop)
            output += self.shops[shop] + "\n"

        return output


ingredients = Ingredients()
menu = open_yaml(sys.argv[1])
folderName = 'output/' + sys.argv[1].split('/')[-1].split('.')[0] + '/'
# os.mkdir(folderName)
# pdb.set_trace()
for item in menu:
    skip = False
    try:
        # if 'people' not in menu[item]: #Assume listing days, rather than just people
        #     menu[item]['people'] = 0
        #     for day in menu[item]:
        #         menu[item]['people'] += int(menu[item][day])
        # people = int(menu[item]['people'])
        file = "recipe/" + item + ".yaml"
        recipe = open_yaml(file)
    except:
        # not very elegant
        print("Can't open %s as recipe... trying as single ingredient" % item)
        (number, unit) = amount_units(menu[item])
        # pdb.set_trace()
        if unit == '':
            unit = 'unit'
        print("%20s: %8.2f %s" % (item, float(number), unit))
        ingredients.add(item, float(number), unit)
        print("skip ingredients")
        skip = True
        continue

    if not skip:
        for day in menu[item]:
            people = int(menu[item][day])
            if day == 'people':
                day = 'All'
            mdname = day+'_'+os.path.basename(item + ".md")
            print(mdname)

            f = open(folderName + mdname, "w")
            f.write("# {!s} {!s}\n".format(day, recipe['name']))
            f.write("\n")

            # DO we have serves?
            if 'serves' in recipe:
                serves = float(recipe['serves'])
                f.write("### Serves: {!s}\n".format(people))
                f.write("\n")
            else:
                serves = float(1)

            f.write("### Ingredients: \n")
            f.write("\n")
            for ingredient in recipe['ingredients']:
                amount = recipe['ingredients'][ingredient]
                (number, unit) = amount_units(amount)
                number = float(number) / serves
                f.write("%28s: %8.2f %s\n" % (ingredient, float(number) * people, unit))
                ingredients.add(ingredient, float(number) * people, unit)

            if 'method' in recipe:
                try:
                    f.write("### Description\n")
                    f.write(recipe['method'])#.encode('utf-8'))
                    f.write("\n")
                except:
                    pass
            
            f.write("\n\pagebreak")
            f.close()

outfile = open(folderName + "shoppinglist.md", "w")
outfile.write(ingredients.all_byshop())
outfile.write('\pagebreak')
outfile.close()

if compile_pandoc:
    # print('not implemented yet')
    os.system("pandoc {!s}*.md --pdf-engine=xelatex -o {!s}All_Recipe.pdf".format(folderName,folderName))


