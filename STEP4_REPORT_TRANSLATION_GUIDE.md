# Step4Report.vue Translation Guide
## Backend Output Format Specification

**Document Purpose**: This guide specifies all Chinese labels that must be translated to English in the backend report output for the frontend Step4Report.vue component to parse correctly.

**Status**: Frontend is ready for translation. Backend coordination needed to output English labels instead of Chinese.

---

## Overview

The Step4Report.vue frontend component contains **~40+ regex patterns** that parse backend-generated report output. Each regex pattern matches specific Chinese labels and extracts data.

**Critical Point**: The frontend regex patterns must match the backend output labels. If the backend outputs Chinese labels, the regexes must match Chinese. If the backend outputs English labels, the regexes must match English.

### Current Situation
- Frontend: All Chinese text UI already translated to English (ready)
- Backend: Still outputs report content in Chinese
- Gap: Regex patterns need to be updated to match English backend output

### Required Changes
1. **Backend Team**: Translate all report generation output labels from Chinese to English
2. **Frontend Team**: Update regex patterns to match English labels (already identified below)

---

## Translation Mapping by Function

### 1. parseInsightForge() - Deep Insight Response Parsing

This function parses the output from the Deep Insight Tool which performs deep analysis of questions/scenarios.

| Current Chinese | New English | Pattern | Context | Example |
|---|---|---|---|---|
| `分析问题:` | `Analysis Question:` | `/分析问题:\s*(.+?)(?:\n\|$)/` | Extracts user's question | `Analysis Question: What are key factors?` |
| `预测场景:` | `Prediction Scenario:` | `/预测场景:\s*(.+?)(?:\n\|$)/` | Scenario description | `Prediction Scenario: 2025 education policy` |
| `相关预测事实:` | `Related Prediction Facts:` | `/相关预测事实:\s*(\d+)/` | Count of facts | `Related Prediction Facts: 45` |
| `涉及实体:` | `Involved Entities:` | `/涉及实体:\s*(\d+)/` | Count of entities | `Involved Entities: 12` |
| `关系链:` | `Relationship Chain:` | `/关系链:\s*(\d+)/` | Count of relationships | `Relationship Chain: 8` |
| `### 分析的子问题` | `### Analysis Sub-questions` | `/### 分析的子问题\n/` | Section header | See below |
| `### 【关键事实】` | `### 【Key Facts】` | `/### 【关键事实】[\s\S]*?\n/` | Section header | See below |
| `### 【核心实体】` | `### 【Core Entities】` | `/### 【核心实体】\n/` | Section header | See below |
| `### 【关系链】` | `### 【Relationship Chain】` | `/### 【关系链】\n/` | Section header | See below |
| `摘要:` | `Summary:` | `/摘要:\s*"?(.+?)"?(?:\n\|$)/` | Entity summary | `Summary: "Key institution"` |
| `相关事实:` | `Related Facts:` | `/相关事实:\s*(\d+)/` | Entity related count | `Related Facts: 25` |

#### Sub-section Formats

**Analysis Sub-questions Format:**
```
### Analysis Sub-questions
1. First sub-question here
2. Second sub-question here
3. Third sub-question here
```

**Key Facts Format:**
```
### 【Key Facts】
1. "First fact here"
2. "Second fact here"
3. "Third fact here"
```

**Core Entities Format:**
```
### 【Core Entities】
- **School System** (Educational Institution)
  Summary: "A key institution"
  Related Facts: 25

- **Student Population** (Group)
  Summary: "The learners"
  Related Facts: 15
```

**Relationship Chain Format:**
```
### 【Relationship Chain】
- School --[influences]--> Student
- Policy --[affects]--> School
- School --[employs]--> Teacher
```

---

### 2. parsePanorama() - Panorama Search Response Parsing

This function parses the output from the Panorama Search Tool which queries the knowledge graph.

| Current Chinese | New English | Pattern | Context | Example |
|---|---|---|---|---|
| `查询:` | `Query:` | `/查询:\s*(.+?)(?:\n\|$)/` | Query text | `Query: education policy` |
| `总节点数:` | `Total Nodes:` | `/总节点数:\s*(\d+)/` | Node count | `Total Nodes: 234` |
| `总边数:` | `Total Edges:` | `/总边数:\s*(\d+)/` | Edge count | `Total Edges: 567` |
| `当前有效事实:` | `Current Valid Facts:` | `/当前有效事实:\s*(\d+)/` | Active facts | `Current Valid Facts: 89` |
| `历史\/过期事实:` | `Historical/Expired Facts:` | `/历史\/过期事实:\s*(\d+)/` | Inactive facts | `Historical/Expired Facts: 34` |
| `### 【当前有效事实】` | `### 【Current Valid Facts】` | `/### 【当前有效事实】[\s\S]*?\n/` | Section header | See below |
| `### 【历史\/过期事实】` | `### 【Historical/Expired Facts】` | `/### 【历史\/过期事实】[\s\S]*?\n/` | Section header | See below |
| `### 【涉及实体】` | `### 【Involved Entities】` | `/### 【涉及实体】\n/` | Section header | See below |

#### Sub-section Formats

**Current Valid Facts Format:**
```
### 【Current Valid Facts】
1. "First active fact"
2. "Second active fact"
3. "Third active fact"
```

**Historical/Expired Facts Format:**
```
### 【Historical/Expired Facts】
1. "First historical fact"
2. "Second historical fact"
```

**Involved Entities Format:**
```
### 【Involved Entities】
- **School** (Organization)
- **Policy** (Concept)
- **Student** (Person)
```

---

### 3. parseInterview() - Agent Interview Response Parsing

This function parses the output from the Agent Interview Tool which conducts interviews with AI agents.

| Current Chinese | New English | Pattern | Context | Example |
|---|---|---|---|---|
| `**采访主题:**` | `**Interview Topic:**` | `/\*\*采访主题:\*\*\s*(.+?)(?:\n\|$)/` | Topic title | `**Interview Topic:** Education policy impact` |
| `**采访人数:**` | `**Interview Count:**` | `/\*\*采访人数:\*\*\s*(\d+)\s*\/\s*(\d+)/` | Success/Total | `**Interview Count:** 5 / 9` |
| `### 采访对象选择理由` | `### Interview Subject Selection Reason` | `/### 采访对象选择理由\n/` | Section header | See below |
| `_简介:` | `_Biography:` | `/_简介:\s*([\s\S]*?)_\n/` | Person biography | `_Biography: Long description_` |
| `**Q:**` | `**Q:**` | `/\*\*Q:\*\*\s*/` | Question marker | `**Q:** Question text` |
| `**A:**` | `**A:**` | `/\*\*A:\*\*\s*/` | Answer marker | `**A:** Answer text` |
| `【Twitter平台回答】` | `【Twitter Platform Answer】` | `/【Twitter平台回答】\n?/` | Platform section | See below |
| `【Reddit平台回答】` | `【Reddit Platform Answer】` | `/【Reddit平台回答】\n?/` | Platform section | See below |
| `**关键引言:**` | `**Key Quotes:**` | `/\*\*关键引言:\*\*\n/` | Quotes section | See below |
| `### 采访摘要与核心观点` | `### Interview Summary and Core Insights` | `/### 采访摘要与核心观点\n/` | Summary section | See below |

#### Interview Selection Reason Format

The regex pattern for extracting individual reasons supports 3 formats:

**Format 1 (Numbered Bold with Index):**
```
1. **Interviewee Name（index=0）**：Reason text goes here...
2. **Another Person（index=1）**：Their reason here...
```

**Format 2 (Selection Style):**
```
- 选择 Person Name（index 0）：Reason text here...
- 选择 Another Person（index 1）：Reason here...
```

**Format 3 (Bullet Bold):**
```
- **Person Name（index=0）**：Reason text here...
- **Another Person（index=1）**：Reason here...
```

#### Interview Records Format

```
#### Interview #1:
Student

**李明** (Student, School A)

_Biography: A 16-year-old student interested in education policy._

**Q:**
1. What is your view on education reform?
2. How should policy be implemented?

**A:**
Some answer text here.

【Twitter Platform Answer】
Response tailored for Twitter here

【Reddit Platform Answer】
Response tailored for Reddit here

**Key Quotes:**
> "This is an important quote from the response"
> "Another memorable quote"


#### Interview #2:
[Next interview follows same format]
```

---

### 4. parseQuickSearch() - Quick Search Response Parsing

This function parses the output from the Quick Search Tool which performs rapid fact lookups.

| Current Chinese | New English | Pattern | Context | Example |
|---|---|---|---|---|
| `搜索查询:` | `Search Query:` | `/搜索查询:\s*(.+?)(?:\n\|$)/` | Query text | `Search Query: education` |
| `找到 X 条` | `Found X results` | `/找到\s*(\d+)\s*条/` | Result count | `Found 45 results` |
| `### 相关事实:` | `### Related Facts:` | `/### 相关事实:\n/` | Section header | See below |
| `### 相关边:` | `### Related Edges:` | `/### 相关边:\n/` | Section header | See below |
| `### 相关节点:` | `### Related Nodes:` | `/### 相关节点:\n/` | Section header | See below |

#### Sub-section Formats

**Related Facts Format:**
```
### Related Facts:
1. "First relevant fact"
2. "Second relevant fact"
3. "Third relevant fact"
```

**Related Edges Format:**
```
### Related Edges:
- School --[influences]--> Student
- Policy --[affects]--> School
```

**Related Nodes Format:**
```
### Related Nodes:
- **School** (Organization)
- **Student** (Person)
- **Policy** (Concept)
```

---

## Special Formatting Rules

### 1. Numbers and Counts
- Use standard Arabic numerals: `1`, `2`, `3`
- Count format: `Label: 42` (number on same line or next line)
- Fraction format: `5 / 9` (with spaces around slash)

### 2. Bold Text
- Use markdown: `**text**` for bold
- Used for: entity names, labels, person names, markers (Q:, A:)
- Example: `- **School System** (Type)`

### 3. Section Headers
- Use markdown: `### ` for level 3 headers
- Chinese bracket notation: `【Key Facts】` (NOT English square brackets `[Key Facts]`)
- Format: `### 【Key Facts】` or just `### Key Facts`

### 4. Lists
- Numbered: `1. `, `2. `, `3. ` (with period and space)
- Bulleted: `- ` (dash and space)
- No indentation needed

### 5. Multi-line Sections
- Sections are delimited by headers starting with `###` or `---` (three dashes)
- Content ends at next section or end of response
- Internal blank lines preserved

### 6. Quotes
- Use standard double quotes: `"text"`
- Or curly quotes: `"text"` (U+201C/U+201D)
- Format in output: `> "quote text"` (on separate lines with >)

### 7. Parentheses
- Entity types: `- **Name** (Type)`
- Person info: `**Name** (Role)`
- Index notation: `**Name（index=0）**` (full-width parenthesis for index)
- Format: Full-width parentheses `（）` preferred for index notation

### 8. Platform Indicators
- Use Chinese bracket notation: `【Twitter Platform Answer】`
- Keep the bracket marks as part of the label
- Format: `【Twitter Platform Answer】\n` (newline after)

---

## Frontend Translation Checklist

Once backend output is updated to English, frontend team should:

- [ ] Search for all Chinese labels in Step4Report.vue regexes
- [ ] Replace with corresponding English labels from this guide
- [ ] Update section header patterns (e.g., `### 分析的子问题` → `### Analysis Sub-questions`)
- [ ] Update all `.match()` patterns
- [ ] Update any section delimiter patterns
- [ ] Test with backend output to verify parsing works
- [ ] Create commit: `chore: Translate Step4Report from Chinese to English`
- [ ] Push to fork

---

## Testing Strategy

### 1. Backend Output Validation
Before frontend translation, backend should validate that:
- All labels match this specification exactly
- All format rules (spacing, capitalization, punctuation) are followed
- Section delimiters work correctly
- Bracket notation matches specification

### 2. Frontend Testing
After frontend translation, test that:
- Each parsing function correctly extracts data
- No parsing errors in browser console
- All sections display correctly in UI
- Numbers and counts display properly
- Quotes and emphasis render correctly

### 3. Integration Testing
- Report generation from start to finish
- Verify all sections populate correctly
- Check timeline log display
- Validate all extracted data displays in the workflow

---

## Questions & Support

For clarifications on:
- **Exact output format**: See "Sub-section Formats" for each function
- **Special characters**: See "Special Formatting Rules"
- **Testing**: See "Testing Strategy" section
- **Edge cases**: Contact frontend team with specific example

---

## Appendix: Complete Regex Pattern Reference

### For Backend Developers (Understanding Pattern Matching)

The following are the actual JavaScript regex patterns that will parse the output:

```javascript
// parseInsightForge()
/分析问题:\s*(.+?)(?:\n|$)/  →  /Analysis Question:\s*(.+?)(?:\n|$)/
/预测场景:\s*(.+?)(?:\n|$)/  →  /Prediction Scenario:\s*(.+?)(?:\n|$)/
/相关预测事实:\s*(\d+)/  →  /Related Prediction Facts:\s*(\d+)/
/涉及实体:\s*(\d+)/  →  /Involved Entities:\s*(\d+)/
/关系链:\s*(\d+)/  →  /Relationship Chain:\s*(\d+)/
/### 分析的子问题\n/  →  /### Analysis Sub-questions\n/
/### 【关键事实】[\s\S]*?\n/  →  /### 【Key Facts】[\s\S]*?\n/
/### 【核心实体】\n/  →  /### 【Core Entities】\n/
/### 【关系链】\n/  →  /### 【Relationship Chain】\n/
/摘要:\s*"?(.+?)"?(?:\n|$)/  →  /Summary:\s*"?(.+?)"?(?:\n|$)/
/相关事实:\s*(\d+)/  →  /Related Facts:\s*(\d+)/

// parsePanorama()
/查询:\s*(.+?)(?:\n|$)/  →  /Query:\s*(.+?)(?:\n|$)/
/总节点数:\s*(\d+)/  →  /Total Nodes:\s*(\d+)/
/总边数:\s*(\d+)/  →  /Total Edges:\s*(\d+)/
/当前有效事实:\s*(\d+)/  →  /Current Valid Facts:\s*(\d+)/
/历史\/过期事实:\s*(\d+)/  →  /Historical\/Expired Facts:\s*(\d+)/
/### 【当前有效事实】[\s\S]*?\n/  →  /### 【Current Valid Facts】[\s\S]*?\n/
/### 【历史\/过期事实】[\s\S]*?\n/  →  /### 【Historical\/Expired Facts】[\s\S]*?\n/
/### 【涉及实体】\n/  →  /### 【Involved Entities】\n/

// parseInterview()
/\*\*采访主题:\*\*\s*(.+?)(?:\n|$)/  →  /\*\*Interview Topic:\*\*\s*(.+?)(?:\n|$)/
/\*\*采访人数:\*\*\s*(\d+)\s*\/\s*(\d+)/  →  /\*\*Interview Count:\*\*\s*(\d+)\s*\/\s*(\d+)/
/### 采访对象选择理由\n/  →  /### Interview Subject Selection Reason\n/
/_简介:\s*([\s\S]*?)_\n/  →  /_Biography:\s*([\s\S]*?)_\n/
/【Twitter平台回答】\n?/  →  /【Twitter Platform Answer】\n?/
/【Reddit平台回答】\n?/  →  /【Reddit Platform Answer】\n?/
/\*\*关键引言:\*\*\n/  →  /\*\*Key Quotes:\*\*\n/
/### 采访摘要与核心观点\n/  →  /### Interview Summary and Core Insights\n/

// parseQuickSearch()
/搜索查询:\s*(.+?)(?:\n|$)/  →  /Search Query:\s*(.+?)(?:\n|$)/
/找到\s*(\d+)\s*条/  →  /Found\s*(\d+)\s*results/
/### 相关事实:\n/  →  /### Related Facts:\n/
/### 相关边:\n/  →  /### Related Edges:\n/
/### 相关节点:\n/  →  /### Related Nodes:\n/
```

---

**Document Version**: 1.0
**Last Updated**: March 16, 2026
**Status**: Ready for Backend Implementation
