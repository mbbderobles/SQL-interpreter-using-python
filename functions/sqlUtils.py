# Collection of extra functions

import readMeta

#desc statement
def descTable(tbl):
	tb = readMeta.tb
	print("==========================================================================================")
	print("\tColumn Name\t\tType\t\tSize\t\tPrimary Key")
	print("==========================================================================================")
	for k in tb[tbl].keys():
		print("%20s%20s%20s%20s " % (tb[tbl][k][0], tb[tbl][k][1], tb[tbl][k][2], tb[tbl][k][3]))
	print("==========================================================================================")
	print()

