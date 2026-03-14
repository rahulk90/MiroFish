#!/usr/bin/env python3
"""
Minimal MiroFish Example Demo

This script demonstrates the core MiroFish pipeline:
1. Generate ontology from text
2. Build knowledge graph
3. Generate agent personas
4. Display results

Usage:
    python example_minimal_demo.py

Requirements:
    - conda activate ml (or ensure OpenAI, zep-cloud packages are installed)
    - .env file with LLM_API_KEY and ZEP_API_KEY
"""

import sys
import os
import json
from pathlib import Path

# Add backend to path
backend_dir = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_dir))

# Load environment
from dotenv import load_dotenv
load_dotenv()

# Import MiroFish services
from app.services.ontology_generator import OntologyGenerator
from app.services.graph_builder import GraphBuilderService
from app.services.oasis_profile_generator import OasisProfileGenerator
from app.services.zep_entity_reader import ZepEntityReader
from app.utils.logger import get_logger

logger = get_logger(__name__)


def load_example_text():
    """Load the example text file"""
    example_file = Path(__file__).parent / "example_data" / "university_incident.md"
    if not example_file.exists():
        raise FileNotFoundError(f"Example file not found: {example_file}")

    with open(example_file, 'r', encoding='utf-8') as f:
        return f.read()


def demo_step_1_ontology():
    """Step 1: Generate ontology from text"""
    print("\n" + "="*70)
    print("STEP 1: ONTOLOGY GENERATION")
    print("="*70)
    print("Analyzing text to extract entity and relationship types...\n")

    text = load_example_text()
    simulation_requirement = "Simulate how the university plagiarism scandal evolves over 2 weeks on social media and campus forums"

    try:
        generator = OntologyGenerator()
        ontology = generator.generate(
            document_texts=[text],
            simulation_requirement=simulation_requirement
        )

        print("✓ Ontology Generated Successfully!\n")

        # Display results
        print(f"Entity Types ({len(ontology['entity_types'])}):")
        for ent in ontology['entity_types']:
            print(f"  • {ent['name']}: {ent['description']}")

        print(f"\nEdge Types ({len(ontology['edge_types'])}):")
        for edge in ontology['edge_types']:
            print(f"  • {edge['name']}: {edge['description']}")

        print(f"\nAnalysis Summary:")
        print(f"  {ontology.get('analysis_summary', 'N/A')[:200]}...\n")

        return ontology, text

    except Exception as e:
        print(f"✗ Error generating ontology: {e}")
        raise


def demo_step_2_graph_building(ontology, text):
    """Step 2: Build knowledge graph"""
    print("\n" + "="*70)
    print("STEP 2: KNOWLEDGE GRAPH BUILDING")
    print("="*70)
    print("Extracting entities and relationships from text...\n")

    try:
        builder = GraphBuilderService()

        # Build graph synchronously for demo (normally async)
        task_id = builder.build_graph_async(
            text=text,
            ontology=ontology,
            graph_name="University Incident Graph"
        )

        print(f"✓ Graph Building Started")
        print(f"  Task ID: {task_id}\n")

        # For demo purposes, return the task_id
        # In production, you'd poll task_manager to check completion
        return task_id

    except Exception as e:
        print(f"✗ Error building graph: {e}")
        print("  Note: This requires Zep API credentials\n")
        return None


def demo_step_3_profile_generation_mock():
    """Step 3: Generate persona profiles (mock example)"""
    print("\n" + "="*70)
    print("STEP 3: AGENT PERSONA GENERATION (Mock Example)")
    print("="*70)
    print("Generating detailed personas for each entity...\n")

    # Mock personas that would be generated
    mock_personas = [
        {
            "name": "Professor Zhang Wei",
            "type": "Professor",
            "bio": "Tenured CS professor with 20+ years experience and 50+ publications",
            "persona": "Professor Zhang Wei is a 45-year-old computer scientist known for rigorous standards and high expectations. He has built a strong reputation through years of research and mentorship. Recent promotion to vice-chair has elevated his status but also increased scrutiny. He values academic integrity deeply but is now facing questions about his own work. Somewhat defensive about the accusations but maintains he followed proper citation practices.",
            "age": 45,
            "gender": "male",
            "mbti": "INTJ",
            "profession": "Professor",
            "interested_topics": ["Research Ethics", "Computer Science", "Academic Integrity"]
        },
        {
            "name": "Alice Chen",
            "type": "Student",
            "bio": "Recent graduate, first-gen college student, now working in tech industry",
            "persona": "Alice Chen, 26, is a first-generation college student whose family made significant sacrifices for her education. As Prof. Zhang's graduate student, she conducted extensive research on neural network optimization. When she discovered similarities between her thesis and his published paper, she faced a difficult decision. She decided to speak up despite fears about her career. Articulate, principled, but anxious about the consequences of her actions.",
            "age": 26,
            "gender": "female",
            "mbti": "INFP",
            "profession": "Software Engineer",
            "interested_topics": ["Academic Ethics", "Whistleblower Protection", "AI Research"]
        },
        {
            "name": "Dr. Wang Ming",
            "type": "Journalist",
            "bio": "Science journalist with 15-year career investigating academic misconduct",
            "persona": "Dr. Wang Ming is an experienced science journalist dedicated to uncovering truth. With 15 years covering academic integrity issues, he has developed strong investigative skills and industry connections. He initially published Alice's allegations based on her account and supporting evidence. Now balancing his responsibility to report accurately while being fair to all parties involved.",
            "age": 48,
            "gender": "male",
            "mbti": "ENTJ",
            "profession": "Journalist",
            "interested_topics": ["Academic Integrity", "Investigative Journalism", "Higher Education"]
        }
    ]

    print("Generated Personas:\n")
    for i, persona in enumerate(mock_personas, 1):
        print(f"{i}. {persona['name']} ({persona['type']})")
        print(f"   Age: {persona['age']}, Gender: {persona['gender']}, MBTI: {persona['mbti']}")
        print(f"   Bio: {persona['bio']}")
        print(f"   Persona: {persona['persona'][:150]}...")
        print(f"   Topics: {', '.join(persona['interested_topics'])}")
        print()

    return mock_personas


def demo_summary():
    """Display summary and next steps"""
    print("\n" + "="*70)
    print("SUMMARY & NEXT STEPS")
    print("="*70)

    summary = """
With these three steps completed, you would have:

✓ Step 1 Output: Ontology definition
  - 10 entity types (e.g., Professor, Student, Journalist, University, etc.)
  - 6-10 relationship types (e.g., STUDIES_AT, WORKS_FOR, REPORTS_ON, etc.)
  - Analysis of the text content

✓ Step 2 Output: Knowledge graph in Zep
  - Extracted entities with attributes and summaries
  - Relationships between entities with factual descriptions
  - Full-text searchable storage

✓ Step 3 Output: Detailed persona profiles
  - Rich character descriptions for each entity
  - MBTI types, demographics, background
  - Social media behavior patterns
  - Memory of the event context

🎭 Ready for Simulation!
  These personas would be deployed as agents in a multi-agent simulation where they
  interact, discuss, and respond to the scandal on social media platforms.

🚀 To Run Full Pipeline:

  1. Ensure you have API keys:
     - LLM_API_KEY (OpenAI-compatible LLM)
     - ZEP_API_KEY (Zep Cloud)
     - Update .env file

  2. Run the web interface:
     npm run dev

  3. Upload your data and configure simulation through http://localhost:3000

  4. Or run simulations programmatically using the backend services.

📝 Example Files Location:
  Text input: example_data/university_incident.md
"""

    print(summary)


def main():
    """Run the minimal demo"""
    print("\n" + "🐟 "*35)
    print("MiroFish Minimal Example Demo")
    print("🐟 "*35)

    try:
        # Step 1: Generate Ontology
        ontology, text = demo_step_1_ontology()

        # Step 2: Build Graph (requires API keys)
        print("\nAttempting Step 2 (Graph Building)...")
        task_id = demo_step_2_graph_building(ontology, text)

        # Step 3: Generate Personas (mock for demo)
        personas = demo_step_3_profile_generation_mock()

        # Summary
        demo_summary()

        print("\n" + "="*70)
        print("Demo completed! Check the output above for results.")
        print("="*70 + "\n")

    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        print("\nMake sure you have:")
        print("  - .env file with LLM_API_KEY and ZEP_API_KEY")
        print("  - All dependencies installed (pip install -r backend/requirements.txt)")
        sys.exit(1)


if __name__ == "__main__":
    main()
