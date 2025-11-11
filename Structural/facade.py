# --- Step 1: Identify Subsystems and their Responsibilities ---
class Decoder:
    def decode(self, source: str) -> str:
        print(f"SUBSYSTEM: 🔄 Decoding source file: {source}")
        return f"RawData({source})"

class Compressor:
    def compress(self, raw_data: str, format: str) -> str:
        print(f"SUBSYSTEM: 📦 Compressing data for {format}")
        # Add simulated compression logic (e.g., reduces size indicator)
        return f"CompressedData({raw_data}, Quality=High)"

class Encoder:
    def encode(self, compressed_data: str, target_format: str) -> str:
        print(f"SUBSYSTEM: ⚙️ Encoding data into target format: {target_format}")
        return f"FinalFile_{target_format}"

class FileManager:
    def read_file(self, filename: str) -> str:
        print(f"SUBSYSTEM: 💾 Reading input file: {filename}")
        return filename

    def write_file(self, content: str, output_name: str) -> None:
        print(f"SUBSYSTEM: 💾 Writing final output file: {output_name}")

# --- Step 2: Design the Facade Class ---
class MediaConverterFacade:
    """
    Provides a simple, high-level interface to the complex media subsystem.
    step_result:: Simplified interface for client interaction.
    """
    def __init__(self):
        # The Facade holds references to all subsystems
        self._decoder = Decoder()
        self._compressor = Compressor()
        self._encoder = Encoder()
        self._file_manager = FileManager()

    # --- Step 3: Implement Orchestration Logic ---
    def convert(self, source_path: str, target_format: str) -> str:
        """
        Exposes the high-level operation clients need: convert a file.
        step_traceability:: Coordinate subsystem calls in the correct sequence.
        """
        output_path = f"output/{source_path.split('/')[-1].split('.')[0]}.{target_format}"

        try:
            # 1. Read File
            source_filename = self._file_manager.read_file(source_path)

            # 2. Decode
            raw_data = self._decoder.decode(source_filename)

            # 3. Compress
            compressed_data = self._compressor.compress(raw_data, target_format)

            # 4. Encode
            final_content = self._encoder.encode(compressed_data, target_format)

            # 5. Write File
            self._file_manager.write_file(final_content, output_path)

            # step_result:: Encapsulated workflow logic.
            return f"FACADE: ✅ Conversion successful. Output at {output_path}"

        except Exception as e:
            # Handle complex internal errors centrally
            return f"FACADE: ❌ Conversion failed due to internal error: {e}"

    # --- Step 5: Extend the Facade (New Workflow Support) ---
    def extract_audio(self, source_path: str) -> str:
        """
        New high-level method using a different sequence of subsystems.
        step_result:: Scalable, stable API surface.
        """
        print("\n--- FACADE: Running specialized audio extraction workflow ---")
        # Simplified workflow for audio: Decode -> Encode (no compression needed)

        self._file_manager.read_file(source_path)
        raw_data = self._decoder.decode(source_path)
        audio_file = self._encoder.encode(raw_data, "mp3")
        self._file_manager.write_file(audio_file, f"audio_output.mp3")
        return f"FACADE: ✅ Audio extracted to mp3."

# --- 2. Client Code ---
def client_app(converter: MediaConverterFacade):
    """Client interacts only with the simple Facade interface."""

    # 1. Simple file conversion
    print("=== CLIENT: Running Standard Video Conversion ===")
    result_video = converter.convert("input/source_video.avi", "mp4")
    print(result_video)

    # 2. Specialized workflow
    print("\n=== CLIENT: Running Audio Extraction ===")
    # step_traceability:: Refactor client code to use MediaConverterFacade only.
    result_audio = converter.extract_audio("input/source_video.avi")
    print(result_audio)
    # step_result:: Reduced coupling and improved maintainability.

if __name__ == "__main__":

    # The client only instantiates and calls the Facade
    converter_facade = MediaConverterFacade()
    client_app(converter_facade)
