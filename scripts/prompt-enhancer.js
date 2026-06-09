// prompt-enhancer.js
// Turns a base prompt (parsed from ai-image-prompts.md) into a Leonardo-ready
// prompt by appending consistent premium export-house realism + cinematic
// modifiers, and merges a strong anti-"AI-art" negative prompt.
//
// It is deliberately idempotent-ish: a modifier is only appended if a marker
// word for it isn't already present, so hand-written prompts that already
// describe (say) "cinematic lighting" don't get it twice.

/* Premium brand + realism style modifiers appended to every prompt. */
export const STYLE_MODIFIERS = [
  ['photorealistic',        'ultra realistic, photorealistic'],
  ['commercial',            'high-end commercial product photography'],
  ['cinematic',             'cinematic lighting'],
  ['rim light',             'soft directional key light with warm gold rim light'],
  ['depth of field',        'shallow depth of field'],
  ['full-frame',            'full-frame DSLR look, prime lens'],
  ['navy',                  'deep navy and warm gold colour palette'],
  ['export house',          'luxury Indian export-house aesthetic, editorial industrial mood'],
  ['material texture',      'fine real material texture'],
  ['sharp focus',           '8k, sharp focus, intricate detail'],
];

/* Realism reinforcement — nudges away from the synthetic look. */
export const REALISM_MODIFIERS = [
  ['natural',  'natural light'],
  ['believable optics', 'believable optics, true-to-life proportions'],
];

/* Global negative baseline (mirrors §1.1 of ai-image-prompts.md). Used as a
   fallback if the markdown's global negative can't be parsed. */
export const NEGATIVE_BASE = [
  'text', 'words', 'letters', 'typography', 'watermark', 'logo', 'brand name',
  'signage', 'label', 'caption', 'signature', 'UI', 'frame border',
  'deformed', 'distorted', 'disfigured', 'mutated', 'extra fingers', 'extra limbs',
  'bad anatomy', 'low quality', 'lowres', 'blurry', 'out of focus',
  'jpeg artifacts', 'noise', 'oversaturated', 'neon colors', 'HDR halo', 'overexposed',
  'plastic skin', 'waxy', 'CGI', '3d render', 'video game', 'illustration', 'cartoon',
  'anime', 'painting', 'sketch', 'stock photo overlay', 'cluttered', 'messy',
  'dirty lens', 'duplicate', 'cropped subject', 'tiling',
].join(', ');

/* Hard anti-AI / anti-text guards always forced into the negative prompt,
   even if the parsed negative somehow drops them (task requirements 4 & 13). */
export const FORCED_NEGATIVE = [
  'text', 'logo', 'watermark', 'brand name', 'lettering', 'cartoon', 'anime',
  'illustration', '3d render', 'CGI', 'plastic look',
].join(', ');

/**
 * Fill {SUBJECT} / {ROLE} / {PLACE} / {THEME} placeholders in a template prompt.
 */
export function fillPlaceholders(text, subject) {
  if (!subject) return text;
  return text.replace(/\{SUBJECT\}|\{ROLE\}|\{PLACE\}|\{THEME\}/g, subject);
}

/**
 * Enhance a base prompt with style + realism modifiers (no duplication).
 * @returns {string} the enhanced positive prompt.
 */
export function enhancePrompt(base, { maxLen = 1450 } = {}) {
  let p = String(base || '').replace(/\s+/g, ' ').trim().replace(/[.\s]+$/, '');
  const lower = p.toLowerCase();
  const add = [];
  for (const [marker, phrase] of [...STYLE_MODIFIERS, ...REALISM_MODIFIERS]) {
    if (!lower.includes(marker.toLowerCase())) add.push(phrase);
  }
  if (add.length) p = `${p}. ${add.join(', ')}`;
  p = `${p}.`;
  if (p.length > maxLen) p = p.slice(0, maxLen).replace(/[,\s]+\S*$/, '') + '.';
  return p;
}

/**
 * Build the final negative prompt: a global base + this block's extra negatives
 * + the always-forced anti-AI/anti-text guards (de-duplicated).
 */
export function buildNegative(globalNegative, blockNegative = '') {
  const parts = [globalNegative || NEGATIVE_BASE, blockNegative, FORCED_NEGATIVE]
    .filter(Boolean)
    .join(', ');
  const seen = new Set();
  const out = [];
  for (let term of parts.split(',')) {
    term = term.trim();
    const key = term.toLowerCase();
    if (term && !seen.has(key)) { seen.add(key); out.push(term); }
  }
  return out.join(', ');
}

/**
 * Convenience: produce the final {prompt, negative} for a resolved job.
 */
export function preparePrompt({ main, subject, blockNegative, globalNegative }) {
  const filled = fillPlaceholders(main, subject);
  return {
    prompt: enhancePrompt(filled),
    negative: buildNegative(globalNegative, blockNegative),
  };
}
