import { allTopics, allPapers, B } from '../../lib/data';
import spec from '../../data/spec.json';
const tools = [
  ['Practice player', '/practice/'], ['Mock builder', '/mock/'], ['Question of the day', '/today/'], ['Spec checklist', '/specification/'],
  ['Grade boundaries and calculator', '/grade-boundaries/'], ['Exam dates', '/exam-dates/'], ['Revision planner', '/planner/'], ['What comes up (analysis)', '/analysis/'],
  ['What came up last summer', '/what-came-up/'], ['Every paper as a timeline', '/timeline/'], ['Tutors', '/tutors/'], ['Essays and timed essay', '/essays/'],
  ...(B.types || []).map((t: any) => [t[2], `/questions/type/${t[0]}/`]),
].map(([t, u]) => ({ t, u, kind: 'Tool' }));
export function GET() {
  const items = [
    ...allTopics.map((t) => ({ t: t.name, k: t.group, u: `/questions/${t.slug}/`, kind: 'Topic' })),
    ...allPapers.map((p) => ({ t: `${p.series} ${p.qual === 'AS' ? 'AS ' : ''}${p.paper}${p.name ? ' ' + p.name : ''}`, k: p.spec, u: `/past-papers/${p.slug}/`, kind: 'Paper' })),
    ...spec.flatMap((s) => s.statements.filter(() => s.topic).map((st) => ({ t: `${st.id} ${st.text.slice(0, 80)}`, k: s.title, u: `/questions/${s.topic}/`, kind: 'Spec' }))),
    ...tools,
  ];
  return new Response(JSON.stringify(items), { headers: { 'Content-Type': 'application/json' } });
}
