CC=g++

LIBS=""

for f in /opt/ros/noetic/lib/lib*; do
	if [ -f ${f} ]; then 
		LIBS=$(echo $LIBS -l:$(basename ${f}))
	fi
done

echo $LIBS

$CC -o build/robot src/*.cpp -I/opt/ros/noetic/include -L/opt/ros/noetic/lib/ $LIBS
