while getopts f:t:o: flag
do
	case "${flag}" in
		f) from=${OPTARG};;
		t) to=${OPTARG};;
		o) output=${OPTARG};;
	esac
done

now=`python3 -c 'from time import time; print (int(round(time() * 1000)))'`
echo $now $from $to >> $output
