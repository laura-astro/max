# Max

(.max) File Reader and Sorter

This is a short python program that helps you sort out the useful lines in your max file. Below are a few lines of code for when you run this program on a Linux terminal, simply to clean the table and make it more accessible.

Notice that the original max file will have 6 columns (3 numbers, 3 units) and blank spaces in the beginning of every line.

Use this line of code to get rid of the blank spaces first:

```bash
sed -i 's/^[ \t]*//' example.max
```

Use this line of code to clean the table and keep only numbers as valid columns:

```bash
awk '{$2=""; $0=$0; print}' example.max > tmp && mv tmp example.max
```

Notice that this example only removes column 2 (unit) in the original file, you shall redo this step two more times. If you're interested in backing up the file first, then use:

```bash
cp example.max backup-example.max
```

## Results

The program will generate both a graph and a table simultaneously, so you can compare the results.

![graph](https://github.com/laura-astro/max/blob/main/graph.png)
![terminal](https://github.com/laura-astro/max/blob/main/linux-terminal.png)

You can search through the original max table based on the "Y Max" column and compare it to the "X Max" column to make sure they match.

## Parameters

- Data file: example.max  
- X Column: 0  
- Y Column: 2 (if you keep the period column in the original file, otherwise use 1)  
- Minimum A0 value (fap): use the first 3 digits or less (use 1.66 instead of 1.6659841) or round it to an approximate value such as 1.7, I suggest the approximation or an integer  
- Minimum length (X units): when the peaks are very close together and are not part of the same peak when you zoom in, use 1; when you zoom in and notice one peak is made of many smaller peaks forming a Gaussian curve, then it has to be more ample, use 4 or 5.

_*In the graph above, the minimum length was 5._
