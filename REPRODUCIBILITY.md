# Reproducibility

A clean checkout must reproduce installation, checks, tests, and build artifacts
using the committed runtime version and `uv.lock`:

```sh
make setup
make check
make audit
make build
```

Record external inputs, configuration, tool/runtime versions, and commands needed
to reproduce material results. Never depend silently on developer-machine state.
