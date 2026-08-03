# Project Principles

> "Technology can preserve knowledge, but only people can preserve culture."

Aksara Nusantara is an open ecosystem dedicated to preserving Indonesian traditional scripts through technology, education, and community.

These principles guide every decision we make.

---

# 1. Culture Comes First

Technology is only a tool.

Our primary mission is preserving the cultural heritage of Indonesian traditional scripts.

---

# 2. Open Knowledge

Knowledge grows when shared.

Whenever possible, we build using open standards, open-source software, and open documentation.

---

# 3. Respect Every Creator

We respect copyrights, licenses, trademarks, and the work of other creators.

Every third-party resource used in this project must be properly attributed.

---

# 4. Community Before Popularity

We do not measure success only by stars, downloads, or followers.

A healthy community is more valuable than rapid growth.

---

# 5. Documentation Is Part of the Product

Good software deserves good documentation.

Documentation is not an afterthought.

It is part of the product.

---

# 6. Beginners Are Welcome

Everyone starts somewhere.

Questions are welcome.

Learning is encouraged.

Teaching is appreciated.

---

# 7. Long-Term Thinking

We build for years, not weeks.

Every decision should make the project easier to maintain in the future.

---

# 8. Ethical Sustainability

Open source and sustainability can coexist.

We believe projects can remain open while generating income through education, services, documentation, and support—not by restricting freedom.

---

# 9. Output Responsibility

Every layer is responsible only for its own output.

### Principles

- The Application layer is responsible for application startup,
  logging configuration, diagnostics, and user-visible output.

- The GUI layer is responsible only for visual presentation and
  user interaction. It must not write directly to the console.

- The Core Engine may expose diagnostic information through the
  project's logging infrastructure, but must never write directly
  to standard output during normal operation.

- ScriptPacks are pure providers of data and assets. They must not
  produce console output, logging messages, or user-visible
  notifications during normal operation.

### Rationale

A component should never assume how it will be used.

The same ScriptPack may be loaded by:

- Desktop applications
- Command-line tools
- Automated tests
- Future web applications
- Third-party software

Because of this, ScriptPacks should communicate only through:

- return values,
- exceptions,
- or well-defined public interfaces.

The responsibility for presenting or recording information belongs
to the application layer.

### Layer Responsibilities

| Layer | Console Output | Logging | User Interface |
|-------|:--------------:|:-------:|:--------------:|
| Application | Yes | Yes | Yes |
| GUI | No | Optional | Yes |
| Core Engine | No | Yes | No |
| ScriptPack | No | No | No |