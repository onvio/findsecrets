# Findsecrets
Recursively scans a local directory for common secret keywords and strings

## Configuration
Edit config.yml for the scanfolder and exclusions.\
The scanfolder in config.yml will automatically overridden by the "-f" cmdline argument so chose either

## Instructions
Only works with Python 3.x

```pip install -r requirements.txt```<br>
```python findsecrets.py -f <folder> -v```
```
optional arguments:
  -h, --help                    show this help message and exit
  -f, --folder FOLDER           Local Folder to scan / Cloned Repo
  -e, --exclude                 Comma separated list of files to exclude
  -m, --mask                    Mask Secrets (Default = False)
  -v, --verbose                 Verbose output, shows secrets in STDOUT / Console (Default = False)
```

Docker

```
docker pull seqhub/findsecrets
docker run --rm -v $(pwd):/wrk -t seqhub/findsecrets -f /wrk -r /wrk/findsecrets-reports -v

## Reports
Reports are automatically saved in the current folder:
```
report.json
seqhubreport.json // for SEQHUB parsing
```

## To-Do's:
*   Git commit scanning, history, multiple branches etc. same as gitleaks.
*   Value checks based on known secret regexes
*   XML / JSON / YAML Parser, Traverse trough Key/Values to get secret pairs