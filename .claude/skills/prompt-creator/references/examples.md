# Worked Examples

## Table of Contents

1. [Overview](#overview)
2. [Example 1: React Component (Simple Coding)](#example-1-react-component-simple-coding)
3. [Example 2: API Authentication (Complex Coding)](#example-2-api-authentication-complex-coding)
4. [Example 3: Performance Analysis](#example-3-performance-analysis)
5. [Example 4: Multi-Step Feature](#example-4-multi-step-feature)

## Overview

Complete examples showing how to structure prompts for different task types. Each demonstrates:
- User request
- Brief analysis
- Generated prompt following best practices
- Key structural decisions

## Example 1: React Component (Simple Coding)

### User Request
"Create a login form component for our React app with email and password fields."

### Analysis
- Task type: Simple coding (single component)
- Missing info: Validation, styling, error handling
- Required sections: objective, context, requirements, constraints, examples, verification

### Generated Prompt

```xml
<objective>
Create a React login form component with email and password validation.
Include real-time validation feedback, error handling, and loading states.

WHY: Users need secure authentication with clear feedback on input errors.
</objective>

<context>
Current state:
- React 18 app with TypeScript, Tailwind CSS
- Auth API at POST /api/auth/login
- React Hook Form used in other components

WHY: Current login is basic HTML form with no validation, causing user confusion.
</context>

<requirements>
<file path="src/components/LoginForm.tsx">
  <purpose>Login form component with validation</purpose>
  <specifications>
    - Email/password inputs with validation (format, min 8 chars)
    - Real-time validation feedback, disabled submit when invalid
    - Loading state during API call, error message display
    - TypeScript interfaces, Tailwind CSS styling
  </specifications>
</file>
</requirements>

<constraints>
- Under 150 lines
  WHY: Components should be focused and composable

- Use React Hook Form library
  WHY: Consistent with other forms in the app

- TypeScript strict mode
  WHY: Catch errors at compile time
</constraints>

<examples>
<example name="form-with-validation">
  <scenario>Form with real-time validation using React Hook Form</scenario>
  <implementation>
  ```typescript
  const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm<LoginFormData>();

  <input {...register('email', {
    required: 'Email is required',
    pattern: { value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i }
  })} />
  {errors.email && <span>{errors.email.message}</span>}
  ```
  </implementation>
</example>
</examples>

<verification>
- [ ] Component created at src/components/LoginForm.tsx
- [ ] No TypeScript errors, under 150 lines
- [ ] Email/password validation works
- [ ] Submit disabled when invalid, loading state during submission
- [ ] Error messages display correctly
</verification>
```

### Key Decisions
- Objective includes WHY for user needs
- Context explains technical stack and existing patterns
- Single file with detailed specifications
- Constraints have WHY explanations
- Example shows React Hook Form pattern
- Verification covers structural and functional checks

## Example 2: API Authentication (Complex Coding)

### User Request
"Build authentication for the backend API with registration and login."

### Analysis
- Task type: Complex coding (multiple files, security critical)
- Missing info: Token type, password hashing, database schema
- Required sections: All standard sections plus parallel_tool_calling

### Generated Prompt

```xml
<objective>
Implement JWT-based authentication for Express.js API.
Include user registration, login, token refresh, and protected route middleware.

WHY: Secure user access and enable user-specific features. Currently all 12 endpoints are public, exposing sensitive data.
</objective>

<context>
Current state:
- Express.js 4.18 API with 12 public endpoints
- PostgreSQL 14 with Sequelize ORM, User model exists
- No authentication or authorization

WHY critical: 8 of 12 endpoints expose sensitive user data.
</context>

<requirements>
<requirement name="authentication-routes">
  <file path="src/routes/auth.js">
    <purpose>Authentication endpoint handlers</purpose>
    <specifications>
      - POST /api/auth/register
        - Input: { email, password }
        - Validation: Email format, password min 8 chars
        - Returns: { success: true, token: "jwt" }
        - Error codes: 400 (validation), 409 (duplicate)

      - POST /api/auth/login
        - Input: { email, password }
        - Returns: { success: true, token: "jwt", refreshToken: "..." }
        - Error codes: 401 (invalid credentials)

      - POST /api/auth/refresh
        - Input: { refreshToken }
        - Returns: { success: true, token: "new jwt" }
    </specifications>
  </file>

  <file path="src/controllers/authController.js">
    <purpose>Authentication business logic</purpose>
    <specifications>
      - registerUser(email, password): Promise<{ user, token }>
        - Hash password with bcrypt (10 salt rounds)
        - Generate JWT token (24h expiry)

      - loginUser(email, password): Promise<{ token, refreshToken }>
        - Compare password with bcrypt
        - Generate JWT and refresh tokens

      - JWT secret from process.env.JWT_SECRET
      - Token payload: { userId, email }
    </specifications>
  </file>

  <file path="src/middleware/authenticateToken.js">
    <purpose>Middleware to protect routes</purpose>
    <specifications>
      - Extract JWT from Authorization header (Bearer token)
      - Verify token with jsonwebtoken
      - Attach decoded user to req.user
      - Return 401 if token missing, invalid, or expired
    </specifications>
  </file>
</requirement>
</requirements>

<constraints>
- Under 400 lines total
  WHY: Authentication should be focused and auditable

- Never store plaintext passwords
  WHY: Critical security requirement

- JWT secret in environment variable
  WHY: Never hardcode secrets

- Passwords hashed with bcrypt, 10 salt rounds minimum
  WHY: Industry standard for password hashing

- Token expiry: 24 hours (JWT), 7 days (refresh)
  WHY: Balance security with UX
</constraints>

<parallel_tool_calling>
Read existing files to understand integration points simultaneously.
Example: Read src/app.js, src/models/User.js in parallel.
</parallel_tool_calling>

<verification>
- [ ] All 3 files created, no syntax errors
- [ ] Registration creates hashed password, login returns JWT
- [ ] Protected routes reject invalid tokens
- [ ] Bcrypt 10+ rounds, JWT secret from env, no hardcoded secrets
- [ ] Tests pass with >90% coverage
</verification>
```

### Key Decisions
- Objective quantifies business impact (8 of 12 endpoints)
- Context explains critical need
- Nested requirements with detailed API contracts
- Security-focused constraints with WHY
- Parallel tool calling for efficiency
- Comprehensive verification across multiple dimensions

## Example 3: Performance Analysis

### User Request
"Our dashboard is slow. Can you find out why?"

### Analysis
- Task type: Investigation/analysis (not coding)
- Focus: Performance bottlenecks
- Required sections: analysis_focus, data_sources, analysis_requirements, output_format

### Generated Prompt

```xml
<objective>
Analyze the user dashboard codebase to identify performance bottlenecks.
Focus on load time optimization targeting <500ms initial render.

This analysis will inform Phase 2 optimization work.
</objective>

<analysis_focus>
Thoroughly analyze performance from multiple angles:
- Database queries: N+1 problems, missing indexes
- Frontend rendering: React re-renders, bundle size
- Network requests: Sequential vs parallel, caching
- Asset loading: Images, fonts, third-party scripts

Consider tradeoffs between different optimization strategies.
Explore various approaches before recommending the optimal combination.

Evaluate both quick wins and long-term architectural improvements.
</analysis_focus>

<data_sources>
Files: @src/pages/Dashboard.tsx, @src/components/widgets/*.tsx, @backend/routes/dashboard.js
Commands: !npm run build -- --analyze, !npm run lighthouse
DevTools: Network waterfall, Performance flame graph, Coverage
</data_sources>

<parallel_tool_calling>
Read all source files simultaneously rather than sequentially.
</parallel_tool_calling>

<analysis_requirements>
For each bottleneck: Location (file:line), Issue, Impact (quantified), Severity, Root cause, Recommendation, Expected improvement.
Analyze tradeoffs: Quick wins vs architectural changes, effort vs gain.
</analysis_requirements>

<output_format>
Save to: ./analyses/dashboard-performance-analysis.md
- Executive Summary: Current/target load time, critical findings
- Critical Bottlenecks table: Priority, File, Line, Issue, Impact, Severity
- Detailed Analysis per bottleneck: File:line, Issue, Root Cause, Recommendation, Expected improvement
- Recommendations by Priority: Quick wins vs medium-term
</output_format>

<verification>
- [ ] All data sources examined, specific line references
- [ ] Performance impact quantified, recommendations actionable
- [ ] Expected improvements estimated
</verification>
```

### Key Decisions
- Analysis focus uses extended thinking triggers
- Data sources cover all layers (files, commands, DevTools)
- Parallel tool calling for efficiency
- Structured output format for stakeholders
- Quantified impact and recommendations

## Example 4: Multi-Step Feature

### User Request
"Build user authentication system with registration, login, and profile management."

### Analysis
- Task type: Complex multi-step feature (will be broken into 4 prompts)
- This is Prompt 2 of 4: API endpoints
- Required sections: sequence_context, dependencies, execution_strategy, state_management

### Generated Prompt (Prompt 2 of 4)

```xml
<objective>
Build user authentication system.
This is Prompt 2 of 4: Implement API endpoints for registration, login, and profile.
</objective>

<sequence_context>
Previous prompts completed:
- Prompt 001: Database schema created (Users table, Sequelize models)

This prompt (002):
- Create authentication API endpoints
- Implement JWT token generation
- Build profile management endpoints

Remaining prompts:
- Prompt 003: Build React UI components
- Prompt 004: E2E tests
</sequence_context>

<dependencies>
This prompt requires (from Prompt 001):
- User model (src/models/User.js) must exist
- Database migrations must be run

This prompt produces (for Prompt 003):
- Authentication endpoints: /api/auth/register, /api/auth/login
- Profile endpoints: GET/PUT /api/users/me
- JWT middleware for route protection

Sequelize User model from Prompt 001:
{
  id: UUID,
  email: STRING (unique),
  password_hash: STRING,
  firstName: STRING,
  lastName: STRING
}
</dependencies>

<execution_strategy>
Strategy: SEQUENTIAL
Reason: API endpoints depend on database schema from Prompt 001. UI in Prompt 003 will consume these endpoints.

Flow: Database (001) → API (002) → UI (003) → Tests (004)
</execution_strategy>

<state_management>
Before starting:
- Read STATE.md to confirm Prompt 001 completed
- Verify User model exists at src/models/User.js

After completing:
- Update STATE.md:
  - Mark Prompt 002 (API endpoints) as COMPLETE
  - List files created
  - Document API contracts for Prompt 003
  - Note decisions: JWT expiry (24h), refresh token (7 days)
- Set resume point for Prompt 003
</state_management>

<requirements>
<file path="src/routes/auth.js">
  <purpose>Authentication endpoint handlers</purpose>
  <specifications>
    - POST /api/auth/register
    - POST /api/auth/login
    - POST /api/auth/refresh
  </specifications>
</file>

<file path="src/controllers/authController.js">
  <purpose>Authentication business logic</purpose>
  <specifications>
    - registerUser, loginUser, refreshToken functions
    - JWT generation with 24h expiry
    - bcrypt password hashing (10 rounds)
  </specifications>
</file>

<file path="src/middleware/authenticateToken.js">
  <purpose>JWT verification middleware</purpose>
</file>
</requirements>

<output>
After completion:
1. Update STATE.md with completion status
2. Document API contracts for Prompt 003
3. Provide usage examples
4. Confirm readiness for Prompt 003
</output>

<verification>
- [ ] STATE.md updated with Prompt 002 completion
- [ ] API contracts documented, all endpoints tested
- [ ] No blockers for Prompt 003
- [ ] Registration works, login returns JWT, protected routes require auth
</verification>
```

### Key Decisions
- Sequence context clearly states "2 of 4" with what's done and what's next
- Dependencies explicit about inputs from previous prompts and outputs for next
- Execution strategy explains why sequential
- State management instructions for reading/updating STATE.md
- Output section ensures proper handoff to next prompt
- Verification includes state tracking checks
