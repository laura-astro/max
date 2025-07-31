# Max

(.max) Archive Reader and Sorter

This is a short python program that helps you sort out the useful lines in the archive from max. Below are a few lines of code for when you run this program on a Linux terminal, simply to clean the table and make it more accessible.

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
