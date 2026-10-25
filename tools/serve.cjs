// Vista previa local, sin instalar paquetes: node tools/serve.cjs
const http = require('node:http');
const fs = require('node:fs');
const path = require('node:path');
const root = path.resolve(__dirname, '..');
const mime = { '.html': 'text/html; charset=utf-8', '.css': 'text/css; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.jfif': 'image/jpeg', '.png': 'image/png', '.woff2': 'font/woff2' };
const server = http.createServer((request, response) => {
  try {
    const url = new URL(request.url, 'http://localhost');
    const decoded = decodeURIComponent(url.pathname);
    const target = path.resolve(root, '.' + (decoded === '/' ? '/index.html' : decoded));
    if (!target.startsWith(root + path.sep)) {
      response.writeHead(403); response.end('Acceso no permitido.'); return;
    }
    fs.readFile(target, (error, data) => {
      if (error) { response.writeHead(404); response.end('Archivo no encontrado.'); return; }
      response.writeHead(200, { 'Content-Type': mime[path.extname(target).toLowerCase()] || 'application/octet-stream', 'Cache-Control': 'no-cache' });
      response.end(data);
    });
  } catch {
    response.writeHead(400); response.end('Solicitud no válida.');
  }
});
server.listen(4173, '127.0.0.1', () => console.log('Local: http://127.0.0.1:4173'));
