Mass Catering - menu compiler
=============================

The basic use of this is to take a bunch of recipes work out the quantities for the number of servings requested, and finally produce scaled up versions of each recipe as well as a complete shopping list.

Example usage:

```
python compile_menu.py menu/weekend.yaml

```


Compile md to pdf requires pandoc and latex installations.

# Standards
Convention when creating a recipe, is that all ingredients are defined in the singular. 


# Required modules

pint

yaml