# `hosts`

## Lists

Type | URL
---- | ---
All  | https://raw.githubusercontent.com/rramphal/hosts/master/lists/blacklist

## Updating

1. Update relevant file in `/data` or create a new file with the `.txt` extension.
2. Run `node generate.js` to generate lists.

### Guidelines

* `www.` is prepended to all domains automatically.
* Each file in `/data` must have a descriptive comment that starts with `#` as the first line of the file.
* Each file in `/data` must end with a blank line.
* When listing domains, only list the domain itself.
