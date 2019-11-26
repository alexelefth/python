#!/usr/bin/python3
import pprint
import argparse
import os
import collections
#from dict2xml import dict2xml as xmlify

parser = argparse.ArgumentParser(description="OSS handling automation script")
parser.add_argument('-f', '--file', metavar='FILE', type=str, help='licence.manifest file from yocto',required=True)
parser.add_argument('-t', '--type', metavar='TYPE', type=str, help='file type: txt or html',required=True)
parser.add_argument('-o', '--out', metavar='OUTPUT', type=str, help='output file name',required=True)
args = parser.parse_args()
#print(args)
pwd = os.getcwd()
LicenseManifest = args.file
FileType = args.type
Output = args.out
OutputFile = os.path.join(pwd,Output)
filepath = os.path.join(pwd, LicenseManifest)
#filepath = os.path.join(pwd, "license.manifest")

################# collect recipes #####################
with open(filepath) as fp:
	#read all lines
	lines = (line.rstrip() for line in fp)
	#skip blank lines
	lines = list(line for line in lines if line)
	packets = list()
	#print(lines)
	for line in lines:
		if line.startswith('RECIPE'):
			packets.append(line.replace('RECIPE NAME: ',''))

#######################################################

################# collect versions #####################
with open(filepath) as fp:
        #read all lines
        lines = (line.rstrip() for line in fp)
        #skip blank lines
        lines = list(line for line in lines if line)
        versions = list()
        #print(lines)
        for line in lines:
                if line.startswith('PACKAGE VERSION'):
                        versions.append(line.replace('PACKAGE VERSION: ',''))
#######################################################

################### collect licenses ##################
with open(filepath) as fp:
        #read all lines
        lines = (line.rstrip() for line in fp)
        #skip blank lines
        lines = list(line for line in lines if line)
        licenses = list()
        #print(lines)
        for line in lines:
                if line.startswith('LICENSE'):
                        licenses.append(line.replace('LICENSE: ',''))
#######################################################

############### collect subcomponents #################
with open(filepath) as fp:
        lines = (line.rstrip() for line in fp)
        lines = list(line for line in lines if line)
        subcomponents = list()
        for line in lines:
                if line.startswith('PACKAGE NAME'):
                        subcomponents.append(line.replace('PACKAGE NAME: ',''))

sub_length = len(subcomponents)
#######################################################

############### map recipes to licenses ################
map_rec_lic = {}
for i in range(len(packets)):
	map_rec_lic[packets[i]] = licenses[i]

od_map_rec_lic = collections.OrderedDict(sorted(map_rec_lic.items()))
#print(od_map_rec_lic)
############### map recipes to versions ################
map_rec_ver = {}
for i in range(len(packets)):
	map_rec_ver[packets[i]] = versions[i]

packets_length = len(map_rec_ver)
od_map_rec_ver = collections.OrderedDict(sorted(map_rec_ver.items()))
#print(od_map_rec_ver)
########### map packages to their recipes ##############
map_pack_rec = {}
for i in range(len(packets)):
	map_pack_rec[packets[i]] = []
for i in range(len(packets)):
        map_pack_rec[packets[i]].append(subcomponents[i])

od_map_pack_rec = collections.OrderedDict(sorted(map_pack_rec.items()))
#######################################################

#pprint.pprint(map_rec_lic)
'''
i=1
for key,value in map_rec_lic.items():
	print("{}. Package: {} | License: {} | Version: {}".format(i,key,value,map_rec_ver[key]))
	i+=1
'''
if FileType == 'html':
	fh = open(OutputFile,"w+")
	i=1
	fh.write('<!DOCTYPE html>\n<html>\n<head>')
	fh.write('<!DOCTYPE html>\n<html>\n<head>')
	fh.write('<style>table,th,td { border: 1px solid black; border-collapse: collapse;} th,td {padding: 5px;} th {text-align: left;}</style>')
	fh.write('</head><body>')
	fh.write('\n<table style="width:100%">')
	fh.write('\n<tr>\n<th>No\n</th>\n<th>Package (%s)\n</th>\n<th>Version\n</th>\n<th>License\n</th>\n<th>Subcomponents (%s)</th>\n</tr>' % (packets_length,sub_length))
	for key,value in od_map_rec_lic.items():
		fh.write("<tr>\n<td>%d</td>\n<td>%s</td>\n<td>%s</td>\n<td>%s</td>\n<td>%s</td>\n<tr>" % (i,key,od_map_rec_ver[key],value,od_map_pack_rec[key]))
		i+=1
	fh.write('</table')
	fh.write('</body></html>')
	fh.close()
elif FileType == 'txt':
	fh = open(OutputFile,"w+")
	i=1
	for key,value in od_map_rec_lic.items():
	        #fh.write("%s %s %s\n" % (key,od_map_rec_ver[key],value))
	        fh.write("%s %s\n" % (key,od_map_rec_ver[key]))
	        i+=1
	fh.close()

#print(xmlify(map_rec_lic, wrap="all",indent=" "))
