# SYSTEM DESIGN

## Purpose

This repository is not a collection of scripts.

It is a deterministic, LLM-safe system for generating, validating, and evolving structured organizational state.

The goal is to create a system that is:

- reproducible
- enforceable
- testable
- scalable
- safe for AI-assisted interaction

All design decisions must reinforce these properties.

---

## Core Principles

### Single Operational Truth

The system must have exactly one valid way to perform any operation.

Dead paths are not allowed.

Removing dead paths:
- reduces confusion
- reduces maintenance burden
- enforces clarity
- ensures teachability for humans and models

If a path is not used, it must be removed.

---

### Deterministic Behavior

The system must behave in a constrained and predictable way.

- same inputs produce same class of outputs
- no hidden side effects
- no ambiguous execution paths

The system is not allowed to rely on model creativity for correctness.

---

### CLI as Execution Boundary

The CLI defines the only valid entry point into system behavior.

All operations must go through the CLI.

This ensures:
- consistent invocation
- controlled inputs
- standardized outputs
- enforceable error handling

No direct internal function calls from external workflows.

---

### Templates as Generation Boundary

All generation must flow through templates.

The system does not allow freeform file creation.

Templates ensure:
- structural consistency
- predictable formats
- safe model interaction
- easier validation and parsing

The model fills structure. It does not invent structure.

---

### Validation as Enforcement Boundary

Validation is mandatory.

The system must reject invalid state.

Validation must enforce:
- required fields
- valid values
- structural integrity
- relationship correctness
- absence of drift

No write is accepted unless it passes validation.

---

### LLM-Safe Writes

LLMs do not write directly to the system.

LLMs:
- propose structured inputs
- fill templates
- generate candidate values

The system:
- validates
- accepts or rejects
- writes only valid state

The model is not trusted. The system is.

---

### Local Execution Truth

Local success is required.

When local tests pass, it confirms:
- install path is real
- CLI commands are real
- system is executable
- repo is minimally self-consistent

A system that does not run locally is not valid.

---

### CI Mirrors Real Usage

CI must run the same commands as real users.

No shadow scripts.
No alternate execution paths.

CI verifies:
- actual CLI behavior
- actual install path
- actual system usage

If CI passes but real usage fails, CI is incorrect.

---

### Branch-Based State Integrity

All changes must go through branches.

This ensures:
- consistent shared state
- reproducible history
- reliable CI evaluation
- clean review process

Local state and remote state must match.

---

## System Boundaries

Execution boundary
CLI

Generation boundary
Templates

Enforcement boundary
Validation

These boundaries must never be bypassed.

---

## System Shape

The system evolves through controlled transformations.

Spec to Template to Validation to State

- Spec defines intent
- Template defines structure
- Validation enforces correctness
- State becomes accepted reality

This is a compiler-like model.

---

## Role Compiler

Roles are structured artifacts, not text blobs.

A role includes:
- identity
- responsibilities
- relationships
- constraints
- context

The system must be able to transform role definitions into consistent downstream artifacts.

---

## Organization Expansion Engine

The system must support structured expansion.

High-level intent must be transformable into:
- roles
- hierarchy
- files
- context
- dependencies

Expansion must:
- follow rules
- use templates
- pass validation

---

## Founder Workflow

The founder operates at the level of intent.

Flow:

- Founder provides structured direction
- Direction becomes machine-readable contract
- Contract is validated
- System expands organization deterministically

Manual file manipulation is not the goal.

---

## Anti-Patterns

The following are not allowed:

- freeform file generation
- bypassing CLI
- bypassing validation
- duplicate command paths
- legacy compatibility layers
- hidden execution logic
- CI that does not reflect real usage
- accepting invalid state
- relying on model correctness instead of system enforcement

---

## Definition of Done

A feature is complete only if:

- it is exposed via CLI
- it uses templates for generation
- it passes validation
- it is covered by tests
- it works locally
- it works in CI
- it introduces no dead paths

---

## Philosophy

This system treats AI as an input mechanism, not an authority.

The goal is not to generate text.

The goal is to generate valid, enforceable system state.

Structure is more important than flexibility.

Constraints are what enable scale.

---

## Summary

This repository is a controlled system, not a flexible playground.

Every contribution must:

- reduce ambiguity
- reinforce boundaries
- increase determinism
- preserve validation integrity

If a change weakens the system, it is not accepted.

If a change strengthens the system, it compounds.

This is how the system scales.
