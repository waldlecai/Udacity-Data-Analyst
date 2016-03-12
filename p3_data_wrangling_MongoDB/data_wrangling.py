#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
from collections import defaultdict
import pprint
import re
import codecs
import json

OSMFILE = "hong-kong_china.osm"
#OSMFILE = "hong-kong_china_sample.osm" # sample file
# regular expression for matching key formats in 'tag' tags
# lower: tag with lower case char
# lower_colon: tag with lower case char and single colon
# laddr_colon: address tag with single colon
# addr_2colon: address tag with double colons 
# problemchars: tag with invalid chars
# non-standard phone number in Hongkong
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
upper = re.compile(r'^([A-Z]|_)*$')
addr_colon = re.compile(r'^(addr):([a-z]*)$')
addr_2colon = re.compile(r'^(addr):([a-z]*):([a-z]*)$')
name_key = re.compile(r'^(name)$')
name_colon = re.compile(r'^(name):([a-z]*)$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
non_standard_phone_num = re.compile(r'(\d\d\d\d)\s*(\d\d\d\d)') 

# regular expression for matching street type
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

# regular expression for matching color key
color_key_re = re.compile(r'^[Cc]olo[u]*r$')

# not complete list but most expected street type in Hongkong
expected_street = ["Street", "Road", "Circuit", "Crescent", "Lane", "Boulevard", "Path", "Court", "DaDao", "Drive", "Avenue", "Bay", "Central", "Square"]

# mapping of bad street names to better one
street_mapping = { 
			"St": "Street",
			"AVE": "Avenue",
			"Rd": "Road"
			}

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]

# function to count all tags in OSM file
# input: full path of OSM file
# output: dictionary containing all tags
def count_tags(filename):
    tags_dict = {}
    for _, elem in ET.iterparse(filename):
        if elem.tag in tags_dict:
            tags_dict[elem.tag] += 1
        else:
            tags_dict[elem.tag] = 1
    return tags_dict

# function to count key format and actual str in a single 'tag' element
# input: element of OSM xml file
#        dict of key formats and counts
#        dict of actual keys and counts
#        dict of bad keys
# output: dict of key formats and counts 
#         dict of actual keys and counts
def key_type(element, format_dict, keys_dict):
	if element.tag == "tag":
		
		# count various key format
		k = element.attrib['k']
		if problemchars.match(k):
			format_dict['problemchars'] += 1
		elif addr_colon.match(k):
			format_dict['addr_colon'] += 1
		elif addr_2colon.match(k):
			format_dict['addr_2colon'] += 1
		elif lower_colon.match(k):
			format_dict['lower_colon'] += 1
		elif lower.match(k):
			format_dict['lower'] += 1
		elif upper.match(k):
			format_dict['upper'] += 1
		else:
			format_dict['other'] += 1

		# count actual keys
		if k in keys_dict:
			keys_dict[k] += 1
		else:
			keys_dict[k] = 1
	return (format_dict, keys_dict)

def find_problem_key(element, problem_keys):
	if element.tag == "tag":
		k = element.attrib['k']
		if upper.match(k):
			problem_keys["upper_case_key"].add(k)

		# check if it's color key
		m = color_key_re.search(k)
		if m:
			problem_keys['color_key'].add(k)

		return problem_keys

# function to audit keys of 'tag' tags in entire OSM file
# input: full path of OSM file
# output: dict of key formats and counts 
#         dict of actual keys and counts
def audit_keys(filename):
	keys_dict = {}
	problem_keys = defaultdict(set)
	formats_dict = {"upper": 0, "lower": 0, "lower_colon": 0, "addr_colon": 0, "addr_2colon": 0, "problemchars": 0, "other": 0}
	for _, element in ET.iterparse(filename):
		formats_dict, keys_dict = key_type(element, formats_dict, keys_dict)
		find_problem_key(element, problem_keys)

	return formats_dict, keys_dict, problem_keys

# function to check if a key of 'tag' tag is a street name
# input: element of OSM xml file
# output: boolean value of checking result
def is_street_name(elem):
	return "addr:street" in elem.attrib['k']

# function to audit street type in a single 'tag' tag
# input: street type dict for storing uncommon types
#        street name to be audited
# output: street type dict storing uncommon types 
def audit_street_type(street_types, street_name):
	m =street_type_re.search(street_name)
	if m:
		street_type = m.group()
		if street_type not in expected_street:
			street_types[street_type].add(street_name)
	return street_types

# function to audit 'way' tag in entire OSM file
# input: full path of OSM file
# output: street type dict storing uncommon types in entire OSM file
def audit_way(filename):
	street_types = defaultdict(set)
	for event, elem in ET.iterparse(filename, events=("start", )):
		if elem.tag == "way":
			for tag in elem.iter("tag"):
				if is_street_name(tag):
					audit_street_type(street_types, tag.attrib['v'])
	return street_types


# function to update bad street names to better ones
# input: original bad street name
# output: updated better street name
def update_name(name, mapping):
    for bad, good in mapping.iteritems():
        if name.find(bad) > 0:
            name = re.sub(r'\b' + bad + r'\b', mapping[bad], name)
            break
    return name

# function to 1. standarize various color keys to 'color'
# and to 2. convert upper case keys to lower cases
# input: key in question
# output: updated key
def update_key(key):
	key = key.lower() # update keys in upper case
	m = color_key_re.search(key)
	if m:
		return 'color'
	return key

# function to standardize phone number format: 
# +XXX YYYY YYYY ('+XXX': country/area code; 'YYYY YYYY': phone number)
# input: phone number
# ouput: updated number
def update_phone(phone):
	m = non_standard_phone_num.match(phone)
	if m > 0:
		return "+852 {} {}".format(m.group(1), m.group(2))
	return phone

# function to process 'tag' tag within 'node' and 'way' element
# input: 'tag' element; 
# output: 
def process_tag(elem, node, address, name):
	key = update_key(elem.attrib['k']) 					# fix key issue if any
	value = elem.attrib['v']
	if key == 'phone':
		value = update_phone(value)						# fix phone format issue if any
	if "addr:street" in key:
		value = update_name(value, street_mapping) 		# fix street name issue if any
	if addr_colon.match(key):							# put all address key/value into one dict
		address[addr_colon.match(key).group(2)] = value
	elif problemchars.match(key): 						# ignore problematic keys
		return
	elif addr_2colon.match(key): 						# ignore 'addr:xx:xx' keys
		return
	elif name_key.match(key): 							# below four lines put all name key/value into one dict 
		name['default'] = value
	elif name_colon.match(key):
			name[name_colon.match(key).group(2)] = value
	elif lower_colon.match(key):
		node[key] = value
	else:
		node[key] = value

# function to convert OSM file element into a predefined data model
# input: single element in OSM file
# ouput: new node in predefined data model
def shape_element(element):
    node = {}
    if element.tag == "node" or element.tag == "way" :
        
    	# data containers for node
        created = defaultdict(dict)
        pos = []
        node_refs = []
        address = defaultdict(dict)
        name = defaultdict(dict)


        node['type'] = element.tag

        # process attributes of 'node' and 'way' element
        for attr_name, attr_value in element.items():
            if attr_name in CREATED:
                created[attr_name] = attr_value
            elif attr_name == "lat":
                pos.insert(0, float(attr_value))
            elif attr_name == "lon":
                pos.insert(1, float(attr_value))
            else:
                node[attr_name] = attr_value
                
        # process sub elements of 'node' and 'way' element
        for elem in element.iter('*'):
            if elem.tag == 'tag':
            	process_tag(elem, node, address, name) 
            elif elem.tag == 'nd':
                node_refs.append(elem.get('ref'))
        
        # add data containers to node if not empty
        if len(pos) != 0:
            node['pos'] = pos
        if len(created) != 0:
            node['created'] = created
        if len(address) != 0:
            node['address'] = address
        if len(node_refs) != 0:
            node['node_refs'] = node_refs
        if len(name) != 0:
        	node['name'] = name
        
        return node
    else:
        return None


def process_map(file_in, pretty = False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data

# main function: type 'python data_wrangling.py' in command prompt to execute
if __name__ == "__main__":
	
	print("Please key in following number to perform corresponding task:")
	print("1: audit keys format")
	print("2: audit keys and their counts")
	print("3: audit street names ")
	print("4: diplay data fixes (not in acutal json file)")
	print("5: transform to predefined json data model (including data fixes)")
	print("0: exit")

	while True:
		input_var = raw_input("Please select the option: ")
		if input_var.isdigit():
			if int(input_var) not in range(0, 6):
				continue
			else:
				break
		else:
			continue

	if input_var == '1':
		# audit 'tag' keys format
		formats, _, _ = audit_keys(OSMFILE)
		pprint.pprint(formats)
	elif input_var == '2':
		# audit 'tag' keys and counts
		_, keys, _ = audit_keys(OSMFILE)
		pprint.pprint(keys)
	elif input_var == '3':
		# audit 'way' element and print out those uncommon ones
		street_types = audit_way(OSMFILE)
		pprint.pprint(dict(street_types))
	elif input_var == '4':
		# showing street name issue fixes
		print("####### Data fixes for Street Name #######")
		street_types = audit_way(OSMFILE)
		for st_type, ways in street_types.iteritems():
			for name in ways:
				better_name = update_name(name, street_mapping)
				if better_name != name:
					print name, "=>", better_name

		# showing key issue fixes
		print("####### Data fixes for 'tag' tag's key #######")
		_, _, problem_keys = audit_keys(OSMFILE)
		for issue, tag_keys in problem_keys.iteritems():
			for tag_key in tag_keys:
				better_key = update_key(tag_key)
				if better_key != tag_key:
					print tag_key, "=>", better_key

	elif input_var == '5':
		# transform OSM file into predefined json data model
		# include data fixes that have been identified
		process_map(OSMFILE, pretty=False)

