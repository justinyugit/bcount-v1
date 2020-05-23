#Wipes the csv file from previous run
#> /home/justin/code/bee/YL.csv
#> /home/justin/code/bee/YR.csv

#Cycles the python count software thru the directory specified by the arg
#Executes simultaenously to save time
#$1 is the pass thru argument


#Runs beecount software; replace PATH.

for file in $1/*.h264; do
    
    python3 /PATH/BeeCount9.py "$file" left & 
    python3 /PATH/BeeCount9.py "$file" right &

    
    wait
done

#Runs dataplot software; replace PATH.

python3 /PATH/Data.py "left" "$file" &
python3 /PATH/Data.py "right" "$file" &
python3 /PATH/DIFF.py "$file" &
python3 /PATH/SMOOTH.py "$file" &
wait
