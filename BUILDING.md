# Building the Book (author notes)

This project uses Quarto. To render the book (HTML and PDF), use the provided helper script which handles the environment configuration required for PDF generation on macOS (M1/Apple Silicon).

## Prerequisites

1.  **Quarto**: Install via `brew install --cask quarto`.
2.  **Google Chrome**: Required for PDF rendering of diagrams. Ensure it is installed in `/Applications/Google Chrome.app`.
3.  **Graphviz**: (Optional but recommended) `brew install graphviz`.

## How to Render

Run the build script in your terminal:

```bash
./render_book.sh
```

This script sets the following environment variables to prevent Chromium crashes on macOS:
- `QUARTO_CHROMIUM`: Points to the system Google Chrome.
- `QUARTO_CHROMIUM_HEADLESS_MODE`: Sets headless mode to `new`.
- `QUARTO_NO_SANDBOX`: Disables the sandbox.
- `OBJC_DISABLE_INITIALIZE_FORK_SAFETY`: Workaround for fork safety issues.

## Previewing

To preview the HTML site locally:

```bash
quarto preview
```
