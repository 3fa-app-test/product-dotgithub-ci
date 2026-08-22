from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "build-project-registry.py"
SPEC = importlib.util.spec_from_file_location("build_project_registry", SCRIPT)
if SPEC is None or SPEC.loader is None:  # pragma: no cover - import bootstrap guard
    raise RuntimeError(f"unable to load {SCRIPT}")
REGISTRY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(REGISTRY)


class ProjectRegistryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.routing = REGISTRY.read_json(ROOT / "organization-routing.json")

    def test_current_routing_projection_is_canonical(self) -> None:
        REGISTRY.validate_routing(self.routing)
        self.assertEqual(self.routing["verifiedAt"], "2026-08-08")
        self.assertEqual(len(self.routing["repositories"]), 14)
        self.assertEqual(
            tuple((entry["name"], entry["role"]) for entry in self.routing["repositories"]),
            REGISTRY.EXPECTED_REPOSITORIES,
        )

    def test_cli_repository_is_present_once_with_exact_identity(self) -> None:
        matches = [
            entry
            for entry in self.routing["repositories"]
            if entry["name"] == "3FA-app-cli" or entry["role"] == "cli"
        ]
        self.assertEqual(
            matches,
            [
                {
                    "name": "3FA-app-cli",
                    "fullName": "3FA-app/3FA-app-cli",
                    "role": "cli",
                }
            ],
        )

    def test_artifact_reciprocally_links_github_linear_slack_and_project_fields(self) -> None:
        artifact = REGISTRY.build_artifact(self.routing)
        self.assertEqual(artifact["github"]["project"]["number"], 1)
        self.assertEqual(artifact["github"]["project"]["linearIssue"], "DEN-2439")
        self.assertEqual(artifact["linear"]["projectName"], "github.com/3FA-app")
        self.assertEqual(artifact["slack"]["channelId"], "C0BL6BEDYFK")

        fields = {field["name"]: field for field in artifact["projectFields"]}
        self.assertEqual(set(fields), {"Linear issue", "Linear project", "Repository role"})
        self.assertEqual(fields["Linear issue"]["type"], "text")
        self.assertEqual(fields["Linear project"]["type"], "text")
        self.assertEqual(fields["Repository role"]["type"], "singleSelect")
        self.assertEqual(
            fields["Repository role"]["options"],
            [role for _, role in REGISTRY.EXPECTED_REPOSITORIES],
        )

    def test_bundle_is_deterministic_and_checksums_verify(self) -> None:
        with tempfile.TemporaryDirectory() as first_dir, tempfile.TemporaryDirectory() as second_dir:
            first = Path(first_dir)
            second = Path(second_dir)
            REGISTRY.write_bundle(ROOT / "organization-routing.json", first)
            REGISTRY.write_bundle(ROOT / "organization-routing.json", second)

            first_files = {path.name: path.read_bytes() for path in first.iterdir()}
            second_files = {path.name: path.read_bytes() for path in second.iterdir()}
            self.assertEqual(first_files, second_files)
            self.assertEqual(
                set(first_files),
                {
                    "3fa-app-project-registry.json",
                    "3fa-app-project-registry.md",
                    "SHA256SUMS",
                },
            )

            for line in first_files["SHA256SUMS"].decode("utf-8").splitlines():
                digest, filename = line.split("  ", 1)
                self.assertEqual(hashlib.sha256(first_files[filename]).hexdigest(), digest)

    def test_generated_bundle_is_public_safe_and_mentions_every_repository(self) -> None:
        artifact = REGISTRY.build_artifact(self.routing)
        markdown = REGISTRY.render_markdown(artifact)
        REGISTRY.validate_public_safe(artifact, "artifact")
        REGISTRY.validate_public_safe(markdown, "markdown")

        for repository in self.routing["repositories"]:
            self.assertIn(repository["fullName"], markdown)
            self.assertIn(f"`{repository['role']}`", markdown)

    def test_secret_like_material_is_rejected(self) -> None:
        for value in (
            "ghp_" + "A" * 36,
            "lin_api_" + "B" * 32,
            "cfat_" + "C" * 32,
            "-----BEGIN " + "PRIVATE KEY-----",
        ):
            with self.subTest(value=value[:12]):
                with self.assertRaisesRegex(ValueError, "credential-like material"):
                    REGISTRY.validate_public_safe({"unsafe": value}, "fixture")

    def test_inventory_drift_fails_closed(self) -> None:
        duplicate = copy.deepcopy(self.routing)
        duplicate["repositories"][-1] = copy.deepcopy(duplicate["repositories"][0])
        with self.assertRaisesRegex(ValueError, "inventory or ordering drift"):
            REGISTRY.validate_routing(duplicate)

        wrong_project = copy.deepcopy(self.routing)
        wrong_project["github"]["project"]["number"] = 2
        with self.assertRaisesRegex(ValueError, "Project number drift"):
            REGISTRY.validate_routing(wrong_project)

    def test_schemas_and_human_docs_include_cli_and_artifact_contract(self) -> None:
        routing_schema = json.loads(
            (ROOT / "schema" / "organization-routing.schema.json").read_text(encoding="utf-8")
        )
        repository_schema = routing_schema["properties"]["repositories"]
        role_enum = repository_schema["items"]["properties"]["role"]["enum"]
        self.assertEqual(repository_schema["minItems"], 14)
        self.assertEqual(repository_schema["maxItems"], 14)
        self.assertIn("cli", role_enum)

        artifact_schema = json.loads(
            (ROOT / "schema" / "project-registry-artifact.schema.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(artifact_schema["properties"]["artifactVersion"]["const"], 1)
        self.assertEqual(
            artifact_schema["properties"]["repositories"]["minItems"],
            14,
        )

        routing_doc = (ROOT / "ORGANIZATION_ROUTING.md").read_text(encoding="utf-8")
        projects_doc = (ROOT / "docs" / "PROJECTS.md").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        for document in (routing_doc, projects_doc, readme):
            self.assertIn("3FA-app/3FA-app-cli", document)
            self.assertIn("project registry", document.lower())


if __name__ == "__main__":
    unittest.main()
