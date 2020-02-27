#Wipes the csv file from previous run
#> /home/justin/code/bee/YL.csv
#> /home/justin/code/bee/YR.csv

#Cycles the python count software thru the directory specified by the arg
#Executes simultaenously to save time
#$1 is the pass thru argument

#12/4/19 testing BeeCount8Texture.py instead of BeeCount7.py
for file in $1/*.h264; do
    
    python3 /home/justin/code/bee/BeeCount9.py "$file" left & 
    python3 /home/justin/code/bee/BeeCount9.py "$file" right &

    
    wait
done

#Runs dataplot software
python3 /home/justin/code/bee/Data.py "left" "$file" &
python3 /home/justin/code/bee/Data.py "right" "$file" &
python3 /home/justin/code/bee/DIFF.py "$file" &
python3 /home/justin/code/bee/SMOOTH.py "$file" &
wait
