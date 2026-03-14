#!/usr/bin/env python3
"""
Interactive Ontology JSON Explorer

Explore and interact with the ontology_output.json file in an easy way.
No dependencies - just Python!

Usage:
    python interact_ontology.py
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any


class OntologyExplorer:
    """Interactive explorer for ontology JSON files"""

    def __init__(self, json_file: str = "ontology_output.json"):
        self.json_file = json_file
        self.data = None
        self.load_data()

    def load_data(self):
        """Load JSON data"""
        if not os.path.exists(self.json_file):
            print(f"❌ File not found: {self.json_file}")
            print(f"   Run: python example_standalone_demo.py")
            exit(1)

        try:
            with open(self.json_file, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
            print(f"✓ Loaded: {self.json_file}\n")
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON: {e}")
            exit(1)

    def show_menu(self):
        """Display main menu"""
        print("\n" + "="*70)
        print("🐟 MiroFish Ontology Explorer")
        print("="*70)
        print("\nOptions:")
        print("  1. List all entity types")
        print("  2. List all edge types")
        print("  3. View specific entity type details")
        print("  4. View specific edge type details")
        print("  5. Show analysis summary")
        print("  6. Export entity types to CSV")
        print("  7. Export edge types to CSV")
        print("  8. Show full JSON")
        print("  9. Search for keyword")
        print("  0. Exit")
        print("="*70)

    def list_entity_types(self):
        """List all entity types"""
        print("\n" + "="*70)
        print("📦 ENTITY TYPES")
        print("="*70 + "\n")

        entities = self.data.get('entity_types', [])
        for i, ent in enumerate(entities, 1):
            print(f"{i}. {ent.get('name', 'N/A')}")
            print(f"   Description: {ent.get('description', 'N/A')}")
            examples = ent.get('examples', [])
            if examples:
                print(f"   Examples: {', '.join(examples[:3])}")
            attrs = ent.get('attributes', [])
            if attrs:
                attr_names = ', '.join([a.get('name', '?') for a in attrs])
                print(f"   Attributes: {attr_names}")
            print()

        print(f"Total: {len(entities)} entity types")

    def list_edge_types(self):
        """List all edge types"""
        print("\n" + "="*70)
        print("🔗 EDGE TYPES")
        print("="*70 + "\n")

        edges = self.data.get('edge_types', [])
        for i, edge in enumerate(edges, 1):
            print(f"{i}. {edge.get('name', 'N/A')}")
            print(f"   Description: {edge.get('description', 'N/A')}")
            sources = edge.get('source_targets', [])
            if sources:
                for st in sources:
                    print(f"   {st.get('source', '?')} → {st.get('target', '?')}")
            print()

        print(f"Total: {len(edges)} edge types")

    def show_entity_details(self):
        """Show details of a specific entity type"""
        entities = self.data.get('entity_types', [])
        print("\nAvailable entity types:")
        for i, ent in enumerate(entities, 1):
            print(f"  {i}. {ent.get('name')}")

        try:
            choice = int(input("\nSelect number (or 0 to cancel): "))
            if choice == 0 or choice > len(entities):
                return

            entity = entities[choice - 1]
            print("\n" + "="*70)
            print(f"📦 {entity.get('name')}")
            print("="*70)
            print(f"Description: {entity.get('description')}")
            print(f"Type: {entity.get('name')}")

            if entity.get('examples'):
                print(f"\nExamples:")
                for ex in entity['examples']:
                    print(f"  • {ex}")

            if entity.get('attributes'):
                print(f"\nAttributes:")
                for attr in entity['attributes']:
                    print(f"  • {attr.get('name')} ({attr.get('type')})")
                    if attr.get('description'):
                        print(f"    └─ {attr.get('description')}")

        except (ValueError, IndexError):
            print("❌ Invalid selection")

    def show_edge_details(self):
        """Show details of a specific edge type"""
        edges = self.data.get('edge_types', [])
        print("\nAvailable edge types:")
        for i, edge in enumerate(edges, 1):
            print(f"  {i}. {edge.get('name')}")

        try:
            choice = int(input("\nSelect number (or 0 to cancel): "))
            if choice == 0 or choice > len(edges):
                return

            edge = edges[choice - 1]
            print("\n" + "="*70)
            print(f"🔗 {edge.get('name')}")
            print("="*70)
            print(f"Description: {edge.get('description')}")

            if edge.get('source_targets'):
                print(f"\nConnections:")
                for st in edge['source_targets']:
                    print(f"  {st.get('source')} --[{edge.get('name')}]--> {st.get('target')}")

            if edge.get('attributes'):
                print(f"\nAttributes:")
                for attr in edge['attributes']:
                    print(f"  • {attr.get('name')}")

        except (ValueError, IndexError):
            print("❌ Invalid selection")

    def show_summary(self):
        """Show analysis summary"""
        print("\n" + "="*70)
        print("📝 ANALYSIS SUMMARY")
        print("="*70 + "\n")
        summary = self.data.get('analysis_summary', 'N/A')
        print(summary)
        print("\n" + "="*70)

    def export_entities_csv(self):
        """Export entity types to CSV"""
        output_file = "entities_export.csv"
        entities = self.data.get('entity_types', [])

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("Name,Description,Examples,Attributes\n")
            for ent in entities:
                name = ent.get('name', '')
                desc = ent.get('description', '').replace(',', ';')
                examples = '|'.join(ent.get('examples', []))
                attrs = '|'.join([a.get('name', '') for a in ent.get('attributes', [])])
                f.write(f'"{name}","{desc}","{examples}","{attrs}"\n')

        print(f"✓ Exported to: {output_file}")

    def export_edges_csv(self):
        """Export edge types to CSV"""
        output_file = "edges_export.csv"
        edges = self.data.get('edge_types', [])

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("Name,Description,Source,Target\n")
            for edge in edges:
                name = edge.get('name', '')
                desc = edge.get('description', '').replace(',', ';')
                sources = edge.get('source_targets', [])
                if sources:
                    for st in sources:
                        source = st.get('source', '')
                        target = st.get('target', '')
                        f.write(f'"{name}","{desc}","{source}","{target}"\n')
                else:
                    f.write(f'"{name}","{desc}","",""\n')

        print(f"✓ Exported to: {output_file}")

    def show_full_json(self):
        """Show full JSON with pretty printing"""
        print("\n" + "="*70)
        print("📄 FULL JSON")
        print("="*70 + "\n")
        print(json.dumps(self.data, ensure_ascii=False, indent=2))

    def search_keyword(self):
        """Search for keyword across ontology"""
        keyword = input("\nSearch keyword: ").lower()
        print(f"\n🔍 Searching for: '{keyword}'\n")

        results = []

        # Search entity types
        for ent in self.data.get('entity_types', []):
            if (keyword in ent.get('name', '').lower() or
                keyword in ent.get('description', '').lower()):
                results.append(('Entity', ent.get('name')))

        # Search edge types
        for edge in self.data.get('edge_types', []):
            if (keyword in edge.get('name', '').lower() or
                keyword in edge.get('description', '').lower()):
                results.append(('Edge', edge.get('name')))

        # Search summary
        if keyword in self.data.get('analysis_summary', '').lower():
            results.append(('Summary', 'Found in analysis summary'))

        if results:
            print("Results:")
            for rtype, rname in results:
                print(f"  • [{rtype}] {rname}")
        else:
            print("❌ No results found")

    def run(self):
        """Main interaction loop"""
        while True:
            self.show_menu()
            choice = input("\nSelect option (0-9): ").strip()

            if choice == '1':
                self.list_entity_types()
            elif choice == '2':
                self.list_edge_types()
            elif choice == '3':
                self.show_entity_details()
            elif choice == '4':
                self.show_edge_details()
            elif choice == '5':
                self.show_summary()
            elif choice == '6':
                self.export_entities_csv()
            elif choice == '7':
                self.export_edges_csv()
            elif choice == '8':
                self.show_full_json()
            elif choice == '9':
                self.search_keyword()
            elif choice == '0':
                print("\n👋 Goodbye!\n")
                break
            else:
                print("❌ Invalid option")

            input("\nPress Enter to continue...")


def main():
    """Entry point"""
    print("\n" + "🐟 "*35)
    print("MiroFish Ontology Explorer")
    print("🐟 "*35)

    explorer = OntologyExplorer()
    explorer.run()


if __name__ == "__main__":
    main()
