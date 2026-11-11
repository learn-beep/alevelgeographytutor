"""Write boards/aqa/topics.json and boards/edexcel/topics.json (site topics -> spec ids) from the two banks."""
import json, re, pathlib, sys
def bank(path):
    js = pathlib.Path(path, 'data', 'index.js').read_text(encoding='utf-8')
    return json.loads(js[len('window.QB='):].rstrip(';\n'))
AQA_BANK, EDX_BANK = sys.argv[1], sys.argv[2]
A = bank(AQA_BANK); E = bank(EDX_BANK)
ids_of = {s['code']: [x['id'] for x in s['st']] for s in A['spec']}
G = {'wc': 'Water and carbon cycles', 'hd': 'Hot desert systems and landscapes', 'co': 'Coastal systems and landscapes', 'gl': 'Glacial systems and landscapes',
     'hz': 'Hazards', 'ec': 'Ecosystems under stress', 'gs': 'Global systems and global governance', 'cp': 'Changing places',
     'ur': 'Contemporary urban environments', 'po': 'Population and the environment', 'rs': 'Resource security', 'fw': 'Fieldwork and geographical skills'}
AQA = [  # slug, name, group, spec sections
 ('water-cycle', 'The water cycle and drainage basins', 'wc', ['3.1.1.1', '3.1.1.2']),
 ('carbon-cycle', 'The carbon cycle', 'wc', ['3.1.1.3']),
 ('water-carbon-climate', 'Water, carbon, climate and life on Earth', 'wc', ['3.1.1.4', '3.1.1.5', '3.1.1.6']),
 ('desert-systems', 'Deserts as systems: processes and sediment', 'hd', ['3.1.2.1', '3.1.2.2']),
 ('arid-landscapes', 'Arid landforms and landscapes', 'hd', ['3.1.2.3']),
 ('desertification', 'Desertification', 'hd', ['3.1.2.4', '3.1.2.5', '3.1.2.6']),
 ('coastal-systems', 'Coastal systems and processes', 'co', ['3.1.3.1', '3.1.3.2']),
 ('coastal-landforms', 'Coastal landforms and landscapes', 'co', ['3.1.3.3']),
 ('coastal-management', 'Coastal management', 'co', ['3.1.3.4', '3.1.3.5', '3.1.3.6']),
 ('glacial-systems', 'Glacial systems and processes', 'gl', ['3.1.4.1', '3.1.4.2', '3.1.4.3']),
 ('glaciated-landscapes', 'Glaciated landforms and landscapes', 'gl', ['3.1.4.4']),
 ('cold-environments', 'Human impacts on cold environments', 'gl', ['3.1.4.5', '3.1.4.6', '3.1.4.7']),
 ('hazard-concept', 'Hazards: concepts, perception and management', 'hz', ['3.1.5.1']),
 ('plate-tectonics', 'Plate tectonics', 'hz', ['3.1.5.2']),
 ('volcanic-hazards', 'Volcanic hazards', 'hz', ['3.1.5.3']),
 ('seismic-hazards', 'Seismic hazards: earthquakes and tsunamis', 'hz', ['3.1.5.4']),
 ('storm-hazards', 'Storm hazards: tropical cyclones', 'hz', ['3.1.5.5']),
 ('wildfires', 'Fires in nature (wildfires)', 'hz', ['3.1.5.6', '3.1.5.7']),
 ('ecosystems-processes', 'Ecosystems: processes and sustainability', 'ec', ['3.1.6.1', '3.1.6.2']),
 ('biomes', 'Biomes', 'ec', ['3.1.6.3']),
 ('british-ecosystems', 'Ecosystems in the British Isles over time', 'ec', ['3.1.6.4']),
 ('marine-ecosystems', 'Marine ecosystems: coral reefs', 'ec', ['3.1.6.5']),
 ('local-ecosystems', 'Local ecosystems', 'ec', ['3.1.6.6', '3.1.6.7']),
 ('globalisation', 'Globalisation and global systems', 'gs', ['3.2.1.1', '3.2.1.2', '3.2.1.6', '3.2.1.7']),
 ('international-trade', 'International trade and access to markets', 'gs', ['3.2.1.3']),
 ('global-governance', 'Global governance', 'gs', ['3.2.1.4']),
 ('antarctica', "The global commons: Antarctica", 'gs', ['3.2.1.5', '3.2.1.5.1']),
 ('nature-of-places', 'The nature and importance of places', 'cp', ['3.2.2.1']),
 ('relationships-connections', 'Places: relationships and connections', 'cp', ['3.2.2.2', '3.2.2.2.1']),
 ('meaning-representation', 'Places: meaning and representation', 'cp', ['3.2.2.2.2']),
 ('place-studies', 'Place studies and changing places skills', 'cp', ['3.2.2.3', '3.2.2.4']),
 ('urbanisation', 'Urbanisation', 'ur', ['3.2.3.1']),
 ('urban-forms', 'Urban forms and social and economic issues', 'ur', ['3.2.3.2', '3.2.3.3']),
 ('urban-climate', 'Urban climate', 'ur', ['3.2.3.4']),
 ('urban-drainage', 'Urban drainage', 'ur', ['3.2.3.5']),
 ('urban-waste', 'Urban waste and other environmental issues', 'ur', ['3.2.3.6', '3.2.3.7']),
 ('sustainable-cities', 'Sustainable urban development', 'ur', ['3.2.3.8', '3.2.3.9']),
 ('population-environment', 'Environment and population', 'po', ['3.2.4.1', '3.2.4.2']),
 ('health-wellbeing', 'Environment, health and well-being', 'po', ['3.2.4.3']),
 ('population-change', 'Population change and population futures', 'po', ['3.2.4.4', '3.2.4.5', '3.2.4.6', '3.2.4.7']),
 ('resource-development', 'Resource development and natural resource issues', 'rs', ['3.2.5.1', '3.2.5.2', '3.2.5.6', '3.2.5.7']),
 ('water-security', 'Water security', 'rs', ['3.2.5.3']),
 ('energy-security', 'Energy security', 'rs', ['3.2.5.4']),
 ('mineral-security', 'Mineral security', 'rs', ['3.2.5.5']),
 ('fieldwork', 'Fieldwork and the geographical investigation', 'fw', ['3.3.F']),
]
out = []
for slug, name, g, secs in AQA:
    ids = [i for s in secs for i in ids_of[s]]
    assert ids, slug
    out.append(dict(slug=slug, name=name, group=G[g], code=', '.join(secs), statements=ids))
allids = {x['id'] for s in A['spec'] for x in s['st']}
miss = allids - {i for t in out for i in t['statements']}
print('AQA topics', len(out), 'unmapped ids', sorted(miss))
pathlib.Path('boards/aqa').mkdir(parents=True, exist_ok=True)
json.dump(out, open('boards/aqa/topics.json', 'w'), indent=1, ensure_ascii=False)

EN = {'1': 'Tectonic processes and hazards', '2A': 'Glaciated landscapes and change', '2B': 'Coastal landscapes and change', '3': 'Globalisation',
      '4A': 'Regenerating places', '4B': 'Diverse places', '5': 'The water cycle and water insecurity', '6': 'The carbon cycle and energy security',
      '7': 'Superpowers', '8A': 'Health, human rights and intervention', '8B': 'Migration, identity and sovereignty'}
ENAME = {
 '1-EQ1': ('tectonic-hazards-risk', 'Tectonic hazards: why some places are at risk'), '1-EQ2': ('tectonic-disasters', 'Tectonic disasters: vulnerability, resilience and impacts'), '1-EQ3': ('tectonic-hazard-management', 'Managing tectonic hazards and disasters'),
 '2A-EQ1': ('glaciation-climate-change', 'Climate change and glaciated landscapes over time'), '2A-EQ2': ('glacier-systems', 'Glacier systems: mass balance and movement'), '2A-EQ3': ('glacial-landforms', 'Glacial landforms and landscapes'), '2A-EQ4': ('glaciated-landscapes-management', 'Using and managing glaciated landscapes'),
 '2B-EQ1': ('coastal-landscapes-processes', 'Coastal landscapes: types and processes'), '2B-EQ2': ('coastal-landforms', 'Coastal landforms, sediment cells and longshore drift'), '2B-EQ3': ('coastal-erosion-sea-level', 'Coastal erosion, sea-level change and coastal risk'), '2B-EQ4': ('coastal-management', 'Coastal management and players'),
 '3-EQ1': ('globalisation-causes', 'Causes of globalisation'), '3-EQ2': ('globalisation-impacts', 'Impacts of globalisation: TNCs, culture and the environment'), '3-EQ3': ('globalisation-consequences', 'Consequences of globalisation: inequality and responses'),
 '4A-EQ1': ('regenerating-places-variation', 'How and why places vary (regenerating places)'), '4A-EQ2': ('regeneration-need', 'Why regeneration might be needed'), '4A-EQ3': ('regeneration-management', 'How regeneration is managed'), '4A-EQ4': ('regeneration-success', 'How successful regeneration is'),
 '4B-EQ1': ('population-structures', 'How population structures vary (diverse places)'), '4B-EQ2': ('diverse-living-spaces', 'How people view diverse living spaces'), '4B-EQ3': ('diverse-places-tensions', 'Demographic and cultural tensions in diverse places'), '4B-EQ4': ('diverse-places-management', 'Managing cultural and demographic issues'),
 '5-EQ1': ('hydrological-cycle', 'The hydrological cycle and drainage basin processes'), '5-EQ2': ('hydrological-change', 'Factors affecting the hydrological system: drought and floods'), '5-EQ3': ('water-insecurity', 'Water insecurity'),
 '6-EQ1': ('carbon-cycle', 'The carbon cycle'), '6-EQ2': ('energy-security', 'Energy demand and energy security'), '6-EQ3': ('carbon-water-climate', 'Carbon, water and the climate system'),
 '7-EQ1': ('superpowers-change', 'What superpowers are and how they change'), '7-EQ2': ('superpowers-impacts', 'Impacts of superpowers'), '7-EQ3': ('superpowers-influence', 'Contested spheres of influence'),
 '8A-EQ1': ('human-development', 'Human development and why it varies'), '8A-EQ2': ('human-rights', 'Why human rights vary'), '8A-EQ3': ('intervention-arguments', 'Human rights and intervention'), '8A-EQ4': ('intervention-outcomes', 'Outcomes of geopolitical interventions'),
 '8B-EQ1': ('international-migration', 'Globalisation and international migration'), '8B-EQ2': ('nation-states', 'Nation states in a globalising world'), '8B-EQ3': ('global-organisations', 'Global organisations and global issues'), '8B-EQ4': ('national-sovereignty', 'Threats to national sovereignty'),
}
out = []
for s in E['spec']:
    slug, name = ENAME[s['code']]; tp = s['code'].split('-')[0]
    out.append(dict(slug=slug, name=name, group=f"Topic {tp}: {EN[tp]}", code=s['code'].replace('-', ' '), statements=[x['id'] for x in s['st']]))
assert len({t['slug'] for t in out}) == len(out)
print('Edexcel topics', len(out))
pathlib.Path('boards/edexcel').mkdir(parents=True, exist_ok=True)
json.dump(out, open('boards/edexcel/topics.json', 'w'), indent=1, ensure_ascii=False)
