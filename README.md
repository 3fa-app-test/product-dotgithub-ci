# 3FA-app organization defaults

This public `.github` repository contains organization-wide community health files, contributor guidance, shared agent policy, and explicit repository, planning, and delivery contracts.

Repository-local policy wins when it is stricter or more specific. Existing project history must be preserved during consolidation and conflict resolution.

## Routing and operations

- [Canonical organization routing](ORGANIZATION_ROUTING.md)
- [Machine-readable routing projection](organization-routing.json)
- [Routing schema](schema/organization-routing.schema.json)
- [GitHub Projects and Linear operating contract](docs/PROJECTS.md)
- [Deterministic project registry generator](scripts/build-project-registry.py)
- [Project registry artifact schema](schema/project-registry-artifact.schema.json)
- [Project registry artifact workflow](.github/workflows/project-registry-artifact.yml)
- Canonical CLI and project-registry consumer: [`3FA-app/3FA-app-cli`](https://github.com/3FA-app/3FA-app-cli)
- [Repository boundaries](REPOSITORY_BOUNDARIES.md)
- [Branching and GitOps policy](BRANCHING_AND_DEPLOYMENT.md)

The canonical execution board is [GitHub Project `3FA-app-project` #1](https://github.com/orgs/3FA-app/projects/1). The planning system of record is the [Linear project `github.com/3FA-app`](https://linear.app/denman/project/githubcom3fa-app-c3db52220894). Projects access reconciliation is tracked in [DEN-2439](https://linear.app/denman/issue/DEN-2439/3fa-app-grant-projects-v2-access-and-reconcile-canonical-project-1) and [GitHub issue #9](https://github.com/3FA-app/.github/issues/9); restricted automation must not create a duplicate board.

Private repository details are intentionally withheld from this public document.

The canonical execution board currently projects 14 repositories, including
[`3FA-app/3FA-app-cli`](https://github.com/3FA-app/3FA-app-cli) with role `cli`.
Pull-request and `main` workflows publish a deterministic Markdown/JSON project
registry plus SHA-256 checksums as a GitHub Actions artifact.

<!-- ore-org-baseline:begin -->
## Organization-wide defaults

This public repository is the canonical source for GitHub-supported community-health fallbacks, organization profile content, contribution guidance, public security/support policy, issue and pull-request templates, and agent-governance declarations for [`3FA-app`](https://github.com/3FA-app).

## Canonical organization links

- GitHub organization: https://github.com/3FA-app
- Public organization defaults: https://github.com/3FA-app/.github
- Canonical Linear project: https://linear.app/denman/project/githubcom3fa-app-c3db52220894
- Fleet tracking issue: https://github.com/ORESoftware/k8s-cluster/issues/1222

## Safety baseline

All Git conflicts must be resolved semantically with full historical, repository-wide, organization-wide, and relevant external-organization context. Automated agents are hard-denied from destructive or history-rewriting operations, including all forms of `git stash`, `git reset`, `git clean`, `git filter-repo`, force pushing, destructive deletion, data or infrastructure teardown, credential revocation, and policy bypass.

## GitHub inheritance boundary

GitHub can use supported community-health files from a public organization `.github` repository as fallbacks and can render `profile/README.md` on the organization page. `agents.md`, `AGENTS.md`, Copilot instructions, workflows, settings, rulesets, branch protections, permissions, and secrets are not automatically inherited merely because they exist here. Each repository must carry or synchronize compatible local policy and explicitly call reusable workflows where enforcement is required.

Generated managed-policy version: `2026-08-08`.
<!-- ore-org-baseline:end -->

<!-- BEGIN MANAGED REPOSITORY RELATIONSHIPS v1 -->
## Repository relationship registry

`3FA-app` declares repository roles, dependency edges, cross-organization capabilities, deployment ownership, and the git-submodule/Zed-package contract:

- [Human-readable map](architecture/REPOSITORY_RELATIONSHIPS.md)
- [Machine-readable manifest](architecture/repository-relationships.json)
- [JSON Schema](architecture/repository-relationships.schema.json)

The public registry withholds private repository names and edges.
<!-- END MANAGED REPOSITORY RELATIONSHIPS v1 -->
