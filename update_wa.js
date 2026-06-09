const fs = require('fs');
const path = require('path');

function walk(dir) {
    let results = [];
    const list = fs.readdirSync(dir);
    list.forEach(function(file) {
        file = dir + '/' + file;
        const stat = fs.statSync(file);
        if (stat && stat.isDirectory()) { 
            if (!file.includes('node_modules')) {
                results = results.concat(walk(file));
            }
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
    
    // Replace href="#" class="btn btn-wa"
    content = content.replace(/href="#"(\s+class="btn btn-wa")/g, 'href="https://wa.me/916290746602" target="_blank"$1');
    content = content.replace(/class="btn btn-wa"(\s+)href="#"/g, 'class="btn btn-wa"$1href="https://wa.me/916290746602" target="_blank"');
    
    // Replace href="#" aria-label="WhatsApp"
    content = content.replace(/href="#"(\s+aria-label="WhatsApp")/g, 'href="https://wa.me/916290746602" target="_blank"$1');
    
    // Replace href="#" class="wa-float"
    content = content.replace(/href="#"(\s+class="wa-float")/g, 'href="https://wa.me/916290746602" target="_blank"$1');
    content = content.replace(/class="wa-float"(\s+)href="#"/g, 'class="wa-float"$1href="https://wa.me/916290746602" target="_blank"');

    // Edge case for combined classes
    content = content.replace(/href="#"(\s+class="[^"]*btn-wa[^"]*")/g, 'href="https://wa.me/916290746602" target="_blank"$1');
    content = content.replace(/class="([^"]*btn-wa[^"]*)"(\s+)href="#"/g, 'class="$1"$2href="https://wa.me/916290746602" target="_blank"');

    if (content !== orig) {
        fs.writeFileSync(file, content, 'utf8');
        changed++;
    }
});
console.log(`Updated ${changed} files for whatsapp links.`);
