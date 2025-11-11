from abc import ABC, abstractmethod
from typing import List

# --- Step 3: Define Visitor Interface (Needed for Step 1 type hinting) ---
class Visitor(ABC):
    """
    Defines the contract with visit methods for each Concrete Element type.
    step_result:: Structured contract for external operations.
    """
    @abstractmethod
    def visit_paragraph(self, element: 'Paragraph') -> None: # Using string hint
        pass

    @abstractmethod
    def visit_table(self, element: 'Table') -> None: # Using string hint
        pass

    @abstractmethod
    def visit_image(self, element: 'Image') -> None: # Using string hint
        pass

# --- Step 1: Define Element Interface (Element) ---
class Element(ABC):
    """
    Defines the contract for components that can accept a visitor.
    step_result:: Unified entry point for external operations.
    """
    @abstractmethod
    def accept(self, visitor: 'Visitor') -> None: # FIX: Use 'Visitor' as a string literal
        """The mechanism to pass control to the visitor."""
        pass

# --- Step 2: Implement Concrete Elements ---
class Paragraph(Element):
    """Concrete element (Leaf)"""
    def __init__(self, text: str):
        self.text = text

    def accept(self, visitor: 'Visitor') -> None:
        """Dispatches control to the visitor."""
        visitor.visit_paragraph(self)

class Table(Element):
    """Concrete element (Composite, but treated uniformly)"""
    def __init__(self, rows: int, cols: int):
        self.rows = rows
        self.cols = cols

    def accept(self, visitor: 'Visitor') -> None:
        visitor.visit_table(self)

class Image(Element):
    """Concrete element (Leaf)"""
    def __init__(self, source: str):
        self.source = source

    def accept(self, visitor: 'Visitor') -> None:
        visitor.visit_image(self)

# --- Document Structure (The Object Structure) ---
class Document:
    def __init__(self):
        self.elements: List[Element] = []

    def apply_visitor(self, visitor: 'Visitor') -> None:
        """Traverses the structure and applies the visitor."""
        for element in self.elements:
            element.accept(visitor)

# --- 4. Implement Concrete Visitors (Logic remains the same) ---
class RenderVisitor(Visitor):
    """Implements the rendering logic for all element types."""
    def visit_paragraph(self, element: 'Paragraph') -> None:
        print(f"[RENDER] P: Displaying text: '{element.text[:30]}...'")

    def visit_table(self, element: 'Table') -> None:
        print(f"[RENDER] T: Drawing a {element.rows}x{element.cols} grid.")

    def visit_image(self, element: 'Image') -> None:
        print(f"[RENDER] I: Loading and displaying image from {element.source}.")

class ExportVisitor(Visitor):
    """Implements the exporting logic for all element types."""
    def visit_paragraph(self, element: 'Paragraph') -> None:
        print(f"[EXPORT] P: Writing <p>{element.text}</p> to file.")

    def visit_table(self, element: 'Table') -> None:
        print(f"[EXPORT] T: Writing <table> with {element.rows} rows.")

    def visit_image(self, element: 'Image') -> None:
        print(f"[EXPORT] I: Writing <img src='{element.source}'> tag.")

# --- Client Usage ---
if __name__ == "__main__":

    doc = Document()
    doc.elements.append(Paragraph("This is the main paragraph of the document."))
    doc.elements.append(Table(rows=5, cols=3))

    print("\n=== Applying RenderVisitor ===")
    render_visitor = RenderVisitor()
    doc.apply_visitor(render_visitor)

    print("\n=== Applying ExportVisitor ===")
    export_visitor = ExportVisitor()
    doc.apply_visitor(export_visitor)
