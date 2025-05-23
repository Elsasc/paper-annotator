import logo from './logo.svg';
import './App.css';
import React, { useState } from "react";
import axios from "axios";
import {
  Container,
  Typography,
  Button,
  Box,
  CircularProgress,
  Card,
  CardContent,
  Divider,
  Stack
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
     <Container maxWidth="md" sx={{ mt: 8 }}>
      <Card elevation={3}>
        <CardContent>
          <Typography variant="h4" align="center" gutterBottom>
            Mega Meta Research Paper Annotator
          </Typography>
          <Divider sx={{ my: 2 }} />

            <Box component="form" onSubmit={handleSubmit}>
                <Stack direction="row" spacing={2} justifyContent="center">
                    <Button variant="outlined" component="label">
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
                        type="submit"
                        disabled={loading}
                    >
                        {loading ? <CircularProgress size={24} color="inherit" /> : "Submit"}
                    </Button>
                </Stack>
            </Box>

          {downloadURL && (
            <Box textAlign="center" mt={3}>
              <Button
                variant="outlined"
                color="success"
                href={downloadURL}
                download="annotated.pdf"
              >
                Download Annotated PDF
              </Button>
            </Box>
          )}
        </CardContent>
      </Card>
    </Container>
  );
}

export default App;