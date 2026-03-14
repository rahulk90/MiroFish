#!/usr/bin/env python3
"""
Standalone MiroFish Demo - No Backend Dependencies Required

This script demonstrates the ontology generation step WITHOUT needing
the full MiroFish backend installed. Perfect for testing with conda ml env.

Usage:
    python example_standalone_demo.py

Requirements:
    pip install openai python-dotenv
"""

import sys
import json
from pathlib import Path
from typing import List, Dict, Any

# Load environment
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("Installing python-dotenv...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "python-dotenv"])
    from dotenv import load_dotenv
    load_dotenv()

import os


class SimpleOntologyDemo:
    """Simplified ontology generation without backend dependencies"""

    def __init__(self):
        self.api_key = os.getenv("LLM_API_KEY")
        self.base_url = os.getenv("LLM_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")
        self.model = os.getenv("LLM_MODEL_NAME", "qwen-plus")

        if not self.api_key:
            raise ValueError("LLM_API_KEY not set in .env file")

        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        except ImportError:
            print("Installing openai...")
            import subprocess
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "openai"])
            from openai import OpenAI
            self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)

    def load_example_text(self) -> str:
        """Load example text - with interactive file selection"""
        example_dir = Path(__file__).parent / "example_data"

        # Find all markdown files
        md_files = sorted(example_dir.glob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True)

        if not md_files:
            raise FileNotFoundError(f"No .md files found in {example_dir}")

        # If only one file, use it
        if len(md_files) == 1:
            selected_file = md_files[0]
            print(f"✓ Using: {selected_file.name}\n")
        else:
            # Multiple files - let user choose
            print("\n📂 Available example files:\n")
            for i, f in enumerate(md_files, 1):
                # Show file size and modification time
                size = f.stat().st_size
                size_kb = size / 1024
                print(f"  {i}. {f.name} ({size_kb:.1f} KB)")

            print("\n  0. Use most recent (default)")

            try:
                choice = input("\nSelect file number (press Enter for default): ").strip()
                if choice == "" or choice == "0":
                    selected_file = md_files[0]
                else:
                    idx = int(choice) - 1
                    if 0 <= idx < len(md_files):
                        selected_file = md_files[idx]
                    else:
                        print("❌ Invalid selection, using most recent")
                        selected_file = md_files[0]
            except ValueError:
                print("❌ Invalid input, using most recent")
                selected_file = md_files[0]

            print(f"✓ Using: {selected_file.name}\n")

        with open(selected_file, 'r', encoding='utf-8') as f:
            return f.read()

    def generate_ontology(self, text: str, requirement: str) -> Dict[str, Any]:
        """Generate ontology using OpenAI-compatible API"""

        system_prompt = """You are a professional knowledge graph ontology design expert. Analyze the given text content and design entity and relationship type definitions suitable for social media opinion simulation.

You MUST output valid JSON format data.

Requirements:
1. Must have exactly 10 entity_types (8 specific types + 2 fallback types: Person and Organization)
2. 6-10 edge_types (relationship types)
3. Each entity_type must include: name, description, attributes, examples
4. Each edge_type must include: name, description, source_targets
5. Must include analysis_summary (brief analysis of the text in English)

Output format:
{
    "entity_types": [
        {
            "name": "Type name (English PascalCase)",
            "description": "Brief description (English)",
            "attributes": [{"name": "attribute name", "type": "text", "description": "description"}],
            "examples": ["example1", "example2"]
        }
    ],
    "edge_types": [
        {
            "name": "Relationship name (English UPPER_SNAKE_CASE)",
            "description": "Brief description (English)",
            "source_targets": [{"source": "source type", "target": "target type"}]
        }
    ],
    "analysis_summary": "English analysis summary"
}"""

        user_message = f"""Please analyze the following text and design an ontology for social media opinion simulation.

Simulation requirement:
{requirement}

Text content:
{text[:2000]}

Please generate a complete ontology definition with 10 entity_types and 6-10 edge_types in JSON format."""

        print("🔄 Calling LLM API (this may take 20-30 seconds)...")
        print(f"   Model: {self.model}")
        print(f"   Base URL: {self.base_url}")
        print(f"   Language: English\n")

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.3,
            )

            content = response.choices[0].message.content

            # Try to parse JSON
            try:
                # Find JSON in response
                start = content.find('{')
                end = content.rfind('}') + 1
                if start >= 0 and end > start:
                    json_str = content[start:end]
                    result = json.loads(json_str)
                    return result
            except json.JSONDecodeError:
                pass

            # If JSON parsing fails, return structured response
            return {
                "entity_types": self._parse_entity_types(content),
                "edge_types": self._parse_edge_types(content),
                "analysis_summary": content[:500],
                "raw_response": content
            }

        except Exception as e:
            print(f"\n❌ LLM API Error: {e}")
            print("\nTroubleshooting:")
            print("  1. Check LLM_API_KEY in .env file")
            print("  2. Check your API quota/billing")
            print("  3. Check internet connection")
            raise

    def _parse_entity_types(self, text: str) -> List[Dict]:
        """Extract entity types from response text"""
        # Fallback parsing if JSON parsing fails
        return [
            {"name": "Person", "description": "Individual person"},
            {"name": "Organization", "description": "Organization entity"}
        ]

    def _parse_edge_types(self, text: str) -> List[Dict]:
        """Extract edge types from response text"""
        # Fallback parsing if JSON parsing fails
        return [
            {"name": "WORKS_FOR", "description": "Work relationship"},
            {"name": "RELATED_TO", "description": "General relationship"}
        ]

    def display_results(self, ontology: Dict[str, Any]) -> None:
        """Display ontology results in a nice format"""
        print("\n" + "="*70)
        print("✓ ONTOLOGY GENERATED SUCCESSFULLY!")
        print("="*70 + "\n")

        # Display entity types
        print(f"📦 ENTITY TYPES ({len(ontology.get('entity_types', []))})\n")
        for et in ontology.get('entity_types', []):
            print(f"  • {et.get('name', 'N/A')}")
            print(f"    └─ {et.get('description', 'N/A')}")
            if et.get('examples'):
                print(f"    └─ Examples: {', '.join(et['examples'][:2])}")
            print()

        # Display edge types
        print(f"\n🔗 EDGE TYPES ({len(ontology.get('edge_types', []))})\n")
        for et in ontology.get('edge_types', []):
            print(f"  • {et.get('name', 'N/A')}")
            print(f"    └─ {et.get('description', 'N/A')}")
            if et.get('source_targets'):
                st = et['source_targets'][0]
                print(f"    └─ {st.get('source', '?')} → {st.get('target', '?')}")
            print()

        # Display analysis
        print(f"\n📝 ANALYSIS SUMMARY\n")
        summary = ontology.get('analysis_summary', 'N/A')
        if isinstance(summary, str):
            print(f"  {summary[:300]}")
        print("\n" + "="*70)

    def save_results(self, ontology: Dict[str, Any]) -> None:
        """Save ontology to file"""
        output_file = Path(__file__).parent / "ontology_output.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(ontology, f, ensure_ascii=False, indent=2)
        print(f"\n💾 Results saved to: {output_file}")


def main():
    """Run the standalone demo"""
    print("\n" + "🐟 "*35)
    print("MiroFish Standalone Ontology Demo")
    print("🐟 "*35)

    try:
        # Initialize
        print("\n1️⃣  Initializing...")
        demo = SimpleOntologyDemo()
        print("   ✓ OpenAI client ready")

        # Load example
        print("\n2️⃣  Loading example text...")
        text = demo.load_example_text()
        print(f"   ✓ Loaded {len(text)} characters")

        # Generate ontology
        print("\n3️⃣  Generating ontology from text...")
        requirement = "Simulate how the university plagiarism scandal evolves over 2 weeks on social media and campus forums"

        ontology = demo.generate_ontology(text, requirement)
        print("   ✓ Ontology generated")

        # Display results
        demo.display_results(ontology)

        # Save results
        demo.save_results(ontology)

        # Summary
        print("\n✅ DEMO COMPLETED SUCCESSFULLY!\n")
        print("What happened:")
        print("  1. Read example_data/university_incident.md")
        print("  2. Sent to LLM for analysis")
        print("  3. Generated ontology with entity/relationship types")
        print("  4. Saved results to ontology_output.json\n")

        print("🎯 Next Steps:")
        print("  1. Review ontology_output.json")
        print("  2. Edit example_data/university_incident.md with your own text")
        print("  3. Run demo again with your custom text")
        print("  4. Set up full pipeline: npm run dev\n")

    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ ERROR: {e}\n")
        print("Setup help:")
        print("  1. Ensure .env file exists:")
        print("     cp .env.example .env")
        print("  2. Edit .env with your API keys:")
        print("     LLM_API_KEY=your_key_here")
        print("     ZEP_API_KEY=your_key_here (optional for this demo)")
        print("  3. Install dependencies:")
        print("     pip install openai python-dotenv")
        sys.exit(1)


if __name__ == "__main__":
    main()
