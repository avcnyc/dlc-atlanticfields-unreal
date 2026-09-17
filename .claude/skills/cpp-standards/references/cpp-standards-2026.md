# Modern C++ Enterprise Development Standards (2026)

> **Purpose:** This document defines enterprise/industry-standard conventions for modern C++ codebases (C++20/23/26). It is intended for use by agents performing codebase audits, refactoring, renaming, linting, and cleanup. All rules should be applied consistently and comprehensively across the entire codebase.
>
> **Standards Status:** C++20 (ISO 14882:2020), C++23 (ISO 14882:2023) are ratified. C++26 reached feature freeze (Sofia, June 2025) and is in final ballot (expected formal approval London, March 2026).

---

## 1. Naming Conventions

### 1.1 Types, Classes, Structs, Enums

- **Rule:** `PascalCase` for all user-defined types.
- Applies to: `class`, `struct`, `union`, `enum class`, `enum`, `using` aliases, `typedef`.

```cpp
// Correct
class RenderGraph {};
struct BufferDesc {};
enum class BlendMode { Additive, Alpha, Opaque };
using TextureHandle = uint32_t;

// Incorrect
class render_graph {};
struct bufferDesc {};
enum class blend_mode { additive, alpha, opaque };
```

### 1.2 Functions and Methods

- **Rule:** `camelCase` for all functions and methods.
- Applies to: free functions, member functions, static methods, lambdas assigned to named variables.

```cpp
// Correct
void buildAccelerationStructure();
bool isFrameReady() const;
uint32_t computeChecksum(const Buffer& buf);

// Incorrect
void Build_Acceleration_Structure();
void build_acceleration_structure();
void BuildAccelerationStructure();
```

### 1.3 Variables

#### Local Variables
- **Rule:** `camelCase`

```cpp
int frameIndex = 0;
float deltaTime = 0.016f;
bool isVisible = true;
```

#### Member Variables
- **Rule:** `m_camelCase` prefix

```cpp
class Renderer {
    int m_frameIndex;
    float m_deltaTime;
    bool m_isInitialized;
};

// Incorrect
int frameIndex_;   // trailing underscore
int _frameIndex;   // leading underscore — reserved in global/namespace scope
int frameindex;    // no casing distinction
```

#### Static Member Variables
- **Rule:** `s_camelCase` prefix

```cpp
static int s_instanceCount;
static Device* s_activeDevice;
```

#### Global Variables
- **Rule:** `g_camelCase` prefix. Minimize global state.

```cpp
RenderContext* g_renderContext = nullptr;
DeviceManager* g_deviceManager = nullptr;
```

### 1.4 Constants and Compile-Time Values

- **Rule:** `kPascalCase` for `constexpr`, `const` globals, and named constants.

```cpp
// Correct
constexpr int kMaxFramesInFlight = 3;
constexpr float kPi = 3.14159265f;
constexpr uint32_t kDefaultAlignment = 256;

// Incorrect (legacy C style)
#define MAX_FRAMES_IN_FLIGHT 3
const int MAX_FRAMES = 3;
```

### 1.5 Enum Values

- **Rule:** `PascalCase` for `enum class` values. `SCREAMING_SNAKE` is legacy — avoid.

```cpp
// Correct
enum class TextureFormat {
    Rgba8Unorm,
    Rgba16Float,
    Depth32Float,
};

// Incorrect
enum class TextureFormat {
    RGBA8_UNORM,
    TEXTURE_FORMAT_RGBA8,
};
```

### 1.6 Namespaces

- **Rule:** `lowercase` or `snake_case`. Short and descriptive.
- **Never** `using namespace` in headers (pollutes all includers).
- Anonymous namespaces for internal linkage in `.cpp` files (replaces `static` for free functions).
- Prefer C++17 nested syntax: `namespace a::b::c {}`.

```cpp
// Correct
namespace radiance {}
namespace radiance::cuda {}
namespace render::core {}

// Incorrect
namespace Radiance {}
namespace RenderCore {}
```

### 1.7 Template Parameters

- **Rule:** `PascalCase` for both type and non-type parameters.

```cpp
template <typename T>
template <typename ElementType, typename Allocator>
template <typename T, size_t N>
template <std::integral T>  // C++20 concept-constrained
```

### 1.8 Macros

- **Rule:** `SCREAMING_SNAKE_CASE` with a project-specific prefix. Minimize macro usage — prefer `constexpr`, `inline`, templates, and concepts.

```cpp
// Correct
#define RADIANCE_API __declspec(dllexport)
#define RADIANCE_CHECK(x) ...

// Incorrect
#define renderCheck(x) ...
#define api __declspec(dllexport)
```

### 1.9 Interface Classes (Pure Virtual)

- **Rule:** Prefix with `I` (optional but common in Windows/plugin/SDK codebases).
- **Always** declare a `virtual` destructor (prevents undefined behavior when deleting through base pointer).

```cpp
class IRenderer
{
public:
    virtual ~IRenderer() = default;
    virtual void render() = 0;
};
```

---

## 2. File Naming and Casing

### 2.1 Source Files

- **Rule:** `PascalCase` — file name matches the primary class defined within it.
- Extensions: `.cpp` for implementation, `.h` for headers, `.cu` for CUDA.

```
RenderGraph.h / RenderGraph.cpp
ReSTIRSampler.h / ReSTIRSampler.cpp
JfaKernels.cu
```

### 2.2 Non-Class Files

- Utility files, free-function collections, and module-level files use `PascalCase` descriptive names.

```
MathUtils.h
StringHelpers.cpp
CudaInterop.h
```

### 2.3 Shader Files

- **Rule:** `PascalCase` or `snake_case` — be consistent within shader directories.

```
PathTracer.hlsl
Denoiser.comp.glsl
```

### 2.4 CMake and Config Files

```
CMakeLists.txt              # always this exact name
compiler_options.cmake       # snake_case for cmake modules
project-config.json          # kebab-case or snake_case for data files
vcpkg.json
```

---

## 3. Folder / Directory Structure

### 3.1 Folder Naming Rules

- **Rule:** `lowercase` preferred. `kebab-case` acceptable. Never `PascalCase` or `camelCase`.
- Folders are organizational buckets — they are not class names.

```
// Correct
src/
include/
third-party/
build/
plugins/

// Incorrect
Src/
Include/
ThirdParty/
Build/
Plugins/
```

### 3.2 Standard Top-Level Layout

```
project-root/
+-- CMakeLists.txt
+-- vcpkg.json
+-- .clang-format
+-- .clang-tidy
+-- .editorconfig
|
+-- include/
|   +-- <projectname>/          # Public API headers, namespaced subfolder
|       +-- Scatter.h
|       +-- Radiance.h
|
+-- src/
|   +-- scatter/                # Subfolder per module/system
|   |   +-- RenderGraph.h       # Private headers alongside .cpp
|   |   +-- RenderGraph.cpp
|   +-- radiance/
|       +-- RadianceCascade.h
|       +-- RadianceCascade.cpp
|
+-- plugins/                    # Plugin wrappers (e.g. TouchDesigner TOPs)
|   +-- ScatterTOP.h
|   +-- ScatterTOP.cpp
|
+-- shaders/
+-- tests/
+-- docs/
+-- cmake/                      # CMake helper scripts and find modules
+-- third-party/                # Vendored dependencies
    +-- donut/
    +-- nrd/
```

### 3.3 Key Structural Rules

- **`include/<projectname>/`** — Public headers live here, namespaced. Consumers `#include <projectname/Scatter.h>`.
- **Private headers** — Live alongside their `.cpp` in `src/`. Not exposed in `include/`.
- **One class per file** — `RenderGraph.h` / `RenderGraph.cpp` contains `class RenderGraph`.
- **`src/` not `source/`** — Always the short form.
- **`tests/` not `test/`** — Plural form is standard in modern projects.
- **`third-party/` not `vendor/`** — More descriptive; `vendor/` is a Go convention.
- **`build/` not `Build/`** — Lowercase like all other directories.
- **`plugins/` not `Plugins/`** — Lowercase like all other directories.

---

## 4. Code Formatting

### 4.1 Indentation and Spacing

- **Indent:** 4 spaces. No tabs.
- **Line length:** 120 characters max.
- **Braces:** Allman style (opening brace on new line) for class/function definitions. K&R acceptable for small lambdas and short control flow.

```cpp
// Allman (preferred for functions and classes)
void buildAccelerationStructure()
{
    if (m_isReady)
    {
        doWork();
    }
}

// K&R acceptable for inline lambdas
auto fn = [](int x) { return x * 2; };
```

### 4.2 Include Order

Includes must be ordered as follows, with blank lines between groups:

```cpp
// 1. Corresponding header (for .cpp files)
#include "RenderGraph.h"

// 2. Project headers
#include "Log.h"
#include "CUDABufferManager.h"

// 3. Third-party headers
#include <cuda_runtime.h>
#include <d3d12.h>

// 4. Standard library headers
#include <cstdint>
#include <memory>
#include <vector>
```

### 4.3 Pointer and Reference Alignment

```cpp
// Correct — attach to type
int* ptr;
const Buffer& buf;
void* data;

// Incorrect
int *ptr;
const Buffer &buf;
```

### 4.4 `auto` Usage

- Use `auto` when the type is obvious from context or avoids verbose iterator/template types.
- Do not use `auto` where it obscures the type.

```cpp
// Good — type is obvious
auto it = m_textures.begin();
auto device = std::make_unique<Device>();
auto [key, value] = *it;  // structured binding

// Bad — type is unclear
auto x = getValue();
```

### 4.5 Designated Initializers (C++20)

Prefer designated initializers for aggregate types — improves readability and resilience to member reordering.

```cpp
struct BufferDesc {
    size_t size = 0;
    uint32_t alignment = 256;
    bool mappable = false;
};

// Correct — clear which field is which
auto desc = BufferDesc{.size = 1024, .alignment = 64, .mappable = true};

// Avoid — positional, fragile
auto desc = BufferDesc{1024, 64, true};
```

### 4.6 `using enum` (C++20)

Reduce verbosity in switch statements over scoped enums:

```cpp
switch (mode)
{
    using enum BlendMode;
    case Additive: break;
    case Alpha:    break;
    case Opaque:   break;
}
```

---

## 5. Comments and Documentation

### 5.1 File Header

Every source file begins with a file header comment.

```cpp
/**
 * @file RenderGraph.h
 * @brief Declares the RenderGraph class for managing frame render passes.
 *
 * @copyright 2026 Radiance
 */
```

### 5.2 Class Documentation

```cpp
/**
 * @brief Manages the directed acyclic graph of render passes for a single frame.
 *
 * @note Not thread-safe. Must be created and used on the render thread.
 */
class RenderGraph { ... };
```

### 5.3 Function Documentation

Use Doxygen-style `@brief`, `@param`, `@return`, `@note`, `@warning` tags on all public API functions.

```cpp
/**
 * @brief Adds a render pass to the graph.
 *
 * @param name    Human-readable name for debugging and profiling.
 * @param setup   Callback to declare resource reads/writes.
 * @param execute Callback to record GPU commands.
 * @return        Handle to the created pass for dependency tracking.
 *
 * @warning Must be called before compile(). Calling after compile() is undefined.
 */
PassHandle addPass(std::string_view name, SetupCallback setup, ExecuteCallback execute);
```

### 5.4 Inline Comments

- Use `//` for single-line inline comments. Not `/* */`.
- Comments explain *why*, not *what*. Code explains what; comments explain intent.
- Place comments on the line above the relevant code.

```cpp
// Correct — explains why
// Align to 256 bytes to satisfy DX12 constant buffer requirements.
size_t alignedSize = align(size, 256);

// Incorrect — explains what (redundant)
size_t alignedSize = align(size, 256); // align the size
```

### 5.5 TODO / FIXME / HACK Tags

```cpp
// TODO(cw): Implement async pipeline compilation when driver support lands.
// FIXME(cw): This leaks memory if compile() throws — add RAII guard.
// HACK(cw): Workaround for NVAPI bug #12345, remove after driver 560+.
```

### 5.6 Commented-Out Code

- **Do not commit commented-out code.** Use version control to recover deleted code.

---

## 6. Class Structure and Organization

### 6.1 Declaration Order Within a Class

```cpp
class RenderGraph
{
public:
    // 1. Type aliases and nested types
    using PassHandle = uint32_t;

    // 2. Constants
    static constexpr uint32_t kMaxPasses = 512;

    // 3. Constructors / Destructor
    RenderGraph() = default;
    explicit RenderGraph(Device* device);
    ~RenderGraph();

    // 4. Delete copy if non-copyable, define move semantics
    RenderGraph(const RenderGraph&) = delete;
    RenderGraph& operator=(const RenderGraph&) = delete;
    RenderGraph(RenderGraph&&) noexcept;
    RenderGraph& operator=(RenderGraph&&) noexcept;

    // 5. Public methods
    PassHandle addPass(...);
    void compile();
    void execute(CommandList* cmd);

    // 6. Accessors / getters (const-correct)
    [[nodiscard]] bool isCompiled() const { return m_isCompiled; }
    [[nodiscard]] uint32_t getPassCount() const;

protected:
    // 7. Protected methods (for inheritance)

private:
    // 8. Private methods
    void resolveBarriers();
    void topologicalSort();

    // 9. Member variables (always private unless good reason)
    Device* m_device = nullptr;
    std::vector<PassEntry> m_passes;
    bool m_isCompiled = false;
};
```

### 6.2 Rule of Five / Zero

- If a class manages a resource, explicitly define or delete all five: destructor, copy constructor, copy assignment, move constructor, move assignment.
- If a class manages no resources, default all five (Rule of Zero).

```cpp
// Rule of Zero — no resource management
class Config
{
    std::string m_name;
    int m_value = 0;
    // compiler-generated defaults are fine
};

// Rule of Five — owns a raw resource
class Buffer
{
public:
    ~Buffer() { release(); }
    Buffer(const Buffer&) = delete;
    Buffer& operator=(const Buffer&) = delete;
    Buffer(Buffer&& other) noexcept;
    Buffer& operator=(Buffer&& other) noexcept;
private:
    ID3D12Resource* m_resource = nullptr;
};
```

### 6.3 `explicit` on Single-Argument Constructors

```cpp
explicit Buffer(size_t sizeInBytes);
explicit Handle(uint32_t id);
```

### 6.4 `const` Correctness

- Mark member functions `const` if they don't modify observable state.
- Pass by `const&` for types larger than a pointer.
- Use `const` iterators when not modifying elements.
- Default to `const` — remove it only when mutation is needed.

```cpp
// Correct
[[nodiscard]] int width() const { return m_width; }
void processBuffer(const Buffer& buf);
for (const auto& pass : m_passes) { ... }

// Incorrect — missing const
int width() { return m_width; }  // should be const
void processBuffer(Buffer& buf); // if not modifying, should be const&
```

---

## 7. Modern C++ Language Features

### 7.1 Core Modernization (pre-C++20)

These are baseline requirements — all new code must use these:

| Legacy | Modern Replacement |
|--------|--------------------|
| `NULL`, `0` for pointers | `nullptr` |
| `typedef` | `using` alias |
| C-style casts `(int)x` | `static_cast<int>(x)`, `reinterpret_cast` |
| Raw owning `new`/`delete` | `std::unique_ptr`, `std::shared_ptr` |
| `#define` constants | `constexpr` values |
| Include guards | `#pragma once` |
| `std::bind` | Lambdas |
| Output parameters `bool find(T* out)` | `std::optional<T>` return |

### 7.2 Smart Pointers and Ownership

- `std::unique_ptr` for exclusive ownership (default choice).
- `std::shared_ptr` only when shared ownership is genuinely required.
- Raw pointer = **non-owning observer**. Never use raw pointers for ownership in new code.

```cpp
auto device = std::make_unique<Device>();
std::shared_ptr<Texture> sharedTex = std::make_shared<Texture>();
```

### 7.3 Concepts and Constraints (C++20)

Prefer concepts over SFINAE for constraining templates. Concepts are readable, produce better error messages, and are the standard way to express generic requirements.

```cpp
// Correct — C++20 concept constraint
template <std::floating_point T>
T lerp(T a, T b, T t) { return a + t * (b - a); }

// Correct — custom concept
template <typename T>
concept Renderable = requires(T obj, CommandList& cmd) {
    { obj.render(cmd) } -> std::same_as<void>;
    { obj.isVisible() } -> std::convertible_to<bool>;
};

template <Renderable T>
void drawAll(std::span<const T> objects, CommandList& cmd);

// Correct — requires clause for ad-hoc constraints
template <typename T>
    requires std::is_trivially_copyable_v<T>
void uploadToGPU(std::span<const T> data);

// Avoid — old SFINAE style
template <typename T, typename = std::enable_if_t<std::is_floating_point_v<T>>>
T lerp(T a, T b, T t);
```

Standard library concepts to prefer: `std::integral`, `std::floating_point`, `std::invocable`, `std::copyable`, `std::movable`, `std::regular`, `std::same_as`, `std::convertible_to`, `std::derived_from`.

### 7.4 `std::format` and `std::print` (C++20/23)

Prefer `std::format` over `sprintf`/`snprintf` for type-safe string formatting. Prefer `std::print`/`std::println` (C++23) over `printf`/`std::cout`.

```cpp
// C++20
auto msg = std::format("Buffer {}x{} allocated ({:.1f} MB)", width, height, vramMB);

// C++23
std::println("Cascade {}: {} probes, {} directions", cascadeIndex, probeCount, dirCount);

// Avoid
char buf[256];
snprintf(buf, sizeof(buf), "Buffer %dx%d allocated (%.1f MB)", width, height, vramMB);
printf("Cascade %d: %d probes\n", cascadeIndex, probeCount);
```

**Note:** In CUDA `.cu` files and C-interop contexts, `printf`/`snprintf` remain acceptable since `<format>` is a host-only C++ feature.

### 7.5 Three-Way Comparison — Spaceship Operator (C++20)

Use `operator<=>` to generate all six comparison operators from one declaration.

```cpp
struct Version
{
    int major, minor, patch;
    auto operator<=>(const Version&) const = default;
};

// Now supports ==, !=, <, >, <=, >= automatically
```

### 7.6 `std::span` (C++20)

Use `std::span` for non-owning views over contiguous data. Replaces `T* ptr, size_t count` parameter pairs.

```cpp
// Correct — non-owning view
void uploadVertices(std::span<const Vertex> vertices);
void clearBuffer(std::span<uint8_t> data);

// Avoid — raw pointer + size
void uploadVertices(const Vertex* data, size_t count);
```

### 7.7 `std::source_location` (C++20)

Replaces `__FILE__` / `__LINE__` macros for logging and diagnostics.

```cpp
void logError(std::string_view msg,
              std::source_location loc = std::source_location::current())
{
    std::println(stderr, "[ERROR] {} ({}:{})", msg, loc.file_name(), loc.line());
}
```

**Note:** Macros like `RLOG_ERROR` remain valid when you need zero-overhead compile-time elimination via `#if`.

### 7.8 `constexpr`, `consteval`, `constinit`

```cpp
// constexpr — may be evaluated at compile time or runtime
constexpr size_t align(size_t value, size_t alignment)
{
    return (value + alignment - 1) & ~(alignment - 1);
}

// consteval (C++20) — MUST be evaluated at compile time
consteval uint32_t computeHash(std::string_view s) { ... }

// constinit (C++20) — must be initialized at compile time, but can be mutated at runtime
// Prevents the static initialization order fiasco
constinit int g_instanceCount = 0;
```

### 7.9 `if constexpr` (C++17+)

Compile-time branch elimination. Prefer over tag dispatch or SFINAE for type-based branching.

```cpp
template <typename T>
void serialize(const T& value)
{
    if constexpr (std::is_trivially_copyable_v<T>)
        memcpy(dst, &value, sizeof(T));
    else
        value.serialize(dst);
}
```

### 7.10 Attributes

```cpp
[[nodiscard]] bool initialize();                    // warn if return value ignored
[[maybe_unused]] int debugCounter = 0;              // suppress unused variable warnings
[[deprecated("Use newAPI() instead")]] void oldAPI();

// C++20 — attribute goes AFTER the condition, on the branch body
if (cache.contains(key)) [[likely]] { ... }
if (error) [[unlikely]] { handleError(); }

// C++23
[[assume(x > 0)]];                                  // optimizer hint (UB if false)
```

### 7.11 `std::unreachable()` (C++23)

Marks code paths that should never execute. Replaces platform-specific `__assume(false)` (MSVC) / `__builtin_unreachable()` (GCC/Clang).

```cpp
switch (mode)
{
    using enum BlendMode;
    case Additive: return blend_add(a, b);
    case Alpha:    return blend_alpha(a, b);
    case Opaque:   return blend_opaque(a, b);
}
std::unreachable();  // all enum values handled — optimizer can assume this
```

### 7.12 `std::expected` (C++23)

The modern error handling primitive. Prefer over out-parameters, error codes, or exceptions for fallible operations (especially in GPU/real-time contexts where exceptions are impractical).

```cpp
// Caller must handle the error
[[nodiscard]] std::expected<Buffer, std::string> createBuffer(size_t size)
{
    void* ptr = allocate(size);
    if (!ptr)
        return std::unexpected("Failed to allocate " + std::to_string(size) + " bytes");
    return Buffer{ptr, size};
}

// Monadic chaining (C++23)
auto result = createBuffer(1024)
    .and_then([](Buffer buf) { return mapBuffer(buf); })
    .transform([](MappedBuffer mb) { return mb.data(); });
```

### 7.13 `std::mdspan` (C++23)

Multidimensional non-owning view over contiguous data. Ideal for image/texture data.

```cpp
// View a flat buffer as a 2D image
auto pixels = std::mdspan(rawData.data(), height, width);
float value = pixels[y, x];  // C++23 multidimensional subscript
```

### 7.14 Ranges and Views (C++20/23)

Prefer `std::ranges` algorithms and views over raw iterator-based algorithms.

```cpp
auto visible = objects | std::views::filter(&Object::isVisible);
auto names = objects | std::views::transform(&Object::name);
std::ranges::sort(objects, {}, &Object::zOrder);

// Avoid — raw iterators for simple operations
std::sort(objects.begin(), objects.end(), [](const auto& a, const auto& b) {
    return a.zOrder() < b.zOrder();
});
```

### 7.15 Deducing `this` (C++23)

Eliminates CRTP boilerplate and const/non-const overload duplication.

```cpp
struct Widget
{
    // One definition covers both const and non-const access
    decltype(auto) getName(this auto&& self) { return std::forward_like<decltype(self)>(self.m_name); }
};
```

### 7.16 C++26 Features (Use When Compiler Support Available)

These features are ratified in C++26. Adopt as compiler support lands:

| Feature | Header | Use Case |
|---------|--------|----------|
| **Contracts** | `<contracts>` | `[[pre: x > 0]]`, `[[post r: r >= 0]]`, `contract_assert(x > 0)` — replaces assertion macros |
| **Static Reflection** | `<meta>` | `std::meta::members_of(^^T)` — compile-time introspection for serialization, UI binding |
| **`std::execution`** | `<execution>` | Senders/receivers for structured async. `schedule`, `then`, `when_all` |
| **`std::inplace_vector<T, N>`** | `<inplace_vector>` | Fixed-capacity, no-heap vector. Perfect for small GPU staging buffers |
| **`std::hive`** | `<hive>` | Stable-address container with O(1) insert/erase. Object pool pattern built-in |
| **`std::simd`** | `<simd>` | Portable SIMD types. `basic_simd<float>`, masks, reductions |
| **`<linalg>`** | `<linalg>` | BLAS-style linear algebra in the standard library |
| **`<debugging>`** | `<debugging>` | `std::breakpoint()`, `std::is_debugger_present()` |

---

## 8. Error Handling and Safety

### 8.1 Error Handling Strategy

Choose the right mechanism for the context:

| Mechanism | When to Use |
|-----------|-------------|
| `std::expected<T, E>` | **Default choice.** Fallible operations in performance-sensitive or GPU-adjacent code |
| Exceptions | Truly exceptional conditions (out of memory, corrupt state). Never in hot paths or CUDA interop |
| Error codes / `bool` | C API boundaries, CUDA API wrappers, legacy interop |
| `std::optional<T>` | "Value or nothing" without error information (e.g., cache lookup) |
| Assertions / contracts | Programming errors that should never happen in correct code |

```cpp
// GPU/real-time code — use expected
[[nodiscard]] std::expected<CudaBuffer, CudaError> allocateBuffer(size_t size);

// CUDA API wrapper — translate error codes
[[nodiscard]] bool checkCuda(cudaError_t err, std::source_location loc = std::source_location::current());

// Lookup with no error info needed
[[nodiscard]] std::optional<Texture> findTexture(std::string_view name);
```

### 8.2 `noexcept` Specification

Mark the following `noexcept` — containers and algorithms depend on this for optimization:

- **Move constructors and move assignment operators** — always `noexcept`
- **Destructors** — implicitly `noexcept`, never throw from destructors
- **Swap functions** — always `noexcept`
- **Simple getters and observers** — `noexcept` when they cannot fail

```cpp
Buffer(Buffer&& other) noexcept;
Buffer& operator=(Buffer&& other) noexcept;
void swap(Buffer& other) noexcept;
[[nodiscard]] size_t size() const noexcept { return m_size; }
```

If a move constructor is not `noexcept`, `std::vector` will copy instead of move during reallocation — significant performance impact.

### 8.3 RAII (Resource Acquisition Is Initialization)

Every resource (memory, file handle, GPU object, lock, CUDA stream) must be owned by an RAII wrapper. No manual `acquire()`/`release()` pairs in calling code.

```cpp
// Correct — RAII scope guard
class CudaStreamGuard
{
public:
    CudaStreamGuard() { cudaStreamCreate(&m_stream); }
    ~CudaStreamGuard() { if (m_stream) cudaStreamDestroy(m_stream); }

    CudaStreamGuard(const CudaStreamGuard&) = delete;
    CudaStreamGuard& operator=(const CudaStreamGuard&) = delete;
    CudaStreamGuard(CudaStreamGuard&& other) noexcept : m_stream(std::exchange(other.m_stream, nullptr)) {}
    CudaStreamGuard& operator=(CudaStreamGuard&& other) noexcept { std::swap(m_stream, other.m_stream); return *this; }

    [[nodiscard]] cudaStream_t get() const noexcept { return m_stream; }

private:
    cudaStream_t m_stream = nullptr;
};

// Avoid — manual resource management
cudaStream_t stream;
cudaStreamCreate(&stream);
// ... 50 lines of code that might return early or throw ...
cudaStreamDestroy(stream);  // leaked if early return
```

### 8.4 Integer Safety

- **Ban implicit narrowing conversions.** Use `static_cast` explicitly.
- Prefer `std::ssize()` (C++20) for signed container sizes when mixing with signed arithmetic.
- Use `std::cmp_less`, `std::cmp_greater`, etc. (C++20) for safe signed/unsigned comparison.
- Use `std::in_range<T>(value)` (C++20) to check if a value fits in a target type.

```cpp
// Correct — explicit and safe
auto count = static_cast<uint32_t>(m_passes.size());

// Correct — safe signed/unsigned comparison (C++20)
if (std::cmp_less(signedIndex, container.size())) { ... }

// Avoid — implicit narrowing, compiler warning
uint32_t count = m_passes.size();  // narrowing on 64-bit

// Avoid — signed/unsigned comparison bug
if (signedIndex < container.size()) { ... }  // bug if signedIndex is negative
```

### 8.5 Lifetime and `std::string_view` Safety

`std::string_view` and `std::span` are **non-owning**. They must not outlive the data they reference.

```cpp
// DANGER — dangling view (local destroyed at return)
std::string_view getName()
{
    std::string local = computeName();
    return local;  // dangling!
}

// DANGER — storing a view to a temporary
struct BadConfig {
    std::string_view m_name;  // non-owning — will dangle
};
BadConfig c{std::string("hello")};  // m_name dangles immediately

// SAFE — use string_view for parameters, std::string for storage
void setName(std::string_view name);   // caller owns data for call duration
struct GoodConfig {
    std::string m_name;                // owns the data
};
std::string getName() const;           // return owned string for computed values
```

---

## 9. Move Semantics and Value Categories

### 9.1 When to Use `std::move`

- **Use** to transfer ownership of expensive-to-copy resources (containers, unique_ptr, strings).
- **Never** move from `const` objects — it silently copies.
- **Never** move local variables being returned — it defeats Return Value Optimization (RVO/NRVO).
- **Never** use a moved-from object except to destroy or reassign it.

```cpp
// Correct — transferring ownership
m_buffer = std::move(newBuffer);

// WRONG — defeats NRVO, may actually be slower
std::vector<int> buildData()
{
    std::vector<int> result;
    result.push_back(42);
    return std::move(result);  // don't do this — just return result
}

// WRONG — silently copies instead of moving (compiles but wastes perf)
void takeName(const std::string& name)
{
    m_name = std::move(name);  // copies, not moves — name is const&
}
```

### 9.2 Parameter Passing Guidelines

| Type | Cheap to copy? | Pass as |
|------|----------------|---------|
| `int`, `float`, `bool`, `uint32_t`, pointers | Yes | By value |
| `std::string`, `std::vector`, large structs | No | `const&` to observe, value to sink |
| `std::unique_ptr` | N/A | Value (forces `std::move` at call site) |
| `std::string_view`, `std::span` | Yes (they are views) | By value |

```cpp
// Sink parameter — takes ownership
void setName(std::string name) { m_name = std::move(name); }

// Observer — just reads
void processBuffer(const Buffer& buf);

// Transfer — unique ownership
void setDevice(std::unique_ptr<Device> device) { m_device = std::move(device); }
```

### 9.3 Return Value Guidelines

- Return by value and rely on RVO/NRVO (guaranteed in C++17 for prvalues).
- Never return `const` values — it prevents move semantics.
- Never `std::move` the return value of a local variable.

```cpp
// Correct — RVO applies
std::vector<Texture> loadTextures() { ... }
std::unique_ptr<Device> createDevice() { ... }
```

---

## 10. Concurrency and Thread Safety

### 10.1 Thread Safety Documentation

Every class must document its thread safety contract in its class documentation:

```cpp
/**
 * @brief Manages the render pipeline.
 *
 * @threadsafety Not thread-safe. Must be used from the render thread only.
 */
class RenderPipeline { ... };

/**
 * @brief Thread-safe logging system.
 *
 * @threadsafety All public methods are thread-safe (internally synchronized).
 */
namespace Log { ... }
```

### 10.2 Preferred Primitives

| Primitive | Use Case |
|-----------|----------|
| `std::jthread` (C++20) | Preferred over `std::thread` — RAII with cooperative cancellation |
| `std::scoped_lock` | Lock multiple mutexes without deadlock risk |
| `std::lock_guard` | Lock a single mutex for a scope |
| `std::atomic<T>` | Lock-free shared state for simple types |
| `std::shared_mutex` | Reader-writer lock (many readers, one writer) |
| `std::latch` / `std::barrier` (C++20) | One-shot / reusable synchronization points |

```cpp
// Correct — RAII thread with stop token
std::jthread worker([](std::stop_token token) {
    while (!token.stop_requested())
    {
        processNextItem();
    }
});
// worker automatically joined on destruction

// Correct — scoped lock
std::scoped_lock lock(m_mutex);
m_data.push_back(item);

// Avoid
std::thread t(func);
// ... 50 lines ...
t.join();  // leaked if exception before join
```

### 10.3 Rules

- **Never use `volatile` for synchronization.** `volatile` is for memory-mapped I/O, not threading. Use `std::atomic`.
- **Never lock a mutex manually** without a lock guard (`lock()`/`unlock()` pairs will leak on exceptions or early returns).
- **Prefer `std::atomic`** for simple shared counters/flags over mutex-guarded primitives.

---

## 11. Modern CMake Practices

### 11.1 Target-Based CMake

Always use target-scoped commands. Never use directory-scoped commands.

```cmake
# Correct — target-scoped
target_include_directories(MyLib PUBLIC ${CMAKE_SOURCE_DIR}/src/core)
target_compile_definitions(MyLib PRIVATE NOMINMAX)
target_link_libraries(MyApp PRIVATE MyLib)

# Incorrect — directory-scoped (pollutes all targets)
include_directories(${CMAKE_SOURCE_DIR}/src/core)
add_definitions(-DNOMINMAX)
link_libraries(MyLib)
```

### 11.2 Visibility Keywords

| Keyword | Meaning |
|---------|---------|
| `PRIVATE` | Used only by this target |
| `PUBLIC` | Used by this target AND propagated to consumers |
| `INTERFACE` | Not used by this target, only propagated to consumers |

```cmake
# RadianceCore's include dir is PUBLIC because consumers need its headers
target_include_directories(RadianceCore PUBLIC ${CMAKE_SOURCE_DIR}/src/core)

# NOMINMAX is PRIVATE — only needed internally
target_compile_definitions(RadianceCore PRIVATE NOMINMAX)
```

### 11.3 Key Practices

- Set `CMAKE_CXX_STANDARD` at the project level. Prefer `target_compile_features(MyLib PUBLIC cxx_std_20)` for per-target control.
- Use generator expressions for config-dependent settings: `$<$<CONFIG:Debug>:DEBUG_MODE>`.
- Never hardcode compiler paths or platform-specific flags without conditionals.
- Use `FetchContent` or vendored `third-party/` for dependencies. Avoid system-installed libraries that vary across machines.

---

## 12. Linting and Tooling Standards

### 12.1 Required Tooling

| Tool | Purpose |
|------|---------|
| `clang-format` | Automated code formatting |
| `clang-tidy` | Static analysis and lint |
| `cppcheck` | Additional static analysis |
| `cmake --build` + warnings | Compiler-level warnings |

### 12.2 Compiler Warning Flags

All code must compile clean with these flags — no suppressed warnings without documented justification.

```cmake
# MSVC
/W4 /WX /permissive- /Zc:__cplusplus

# GCC / Clang
-Wall -Wextra -Wpedantic -Werror -Wshadow -Wnon-virtual-dtor -Wconversion
```

### 12.3 `.clang-format` Reference Config

```yaml
BasedOnStyle: LLVM
IndentWidth: 4
ColumnLimit: 120
PointerAlignment: Left
BreakBeforeBraces: Allman
SortIncludes: true
IncludeBlocks: Regroup
SpaceBeforeParens: ControlStatements
AllowShortFunctionsOnASingleLine: Inline
AllowShortIfStatementsOnASingleLine: Never
```

### 12.4 `.clang-tidy` Recommended Checks

```yaml
Checks: >
  clang-analyzer-*,
  cppcoreguidelines-*,
  modernize-*,
  readability-*,
  performance-*,
  bugprone-*,
  -modernize-use-trailing-return-type,
  -readability-magic-numbers
```

---

## 13. Header File Standards

### 13.1 Include Guards

Prefer `#pragma once` over traditional include guards for all new code.

```cpp
#pragma once
```

### 13.2 Forward Declarations

Use forward declarations in headers to minimize compile-time dependencies. Only include what is strictly necessary.

```cpp
// Header — forward declare instead of including
class Device;
class CommandList;

class RenderGraph
{
    void execute(CommandList* cmd);  // pointer/ref — no full definition needed
};
```

### 13.3 No Implementation in Headers

- Do not define non-trivial function bodies in headers (except templates and `inline`/`constexpr` functions).
- Trivial accessors/one-liners are acceptable inline.

---

## 14. Audit Checklist for Agents

When auditing and refactoring a codebase, apply the following checks comprehensively:

### Naming
- [ ] All classes/structs/enums renamed to `PascalCase`
- [ ] All base classes with virtual methods have `virtual` destructor
- [ ] All functions/methods renamed to `camelCase`
- [ ] All local variables renamed to `camelCase`
- [ ] All member variables prefixed with `m_` and `camelCase`
- [ ] All static members prefixed with `s_`
- [ ] All global variables prefixed with `g_`
- [ ] All constants renamed to `kPascalCase`
- [ ] All enum values renamed to `PascalCase`
- [ ] All namespaces renamed to `lowercase`
- [ ] All macros renamed to `SCREAMING_SNAKE` with project prefix
- [ ] All template parameters renamed to `PascalCase`

### Files and Directories
- [ ] All `.h` / `.cpp` source files renamed to `PascalCase`
- [ ] All folders renamed to `lowercase` or `kebab-case`
- [ ] `source/` renamed to `src/`; `Build/` to `build/`; `Plugins/` to `plugins/`
- [ ] `External/` renamed to `third-party/`
- [ ] Public headers moved to `include/<projectname>/`
- [ ] Private headers co-located with their `.cpp` in `src/`

### Code Modernization
- [ ] All `NULL` replaced with `nullptr`
- [ ] All `typedef` replaced with `using`
- [ ] All C-style casts replaced with `static_cast` / `reinterpret_cast`
- [ ] Raw owning pointers replaced with `std::unique_ptr` / `std::shared_ptr`
- [ ] `[[nodiscard]]` added to functions whose return value must not be ignored
- [ ] `explicit` added to single-argument constructors
- [ ] `#pragma once` replaces old-style include guards
- [ ] SFINAE replaced with concepts where applicable (C++20)
- [ ] `sprintf`/`snprintf` replaced with `std::format` where applicable (C++20)
- [ ] `std::enable_if` replaced with `requires` clauses (C++20)

### Error Handling and Safety
- [ ] Move constructors, move assignment, swap, destructors are `noexcept`
- [ ] No raw `new`/`delete` — all resources managed by RAII wrappers
- [ ] No implicit narrowing conversions — all narrowing uses `static_cast`
- [ ] No `std::string_view` or `std::span` stored as class members (dangling risk)
- [ ] Error-prone operations return `std::expected` or `std::optional`
- [ ] Thread safety documented on all classes

### Comments and Documentation
- [ ] File header block present on all files
- [ ] All public API functions have Doxygen `@brief` / `@param` / `@return`
- [ ] Inline comments explain *why*, not *what*
- [ ] TODO/FIXME/HACK tags follow standardized format
- [ ] No commented-out dead code

### Formatting
- [ ] Consistent 4-space indentation (no tabs)
- [ ] Lines under 120 characters
- [ ] Allman brace style on functions and classes
- [ ] Include order follows standard grouping (corresponding header -> project -> third-party -> stdlib)
- [ ] `const` correctness applied to member functions and parameters
- [ ] `clang-format` applied to all files
- [ ] `clang-tidy` passes with zero warnings

### CMake
- [ ] All commands target-scoped (no `include_directories`, `add_definitions`, `link_libraries`)
- [ ] `PRIVATE` / `PUBLIC` / `INTERFACE` used correctly on all target commands
- [ ] No hardcoded platform paths without conditionals

---

*Reference: C++ Core Guidelines (Stroustrup/Sutter), ISO C++20/23/26 Standards, Google C++ Style Guide, LLVM Coding Standards, cppreference.com.*
