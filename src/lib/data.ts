import questions from '../data/questions.json';
import papers from '../data/papers.json';
import topics from '../data/topics.json';
import board from '../data/board.json';

export type Q = (typeof questions)[number];
export type Paper = (typeof papers)[number];
export type Topic = (typeof topics)[number];

export const B: any = board;
export const allQuestions: Q[] = questions as Q[];
export const allPapers: Paper[] = papers as Paper[];
export const allTopics: Topic[] = topics as Topic[];

export const byId = new Map(allQuestions.map((q) => [q.id, q]));
export const topicByslug = new Map(allTopics.map((t) => [t.slug, t]));

export function questionsForTopic(slug: string): Q[] {
  return allQuestions.filter((q) => q.topics.includes(slug)).sort((a, b) => b.year - a.year || a.paper.localeCompare(b.paper) || a.question.localeCompare(b.question, undefined, { numeric: true }));
}

/** The board's own past-paper page (used when crops are switched off). */
export const MATERIALS: string = B.materials || '#';

/** Where a topic sits: badge number (colour), short label, motif and where it is examined. From board.json. */
export const GROUPS: [string, string, number, string, string][] = B.groups || [];
export function groupInfo(group: string) {
  const g = GROUPS.find((x) => x[0] === group) || GROUPS[0] || ['', '', 1, 'globe', ''];
  return { group: g[0], short: g[1], badge: g[2], motif: g[3], where: g[4], area: g[0].replace(/^Topic \w+: /, '') };
}

/** Question format matcher used by the question-type pages: a format name, or "feature:<name>". */
export function matches(q: Q, matcher: string): boolean {
  if (matcher.startsWith('feature:')) return (q.features || []).includes(matcher.slice(8)) || (matcher === 'feature:synoptic' && q.paper === 'Paper 3');
  if (matcher === 'Calculation') return q.format === 'Calculation' || (q.features || []).includes('stats') || (q.skills || []).some((s: any) => /^SK-(ST|CA)|^SK (4|5|6|7|8|9|10)$/.test(s.code));
  return q.format === matcher;
}

/** Is the part marked in levels? AQA: 6 marks and over; Edexcel: the mark scheme's levels (6 marks and over). */
export const isLevels = (q: { marks: number; format: string }) => q.marks >= 6 && q.format !== 'Multiple choice' && q.format !== 'Calculation';

/** The question sentence of a part, without the marks label, answer lines and the paper's instructions. */
export function essayTitle(text: string): string {
  let t = (text || '').replace(/Extra space/g, '').replace(/\[\d+ marks?\]/g, '').replace(/\(\d+\)\s*$/g, '').replace(/[._]{4,}/g, ' ').replace(/(_ ){3,}/g, ' ');
  t = t.replace(/^(Section [A-C][^\n]*|Answer (all|either|one)[^\n]*|Shade the circle[^\n]*|Question \d \d[^\n]*)\s*\n/gm, '').replace(/^\(?[a-z]\)\s*/m, '');
  return t.replace(/\s+/g, ' ').replace(/\s*\(\d+\)\s*$/, '').trim();
}
