const fs = require('fs');
const path = require('path');

function walk(dir) {
    let results = [];
    const list = fs.readdirSync(dir);
    list.forEach(function(file) {
        file = dir + '/' + file;
        const stat = fs.statSync(file);
        if (stat && stat.isDirectory()) { 
            results = results.concat(walk(file));
        } else { 
            if (file.endsWith('.html')) results.push(file);
        }
    });
    return results;
}

const files = walk('.');
let changed = 0;
files.forEach(file => {
    let content = fs.readFileSync(file, 'utf8');
    let orig = content;
    content = content.replace(/<div class="logo-mark"><span>BU<\/span><\/div>/g, '');
    content = content.replace(/<div class="pcm"><span>BU<\/span><\/div>/g, '');
    if (content !== orig) {
        fs.writeFileSync(file, content, 'utf8');
        changed++;
    }
});
console.log(`Updated ${changed} files.`);
