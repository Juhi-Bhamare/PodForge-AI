import { useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [file, setFile] = useState(null);
  const [documentInfo, setDocumentInfo] = useState(null);
  const [audioUrl, setAudioUrl] = useState("");
  const [isDragging, setIsDragging] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState("");

  const validateFile = (selectedFile) => {
    if (!selectedFile) {
      return "Please select a PDF file.";
    }

    if (selectedFile.type !== "application/pdf") {
      return "Only PDF files are supported.";
    }

    if (selectedFile.size > 20 * 1024 * 1024) {
      return "File size must be less than 20 MB.";
    }

    return "";
  };

  const handleFileSelect = (selectedFile) => {
    const validationError = validateFile(selectedFile);

    if (validationError) {
      setError(validationError);
      setFile(null);
      return;
    }

    setError("");
    setFile(selectedFile);
    setDocumentInfo(null);
    setAudioUrl("");
  };

  const handleFileInput = (event) => {
    const selectedFile = event.target.files[0];

    if (selectedFile) {
      handleFileSelect(selectedFile);
    }
  };

  const handleDragOver = (event) => {
    event.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (event) => {
    event.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (event) => {
    event.preventDefault();
    setIsDragging(false);

    const droppedFile = event.dataTransfer.files[0];

    if (droppedFile) {
      handleFileSelect(droppedFile);
    }
  };

  const generatePodcast = async () => {
    if (!file) {
      setError("Please select a PDF first.");
      return;
    }

    setIsUploading(true);
    setError("");
    setDocumentInfo(null);
    setAudioUrl("");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch(
        `${API_URL}/generate-podcast-audio`,
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Failed to generate podcast."
        );
      }

      setDocumentInfo(data);

      if (data.audio_url) {
        setAudioUrl(
          data.audio_url.startsWith("http")
            ? data.audio_url
            : `${API_URL}${data.audio_url}`
        );
      }
    } catch (err) {
      console.error(err);

      setError(
        err.message ||
          "Something went wrong while generating the podcast."
      );
    } finally {
      setIsUploading(false);
    }
  };

  const resetPodcast = () => {
    setFile(null);
    setDocumentInfo(null);
    setAudioUrl("");
    setError("");
    setIsDragging(false);
  };

  const renderPodcastScript = (script) => {
    if (!script) {
      return null;
    }

    const lines = script.split(/\r?\n/);

    return lines.map((line, index) => {
      const match = line.match(
        /^\s*(HOST 1|HOST 2)\s*:\s*(.*)$/i
      );

      if (!match) {
        if (!line.trim()) {
          return (
            <div
              key={index}
              className="transcript-spacer"
            />
          );
        }

        return (
          <div
            key={index}
            className="transcript-text"
          >
            {line}
          </div>
        );
      }

      const speaker = match[1].toUpperCase();
      const dialogue = match[2].trim();

      const isHostOne = speaker === "HOST 1";

      return (
        <div
          key={index}
          className={`transcript-message ${
            isHostOne
              ? "host-one"
              : "host-two"
          }`}
        >
          <div className="speaker-row">
            <div className="speaker-avatar">
              {isHostOne ? "1" : "2"}
            </div>

            <span className="speaker-name">
              {speaker}
            </span>
          </div>

          <p className="speaker-dialogue">
            {dialogue}
          </p>
        </div>
      );
    });
  };

  return (
    <div className="app">
      <header className="navbar">
        <div className="logo">
          PodForge
        </div>

        <div className="nav-badge">
          AI Podcast Studio
        </div>
      </header>

      <main className="main-content">
        <section className="hero">
          <div className="hero-intro">
            <div className="hero-label">
              DOCUMENT → PODCAST
            </div>

            <p className="hero-description">
              Upload a PDF and let AI transform it into an
              engaging two-host podcast.
            </p>
          </div>

          <div className="hero-content">
            <div className="hero-title">
              <h1>
                Turn your documents
                <br />
                into <span>conversations.</span>
              </h1>
            </div>

            <div className="hero-upload">
              <div
                className={`upload-card ${
                  isDragging ? "dragging" : ""
                }`}
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
              >
                <div className="upload-icon">
                  ↑
                </div>

                <h2>
                  {file
                    ? file.name
                    : "Drop your PDF here"}
                </h2>

                <p>
                  {file
                    ? `${(
                        file.size /
                        (1024 * 1024)
                      ).toFixed(2)} MB`
                    : "or click below to browse your files"}
                </p>

                <label className="browse-button">
                  Browse Files

                  <input
                    type="file"
                    accept=".pdf,application/pdf"
                    onChange={handleFileInput}
                    hidden
                  />
                </label>

                <span className="file-limit">
                  PDF • Maximum 20 MB
                </span>
              </div>

              {file && (
                <button
                  className="generate-button"
                  onClick={generatePodcast}
                  disabled={isUploading}
                >
                  {isUploading
                    ? "Generating..."
                    : "Generate Podcast"}
                </button>
              )}
            </div>
          </div>
        </section>

        {error && (
          <div className="error-message">
            {error}
          </div>
        )}

        {isUploading && (
          <section className="loading-section">
            <div className="loading-spinner"></div>

            <h3>
              Forging your podcast...
            </h3>

            <p>
              AI is analyzing your document, writing the
              conversation, and generating the voices.
            </p>
          </section>
        )}

        {documentInfo && !isUploading && (
          <section className="result-section">
            <div className="result-header">
              <div>
                <p className="result-eyebrow">
                  PODCAST READY
                </p>

                <h2>
                  {documentInfo.filename}
                </h2>
              </div>

              <button
                className="new-podcast-button"
                onClick={resetPodcast}
              >
                + New Podcast
              </button>
            </div>

            <div className="document-stats">
              <div className="stat">
                <span>Pages</span>

                <strong>
                  {documentInfo.pages}
                </strong>
              </div>

              <div className="stat">
                <span>Words</span>

                <strong>
                  {documentInfo.words}
                </strong>
              </div>

              <div className="stat">
                <span>Characters</span>

                <strong>
                  {documentInfo.characters}
                </strong>
              </div>
            </div>

            {audioUrl && (
              <div className="audio-player">
                <h3>
                  Your Podcast
                </h3>

                <audio
                  controls
                  src={audioUrl}
                >
                  Your browser does not support
                  the audio element.
                </audio>
              </div>
            )}

            <div className="script-section">
              <h3>
                Generated Conversation
              </h3>

              <div className="podcast-script">
                {renderPodcastScript(
                  documentInfo.podcast_script
                )}
              </div>
            </div>
          </section>
        )}

        <section className="features">
          <div className="feature">
            <span>01</span>

            <h3>
              Understand
            </h3>

            <p>
              PodForge extracts and processes the
              important information from your document.
            </p>
          </div>

          <div className="feature">
            <span>02</span>

            <h3>
              Generate
            </h3>

            <p>
              Gemini transforms the content into a
              natural conversation between two AI hosts.
            </p>
          </div>

          <div className="feature">
            <span>03</span>

            <h3>
              Listen
            </h3>

            <p>
              Kokoro gives each host a distinct voice
              and turns the conversation into an audio podcast.
            </p>
          </div>
        </section>
      </main>

      <footer className="footer">
        <p>
          Built with React • FastAPI • Gemini • Kokoro
        </p>
      </footer>
    </div>
  );
}

export default App;