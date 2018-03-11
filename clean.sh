#!/usr/bin/env bash


echo "Delete all unnecessary files from this repository:"

function deleteAllFiles {

	for fileExtension in $@; do

		echo "-> Delete all ${fileExtension} files ..."

		for d in ./*.$fileExtension ; do
			rm -f $d
		done

		for d in */*.$fileExtension ; do
			rm -f $d
		done

	done

}

deleteAllFiles aux toc log gz out

echo "Repository successfully cleaned"
