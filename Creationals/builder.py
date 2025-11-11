class Report:
    """The complex object being constructed."""
    def __init__(self, format_type: str):
        self.format = format_type
        self.parts: list[str] = []

    def add_part(self, part: str) -> None:
        self.parts.append(part)

    def show(self) -> str:
        return f"--- {self.format} Report ---\n" + "\n".join(self.parts) + "\n-----------------------"

# --- Step 1: Define Builder Interface ---
from abc import ABC, abstractmethod

class ReportBuilder(ABC):
    """
    Defines methods for creating parts of the report product.
    step_result:: Modular construction logic decoupled from representation.
    """
    @abstractmethod
    def addHeader(self, title: str) -> None:
        pass

    @abstractmethod
    def addBody(self, content: str) -> None:
        pass

    @abstractmethod
    def addFooter(self, date: str) -> None:
        pass

    @abstractmethod
    def getResult(self) -> Report:
        pass

# --- 2. Concrete Builders ---
class PDFReportBuilder(ReportBuilder):
    """
    Creates a report structured for PDF output (simulated).
    step_result:: Flexible output generation from shared construction flow.
    """
    def __init__(self):
        self._report = Report("PDF")

    def addHeader(self, title: str) -> None:
        self._report.add_part(f"[PDF-HEADER] {title.upper()} [PDF-HEADER]")

    def addBody(self, content: str) -> None:
        self._report.add_part(f"Body Content:\n{content}")

    def addFooter(self, date: str) -> None:
        self._report.add_part(f"[PDF-FOOTER] Generated on {date}")

    def getResult(self) -> Report:
        return self._report

class MarkdownReportBuilder(ReportBuilder):
    """
    Creates a report structured for Markdown output.
    """
    def __init__(self):
        self._report = Report("Markdown")

    def addHeader(self, title: str) -> None:
        self._report.add_part(f"# {title}\n")

    def addBody(self, content: str) -> None:
        # Step 5: Extend builders for dynamic content (e.g., Markdown lists)
        formatted_content = "\n".join(f"* {line.strip()}" for line in content.splitlines())
        self._report.add_part(formatted_content)

    def addFooter(self, date: str) -> None:
        self._report.add_part(f"\n---\n*Report generated on {date}*")

    def getResult(self) -> Report:
        return self._report

# --- 3. The Director ---
class ReportDirector:
    """
    Orchestrates the steps of the construction process.
    step_result:: Standardized report structure across formats.
    """
    def __init__(self, builder: ReportBuilder):
        self._builder = builder

    def set_builder(self, builder: ReportBuilder) -> None:
        self._builder = builder

    def construct_full_report(self, title: str, content: str, date: str) -> None:
        """
        Defines the invariant construction sequence.
        step_traceability:: Director calls builder methods in a defined order.
        """
        self._builder.addHeader(title)
        self._builder.addBody(content)
        self._builder.addFooter(date)

# --- 4. Client Usage ---
if __name__ == "__main__":

    report_title = "Q4 Project Summary"
    report_data = "Task 1: Completed.\nTask 2: In progress.\nTask 3: Pending review."
    current_date = "2025-11-11"

    # 1. Prepare Builders and Director
    pdf_builder = PDFReportBuilder()
    md_builder = MarkdownReportBuilder()

    # Initialize the Director with the PDF Builder
    director = ReportDirector(pdf_builder)

    # --- Generate PDF Report ---
    print("Generating PDF Report...")
    director.construct_full_report(report_title, report_data, current_date)

    # Retrieve the final product
    pdf_report = pdf_builder.getResult()
    print(pdf_report.show())

    # --- Generate Markdown Report (Reusing the Director) ---
    print("\nGenerating Markdown Report...")

    # Switch the builder (allows reuse of the Director's logic)
    director.set_builder(md_builder)
    director.construct_full_report(report_title, report_data, current_date)

    # Retrieve the final product
    # step_result:: Clean separation of construction and usage.
    md_report = md_builder.getResult()
    print(md_report.show())
