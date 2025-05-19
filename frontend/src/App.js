import React, { useState } from "react";
import axios from "axios";
import {
  Container,
  Typography,
  Button,
  Box,
  CircularProgress,
  TextField,
} from "@mui/material";

function App() {
  const [file, setFile] = useState(null);
  const [downloadURL, setDownloadURL] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setDownloadURL(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      alert("Please select a PDF file first.");
      return;
    }

    setLoading(true);
    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await axios.post("http://localhost:8000/annotate/", formData, {
        responseType: "blob",
      });

      const blob = new Blob([res.data], { type: "application/pdf" });
      const url = window.URL.createObjectURL(blob);
      setDownloadURL(url);
    } catch (err) {
      alert("Error processing file.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="sm" sx={{ textAlign: "center", mt: 8 }}>
      <Typography variant="h4" gutterBottom>
        Mega Meta Research Paper Annotator
      </Typography>

      <Box component="form" onSubmit={handleSubmit} sx={{ mb: 3 }}>
        <Button
          variant="outlined"
          component="label"
          fullWidth
          sx={{ mb: 2 }}
        >
          {file ? file.name : "Choose PDF File"}
          <input
            type="file"
            accept="application/pdf"
            hidden
            onChange={handleFileChange}
          />
        </Button>

        <Button
          variant="contained"
          color="primary"
          type="submit"
          fullWidth
          disabled={loading}
        >
          {loading ? <CircularProgress size={24} color="inherit" /> : "Submit"}
        </Button>
      </Box>

      {downloadURL && (
        <Button
          variant="outlined"
          color="success"
          href={downloadURL}
          download="annotated.pdf"
        >
          Download Annotated PDF
        </Button>
      )}
    </Container>
  );
}

export default App;
