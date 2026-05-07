import React, { useState } from "react";
import {
  Grid,
  Typography,
  TextField,
  Container,
  Paper,
  Button,
  CircularProgress,
} from "@mui/material";
import { AddCircleOutlined } from "@mui/icons-material";
import Swal from "sweetalert2";
import axios from "axios";
import { API_ENDPOINTS } from "../config/apiConfig";

const AddCourses = () => {
  const [name, setName] = useState("");
  const [lecturesno, setLecturesNo] = useState("");
  const [duration, setDuration] = useState("");
  const [iname, setIName] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    // Validate inputs
    if (!name.trim()) {
      Swal.fire({
        title: "Error",
        text: "Please enter course name!",
        icon: "error",
      });
      return;
    }

    if (!lecturesno || lecturesno === "" || parseInt(lecturesno) <= 0) {
      Swal.fire({
        title: "Error",
        text: "Please enter number of lectures (must be greater than 0)!",
        icon: "error",
      });
      return;
    }

    if (!duration || duration === "" || parseInt(duration) <= 0) {
      Swal.fire({
        title: "Error",
        text: "Please enter duration (must be greater than 0)!",
        icon: "error",
      });
      return;
    }

    if (!iname.trim()) {
      Swal.fire({
        title: "Error",
        text: "Please enter instructor name!",
        icon: "error",
      });
      return;
    }

    setLoading(true);

    try {
      const body = {
        name: name.trim(),
        lectureno: parseInt(lecturesno),
        duration: parseInt(duration),
        instructor_name: iname.trim(),
      };

      await axios.post(API_ENDPOINTS.ADD_COURSE, body);

      Swal.fire({
        title: "Success!",
        text: "Course added successfully!",
        icon: "success",
      });

      // Clear form
      setName("");
      setLecturesNo("");
      setDuration("");
      setIName("");
    } catch (error) {
      console.error("Error:", error);
      const errorMsg =
        error.response?.data?.detail ||
        error.message ||
        "Failed to add course. Please try again.";
      Swal.fire({
        title: "Error",
        text: errorMsg,
        icon: "error",
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Container component="main" maxWidth="sm" sx={{ mb: 4, mt: 4 }}>
        <Paper
          elevation={3}
          sx={{ my: { xs: 3, md: 6 }, p: { xs: 2, md: 3 } }}
        >
          <Typography variant="h5" gutterBottom align="center" sx={{ mb: 3 }}>
            Add New Course
          </Typography>
          <Grid container spacing={3}>
            <Grid item xs={12} sm={12}>
              <TextField
                required
                id="name"
                name="name"
                label="Name of Course"
                fullWidth
                variant="outlined"
                value={name}
                onChange={(e) => setName(e.target.value)}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                required
                id="lecturesno"
                name="lecturesno"
                label="Number of Lectures"
                type="number"
                fullWidth
                variant="outlined"
                helperText="per week"
                value={lecturesno}
                onChange={(e) => setLecturesNo(e.target.value)}
                inputProps={{ min: "1", max: "10" }}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                required
                id="duration"
                name="duration"
                label="Duration of Lecture"
                type="number"
                fullWidth
                variant="outlined"
                helperText="in hours"
                value={duration}
                onChange={(e) => setDuration(e.target.value)}
                inputProps={{ min: "1", max: "4", step: "0.5" }}
              />
            </Grid>
            <Grid item xs={12} sm={12}>
              <TextField
                required
                id="iname"
                name="iname"
                label="Name of Instructor"
                type="text"
                fullWidth
                variant="outlined"
                value={iname}
                onChange={(e) => setIName(e.target.value)}
              />
            </Grid>
            <Grid item xs={12} sm={12}>
              <Button
                color="primary"
                startIcon={<AddCircleOutlined />}
                variant="contained"
                fullWidth
                onClick={handleSubmit}
                disabled={loading}
              >
                {loading ? <CircularProgress size={24} /> : "Add Course"}
              </Button>
            </Grid>
          </Grid>
        </Paper>
      </Container>
    </>
  );
};

export default AddCourses;
