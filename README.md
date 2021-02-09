# Findsecrets
Recursively scans a local directory for common secret keywords and strings

## Update Feb 2021
Total makeover. Removed confusing modular / class oriented code. All the magic now in findsecrets.py

## Instructions
Only works with python 3.x

```pip install -r requirements.txt```<br>
```python findsecrets.py```

## Configuration
Edit config.yml for the scanfolder and exclusions

## To-Do's:

*   Commandline arguments
*   JSON Report output (for SEQHUB) incl. Masking of found secrets
*   Value checks based on known secret regexes
