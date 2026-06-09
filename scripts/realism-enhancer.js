// realism-enhancer.js
// ---------------------------------------------------------------------------
// Builds AUTHENTIC, MODERN, CATEGORY-DISTINCT photography prompts and away from
// the "AI art" look AND away from the old brass-foundry/rustic universe.
//
// Balaji Udhyog is a diversified modern hardware & bathroom-systems exporter.
// Each category gets its own scene + palette (see ../assets/modern-hardware-direction.md):
//   • bathroom  → luxury hotel bathroom, chrome / brushed nickel / matte black, white marble
//   • locks     → architectural door in a minimalist luxury apartment, matte black / brushed steel
//   • furniture → modern handleless kitchen / walk-in wardrobe, brushed steel + warm wood
//   • brass     → the ONE warm heritage line: refined CLEAN studio, brushed brass (never neon)
//   • glass     → contemporary upscale living space
//   • decor     → modern architectural interior
//   • manufacturing / facility / port → clean modern international operation (NOT dusty foundry)
//
// For non-brass scenes the warm/gold/foundry/antique language is stripped from the
// base prompt so nothing carries the old rustic tone.
// ---------------------------------------------------------------------------

import { fillPlaceholders } from './prompt-enhancer.js';

const REALISM_PRESET = 'PHOTOGRAPHY';   // Leonardo Alchemy photographic preset
const NEG_MAX = 1000;                   // Leonardo negative_prompt cap

/* Generic realism spine — physics of real photography, not "beauty". */
const REALISM_CORE = [
  'real unretouched photograph straight out of camera',
  'professional commercial product photography, architectural / interior editorial style',
  'soft natural architectural lighting with believable reflections and gentle shadows',
  'true-to-life white balance, restrained natural contrast, accurate neutral exposure',
  'physically accurate materials, honest clean commercial-grade surfaces',
  'mild natural lens softness, fine organic film grain, NOT over-sharpened',
  'realistic depth of field, natural lens rendering, calm uncluttered composition',
  'internationally manufactured premium quality, modern and trustworthy',
];

/* Camera modes. */
const CAM = {
  env:    'shot on a Sony A7 IV with a 50mm lens at f/4, soft architectural daylight from a large window with a subtle fill',
  studio: 'shot on a Canon EOS R5 with an 85mm lens at f/5.6, one soft studio key and reflector fill',
  wide:   'shot on a Nikon Z7 II with a 24-35mm lens at f/8, available architectural light',
  macro:  'shot on a Canon EOS R5 with a 100mm macro lens at f/8, soft box-lit, clean detail',
};

/* Per-scene recipe: environment + palette + camera mode + scene-specific negatives.
   `warm:true` scenes keep brass/gold/heritage language; all others are modernised. */
const SCENES = {
  bathroom: {
    cam: 'env',
    env: 'staged in a luxury five-star hotel bathroom — large-format white marble and warm timber vanity, a backlit framed mirror, soft architectural daylight; the fixture crisp and clean with realistic reflections, clean contemporary lines, minimalist and uncluttered',
    pal: 'chrome, brushed nickel and matte black against white marble, warm wood and soft neutral light',
    neg: 'antique brass, rustic, dusty, foundry, yellow-gold, ornate, weathered, cluttered, kitsch',
  },
  locks: {
    cam: 'env',
    env: 'mounted on a modern architectural door in a minimalist luxury apartment — warm oak door, clean plaster wall, soft daylight; precise contemporary lever/handle or lock, commercial-grade and architectural',
    pal: 'matte black and brushed stainless steel, charcoal, warm oak, neutral',
    neg: 'antique brass, ornate, rustic, dusty workshop, foundry, yellow-gold, weathered, village',
  },
  furniture: {
    cam: 'env',
    env: 'fitted on contemporary cabinetry in a modern luxury kitchen or walk-in wardrobe — handleless and slab fronts, warm walnut and stone, integrated lighting, a clean modular premium interior',
    pal: 'brushed steel and matte black hardware, warm walnut, stone grey, white; restrained brass accents only',
    neg: 'antique, rustic, dusty, foundry, ornate carving, village craft, yellow-gold dominance',
  },
  brass: {  // the ONE warm heritage category — kept warm, but CLEAN and premium
    warm: true, cam: 'studio',
    env: 'presented in a refined clean modern studio on a dark stone surface with soft warm light — hand-finished brass with honest texture and premium heritage character, professionally lit, NOT dusty or rural',
    pal: 'warm brushed brass, deep navy and warm neutral — restrained, never neon or oversaturated gold',
    neg: 'dusty workshop, rural, derelict, oversaturated gold, grime, cluttered, kitsch',
  },
  glass: {
    cam: 'env',
    env: 'styled in a contemporary upscale living space — clean modern interior, soft daylight, premium minimalist decor styling',
    pal: 'clear or softly coloured glass, soft neutrals, charcoal, warm wood accents',
    neg: 'rustic, dusty, foundry, cluttered, kitsch, oversaturated',
  },
  decor: {
    cam: 'env',
    env: 'placed in a modern architectural interior — clean gallery-like space, contemporary furniture, soft daylight, premium minimalist styling',
    pal: 'neutral, charcoal, warm wood and brushed metal',
    neg: 'rustic, dusty, rural, ornate clutter, yellow-gold dominance',
  },
  manufacturing: {  // Aligarh, generic factory, hero
    cam: 'wide', people: true,
    env: 'inside a clean, modern precision hardware manufacturing facility — CNC machines, stainless work surfaces, neatly organised components, bright even industrial lighting; a contemporary international factory, NOT a dusty rural foundry',
    pal: 'stainless steel, cool grey, clean white light, restrained safety-colour accents',
    neg: 'dusty, foundry fire, rural, derelict, grime, antique, yellow-gold, village, slum, hut, mud, ramshackle, poverty, smoke, third-world stereotype',
  },
  industrial_estate: {  // hub AERIALS — modern 2020s Indian industrial park, NOT a village
    cam: 'wide',
    env: 'a 2020s high aerial drone view of a modern, prosperous Indian industrial manufacturing estate / SEZ — rows of large clean rectangular factory buildings with white, blue and grey corrugated-steel roofs, paved internal roads with painted lane markings, parking lots with modern cars and trucks, water tanks, well-maintained green strips and rooftop HVAC units under hazy daylight; comparable to an SEZ or industrial park in modern Gurgaon, Noida, Ahmedabad or Pune — definitively NOT a slum, village, rural settlement, mud houses, thatched roofs, ruins, war-torn area or anything resembling Afghanistan or Kabul',
    pal: 'neutral industrial greys, white and blue corrugated roofing, hazy sky, restrained warm rooftop accents',
    neg: 'slum, shanty town, village, rural, poverty, mud houses, thatched roof, huts, derelict, war-torn, ruins, ancient, mughal, heritage city, old town, bazaar, narrow lanes, unpaved muddy roads, refugee camp, ramshackle, dense smoke, third-world stereotype, Afghanistan, Kabul, Pakistan village, sand storm',
  },
  brass_workshop: {  // Muradabad interiors — modern Indian SME unit (heritage craft, modern facility)
    warm: true, cam: 'wide', people: true,
    env: 'inside a 2020s clean, modern, well-lit Indian brass manufacturing unit — white-painted plaster walls, organised stainless-steel workbenches, modern bench machinery and tidy tool shelving, fluorescent / LED panel lighting plus a soft warm task lamp, a skilled artisan in clean work clothes finishing brass; resembles a tidy SME unit in a modern Indian industrial estate, NOT a dusty, dark, derelict or rural workshop',
    pal: 'warm brushed brass with clean white walls and neutral greys, mixed daylight and modern overhead lighting',
    neg: 'slum, village, rural, poverty, mud walls, hut, thatched roof, ancient, derelict, dark dungeon, heavy grime, narrow alley, oversaturated gold, third-world stereotype',
  },
  glassworks: {  // Firozabad interiors — modern glass-manufacturing unit (controlled, not derelict)
    cam: 'wide', people: true,
    env: 'inside a 2020s modern, clean glass-manufacturing unit — white-painted walls, organised work area with proper modern furnace / cutting equipment, controlled overhead lighting plus the warm furnace glow, a professional glassblower or cutter in proper clothing at work; contemporary and prosperous, comparable to a modern Indian MSME glass unit, NOT derelict, smoky, dim or rural',
    pal: 'clear glass glow with white walls and neutral greys, a restrained warm furnace accent',
    neg: 'slum, village, rural, poverty, hut, thatched, derelict, dense smoke, dark, dim, ramshackle, ancient, third-world stereotype',
  },
  facility: {  // warehouse, packaging, documentation
    cam: 'wide', people: true,
    env: 'in a clean, modern, well-organised export warehouse or facility — bright, orderly racking and palletised goods, a contemporary international operation',
    pal: 'neutral steel, clean light, kraft cartons, white',
    neg: 'dusty, derelict, dim, grimy, rural, foundry',
  },
  port: {
    cam: 'wide',
    env: 'at a modern container port / inland yard — neatly stacked weathered-but-clean shipping containers, gantry cranes, realistic asphalt and steel under soft overcast daylight; international logistics scale, no readable codes or logos',
    pal: 'steel blues and greys, restrained warm dock accents, neutral',
    neg: 'rural, derelict, dusty village, golden-hour glow, readable codes',
  },
  office: {  // team portraits, offices, showrooms
    cam: 'env', people: true,
    env: 'in a clean modern office or an architectural hardware showroom — soft daylight, glass and steel detailing, contemporary and professional',
    pal: 'neutral, glass, brushed steel, white, warm wood accents',
    neg: 'dusty, rural, factory grime, derelict',
  },
  blog: {
    cam: 'wide',
    env: 'a contemporary, premium trade-editorial scene — clean modern context, soft natural light, sophisticated and uncluttered',
    pal: 'modern neutral palette with restrained metal accents',
    neg: 'rustic, dusty, kitsch, cluttered, readable text',
  },
};

/* Map an image path (+ block code) to a scene key. Path wins; code is fallback. */
function sceneFor(tail = '', code = '') {
  const t = tail.toLowerCase();
  // products + items by group/category
  if (/(^|\/)(bathroom-hardware|towel-holders|bathroom-accessories)(\/|-|$)/.test(t)) return 'bathroom';
  if (/(^|\/)(locks-hardware|door-locks|tower-bolts)(\/|-|$)/.test(t)) return 'locks';
  if (/(^|\/)(furniture-hardware|cabinet-knobs|brass-handles|wall-hooks)(\/|-|$)/.test(t)) return 'furniture';
  if (/(^|\/)(metal-art-ware|home-decor|metal-artware)(\/|-|$)/.test(t)) return 'decor';
  if (/(^|\/)(glassware|glass-decor)(\/|-|$)/.test(t) || /chandelier/.test(t)) return 'glass';
  if (/(^|\/)brassware(\/|-|$)/.test(t)) return 'brass';
  // hubs — aerials = modern industrial estate; interiors = clean modern units
  if (t.startsWith('hubs/moradabad')) return t.endsWith('-aerial.webp') ? 'industrial_estate' : 'brass_workshop';
  if (t.startsWith('hubs/aligarh')) return t.endsWith('-aerial.webp') ? 'industrial_estate' : 'manufacturing';
  if (t.startsWith('hubs/firozabad')) return t.endsWith('-aerial.webp') ? 'industrial_estate' : 'glassworks';
  if (t.startsWith('hubs/')) return 'industrial_estate';
  // export / logistics
  if (/container|shipping|port-arrival/.test(t)) return 'port';
  if (t.startsWith('export/')) return 'facility';
  // team
  if (t.startsWith('team/')) return 'office';
  // gallery
  if (t.startsWith('gallery/')) {
    if (/bathroom/.test(t)) return 'bathroom';
    if (/locks/.test(t)) return 'locks';
    if (/chandelier|glass/.test(t)) return 'glass';
    if (/metal/.test(t)) return 'decor';
    if (/container/.test(t)) return 'port';
    if (/brassware/.test(t)) return 'brass';
    return 'decor';
  }
  // blog
  if (t.startsWith('blog/')) return 'blog';
  // hero
  if (t.startsWith('hero/')) return /port|export/.test(t) ? 'port' : 'manufacturing';
  // category heroes by code
  const byCode = { B1: 'brass', B2: 'decor', B3: 'furniture', B4: 'locks', B5: 'bathroom', B6: 'glass', B7: 'decor' };
  if (byCode[code]) return byCode[code];
  return 'decor';
}

/* Beauty/CGI trigger removal (applies to all). */
const STRIP = [
  [/\b8k\b/gi, ''], [/\b4k\b/gi, ''], [/\bultra[\s-]?detailed\b/gi, 'finely detailed'],
  [/\bhyper[\s-]?\w+/gi, ''], [/\bintricate detail(s)?\b/gi, 'natural detail'],
  [/\bsharp focus\b/gi, 'natural focus'], [/\bcinematic\b/gi, 'naturalistic'],
  [/\bdramatic\b/gi, 'understated'], [/\bhigh dynamic range[^.,]*/gi, ''], [/\bHDR\b/g, ''],
  [/\bcontrolled flare\b/gi, ''], [/\bjewel-like\b/gi, 'clear'], [/\bgold sparkle\b/gi, 'soft highlights'],
  [/\bmuseum-grade\b/gi, 'professional'], [/\bhigh-end\b/gi, ''], [/\s{2,}/g, ' '],
];
/* Warm/foundry/heritage atmosphere removal — applied ONLY to non-brass (modern) scenes. */
const DEWARM = [
  [/golden hour/gi, 'soft daylight'],
  [/warm gold rim light|gold rim light/gi, 'soft daylight'],
  [/brushed gold/gi, 'brushed nickel'],
  [/deep navy tones|deep navy shadows/gi, 'clean neutral tones'],
  [/against navy/gi, 'against a neutral backdrop'],
  [/warm gold(?: accents| tones| highlights)?/gi, 'brushed metal'],
  [/\bgold\b/gi, 'brushed metal'],
  [/deep navy backdrop|navy backdrop|deep navy darkroom backdrop/gi, 'clean neutral backdrop'],
  [/\bantique\b/gi, 'contemporary'], [/\bpatina\b/gi, 'brushed finish'],
  [/foundry|molten/gi, 'modern manufacturing'], [/hammered metal/gi, 'brushed metal'],
  [/heritage|mughal-era|17th century|400-year-old/gi, 'modern'],
  [/single hero object centered on a dark brushed surface/gi, 'shown in a real setting'],
  [/on a (matte )?dark (brushed )?stone[^.,;]*/gi, ''],
];

/* Village/rural/derelict removal — applied to ALL hub & facility scenes so the
   base copy can't drag them back toward a "poor village" look. */
const DEVILLAGE = [
  [/\brural\b/gi, 'modern'], [/\bdusty\b/gi, 'clean'], [/\bworn(?:\s+wooden)?\b/gi, ''],
  [/\bderelict\b/gi, ''], [/\bvillage\b/gi, 'industrial city'], [/\bhistoric\b/gi, 'established'],
  [/\bdense\b/gi, ''], [/low-rise foundry rooftops/gi, 'modern factory rooftops'],
  [/brass-craft district|craft district|craft city|hardware district|glass[-\s]?furnace city|glass furnaces/gi, 'industrial manufacturing estate'],
  [/thin chimney haze|chimney haze|atmospheric haze|dust haze/gi, 'soft haze'],
  [/foundries|foundry|molten/gi, 'modern factories'],
];
const INDUSTRIAL = new Set(['industrial_estate', 'manufacturing', 'brass_workshop', 'glassworks', 'facility']);

function applyList(text, list) { let t = String(text || ''); for (const [re, rep] of list) t = t.replace(re, rep); return t; }
function cleanBase(text) {
  return applyList(text, STRIP)
    .replace(/\s+([.,])/g, '$1').replace(/,(\s*,)+/g, ',').replace(/,\s*\./g, '.')
    .replace(/[,\s]+\.$/, '.').replace(/\s{2,}/g, ' ').trim();
}

/* Standing anti-CGI / anti-synthetic / anti-text wall. */
export const REALISM_NEGATIVE = [
  'CGI', '3d render', 'render', 'octane render', 'unreal engine', 'video game', 'synthetic',
  'AI art', 'AI artifacts', 'computer generated', 'cartoon', 'anime', 'illustration', 'painting',
  'glossy fake reflections', 'over-glossy metal', 'mirror-finish', 'plastic surface', 'plastic-looking',
  'waxy', 'surreal lighting', 'sci-fi lighting', 'fantasy', 'dramatic glow', 'god rays', 'lens flare',
  'bloom', 'synthetic HDR', 'overprocessed', 'over-sharpened', 'oversaturated', 'neon', 'fake texture',
  'impossible geometry', 'melted geometry', 'distorted product', 'warped', 'hyper-symmetry',
  'text', 'words', 'lettering', 'watermark', 'logo', 'brand name', 'signage', 'label',
  'low quality', 'blurry', 'jpeg artifacts', 'duplicate', 'tiling',
].join(', ');

const PEOPLE_NEGATIVE = 'extra fingers, fused fingers, malformed hands, six fingers, deformed hands, distorted face, uncanny smile, asymmetric eyes, mannequin, ';

/**
 * Build a realism-tuned, category-distinct generation spec.
 * @param {{main:string, subject?:string, code?:string, tail?:string, blockNegative?:string, maxLen?:number}} o
 * @returns {{prompt:string, negative:string, presetStyle:string, kind:string}}
 */
export function buildRealism({ main, subject, code = '', tail = '', blockNegative = '', maxLen = 1500 }) {
  const key = sceneFor(tail, code);
  const scene = SCENES[key] || SCENES.decor;

  let base = cleanBase(fillPlaceholders(main, subject));
  if (!scene.warm) base = applyList(base, DEWARM).replace(/\s{2,}/g, ' ').replace(/\s+([.,])/g, '$1').trim();
  if (INDUSTRIAL.has(key)) base = applyList(base, DEVILLAGE).replace(/\s{2,}/g, ' ').replace(/\s+([.,])/g, '$1').replace(/,(\s*,)+/g, ',').trim();

  const prompt = [
    'Authentic professional photograph, real-world modern commercial shoot.',
    base.endsWith('.') ? base : base + '.',
    scene.env + '.',
    'Materials and palette: ' + scene.pal + '.',
    CAM[scene.cam] + '.',
    REALISM_CORE.join(', ') + '.',
  ].join(' ').replace(/\s{2,}/g, ' ').trim();

  const prompt2 = prompt.length > maxLen ? prompt.slice(0, maxLen).replace(/[,\s]+\S*$/, '') + '.' : prompt;

  const peopleNeg = scene.people ? PEOPLE_NEGATIVE : '';
  const seen = new Set();
  let negative = [peopleNeg, scene.neg, blockNegative, REALISM_NEGATIVE]
    .filter(Boolean).join(', ').split(',')
    .map(s => s.trim()).filter(s => { const k = s.toLowerCase(); if (!s || seen.has(k)) return false; seen.add(k); return true; })
    .join(', ');
  if (negative.length > NEG_MAX) negative = negative.slice(0, negative.lastIndexOf(',', NEG_MAX));

  return { prompt: prompt2, negative, presetStyle: REALISM_PRESET, kind: key };
}
