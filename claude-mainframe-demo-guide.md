# Claude for IBM z/TPF Developers: Demo Guide
## Effective Use with z/TPF C++ Codebases

---

## Demo Overview
This guide demonstrates how IBM z/TPF (Transaction Processing Facility) developers can leverage Claude to enhance productivity when working with z/TPF C++ codebases, including real-time transaction processing, debugging, and optimization for high-volume airline and credit card systems.

---

## 1. Code Understanding & Documentation

### Demo Scenario: Understanding Legacy COBOL-to-C++ Migration Code

**What to show:**
```
"I have this C++ code that was migrated from COBOL on our z/Linux mainframe. 
Can you explain what it does and identify any potential issues?"

[Paste a sample of their C++ code]
```

**Claude's capabilities:**
- Explains complex pointer arithmetic and memory management
- Identifies COBOL-style patterns in C++ code
- Documents the code flow with clear explanations
- Highlights potential modernization opportunities

---

## 2. Code Review & Best Practices

### Demo Scenario: Reviewing Mainframe-Specific C++ Code

**Example prompt:**
```
"Review this z/Linux C++ code for:
1. Memory leaks or buffer overflows
2. Thread safety issues in our multi-threaded mainframe environment
3. Performance optimizations for z/Architecture
4. Compliance with our coding standards"

[Paste code snippet]
```

**What Claude can identify:**
- EBCDIC/ASCII conversion issues
- Improper use of z/Linux system calls
- Resource cleanup in high-availability systems
- Big-endian considerations
- Cross-platform compatibility issues

---

## 3. Debugging Assistance

### Demo Scenario: Analyzing Core Dumps and Error Messages

**Example prompt:**
```
"We're getting a segmentation fault in our batch processing system. 
Here's the stack trace and relevant code:

Stack trace:
[Paste stack trace]

Code section:
[Paste code]

What could be causing this?"
```

**Claude helps with:**
- Analyzing stack traces specific to z/Linux environment
- Identifying null pointer dereferences
- Memory corruption patterns
- Race conditions in multi-threaded code
- Suggesting debugging strategies using gdb on z/Linux

---

## 4. Code Modernization

### Demo Scenario: Modernizing Legacy C++ Code

**Example prompt:**
```
"This C++ code was written in the 1990s for our mainframe. 
How can I modernize it to use C++17/20 features while maintaining 
compatibility with z/Linux and our existing systems?"

[Paste legacy code]
```

**Modernization examples:**
- Raw pointers → Smart pointers (unique_ptr, shared_ptr)
- Manual memory management → RAII patterns
- C-style arrays → std::vector, std::array
- Manual threading → std::thread, std::async
- errno checking → Exception handling

---

## 5. Performance Optimization

### Demo Scenario: Optimizing for z/Architecture

**Example prompt:**
```
"This transaction processing code runs on z15 mainframe. 
How can I optimize it for better performance? Consider:
- z/Architecture SIMD instructions
- Cache optimization
- Memory alignment for mainframe architecture"

[Paste performance-critical code]
```

**Claude can suggest:**
- Algorithm improvements
- Data structure optimizations
- Compiler optimization flags for z/Linux GCC
- Memory layout improvements
- Batch processing optimizations

---

## 6. Working with Mainframe-Specific APIs

### Demo Scenario: System Integration

**Example prompt:**
```
"Show me how to properly interface with z/OS subsystems from C++ on z/Linux:
1. Accessing DB2 on z/OS
2. Reading from VSAM datasets
3. Calling CICS transactions
4. Using MQ messaging"
```

**Claude provides:**
- Code examples with proper error handling
- Best practices for resource management
- Connection pooling strategies
- Transaction management patterns

---

## 7. Test Case Generation

### Demo Scenario: Creating Unit Tests

**Example prompt:**
```
"Generate comprehensive unit tests for this C++ function that processes 
mainframe transaction records. Include edge cases for:
- Invalid record formats
- EBCDIC encoding issues
- Large dataset handling
- Concurrent access scenarios"

[Paste function]
```

**Claude generates:**
- Complete test suite using Google Test or Catch2
- Mock objects for mainframe dependencies
- Test data generators
- Coverage scenarios

---

## 8. Migration Planning

### Demo Scenario: COBOL to C++ Migration Strategy

**Example prompt:**
```
"We need to migrate this COBOL batch program to C++ on z/Linux. 
Provide a migration strategy including:
1. Architecture recommendations
2. Data structure mappings
3. File handling conversion
4. Performance considerations"

[Paste COBOL code]
```

**Claude provides:**
- Step-by-step migration plan
- Side-by-side COBOL vs C++ comparisons
- Risk assessment
- Testing strategy

---

## 9. Documentation Generation

### Demo Scenario: Creating Technical Documentation

**Example prompt:**
```
"Generate technical documentation for this C++ module including:
- API reference
- Usage examples
- Integration guide for mainframe environment
- Troubleshooting section"

[Paste code]
```

**Claude creates:**
- Markdown or HTML documentation
- UML diagrams (in text or Mermaid format)
- Code examples
- Configuration guides

---

## 10. Build System & DevOps

### Demo Scenario: CMake and Build Optimization

**Example prompt:**
```
"Help me create a CMakeLists.txt for our z/Linux C++ project that:
1. Supports cross-compilation for s390x architecture
2. Links against mainframe-specific libraries
3. Includes proper compiler flags for z/Architecture optimization
4. Integrates with our Jenkins CI/CD pipeline"
```

**Claude generates:**
- Complete CMake configuration
- Compiler flags for z/Linux GCC
- Dependency management
- Build scripts

---

## Best Practices for Using Claude with Mainframe Code

### 1. **Provide Context**
Always mention:
- z/Linux or z/OS environment
- Compiler version (GCC, XL C++)
- Mainframe architecture (z13, z14, z15, z16)
- Any specific constraints (EBCDIC, big-endian, etc.)

### 2. **Upload Files**
You can upload:
- Source code files (.cpp, .h)
- Build logs
- Core dump analysis
- Configuration files

### 3. **Iterative Refinement**
- Start with general questions
- Drill down into specific issues
- Ask for alternative approaches
- Request explanations of suggestions

### 4. **Use Computer Use Feature**
Claude can:
- Create complete file structures
- Generate build scripts
- Create documentation files
- Produce presentation materials

---

## Sample Demo Flow (30-minute presentation)

### **Phase 1: Introduction (5 min)**
- Brief overview of Claude's capabilities
- Show the interface

### **Phase 2: Live Coding Demo (15 min)**
1. **Code Review** (5 min)
   - Paste a problematic code snippet
   - Get instant feedback
   
2. **Debugging** (5 min)
   - Share a bug scenario
   - Walk through Claude's analysis
   
3. **Modernization** (5 min)
   - Show legacy code transformation
   - Explain the improvements

### **Phase 3: Advanced Features (7 min)**
- File upload and analysis
- Documentation generation
- Test case creation

### **Phase 4: Q&A and Next Steps (3 min)**

---

## Example Code Snippets for Demo

### Legacy Code Example (Before):
```cpp
// Legacy mainframe C++ code
void processTransaction(char* record, int len) {
    char* buffer = (char*)malloc(len + 1);
    memcpy(buffer, record, len);
    buffer[len] = '\0';
    
    // EBCDIC to ASCII conversion
    for(int i = 0; i < len; i++) {
        buffer[i] = ebcdic_to_ascii[buffer[i]];
    }
    
    // Process the record
    updateDatabase(buffer);
    
    // Potential memory leak - no free()!
}
```

### After Claude's Suggestions:
```cpp
// Modernized version
void processTransaction(std::string_view record) {
    // Use RAII and standard library
    std::string buffer = ebcdic_to_utf8(record);
    
    try {
        updateDatabase(buffer);
    } catch (const DatabaseException& e) {
        logError("Transaction failed", e);
        throw;
    }
    // Automatic cleanup, exception-safe
}
```

---

## Key Messages for Your Demo

1. **Claude understands mainframe context** - It knows z/Linux, z/OS, EBCDIC, and mainframe-specific challenges

2. **Saves time** - Code review, documentation, and test generation in seconds

3. **Knowledge transfer** - Helps newer developers understand legacy code

4. **Modernization partner** - Assists in migrating legacy code to modern C++ standards

5. **Available 24/7** - No waiting for code reviews or mentor availability

6. **Keeps code secure** - Works with your code privately, no training on your data

---

## Technical Requirements

- Web browser (Chrome, Firefox, Edge, Safari)
- No installation required
- Can work with uploaded files
- Supports syntax highlighting for C++

---

## Getting Started Checklist

- [ ] Create Claude account at claude.ai
- [ ] Prepare 2-3 code samples from your codebase
- [ ] Identify a recent bug or challenge to demonstrate
- [ ] Have a legacy code snippet ready for modernization demo
- [ ] Prepare questions about mainframe-specific scenarios

---

## Additional Resources

- Claude documentation: docs.claude.com
- Best practices for prompting
- Integration with existing workflows
- API access for automation

---

## Demo Tips

1. **Start simple** - Begin with a straightforward code review
2. **Show real problems** - Use actual issues your team has faced
3. **Be interactive** - Encourage attendees to suggest prompts
4. **Highlight specifics** - Emphasize mainframe-aware responses
5. **Show iteration** - Demonstrate how to refine Claude's responses

---

## Follow-up Ideas

After the demo, developers can:
- Use Claude for daily code reviews
- Generate documentation for undocumented modules
- Plan modernization strategies
- Create test suites for legacy code
- Get help with debugging complex issues

---

*This demo guide is designed to showcase Claude's capabilities specifically for IBM mainframe developers working with z/Linux C++ codebases. Adapt the examples to match your team's specific codebase and challenges.*
