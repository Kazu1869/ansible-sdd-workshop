# SPEC-NNN — Feature name

Status: draft | Version: 0.1 | Owner: assign | Acceptance evidence: pending

## Intent and authorized scope

Describe desired outcome, target inventory/environment, files, privilege, blast radius and the user's existing authorization. Record material open decisions without assuming approval.

## Public interface

| Input | Type | Required | Runtime default | Validation |
| --- | --- | --- | --- | --- |

Keep role argument documentation and runtime defaults consistent. Never default a required input.

## Behavioral requirements

- REQ-001: When ..., the automation shall ... .
- REQ-002: If validation fails, ... before any mutation.
- REQ-003: When an identical request repeats, ... .

Include enabled/disabled behavior, permissions, failure side effects, check mode and rollback where applicable. Define the expected error category for negative cases.

## Traceability and acceptance

| REQ | Positive / negative / idempotency / check-mode test | Expected result | Command |
| --- | --- | --- | --- |

## Policy mapping and dependencies

Applicable control IDs, approved exceptions with evidence, dependency versions and supported test environment. Do not claim compliance with a standard that was not provided.

## Rollback, exclusions and open questions

Specify recovery behavior, what is not covered, and unanswered questions that block implementation. Readiness review and human scope acceptance are separate records.
