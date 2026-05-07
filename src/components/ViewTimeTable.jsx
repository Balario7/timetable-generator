import axios from "axios";
import React, { useState } from "react";
import {
  Button,
  CircularProgress,
  Grid,
  Alert,
  Box,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Chip,
} from "@mui/material";
import Swal from "sweetalert2";
import { API_ENDPOINTS } from "../config/apiConfig";

const ViewTimeTable = () => {
  const [data, setData] = useState({});
  const [loading, setLoading] = useState(false);
  const [clicked, setClicked] = useState(false);
  const [error, setError] = useState("");
  const [highlights, setHighlights] = useState([]);
  const [summary, setSummary] = useState(null);

  const normalizeSchedule = (responseData) => {
    const schedule = responseData?.schedule || responseData || {};
    const temp = {};
    for (const [key, value] of Object.entries(schedule)) {
      const events = Array.isArray(value) ? value : [];
      temp[key] = events.map((elem) => ({
        ...elem,
        startTime: new Date(elem.startTime),
        endTime: new Date(elem.endTime),
      }));
    }
    return temp;
  };

  const getTimeTable = () => {
    setClicked(true);
    setLoading(true);
    setError("");
    axios
      .get(API_ENDPOINTS.GENERATE_TIMETABLE)
      .then((res) => {
        const normalized = normalizeSchedule(res.data);
        const hasEvents = Object.values(normalized).some((day) => day.length > 0);
        if (!hasEvents) {
          setError("No timetable solution found. Please add courses and constraints before generating.");
        } else {
          Swal.fire({
            title: "Success!",
            text: "Full timetable generated successfully!",
            icon: "success",
            timer: 2000,
            showConfirmButton: false,
          });
        }

        setHighlights(res.data?.highlights || []);
        setSummary(res.data?.summary || null);
        setData(normalized);
        setLoading(false);
      })
      .catch((e) => {
        setError(e.response?.data?.detail || "Failed to generate timetable. Please ensure courses and constraints are added.");
        setLoading(false);
      });
  };

  return (
    <Grid container spacing={2} className="fade-slide-in">
      <Grid item xs={12} sm={12}>
        <Button
          onClick={getTimeTable}
          variant="contained"
          disabled={loading}
          sx={{ transition: "transform 180ms ease", "&:hover": { transform: "translateY(-2px)" } }}
        >
          {loading ? "Generating..." : "Generate Time Table"}
        </Button>
      </Grid>

      {clicked && error && (
        <Grid item xs={12} sm={12}>
          <Alert severity="error">{error}</Alert>
        </Grid>
      )}

      {clicked && !error && (
        <Grid item xs={12} sm={12}>
          {loading ? (
            <Box display="flex" justifyContent="center" p={2}>
              <CircularProgress />
            </Box>
          ) : (
            <Box>
              <Typography variant="h6" sx={{ mb: 1 }}>
                Generated Timetable
              </Typography>

              {summary && (
                <Typography variant="body2" sx={{ mb: 2, color: "text.secondary" }}>
                  Total Courses: {summary.total_courses} | Highlighted Changes: {summary.total_highlighted_changes}
                </Typography>
              )}

              {highlights.length > 0 && (
                <Box sx={{ mb: 2 }}>
                  <Typography variant="subtitle2" sx={{ mb: 1 }}>
                    Highlighted Changes
                  </Typography>
                  {highlights.map((h, idx) => (
                    <Chip
                      key={`${h.day}-${h.course}-${idx}`}
                      label={`${h.day}: ${h.course} (${h.reason})`}
                      color="warning"
                      size="small"
                      sx={{ mr: 1, mb: 1 }}
                    />
                  ))}
                </Box>
              )}

              <TableContainer component={Paper}>
                <Table>
                  <TableHead>
                    <TableRow sx={{ backgroundColor: "#1976d2" }}>
                      <TableCell sx={{ color: "white", fontWeight: "bold" }}>Day</TableCell>
                      <TableCell sx={{ color: "white", fontWeight: "bold" }}>Course</TableCell>
                      <TableCell sx={{ color: "white", fontWeight: "bold" }}>Description</TableCell>
                      <TableCell sx={{ color: "white", fontWeight: "bold" }}>Start Time</TableCell>
                      <TableCell sx={{ color: "white", fontWeight: "bold" }}>End Time</TableCell>
                      <TableCell sx={{ color: "white", fontWeight: "bold" }}>Status</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {Object.entries(data).length === 0 ? (
                      <TableRow>
                        <TableCell colSpan={6} align="center">
                          No timetable generated yet. Click "Generate Time Table" to create one.
                        </TableCell>
                      </TableRow>
                    ) : (
                      Object.entries(data).map(([day, events]) =>
                        events.length === 0 ? (
                          <TableRow key={day}>
                            <TableCell>{day}</TableCell>
                            <TableCell colSpan={5} align="center">
                              No classes
                            </TableCell>
                          </TableRow>
                        ) : (
                          events.map((event, idx) => (
                            <TableRow
                              key={`${day}-${idx}`}
                              sx={{
                                backgroundColor: event.highlight ? "#fff8e1" : "inherit",
                                transition: "background-color 250ms ease, transform 180ms ease",
                                "&:hover": { transform: "scale(1.005)" },
                              }}
                            >
                              <TableCell>{day}</TableCell>
                              <TableCell>{event.name}</TableCell>
                              <TableCell>{event.description || "-"}</TableCell>
                              <TableCell>
                                {new Date(event.startTime).toLocaleTimeString("en-US", {
                                  hour: "2-digit",
                                  minute: "2-digit",
                                  hour12: true,
                                })}
                              </TableCell>
                              <TableCell>
                                {new Date(event.endTime).toLocaleTimeString("en-US", {
                                  hour: "2-digit",
                                  minute: "2-digit",
                                  hour12: true,
                                })}
                              </TableCell>
                              <TableCell>
                                {event.highlight ? (
                                  <Chip label="Highlighted Change" size="small" color="warning" />
                                ) : (
                                  <Chip label="Scheduled" size="small" color="success" variant="outlined" />
                                )}
                              </TableCell>
                            </TableRow>
                          ))
                        )
                      )
                    )}
                  </TableBody>
                </Table>
              </TableContainer>
            </Box>
          )}
        </Grid>
      )}
    </Grid>
  );
};

export default ViewTimeTable;
