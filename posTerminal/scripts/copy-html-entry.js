import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { dirname } from "node:path";
// Copy the built index.html into Frappe's www/pos so the route serves the SPA shell.
const src = "../alphax_pos/public/pos/index.html";
const dest = "../alphax_pos/www/pos/index.html";
let html = readFileSync(src, "utf8");
const boot = `{% endraw %}<script>window.csrf_token="{{ csrf_token }}";window.frappe={csrf_token:"{{ csrf_token }}"};</script>{% raw %}`;
html = html.replace("</head>", boot + "</head>");
mkdirSync(dirname(dest), { recursive: true });
writeFileSync(dest, "{% raw %}" + html + "{% endraw %}");
console.log("copied SPA shell → www/pos/index.html");
