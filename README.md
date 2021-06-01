# fix_df_map
Create multiple json files from 1 big file of map exported.

First create map.json in folder where command will be executed using data from cliboard and unix tool:

`xsel --clipboard > ~/map.json`

to run script:

`python3 fixit.py`

Paste data from file to clipboard:

`cat ./df_chunked_1.json | xclip -selection c`
