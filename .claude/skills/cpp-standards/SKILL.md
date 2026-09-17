---
name: cpp-standards
description: Modern C++ enterprise development standards for C++20/23/26 codebases covering naming conventions, formatting, class organization, error handling, and code modernization. Use when writing, reviewing, or refactoring C++ code. Includes audit checklist for comprehensive codebase validation.
---

# Modern C++ Standards Guide

You are the C++ Standards Guide, responsible for ensuring all C++ code follows modern enterprise development standards aligned with C++20, C++23, and C++26 best practices.

## Purpose

This skill provides authoritative guidance on modern C++ coding standards for enterprise development. It covers naming conventions, code formatting, class organization, modern language features, error handling, concurrency patterns, and build system practices. All rules are grounded in the ISO C++ standards, C++ Core Guidelines, and industry best practices.

Modern C++ has evolved significantly with C++20 concepts, ranges, and format, C++23 expected and deducing this, and C++26 contracts and reflection. This skill ensures new code leverages these features correctly while maintaining consistency across the codebase. It replaces legacy patterns (SFINAE, raw pointers, C-style casts, macros) with their modern equivalents.

The skill integrates with code review and refactoring workflows by providing a comprehensive audit checklist. Agents performing codebase audits, renaming, linting, or cleanup should load the full reference for detailed rules and examples.

## Quick Start

### Step 1: Identify the Standard
Determine the C++ standard version the project targets (C++20, C++23, or C++26) and apply only the features available at that level. All projects must meet the baseline modernization requirements (nullptr, using aliases, smart pointers, constexpr).

### Step 2: Apply Naming and Formatting
Follow the naming conventions consistently: PascalCase for types, camelCase for functions and variables, m_ prefix for members, k prefix for constants. Use Allman braces, 4-space indentation, and 120-character line limit.

### Step 3: Review Against the Audit Checklist
Before committing C++ code, load the full reference and run through the audit checklist sections relevant to your changes: naming, files, modernization, error handling, comments, formatting, and CMake.

## Core Concepts

### Naming Convention Summary

| Element | Convention | Example |
|---------|-----------|---------|
| Classes, structs, enums | `PascalCase` | `RenderGraph`, `BlendMode` |
| Functions, methods | `camelCase` | `buildAccelerationStructure()` |
| Local variables | `camelCase` | `frameIndex`, `deltaTime` |
| Member variables | `m_camelCase` | `m_frameIndex`, `m_isReady` |
| Static members | `s_camelCase` | `s_instanceCount` |
| Global variables | `g_camelCase` | `g_renderContext` |
| Constants | `kPascalCase` | `kMaxFramesInFlight` |
| Enum values | `PascalCase` | `Rgba8Unorm`, `Additive` |
| Namespaces | `lowercase` | `radiance::cuda` |
| Template params | `PascalCase` | `typename ElementType` |
| Macros | `SCREAMING_SNAKE` | `RADIANCE_API` |
| Files (.h/.cpp) | `PascalCase` | `RenderGraph.h` |
| Directories | `lowercase` | `src/`, `third-party/` |

### Class Declaration Order

Classes follow a strict declaration order within access specifiers (public, then protected, then private):

1. Type aliases and nested types
2. Constants (`static constexpr`)
3. Constructors and destructor
4. Copy/move operations (delete or define per Rule of Five/Zero)
5. Public methods
6. Accessors/getters (const-correct, `[[nodiscard]]`)
7. Protected methods (for inheritance)
8. Private methods
9. Member variables (always private unless justified)

### Modern Feature Replacements

These replacements are mandatory for all new code:

| Legacy Pattern | Modern Replacement |
|---------------|-------------------|
| `NULL`, `0` for pointers | `nullptr` |
| `typedef` | `using` alias |
| C-style casts `(int)x` | `static_cast<int>(x)` |
| Raw owning `new`/`delete` | `std::unique_ptr`, `std::shared_ptr` |
| `#define` constants | `constexpr` values |
| Include guards | `#pragma once` |
| `std::bind` | Lambdas |
| Output params `bool find(T* out)` | `std::optional<T>` return |
| SFINAE / `std::enable_if` | Concepts and `requires` clauses (C++20) |
| `sprintf` / `snprintf` | `std::format` (C++20) |
| `printf` / `std::cout` | `std::println` (C++23) |
| `T* ptr, size_t count` params | `std::span<T>` (C++20) |
| Error codes / out-params | `std::expected<T, E>` (C++23) |
| `__FILE__` / `__LINE__` | `std::source_location` (C++20) |
| `std::thread` | `std::jthread` (C++20) |

### Error Handling Strategy

Choose the right mechanism based on context:

| Mechanism | When to Use |
|-----------|-------------|
| `std::expected<T, E>` | Default for fallible operations in performance-sensitive code |
| Exceptions | Truly exceptional conditions (OOM, corrupt state), never in hot paths |
| Error codes / `bool` | C API boundaries, CUDA wrappers, legacy interop |
| `std::optional<T>` | Value-or-nothing without error info (cache lookups) |
| Assertions / contracts | Programming errors that should never occur in correct code |

Mark all error-returning functions `[[nodiscard]]`. Move constructors, move assignment, swap, and destructors must be `noexcept`.

### Code Formatting Rules

Apply consistently via `.clang-format`:

- 4-space indentation, no tabs
- 120-character line limit
- Allman brace style for functions and classes (K&R acceptable for short lambdas)
- Pointer/reference aligned left: `int* ptr`, `const Buffer& buf`
- Include order: corresponding header, project headers, third-party headers, standard library
- Blank lines between include groups

## Common Pitfalls

- ❌ **Using `snake_case` for functions** - Violates naming convention → ✅ **Use `camelCase` for all functions and methods**
- ❌ **Storing `std::string_view` as a class member** - Creates dangling reference risk → ✅ **Use `std::string` for owned storage, `string_view` only for parameters**
- ❌ **Non-noexcept move constructors** - Causes `std::vector` to copy instead of move during reallocation → ✅ **Always mark move constructors and move assignment `noexcept`**
- ❌ **Using `std::move` on return values** - Defeats Return Value Optimization (RVO/NRVO) → ✅ **Return local variables by value without `std::move`**
- ❌ **Directory-scoped CMake commands** - `include_directories()` pollutes all targets → ✅ **Use `target_include_directories()` with `PRIVATE`/`PUBLIC`/`INTERFACE`**
- ❌ **Using SFINAE for template constraints** - Unreadable, poor error messages → ✅ **Use C++20 concepts and `requires` clauses**
- ❌ **Missing `explicit` on single-argument constructors** - Allows implicit conversions → ✅ **Always mark single-argument constructors `explicit`**
- ❌ **Comments explaining what code does** - Redundant narration → ✅ **Comments explain *why*, code explains *what***

## When to Load References

Load `references/cpp-standards-2026.md` when:
- **Writing new C++ classes or files** - Full naming, formatting, and class organization rules with code examples
- **Reviewing or auditing C++ code** - Complete audit checklist (Section 14) with checkboxes for naming, files, modernization, error handling, comments, formatting, and CMake
- **Refactoring legacy C++ code** - Detailed modern feature replacement rules with before/after examples for every pattern
- **Configuring build tooling** - `.clang-format` and `.clang-tidy` reference configurations, compiler warning flags, CMake best practices
- **Implementing error handling or concurrency** - Detailed RAII patterns, `std::expected` monadic chaining, `std::jthread` with stop tokens, mutex/atomic guidance
- **Using C++26 features** - Contracts, static reflection, `std::execution`, `std::inplace_vector`, `std::hive`, `std::simd` adoption guidance

## Examples

### Example 1: Writing a New Class

**A resource-managing class following all conventions**:
```cpp
/**
 * @file GpuBuffer.h
 * @brief Declares the GpuBuffer class for managing GPU memory allocations.
 *
 * @copyright 2026 ProjectName
 */
#pragma once

#include <cstdint>
#include <expected>
#include <string>

class Device;

/**
 * @brief Manages a GPU memory allocation with automatic cleanup.
 *
 * @threadsafety Not thread-safe. Must be used from the render thread only.
 */
class GpuBuffer
{
public:
    static constexpr uint32_t kDefaultAlignment = 256;

    GpuBuffer() = default;
    explicit GpuBuffer(Device* device);
    ~GpuBuffer();

    GpuBuffer(const GpuBuffer&) = delete;
    GpuBuffer& operator=(const GpuBuffer&) = delete;
    GpuBuffer(GpuBuffer&& other) noexcept;
    GpuBuffer& operator=(GpuBuffer&& other) noexcept;

    /**
     * @brief Allocates GPU memory with the specified size and alignment.
     *
     * @param sizeInBytes  Total allocation size.
     * @param alignment    Byte alignment (must be power of two).
     * @return The mapped pointer on success, or an error message.
     */
    [[nodiscard]] std::expected<void*, std::string> allocate(
        size_t sizeInBytes, uint32_t alignment = kDefaultAlignment);

    [[nodiscard]] size_t size() const noexcept { return m_size; }
    [[nodiscard]] bool isAllocated() const noexcept { return m_data != nullptr; }

private:
    void release();

    Device* m_device = nullptr;
    void* m_data = nullptr;
    size_t m_size = 0;
};
```

**This demonstrates**: PascalCase class name, camelCase methods, m_ member prefix, k constant prefix, Rule of Five (copy deleted, move noexcept), `[[nodiscard]]`, `std::expected` return, Doxygen comments, `#pragma once`, forward declarations, Allman braces, thread safety documentation.

### Example 2: Reviewing Code Against Standards

**Given this code to review**:
```cpp
class render_pipeline {
    ID3D12PipelineState* pipeline;
    int ref_count;
public:
    render_pipeline(ID3D12Device* dev) { /* ... */ }
    ~render_pipeline() { if (pipeline) pipeline->Release(); }
    bool Initialize(const char* shader_path);
    int GetRefCount() { return ref_count; }
};
```

**Issues identified and corrected**:
```cpp
class RenderPipeline                                    // PascalCase class name
{
public:
    explicit RenderPipeline(ID3D12Device* device);      // explicit, camelCase param
    ~RenderPipeline();

    RenderPipeline(const RenderPipeline&) = delete;     // Rule of Five
    RenderPipeline& operator=(const RenderPipeline&) = delete;
    RenderPipeline(RenderPipeline&& other) noexcept;
    RenderPipeline& operator=(RenderPipeline&& other) noexcept;

    [[nodiscard]] std::expected<void, std::string>      // std::expected over bool
        initialize(std::string_view shaderPath);        // camelCase, string_view

    [[nodiscard]] int refCount() const noexcept         // camelCase, const, noexcept
    { return m_refCount; }

private:
    ComPtr<ID3D12PipelineState> m_pipeline;             // RAII wrapper, m_ prefix
    int m_refCount = 0;                                 // m_ prefix, initialized
};
```

**This demonstrates**: Applying the audit checklist to identify naming violations, missing Rule of Five, missing `explicit`, raw resource ownership, missing const-correctness, and missing `[[nodiscard]]`.

### Example 3: Modern C++20/23 Patterns

**Using concepts, ranges, and std::expected together**:
```cpp
template <typename T>
concept GpuUploadable = requires {
    requires std::is_trivially_copyable_v<T>;
    requires (sizeof(T) % 4 == 0);
};

template <GpuUploadable T>
[[nodiscard]] std::expected<GpuBuffer, std::string> uploadToGpu(
    Device* device, std::span<const T> data)
{
    auto buffer = GpuBuffer(device);
    auto result = buffer.allocate(data.size_bytes());
    if (!result)
        return std::unexpected(result.error());

    std::memcpy(*result, data.data(), data.size_bytes());
    return buffer;
}

// Using ranges to filter and process
auto visibleMeshes = scene.meshes()
    | std::views::filter(&Mesh::isVisible)
    | std::views::filter([&](const Mesh& m) {
        return frustum.contains(m.boundingBox());
    });

for (const auto& mesh : visibleMeshes)
{
    auto uploadResult = uploadToGpu(device, mesh.vertices());
    if (!uploadResult)
    {
        logError(std::format("Failed to upload mesh '{}': {}",
            mesh.name(), uploadResult.error()));
        continue;
    }
}
```

**This demonstrates**: Custom concepts with compound requirements, `std::span` for non-owning data views, `std::expected` for error propagation, ranges pipeline with views::filter, `std::format` for type-safe string formatting, Allman braces throughout.
