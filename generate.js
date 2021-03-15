const path = require('path');
const fs   = require('fs');

const INPUT_DIRECTORY = path.join(__dirname, 'data');
const OUTPUT_FILEPATH = path.join(__dirname, 'lists', 'blacklist');

const PREAMBLE = `
# Source: https://raw.githubusercontent.com/rramphal/hosts/master/lists/blacklist

`;

const POSTAMBLE = `
# Last updated: ${getDate()}
`;

function getDate () {
  return new Date().toLocaleString('sv-SE', {
    year     : 'numeric',
    month    : '2-digit',
    day      : '2-digit',
    hour     : '2-digit',
    minute   : '2-digit',
    hour12   : false,
    timeZone : 'America/Chicago'
  });
}

function formatDomain (domain) {
  return [
    `0.0.0.0 ${domain}`,
    `0.0.0.0 www.${domain}`,
  ].join('\n');
}

function pad (input) {
  return `[${input}]`.padEnd(12);
}


const all_files = fs.readdirSync(INPUT_DIRECTORY);

const files = all_files
  .filter((filename) => filename.endsWith('.txt')) // only `.txt` files
  .filter((filename) => !filename.startsWith('.')) // no hidden files
;

const output = [];

files.forEach((fileName) => {
  const filePath = path.join(INPUT_DIRECTORY, fileName);

  console.log(pad('PROCESSING'), filePath);

  const data     = fs.readFileSync(filePath, 'utf8').toString();
  const lines    = data.split('\n');

  lines.forEach((line) => {
    const trimmedLine = line.trim();

    if (trimmedLine.startsWith('#') || trimmedLine.length === 0) {
      output.push(trimmedLine);
    } else {
      output.push(formatDomain(trimmedLine));
    }
  });
});

console.log(pad('WRITING'), OUTPUT_FILEPATH);

fs.writeFileSync(OUTPUT_FILEPATH, PREAMBLE + output.join('\n') + POSTAMBLE);

console.log(pad('DONE'));
