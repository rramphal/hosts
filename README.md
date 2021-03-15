# `hosts`

## Lists

Type | URL
---- | ---
All  | https://raw.githubusercontent.com/rramphal/hosts/master/lists/blacklist

## Updating

Update relevant file in `/lists` or create a new file with the `.txt` extension.
If you create a new file, please have a descriptive comment that starts with `#` as the first line of the file.
When listing domains, only list the domain itself.
Then run `node generate.js` to generate lists.

NOTE: `www.` is prepended to all domains automatically.
