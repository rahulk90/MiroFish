import json

with open('ontology_output.json') as f:
    data = json.load(f)

print("\n" + "="*70)
print("📦 ENTITY TYPES")
print("="*70)
for i, ent in enumerate(data['entity_types'], 1):
    print(f"\n{i}. {ent['name']}")
    print(f"   Description: {ent['description']}")
    print(f"   Examples: {', '.join(ent.get('examples', []))}")
    attrs = ent.get('attributes', [])
    if attrs:
        print(f"   Attributes: {', '.join([a['name'] for a in attrs])}")

print("\n" + "="*70)
print("🔗 EDGE TYPES")
print("="*70)
for i, edge in enumerate(data['edge_types'], 1):
    print(f"\n{i}. {edge['name']}")
    print(f"   Description: {edge['description']}")
    if edge.get('source_targets'):
        for st in edge['source_targets']:
            print(f"   {st['source']} → {st['target']}")

print("\n" + "="*70)
print("📝 ANALYSIS")
print("="*70)
print(f"\n{data.get('analysis_summary', 'N/A')}\n")
