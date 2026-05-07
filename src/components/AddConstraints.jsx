import React, { useEffect, useState } from "react";
import {
  Typography,
  Stack,
  Chip,
  Container,
  Paper,
  Grid,
  TextField,
  Checkbox,
  FormGroup,
  FormControlLabel,
  Autocomplete,
  CircularProgress,
  Button,
} from "@mui/material";
import { AddCircleOutlined } from "@mui/icons-material";
import Swal from "sweetalert2";
import axios from "axios";
import { API_ENDPOINTS } from "../config/apiConfig";

const DAY_NAMES = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];

const AddConstraints = () => {
  const [loading, setLoading] = useState(true);
  const [courses, setCourses] = useState([]);
  const [subjects, setSubjects] = useState([]);
  const [selectedDays, setSelectedDays] = useState({});
  const [dayHours, setDayHours] = useState({});
  const [dayCourseSelection, setDayCourseSelection] = useState({});
  const [checkedA, setCheckedA] = useState(false);
  const [nsub1, setnSub1] = useState("");
  const [nsub2, setnSub2] = useState("");

  useEffect(() => {
    const init = async () => {
      try {
        const res = await axios.get(API_ENDPOINTS.GET_COURSES);
        const list = res.data || [];
        setCourses(list);
        setSubjects(list.map((item) => ({ label: item.name, value: item.name })));
        const defaultHours = {};
        DAY_NAMES.forEach((day) => {
          defaultHours[day] = { start_hr: "09", end_hr: "16" };
        });
        setDayHours(defaultHours);
      } catch (err) {
        console.error("Failed to load courses:", err);
      } finally {
        setLoading(false);
      }
    };
    init();
  }, []);

  const toggleDay = (day) => {
    setSelectedDays((prev) => ({ ...prev, [day]: !prev[day] }));
  };

  const updateDayHours = (day, key, value) => {
    const hour = (value || "00:00").split(":")[0];
    setDayHours((prev) => ({
      ...prev,
      [day]: {
        ...prev[day],
        [key]: hour,
      },
    }));
  };

  const updateDayCourse = (day, selectedName) => {
    const match = courses.find((c) => c.name === selectedName);
    setDayCourseSelection((prev) => ({
      ...prev,
      [day]: {
        name: selectedName || "",
        description: match?.description || "",
      },
    }));
  };

  const buildConstraintBody = (resolutionMode = "ask") => {
    const working_days = DAY_NAMES.filter((day) => selectedDays[day]).map((day) => {
      const startHr = parseInt(dayHours[day]?.start_hr || "9", 10);
      const endHr = parseInt(dayHours[day]?.end_hr || "16", 10);
      return {
        day,
        start_hr: String(startHr),
        end_hr: String(endHr),
        total_hours: String(Math.max(0, endHr - startHr)),
      };
    });

    const day_course_map = {};
    DAY_NAMES.filter((day) => selectedDays[day]).forEach((day) => {
      const data = dayCourseSelection[day];
      if (data?.name) {
        day_course_map[day] = {
          name: data.name,
          description: data.description || "",
        };
      }
    });

    return {
      working_days,
      consecutive_subjects: ["", ""],
      non_consecutive_subjects: checkedA ? [nsub1, nsub2] : ["", ""],
      day_course_map,
      resolution_mode: resolutionMode,
    };
  };

  const submitConstraint = async (resolutionMode = "ask") => {
    const body = buildConstraintBody(resolutionMode);

    if (!body.working_days.length) {
      Swal.fire({ title: "Error", text: "Please select at least one working day.", icon: "error" });
      return;
    }

    try {
      await axios.post(API_ENDPOINTS.ADD_CONSTRAINTS, body);
      Swal.fire({ text: "Constraints added successfully!", icon: "success" });
    } catch (e) {
      const detail = e.response?.data?.detail;
      if (e.response?.status === 409 && detail?.conflicts?.length) {
        const conflictText = detail.conflicts
          .map(
            (c) =>
              `${c.day}: existing '${c.existing_name}' (${c.existing_description || "No description"}) vs new '${c.incoming_name}' (${c.incoming_description || "No description"})`
          )
          .join("<br/><br/>");

        const result = await Swal.fire({
          title: "Constraint conflict found",
          html: `${detail.message}<br/><br/>${conflictText}`,
          icon: "warning",
          showCancelButton: true,
          showDenyButton: true,
          confirmButtonText: "Overwrite",
          denyButtonText: "Keep Previous",
          cancelButtonText: "Cancel",
        });

        if (result.isConfirmed) {
          await submitConstraint("overwrite");
          return;
        }
        if (result.isDenied) {
          await submitConstraint("keep_previous");
          return;
        }
        return;
      }

      Swal.fire({
        title: "Error",
        text: detail?.message || detail || e.message || "Failed to add constraints.",
        icon: "error",
      });
    }
  };

  if (loading) return <CircularProgress />;

  return (
    <Container component="main" maxWidth="md" sx={{ mb: 4 }} className="fade-slide-in">
      <Paper
        variant="outlined"
        sx={{
          my: { xs: 3, md: 6 },
          p: { xs: 2, md: 3 },
          transition: "transform 220ms ease, box-shadow 220ms ease",
          "&:hover": { transform: "translateY(-4px)", boxShadow: 6 },
        }}
      >
        <Typography variant="h6" gutterBottom align="center">
          Add Constraints
        </Typography>

        <Grid container spacing={2}>
          <Grid item xs={12}>
            <Stack direction="row" spacing={1} justifyContent="center" flexWrap="wrap" useFlexGap>
              {DAY_NAMES.map((day) => (
                <Chip
                  key={day}
                  label={day}
                  color="primary"
                  variant={selectedDays[day] ? "filled" : "outlined"}
                  onClick={() => toggleDay(day)}
                  sx={{ transition: "transform 180ms ease", "&:hover": { transform: "translateY(-2px)" } }}
                />
              ))}
            </Stack>
          </Grid>

          {DAY_NAMES.filter((day) => selectedDays[day]).map((day) => (
            <React.Fragment key={day}>
              <Grid item xs={12} sm={3}>
                <TextField
                  type="time"
                  label={`${day} Start`}
                  fullWidth
                  value={`${(dayHours[day]?.start_hr || "09").padStart(2, "0")}:00`}
                  onChange={(e) => updateDayHours(day, "start_hr", e.target.value)}
                  InputLabelProps={{ shrink: true }}
                  sx={{ "& .MuiOutlinedInput-root": { transition: "all 200ms ease" } }}
                />
              </Grid>
              <Grid item xs={12} sm={3}>
                <TextField
                  type="time"
                  label={`${day} End`}
                  fullWidth
                  value={`${(dayHours[day]?.end_hr || "16").padStart(2, "0")}:00`}
                  onChange={(e) => updateDayHours(day, "end_hr", e.target.value)}
                  InputLabelProps={{ shrink: true }}
                  sx={{ "& .MuiOutlinedInput-root": { transition: "all 200ms ease" } }}
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <Autocomplete
                  options={subjects}
                  value={subjects.find((s) => s.label === dayCourseSelection[day]?.name) || null}
                  onChange={(event, value) => updateDayCourse(day, value ? value.label : "")}
                  isOptionEqualToValue={(option, value) => option.label === value?.label}
                  renderInput={(params) => (
                    <TextField
                      {...params}
                      label={`${day} Course`}
                      sx={{ "& .MuiOutlinedInput-root": { transition: "all 200ms ease" } }}
                    />
                  )}
                />
                <Typography variant="caption" sx={{ color: "text.secondary" }}>
                  {dayCourseSelection[day]?.description || "Select a course to include its description."}
                </Typography>
              </Grid>
            </React.Fragment>
          ))}

          <Grid item xs={12}>
            <FormGroup>
              <FormControlLabel
                control={<Checkbox checked={checkedA} onChange={() => setCheckedA(!checkedA)} />}
                label="Two subjects which cannot be consecutive"
              />
            </FormGroup>
          </Grid>

          {checkedA && (
            <>
              <Grid item xs={12} sm={6}>
                <Autocomplete
                  options={subjects}
                  value={subjects.find((s) => s.label === nsub1) || null}
                  onChange={(event, value) => setnSub1(value ? value.label : "")}
                  isOptionEqualToValue={(option, value) => option.label === value?.label}
                  renderInput={(params) => (
                    <TextField
                      {...params}
                      label="Subject 1 (Non-Consecutive)"
                      sx={{ "& .MuiOutlinedInput-root": { transition: "all 200ms ease" } }}
                    />
                  )}
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <Autocomplete
                  options={subjects}
                  value={subjects.find((s) => s.label === nsub2) || null}
                  onChange={(event, value) => setnSub2(value ? value.label : "")}
                  isOptionEqualToValue={(option, value) => option.label === value?.label}
                  renderInput={(params) => (
                    <TextField
                      {...params}
                      label="Subject 2 (Non-Consecutive)"
                      sx={{ "& .MuiOutlinedInput-root": { transition: "all 200ms ease" } }}
                    />
                  )}
                />
              </Grid>
            </>
          )}

          <Grid item xs={12}>
            <Button
              color="primary"
              startIcon={<AddCircleOutlined />}
              variant="outlined"
              fullWidth
              onClick={() => submitConstraint("ask")}
              sx={{ transition: "transform 180ms ease", "&:hover": { transform: "translateY(-2px)" } }}
            >
              Add Constraints
            </Button>
          </Grid>
        </Grid>
      </Paper>
    </Container>
  );
};

export default AddConstraints;
