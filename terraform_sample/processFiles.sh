#!/bin/bash

# full path to directory that contains the files to be processed
dirName="${1}"

# get the list of files and write to a file in pwd
find "${dirName}/" -maxdepth 1 -type f > "fileNames.lst"
origFileCount=$(wc -l "fileNames.lst")
echo "*******   Original File Count  *******"
echo "*******     ${origFileCount}   *******"
echo "**************************************"

# process the files as specified
fileCount=0
while IFS= read -r line
do
	  # take action on $line #
	    #echo "$line"
	      baseFilename=$(basename "${line}")

	        # get the year/month/day/FScode
		  fileYear=$(echo "${baseFilename}" | awk -F  "." '/1/ {print substr($2,5,2)}')
		    fileMonth=$(echo "${baseFilename}" | awk -F  "." '/1/ {print substr($2,3,2)}')
		      fileDay=$(echo "${baseFilename}" | awk -F  "." '/1/ {print substr($2,1,2)}')
		        fileCode=$(echo "${baseFilename}" | awk -F  "." '/1/ {print $1}')
			  # echo "Dir to create: ${fileYear}/${fileMonth}/${fileDay}/${fileCode}"
			    newDir=${fileYear}/${fileMonth}/${fileDay}/${fileCode}

			      # create the directory
			        mkdir -p "${dirName}/${newDir}"
				  mv "${line}" "${dirName}/${newDir}/"
				    ((fileCount+=1))
			    done < "fileNames.lst"

			    # Results
			    echo "*******    Files Moved Count    *******"
			    echo "*******      ${fileCount}       *******"
			    echo "***************************************"
