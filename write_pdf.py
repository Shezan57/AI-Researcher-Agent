# Step1: Import deps
from langchain_core.tools import tool
from datetime import datetime
from pathlib import Path
import subprocess
import shutil

# latex_content = """
# \\documentclass{article}
# \\begin{document}
# Hello, World! From LaTeX to PDF with python. Version 3.
# \\end{document}"""


@tool
def render_latex_pdf(latex_content: str) -> str:
    """Render a LaTeX document to PDF.

    Args:
        latex_content: The LaTeX document content as a string

    Returns:
        Path to the generated PDF document
    """
    # if shutil.which("tectonic") is None:
    #     raise RuntimeError(
    #         "tectonic is not installed. Install it first on your system."
    #     )

    try:
        # Step2: Create directory
        output_dir = Path("output").absolute()
        output_dir.mkdir(exist_ok=True)
        # Step3: Setup filenames
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        tex_filename = f"paper_{timestamp}.tex"
        pdf_filename = f"paper_{timestamp}.pdf"
        # Step4: Export as tex & pdf
        tex_file = output_dir / tex_filename
        tex_file.write_text(latex_content)

        engine = (
            shutil.which("pdflatex")
            or shutil.which("xelatex")
            or ("C:/Program Files/MiKTeX/miktex/bin/x64/pdflatex.exe" if Path("C:/Program Files/MiKTeX/miktex/bin/x64/pdflatex.exe").exists() else None)
            or (str(Path.home() / "AppData/Local/Programs/MiKTeX/miktex/bin/x64/pdflatex.exe") if Path(Path.home() / "AppData/Local/Programs/MiKTeX/miktex/bin/x64/pdflatex.exe").exists() else None)
        )

        if not engine:
            raise RuntimeError(
                "No LaTeX engine found. Install MiKTeX/TeX Live or add pdflatex to PATH."
            )

        # Build command using absolute paths; don't rely on cwd
        cmd = [
            engine,
            "-interaction=nonstopmode",  # non-interactive
            "-halt-on-error",
            "-synctex=0",               # don't generate synctex
            "-quiet",                   # minimize console output
            "-output-directory",
            str(output_dir),
            str(tex_file),
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            # Include a short tail of stdout/stderr for debugging on failure only
            msg = "LaTeX compilation failed."
            if result.stderr:
                msg += f"\nStderr (tail):\n{result.stderr[-2000:]}"
            if result.stdout:
                msg += f"\nStdout (tail):\n{result.stdout[-2000:]}"
            raise RuntimeError(msg)

        pdf_path = output_dir / (Path(tex_filename).stem + ".pdf")
        
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        

        # Cleanup auxiliary files the user doesn't need
        stem = Path(tex_filename).stem
        cleanup_candidates = [
            output_dir / f"{stem}.aux",
            output_dir / f"{stem}.log",
            output_dir / f"{stem}.out",
            output_dir / f"{stem}.toc",
            output_dir / f"{stem}.synctex.gz",
            output_dir / f"{stem}.fls",
            output_dir / f"{stem}.fdb_latexmk",
        ]
        for p in cleanup_candidates:
            try:
                if p.exists():
                    p.unlink()
            except Exception:
                pass  # ignore cleanup errors

        return str(pdf_path)
    except Exception as e:
        print(f"Error occurred: {e}")
        raise
    

# render_latex_pdf(latex_content)