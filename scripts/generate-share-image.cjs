// Render website-native SVG artwork and the licensed Inter font into share assets.
// Run with Node and sharp available (NODE_PATH can point to the bundled runtime).
const sharp = require('sharp');
const path = require('node:path');
const fs = require('node:fs/promises');
const assets = path.resolve(__dirname, '../assets');
const fontfile = path.join(assets, 'fonts/InterVariable.ttf');
const text = async (value, size, color, weight = 'normal') => sharp({text:{text:`<span foreground="${color}" weight="${weight}">${value}</span>`,font:`Inter ${size}`,fontfile,rgba:true,dpi:72}}).png().toBuffer();
(async () => {
  const illustration = await sharp(path.join(assets,'illustrations/homes.svg')).resize({width:560}).png().toBuffer();
  const symbol = await sharp(path.join(assets,'brand-board.png')).extract({left:64,top:328,width:132,height:132}).png().toBuffer();
  await sharp(symbol).resize(132,132).png().toFile(path.join(assets,'favicon.png'));
  const layers = [
    {input:await sharp(symbol).resize(45,45).png().toBuffer(),left:62,top:55},
    {input:await text('Mietblick',30,'#18324A','semibold'),left:118,top:63},
    {input:await text('DIE VERMIETER-APP FÜR MAC, IPHONE &amp; IPAD',12,'#247777','medium'),left:64,top:155},
    {input:await text('Einfach vermieten.',49,'#18324A','semibold'),left:62,top:214},
    {input:await text('Alles im Blick.',49,'#247777','semibold'),left:62,top:276},
    {input:await text('Immobilien. Mietverträge. Mietzahlungen.',16,'#586774'),left:64,top:373},
    {input:await text('Lokal auf deinem Gerät. Ohne Mietblick-Konto.',14,'#586774'),left:64,top:410},
    {input:await text('mietblick-app.de',15,'#18324A','medium'),left:64,top:538},
    {input:illustration,left:620,top:99}
  ];
  await sharp({create:{width:1200,height:630,channels:4,background:'#F5F6F7'}}).composite(layers).png({compressionLevel:9}).toFile(path.join(assets,'social-preview.png'));
  console.log('Share image 1200×630, original-board favicon rendered.');
})().catch(error => {console.error(error.message);process.exitCode=1;});
