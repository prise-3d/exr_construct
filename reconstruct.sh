declare -a scenes 
#scenes=( "barcelona-pavilion" "bmw-m6" "breakfast" "chopper-titan" "coffee-splash" "crown" "white-room" )
scenes=( "pavilion-day" "breakfast" "chopper-titan" "splash" "crown" )


for scene in ${scenes[@]}; do
	echo ${scene}
	python exr_construct.py -s 5 -o ../data/pbrt-scenes/reconstructed-scenes/${scene} -i 10 -I ../data/pbrt-scenes/generated-scenes/${scene}/
done
