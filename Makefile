APP_RELEASE ?= 0.1.0
APP_REVISION ?= local

.PHONY: setup format lint typecheck test check audit build container container-smoke deployment-smoke
setup:
	uv sync --frozen --dev
format:
	uv run ruff format .
lint:
	uv run ruff check .
	uv run ruff format --check .
typecheck:
	uv run pyright
test:
	uv run python -m unittest discover -s tests
check: lint typecheck test
audit:
	uv audit --preview-features audit-command --locked --no-dev
build:
	uv build
container:
	docker build --build-arg APP_RELEASE="$(APP_RELEASE)" --build-arg APP_REVISION="$(APP_REVISION)" --tag gambit-mcp:local .
container-smoke:
	APP_RELEASE="$(APP_RELEASE)" APP_REVISION="$(APP_REVISION)" uv run python tools/container_smoke.py
deployment-smoke:
	@test -n "$(BASE_URL)" || (echo "BASE_URL is required"; exit 2)
	@test -n "$(EXPECTED_ENVIRONMENT)" || (echo "EXPECTED_ENVIRONMENT is required"; exit 2)
	@test -n "$(EXPECTED_RELEASE)" || (echo "EXPECTED_RELEASE is required"; exit 2)
	@test -n "$(EXPECTED_REVISION)" || (echo "EXPECTED_REVISION is required"; exit 2)
	uv run python tools/deployment_smoke.py --base-url "$(BASE_URL)" --expected-service "gambit-mcp" --expected-environment "$(EXPECTED_ENVIRONMENT)" --expected-release "$(EXPECTED_RELEASE)" --expected-revision "$(EXPECTED_REVISION)"
