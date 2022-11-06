# Tool for extracting all possible SoftwareVersionExternalIdentifiers from iOS app data.
# Supported files: "iTunesMetadata.plist"

mylines = []
foundids = []

with open ('iTunesMetadata.plist', 'rt') as myfile:
	for myline in myfile:
		mylines.append(myline)

outfile = open ('verextid-out.txt', 'wt')

i = 0
ret = 0
rtwo = 0
offs = 0
j = 0
count = 0
stringout = ''

for linex in mylines:

	# Look for this version's ID (a single ID)
	ret = linex.find("<key>softwareVersionExternalIdentifier</key>")
	if ret > -1:
		j = 0
		for liney in mylines:
			if j >= i:
				ret = liney.find("<integer>")
				rtwo = liney.find("</integer>")
				if ret > -1:
					stringout = mylines[j]
					if rtwo > -1:
						stringout = stringout[ret+9:rtwo:1] # Fix this later
					else:
						print("Unexpected: </integer> tag not on same line")
						stringout = stringout[ret+9::]
					count = count + 1
					foundids.append(stringout)
					break
			j = j + 1
		# end of for-loop

	# Look for array of IDs (undefined quantity)
	ret = linex.find("<key>softwareVersionExternalIdentifiers</key>")
	if ret > -1:
		j = 0
		for liney in mylines:
			if j >= i:
				ret = liney.find("</array>")
				if ret > -1:
					break # Break at end of array
				ret = liney.find("<integer>")
				rtwo = liney.find("</integer>")
				if ret > -1:
					stringout = mylines[j]
					if rtwo > -1:
						stringout = stringout[ret+9:rtwo:1]
					else:
						print("Unexpected: </integer> tag not on same line")
						stringout = stringout[ret+9::]
					count = count + 1
					foundids.append(stringout)
			j = j + 1
		# end of for-loop

	i = i + 1
# end of for-loop

print(count)

# Remove duplicates, copy to outfile
arrindexskip = []
k = 0
i = 0
while i < len(foundids):

	goodtogo = 1
	j = i
	for k in arrindexskip:
		if j == k:
			goodtogo = 0

	if goodtogo == 1:

		outfile.write(foundids[i])
		outfile.write('\n')

		# find indices of duplicates, exclude them when that while-loop runs in the future
		j = 0
		while j < len(foundids):
			if foundids[i] == foundids[j] and j != i:
				count = count - 1
				arrindexskip.append(j)
			j = j + 1

	i = i + 1
# end of while-loop


outfile.close()
print("IDs Found:")
print(count)
print("Done")
