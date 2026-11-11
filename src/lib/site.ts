import site from '../data/site.json';
import board from '../data/board.json';
const B: any = board;

export const cropsOn = (import.meta.env.CROPS ?? process.env.CROPS ?? 'on') !== 'off';

/** WhatsApp link with Tom's wording; the board is named when the page belongs to one. */
export function waLink(_context: string): string {
  const who = B.id ? `an ${B.wa === 'AQA' ? 'AQA' : 'Edexcel'} Geography Tutor` : 'an A-level Geography Tutor';
  const msg = `Hi, I'm looking for ${who}. The student is in Year ..... Their name is ..................... we would like ........ lessons per week, the best two times for tutoring are ................. and ......................`;
  return `https://wa.me/${site.whatsapp}?text=${encodeURIComponent(msg)}`;
}

export function pageTitle(t: string): string {
  return B.id ? `${t} | ${B.full}` : `${t} | A-level Geography`;
}
