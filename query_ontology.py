#!/usr/bin/env python3
"""
Quick Query Script for Ontology JSON

Fast command-line queries without interactive menu.

Usage:
    python query_ontology.py entities              # List all entity types
    python query_ontology.py edges                 # List all edge types
    python query_ontology.py entity Professor      # Get entity details
    python query_ontology.py edge WORKS_FOR        # Get edge details
    python query_ontology.py summary               # Show analysis
    python query_ontology.py search "keyword"      # Search
    python query_ontology.py count                 # Show stats
"""

import json
import sys
import os
from typing import Optional


class QuickQuery:
    """Quick query interface for ontology"""

    def __init__(self, json_file: str = "ontology_output.json"):
        if not os.path.exists(json_file):
            print(f"❌ Error: {json_file} not found")
            print("   Run: python example_standalone_demo.py")
            sys.exit(1)

        with open(json_file, 'r', encoding='utf-8') as f:
            self.data = json.load(f)

    def list_entities(self):
        """List all entities"""
        print("\n📦 ENTITY TYPES\n")
        for i, ent in enumerate(self.data['entity_types'], 1):
            print(f"{i}. {ent['name']:<20} - {ent['description']}")
        print()

    def list_edges(self):
        """List all edges"""
        print("\n🔗 EDGE TYPES\n")
        for i, edge in enumerate(self.data['edge_types'], 1):
            print(f"{i}. {edge['name']:<20} - {edge['description']}")
        print()

    def get_entity(self, name: str):
        """Get details of specific entity"""
        for ent in self.data['entity_types']:
            if ent['name'].lower() == name.lower():
                print(f"\n📦 {ent['name']}")
                print(f"   Description: {ent['description']}")
                if ent.get('examples'):
                    print(f"   Examples: {', '.join(ent['examples'])}")
                if ent.get('attributes'):
                    print(f"   Attributes:")
                    for attr in ent['attributes']:
                        print(f"     • {attr['name']} ({attr['type']})")
                print()
                return True
        print(f"❌ Entity '{name}' not found")
        return False

    def get_edge(self, name: str):
        """Get details of specific edge"""
        for edge in self.data['edge_types']:
            if edge['name'].lower() == name.lower():
                print(f"\n🔗 {edge['name']}")
                print(f"   Description: {edge['description']}")
                if edge.get('source_targets'):
                    print(f"   Connections:")
                    for st in edge['source_targets']:
                        print(f"     {st['source']} → {st['target']}")
                print()
                return True
        print(f"❌ Edge '{name}' not found")
        return False

    def show_summary(self):
        """Show analysis summary"""
        print("\n📝 ANALYSIS SUMMARY\n")
        print(self.data.get('analysis_summary', 'N/A'))
        print()

    def search(self, keyword: str):
        """Search for keyword"""
        keyword = keyword.lower()
        print(f"\n🔍 Search results for '{keyword}':\n")

        found = False

        # Search entities
        for ent in self.data['entity_types']:
            if keyword in ent['name'].lower() or keyword in ent['description'].lower():
                print(f"  [Entity] {ent['name']}")
                found = True

        # Search edges
        for edge in self.data['edge_types']:
            if keyword in edge['name'].lower() or keyword in edge['description'].lower():
                print(f"  [Edge] {edge['name']}")
                found = True

        # Search summary
        if keyword in self.data.get('analysis_summary', '').lower():
            print(f"  [Summary] Found in analysis")
            found = True

        if not found:
            print(f"  No results found")
        print()

    def show_stats(self):
        """Show ontology statistics"""
        entities = len(self.data.get('entity_types', []))
        edges = len(self.data.get('edge_types', []))
        total_attrs = sum(len(e.get('attributes', [])) for e in self.data.get('entity_types', []))

        print("\n📊 ONTOLOGY STATISTICS\n")
        print(f"  Entity Types:     {entities}")
        print(f"  Edge Types:       {edges}")
        print(f"  Total Attributes: {total_attrs}")
        print(f"  File Size:        {os.path.getsize('ontology_output.json')} bytes")
        print()

    def show_help(self):
        """Show help"""
        print("""
🐟 MiroFish Ontology Query Tool

Usage:
  python query_ontology.py entities              # List all entities
  python query_ontology.py edges                 # List all edges
  python query_ontology.py entity <name>         # Get entity details
  python query_ontology.py edge <name>           # Get edge details
  python query_ontology.py summary               # Show analysis
  python query_ontology.py search "<keyword>"    # Search
  python query_ontology.py count                 # Show statistics
  python query_ontology.py help                  # Show this help

Examples:
  python query_ontology.py entity Professor
  python query_ontology.py edge WORKS_FOR
  python query_ontology.py search "conflict"
        """)


def main():
    """Main entry point"""
    query = QuickQuery()

    if len(sys.argv) < 2:
        query.show_help()
        return

    command = sys.argv[1].lower()

    if command == 'entities':
        query.list_entities()
    elif command == 'edges':
        query.list_edges()
    elif command == 'entity' and len(sys.argv) > 2:
        query.get_entity(sys.argv[2])
    elif command == 'edge' and len(sys.argv) > 2:
        query.get_edge(sys.argv[2])
    elif command == 'summary':
        query.show_summary()
    elif command == 'search' and len(sys.argv) > 2:
        query.search(sys.argv[2])
    elif command == 'count':
        query.show_stats()
    elif command == 'help' or command == '-h':
        query.show_help()
    else:
        print(f"❌ Unknown command: {command}")
        print("   Try: python query_ontology.py help")


if __name__ == "__main__":
    main()
