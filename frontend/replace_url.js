const fs = require('fs');
const path = require('path');

function replaceInDirectory(dir) {
  const files = fs.readdirSync(dir);

  for (const file of files) {
    const fullPath = path.join(dir, file);
    const stat = fs.statSync(fullPath);

    if (stat.isDirectory()) {
      replaceInDirectory(fullPath);
    } else if (fullPath.endsWith('.ts') || fullPath.endsWith('.tsx') || fullPath.endsWith('.js')) {
      let content = fs.readFileSync(fullPath, 'utf8');
      
      // Case 1: URL inside template literal
      // e.g. `http://127.0.0.1:8000/api/v1/...` -> `${process.env.NEXT_PUBLIC_API_URL}/api/v1/...`
      content = content.replace(/http:\/\/127\.0\.0\.1:8000/g, '${process.env.NEXT_PUBLIC_API_URL}');
      
      // Case 2: URL as a plain string inside single or double quotes
      // We need to convert the quotes to backticks and inject the env var
      // Wait, the previous replace changes all occurrences to ${...}.
      // If the original string was 'http://.../xyz', it is now '${process.env.NEXT_PUBLIC_API_URL}/xyz'
      // BUT it is still surrounded by single or double quotes! It needs backticks!
      // So we can fix it by regex:
      // match: ' or " followed by ${process.env.NEXT_PUBLIC_API_URL} ... followed by ' or "
      // replace with: `...`
      content = content.replace(/(["'])(\$\{process\.env\.NEXT_PUBLIC_API_URL\}[^"']*)\1/g, '`$2`');
      
      fs.writeFileSync(fullPath, content, 'utf8');
    }
  }
}

const srcDir = path.join(__dirname, 'src');
replaceInDirectory(srcDir);
console.log('URLs replaced successfully!');
