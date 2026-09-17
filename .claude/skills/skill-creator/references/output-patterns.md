# Skill Output Patterns and Quality Standards

## Overview

This document defines quality standards, templates, and verification patterns for skill output. Use these patterns to ensure consistent, high-quality skill creation.

## Pattern 1: SKILL.md Quality Standards

### When to Use

Use this checklist when writing or reviewing any SKILL.md file.

### Quality Checklist

**Frontmatter Requirements:**
- [ ] `name` field present and lowercase
- [ ] `name` matches directory name exactly
- [ ] `description` field present
- [ ] `description` under 200 characters
- [ ] `description` includes trigger ("Use when...")
- [ ] No extra fields (keep it minimal)

**Structure Requirements:**
- [ ] Title matches skill name (formatted for display)
- [ ] Role statement present ("You are the {Role}")
- [ ] Purpose section 2-3 paragraphs
- [ ] Quick Start section with 3 steps
- [ ] 2-4 core knowledge sections
- [ ] Common Pitfalls section with 3+ items
- [ ] When to Load References section
- [ ] Examples section with 2-3 working examples
- [ ] Total under 500 lines

**Content Quality:**
- [ ] Role is specific and actionable
- [ ] Purpose explains value and outcomes
- [ ] Quick Start steps are immediately actionable
- [ ] Core sections teach essential knowledge
- [ ] Pitfalls show wrong approach → correct approach
- [ ] Reference triggers are clear and specific
- [ ] Examples are complete and self-contained
- [ ] No placeholder or TODO content

**Writing Quality:**
- [ ] Clear, direct language
- [ ] Active voice preferred
- [ ] Technical accuracy verified
- [ ] Code examples are syntactically correct
- [ ] Formatting is consistent
- [ ] No grammatical errors
- [ ] Appropriate use of markdown

### Example: High-Quality SKILL.md Header

```markdown
---
name: api-testing
description: Guide for creating REST API tests with Jest and Supertest. Use when building API test suites or validating endpoints.
---

# API Testing

You are the API Testing Guide, responsible for helping developers create comprehensive, maintainable API test suites.

## Purpose

API testing ensures your backend endpoints work correctly, handle errors gracefully, and maintain contracts with frontend clients. This skill provides patterns for writing clear, reliable tests that catch bugs early and document API behavior.

Well-tested APIs reduce production bugs, speed up development through confidence in changes, and serve as living documentation for API consumers. This skill focuses on Jest and Supertest for Node.js APIs, but patterns apply broadly.

## Quick Start

### Step 1: Set Up Test Environment

Install dependencies and configure Jest:
```bash
npm install --save-dev jest supertest
```

Create `jest.config.js`:
```javascript
module.exports = {
  testEnvironment: 'node',
  coveragePathIgnorePatterns: ['/node_modules/'],
};
```

### Step 2: Write Your First Test
...
```

**What Makes This Good:**
- Frontmatter is minimal and complete
- Role is specific and clear
- Purpose explains value (3 paragraphs)
- Quick Start is immediately actionable
- Code examples are complete and correct

### Example: Poor-Quality SKILL.md Header

```markdown
---
name: api-testing-v2
description: API testing helper
tools: bash, node
version: 2.0
---

# API Testing Helper V2

You are an API testing assistant.

## About

This skill helps with API testing.

## Getting Started

First, you need to set up your environment. Then you can start testing.
...
```

**What's Wrong:**
- Version in name and frontmatter
- Vague description without trigger
- Extra fields in frontmatter
- Generic role statement
- Purpose doesn't explain value
- Quick Start isn't actionable
- No code examples

## Pattern 2: Reference File Standards

### When to Use

Use these standards when creating any reference file in `references/` directory.

### Reference File Structure

```markdown
# {Clear Topic Title}

## Overview
{2-3 sentences explaining what this reference covers}

## Pattern 1: {Descriptive Name}

### When to Use
{Clear trigger conditions for this pattern}

### Implementation
{Step-by-step instructions OR complete code example}

### Example
{Working example showing the pattern in use}

## Pattern 2: {Descriptive Name}

### When to Use
{Clear trigger conditions}

### Implementation
{Instructions or code}

### Example
{Working example}

## Pattern 3-6: {More Patterns}
{Follow same structure}
```

### Quality Standards

**Structure:**
- [ ] Title clearly identifies topic
- [ ] Overview section present (2-3 sentences)
- [ ] 4-8 patterns included
- [ ] Each pattern has all three subsections
- [ ] Consistent formatting throughout
- [ ] 200-500 lines total

**Content:**
- [ ] "When to Use" is specific and actionable
- [ ] Implementation is step-by-step or code
- [ ] Examples are complete and working
- [ ] No placeholder content
- [ ] Cross-references are accurate
- [ ] Technical accuracy verified

**Code Examples:**
- [ ] Syntactically correct
- [ ] Self-contained (includes imports, context)
- [ ] Properly formatted
- [ ] Comments explain non-obvious parts
- [ ] Realistic (not toy examples)

### Example: High-Quality Reference File

```markdown
# API Testing Workflows

## Overview

Complete workflows for creating, organizing, and maintaining API test suites using Jest and Supertest. Each workflow includes step-by-step instructions and examples.

## Pattern 1: Test Suite Creation Workflow

### When to Use

Use this workflow when starting a new API test suite from scratch or adding tests to an existing API.

### Implementation

**Step 1: Analyze API Endpoints**

List all endpoints to test:
- `GET /api/users` - List users
- `GET /api/users/:id` - Get user by ID
- `POST /api/users` - Create user
- `PUT /api/users/:id` - Update user
- `DELETE /api/users/:id` - Delete user

Identify test cases for each:
- Happy path (valid input, expected output)
- Error cases (validation, not found, unauthorized)
- Edge cases (empty list, special characters, limits)

**Step 2: Create Test File Structure**

Organize tests by resource:
```
tests/
├── setup.js          # Test environment setup
├── users.test.js     # User endpoint tests
├── posts.test.js     # Post endpoint tests
└── auth.test.js      # Auth endpoint tests
```

**Step 3: Write Setup File**

Create `tests/setup.js`:
```javascript
const { sequelize } = require('../models');

beforeAll(async () => {
  // Connect to test database
  await sequelize.sync({ force: true });
});

afterAll(async () => {
  // Close connections
  await sequelize.close();
});
```

**Step 4: Write First Test File**

Create `tests/users.test.js`:
```javascript
const request = require('supertest');
const app = require('../app');
const { User } = require('../models');

describe('User Endpoints', () => {
  beforeEach(async () => {
    // Clear data before each test
    await User.destroy({ where: {} });
  });

  describe('GET /api/users', () => {
    it('should return empty array when no users', async () => {
      const response = await request(app)
        .get('/api/users')
        .expect(200);

      expect(response.body).toEqual([]);
    });

    it('should return all users', async () => {
      // Create test users
      await User.bulkCreate([
        { name: 'Alice', email: 'alice@example.com' },
        { name: 'Bob', email: 'bob@example.com' },
      ]);

      const response = await request(app)
        .get('/api/users')
        .expect(200);

      expect(response.body).toHaveLength(2);
      expect(response.body[0]).toMatchObject({
        name: 'Alice',
        email: 'alice@example.com',
      });
    });
  });
});
```

**Step 5: Run and Verify**

```bash
npm test
```

Verify all tests pass, then continue with remaining endpoints.

### Example

Complete workflow for a simple blog API:

1. **Analyzed endpoints:**
   - `GET /api/posts` - List posts
   - `POST /api/posts` - Create post
   - `PUT /api/posts/:id` - Update post
   - `DELETE /api/posts/:id` - Delete post

2. **Created test structure:**
   ```
   tests/
   ├── setup.js
   └── posts.test.js
   ```

3. **Wrote setup file** (database initialization)

4. **Wrote posts.test.js** with 12 test cases:
   - List empty, list with posts
   - Create valid post, create invalid post
   - Update existing, update non-existent
   - Delete existing, delete non-existent
   - Authorization tests (4 cases)

5. **Ran tests:** All 12 passing

**Result:** Complete, maintainable test suite
```

**What Makes This Good:**
- Clear workflow with numbered steps
- Each step has concrete actions
- Code examples are complete and realistic
- Example shows end-to-end application
- 200+ lines of practical guidance

## Pattern 3: Code Example Requirements

### When to Use

Use these standards for any code example in skills or references.

### Code Example Standards

**Minimal Example (1-10 lines):**
```javascript
// ✅ Good: Clear, self-contained, correct
const response = await request(app)
  .get('/api/users')
  .expect(200);

expect(response.body).toHaveLength(2);
```

```javascript
// ❌ Bad: Unclear context, incomplete
const response = await request(app).get('/api/users');
expect(response.body).toHaveLength(2); // What about status?
```

**Medium Example (10-50 lines):**
```javascript
// ✅ Good: Includes imports, setup, implementation, assertions
const request = require('supertest');
const app = require('../app');
const { User } = require('../models');

describe('GET /api/users/:id', () => {
  it('should return user by ID', async () => {
    // Setup
    const user = await User.create({
      name: 'Alice',
      email: 'alice@example.com',
    });

    // Execute
    const response = await request(app)
      .get(`/api/users/${user.id}`)
      .expect(200);

    // Assert
    expect(response.body).toMatchObject({
      id: user.id,
      name: 'Alice',
      email: 'alice@example.com',
    });
  });
});
```

```javascript
// ❌ Bad: Missing imports, unclear setup, incomplete
describe('GET /api/users/:id', () => {
  it('works', async () => {
    const response = await request(app).get('/api/users/1');
    expect(response.body.name).toBe('Alice'); // Where did Alice come from?
  });
});
```

**Large Example (50+ lines):**
```javascript
// ✅ Good: Complete file with all context
// tests/users.test.js
const request = require('supertest');
const app = require('../app');
const { User } = require('../models');

describe('User Endpoints', () => {
  beforeEach(async () => {
    await User.destroy({ where: {} });
  });

  describe('POST /api/users', () => {
    it('should create user with valid data', async () => {
      const userData = {
        name: 'Alice',
        email: 'alice@example.com',
        password: 'securepass123',
      };

      const response = await request(app)
        .post('/api/users')
        .send(userData)
        .expect(201);

      expect(response.body).toMatchObject({
        name: 'Alice',
        email: 'alice@example.com',
      });
      expect(response.body.password).toBeUndefined();
      expect(response.body.id).toBeDefined();
    });

    it('should return 400 for invalid email', async () => {
      const userData = {
        name: 'Bob',
        email: 'invalid-email',
        password: 'securepass123',
      };

      const response = await request(app)
        .post('/api/users')
        .send(userData)
        .expect(400);

      expect(response.body.error).toMatch(/email/i);
    });

    it('should return 400 for duplicate email', async () => {
      await User.create({
        name: 'Alice',
        email: 'alice@example.com',
        password: 'hashedpass',
      });

      const userData = {
        name: 'Bob',
        email: 'alice@example.com',
        password: 'securepass123',
      };

      const response = await request(app)
        .post('/api/users')
        .send(userData)
        .expect(400);

      expect(response.body.error).toMatch(/email.*exists/i);
    });
  });
});
```

### Quality Checklist

**All Examples:**
- [ ] Syntactically correct
- [ ] Follows language conventions
- [ ] Properly indented and formatted
- [ ] No typos in code
- [ ] Comments explain non-obvious parts

**Context:**
- [ ] Imports/requires included if needed
- [ ] Setup/teardown shown if needed
- [ ] Dependencies clear
- [ ] File path indicated for large examples

**Realism:**
- [ ] Not a toy example
- [ ] Realistic variable names
- [ ] Realistic data
- [ ] Production-quality patterns

**Completeness:**
- [ ] Can be copy-pasted and run (with minimal setup)
- [ ] No missing pieces
- [ ] No "..." placeholders without explanation
- [ ] Error handling shown where appropriate

## Pattern 4: Documentation Standards

### When to Use

Use these standards for all documentation in skills and references.

### Writing Style

**Clarity:**
- Use clear, direct language
- Prefer active voice: "Create a file" vs. "A file should be created"
- Use present tense: "The function returns" vs. "The function will return"
- Avoid jargon unless necessary and defined

**Structure:**
- Start with overview/context
- Use numbered lists for sequences
- Use bulleted lists for options/features
- Use headers for sections
- Use code blocks for code
- Use quotes for commands/file paths

**Tone:**
- Professional but friendly
- Direct and actionable
- Avoid filler words
- Focus on what matters

### Example: Good Documentation

```markdown
## Setting Up Jest for API Testing

Jest is a testing framework that provides test runners, assertions, and mocking. For API testing, combine it with Supertest for HTTP request simulation.

**Installation:**

```bash
npm install --save-dev jest supertest
```

**Configuration:**

Create `jest.config.js`:
```javascript
module.exports = {
  testEnvironment: 'node',
  coveragePathIgnorePatterns: ['/node_modules/'],
  testMatch: ['**/__tests__/**/*.js', '**/?(*.)+(spec|test).js'],
};
```

**Package.json:**

Add test script:
```json
{
  "scripts": {
    "test": "jest",
    "test:watch": "jest --watch"
  }
}
```

**Verify:**

Run `npm test` - you should see "No tests found" if no tests exist yet.
```

**What's Good:**
- Clear section structure
- Direct, actionable instructions
- Complete code examples
- Verification step included

### Example: Poor Documentation

```markdown
## Jest Setup

You might want to install Jest and probably Supertest too.

```bash
npm install jest supertest
```

Then you need to configure it somehow. Create a config file with the right settings.

After that you can run tests.
```

**What's Wrong:**
- Vague language ("might", "probably", "somehow")
- Incomplete instructions
- No code examples for config
- No verification step
- Passive, uncertain tone

## Pattern 5: Verification Patterns

### When to Use

Use these patterns to verify skill quality before considering it complete.

### Verification Workflow

**Step 1: Automated Checks**

Run these checks programmatically if possible:
- [ ] File exists at correct path
- [ ] Frontmatter valid YAML
- [ ] Line count under limits
- [ ] Markdown syntax valid
- [ ] Code blocks have language specified
- [ ] No broken internal links

**Step 2: Structural Review**

Verify structure manually:
- [ ] All required sections present
- [ ] Sections in correct order
- [ ] Consistent heading levels
- [ ] Proper markdown formatting

**Step 3: Content Review**

Verify content quality:
- [ ] Role statement is specific
- [ ] Purpose explains value
- [ ] Quick Start is actionable
- [ ] Examples are complete
- [ ] Code is correct
- [ ] No placeholders

**Step 4: Integration Review**

Verify framework fit:
- [ ] Name follows conventions
- [ ] Description has clear trigger
- [ ] References use standard naming
- [ ] Cross-references are accurate

**Step 5: User Testing**

Simulate actual use:
- [ ] Read description - would I invoke this skill?
- [ ] Read Quick Start - can I start immediately?
- [ ] Try example - does it work?
- [ ] Load reference - is trigger clear?

### Example Verification Report

**Skill:** `api-testing`

**Automated Checks:**
- ✅ Path: `.claude/skills/api-testing/SKILL.md`
- ✅ Frontmatter valid
- ✅ SKILL.md: 412 lines (< 500)
- ✅ workflows.md: 287 lines (200-500)
- ✅ patterns.md: 356 lines (200-500)
- ✅ Markdown valid
- ✅ All code blocks tagged
- ✅ No broken links

**Structural Review:**
- ✅ Frontmatter, role, purpose present
- ✅ Quick Start has 3 steps
- ✅ 4 core sections
- ✅ Common Pitfalls section
- ✅ 3 examples
- ✅ Consistent H2/H3 usage

**Content Review:**
- ✅ Role: "API Testing Guide" - specific
- ✅ Purpose: 3 paragraphs explaining value
- ✅ Quick Start: Setup, write test, run - actionable
- ✅ Examples: Complete with imports and assertions
- ✅ Code tested and working
- ✅ No TODOs or placeholders

**Integration Review:**
- ✅ Name: `api-testing` (no version, clear)
- ✅ Description: "Guide for creating REST API tests... Use when building test suites"
- ✅ References: workflows.md, patterns.md (standard names)
- ✅ Cross-refs accurate

**User Testing:**
- ✅ Description clearly indicates API testing use case
- ✅ Quick Start immediately actionable
- ✅ Tried GET request example - works
- ✅ Loaded workflows.md - trigger was clear

**Result:** ✅ Skill passes all verification checks
