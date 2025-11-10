syft packages dir:. -o spdx-json=sbom.spdx.json
trivy fs --exit-code 1 --format table .
