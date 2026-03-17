from __future__ import annotations

from textwrap import dedent


def role_meta_template() -> str:
    return dedent("""\
    role_id: {role_id}
    role_name: {role_name}

    role_group: {role_group}
    role_family: {role_family}
    role_type: {role_type}
    role_level: {role_level}
    status: active

    reports_to: {reports_to}
    managed_role: {managed_role}
    manages: {manages}

    is_ic_anchor: {is_ic_anchor}
    ic_anchor_role_id: {ic_anchor_role_id}

    company_role_path: {company_role_path}

    required_files:
      - ROLE_META.yaml
      - CONTEXT.txt
      - DIRECTIVES.txt
      - ROLE_SPEC.txt

    version: 1
    """)


def context_template() -> str:
    return dedent("""\
    ROLE ID
    {role_id}

    ROLE NAME
    {role_name}

    MISSION
    {mission}

    POSITION IN HIERARCHY
    Reports to {reports_to}. Managed role {managed_role}. IC anchor {ic_anchor_role_id}.

    CORE CONTEXT
    {core_context}

    PRIMARY RESPONSIBILITIES
    {primary_responsibilities}

    SCOPE OF PRACTICE
    This role may ONLY operate within its defined responsibilities.
    Any task outside scope must be escalated.

    BOUNDARIES
    {boundaries}

    COLLABORATION RULES
    {collaboration_rules}

    OUTPUT EXPECTATIONS
    {output_expectations}

    QUALITY STANDARD
    {quality_standard}

    CONTEXT UPDATE RULES
    {context_update_rules}
    """)


def directives_template() -> str:
    return dedent("""\
    You are the {role_name}.

    You must:

    - operate only within scope
    - follow hierarchy
    - not exceed authority
    - escalate when needed
    - produce structured outputs
    - align with company mission

    You must NOT:

    - act outside role responsibilities
    - override other roles
    - fabricate authority
    """)


def role_spec_template() -> str:
    return dedent("""\
    ROLE NAME
    {role_name}

    ROLE ID
    {role_id}

    MISSION
    {mission}

    WHY THIS ROLE EXISTS
    {why_exists}

    ROLE GROUP
    {role_group}

    ROLE FAMILY
    {role_family}

    ROLE TYPE
    {role_type}

    ROLE LEVEL
    {role_level}

    REPORTS TO
    {reports_to}

    MANAGED ROLE
    {managed_role}

    IS IC ANCHOR
    {is_ic_anchor}

    IC ANCHOR ROLE ID
    {ic_anchor_role_id}

    CORE RESPONSIBILITIES
    {core_responsibilities}

    CAPABILITIES

    - skills
      {skills}
    - tools
      {tools}
    - systems
      {systems}

    DECISION RIGHTS
    {decision_rights}

    INPUTS
    {inputs}

    OUTPUTS
    {outputs}

    KEY COLLABORATORS
    {key_collaborators}

    SUCCESS METRICS
    {success_metrics}

    FAILURE MODES
    {failure_modes}

    SCOPE OF PRACTICE
    This role must only operate within its defined responsibilities.

    ESCALATION PATH
    {escalation_path}
    """)


def role_creation_template() -> str:
    return dedent("""\
    ROLE CREATION REQUEST

    role_name:
    role_id:
    role_group:
    role_family:
    role_type:
    role_level:

    business_reason:

    reports_to:
    managed_role:

    is_ic_anchor:

    if new family:
    generate full chain to IC

    expected_outputs:

    decision_scope:

    constraints:
    """)


def founder_init_prompt_template() -> str:
    return dedent("""\
    FOUNDER INITIALIZATION PROMPT

    You are initializing a new virtual company from the deterministic company template.

    Your job is to collect founder-approved input before any new project is generated.

    Ask the founder for these items.

    1. company name
    2. company mission
    3. company strategy
    4. desired company structure
    5. whether only c_suite should be created initially
    6. which business functions are required now
    7. which roles the founder already knows are required
    8. which roles can wait until later
    9. constraints on scope, budget, or headcount
    10. output expectations for each early role

    After the founder responds, suggest an initial role set and explain why each role is needed.

    Do not write any role files yet.

    Wait for founder confirmation.

    Once confirmed, produce a founder-approved expansion confirmation file at inputs/FOUNDER_EXPANSION_CONFIRMATION.yaml.

    The confirmation file must contain only approved roles.

    Any role outside the confirmed set must not be created.
    """)


def founder_expansion_confirmation_template() -> str:
    return dedent("""\
    company_name: my_company
    company_mission: Replace this with the confirmed mission.
    company_strategy: Replace this with the confirmed strategy.
    confirmed_by_founder: false

    approved_roles:
      - role_id: chief_executive_officer
        role_name: Chief Executive Officer
        role_group: c_suite
        role_family: executive
        role_type: executive
        role_level: c_suite
        reports_to: founder
        managed_role: null
        manages: []
        is_ic_anchor: true
        ic_anchor_role_id: chief_executive_officer
        mission: Own company execution and enterprise-level coordination.
        why_exists: Ensures the company has one executive operator responsible for aligned execution.
        core_responsibilities: Translate founder intent into operating priorities, coordinate the executive team, and drive company execution.

    notes: Add or remove approved roles, then set confirmed_by_founder to true.
    """)


def init_config_template() -> str:
    return dedent("""\
    company_name: my_company

    include_c_suite: true

    initial_role_families: []

    generate_default_chains: false
    """)
