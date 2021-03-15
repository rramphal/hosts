const path = require('path');
const fs   = require('fs');

const INPUT_DIRECTORY  = path.join(__dirname, 'data');
const OUTPUT_DIRECTORY = path.join(__dirname, 'lists');

const LISTS = [
  {
    name   : 'all',
    filter : (filenames) => {
      return filenames
        .filter((filename) => !filename.startsWith('.')) // no hidden files
        .filter((filename) => filename.endsWith('.txt')) // only `.txt` files
      ;
    },
  },
  {
    name   : 'blacklist',
    filter : (filenames) => {
      return filenames
        .filter((filename) => !filename.startsWith('.'))        // no hidden files
        .filter((filename) => filename.endsWith('.txt'))        // only `.txt` files
        .filter((filename) => !filename.includes('toggleable')) // no toggleable files
      ;
    },
  },
  {
    name   : 'toggleable',
    filter : (filenames) => {
      return filenames
        .filter((filename) => filename.endsWith('.txt'))       // only `.txt` files
        .filter((filename) => !filename.startsWith('.'))       // no hidden files
        .filter((filename) => filename.includes('toggleable')) // only toggleable files
      ;
    },
  },
];

function getDate () {
  return new Date().toLocaleString('sv-SE', {
    year     : 'numeric',
    month    : '2-digit',
    day      : '2-digit',
    hour     : '2-digit',
    minute   : '2-digit',
    hour12   : false,
    timeZone : 'America/Chicago',
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

console.log();

LISTS.forEach(({ name, filter }) => {
  const preamble  = `\n# Source: https://raw.githubusercontent.com/rramphal/hosts/master/lists/${name}\n\n`;
  const postamble = `\n# Last updated: ${getDate()}\n`;

  const allFiles = fs.readdirSync(INPUT_DIRECTORY);
  const files    = filter(allFiles);

  const output = [];

  console.log(pad('LIST'), name);

  files.forEach((fileName) => {
    const filePath = path.join(INPUT_DIRECTORY, fileName);

    console.log(pad('PROCESSING'), filePath);

    const data  = fs.readFileSync(filePath, 'utf8').toString();
    const lines = data.split('\n');

    lines.forEach((line) => {
      const trimmedLine = line.trim();

      if (trimmedLine.startsWith('#') || trimmedLine.length === 0) {
        output.push(trimmedLine);
      } else {
        output.push(formatDomain(trimmedLine));
      }
    });
  });

  const outputFilepath = path.join(OUTPUT_DIRECTORY, name);

  console.log(pad('WRITING'), outputFilepath);

  fs.writeFileSync(outputFilepath, preamble + output.join('\n') + postamble);

  console.log(pad('DONE'));
  console.log();
});
