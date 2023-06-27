import * as React from "react";
import Box from "@mui/material/Box";
import FormLabel from "@mui/material/FormLabel";
import FormControl from "@mui/material/FormControl";
import FormGroup from "@mui/material/FormGroup";
import FormControlLabel from "@mui/material/FormControlLabel";
import Checkbox from "@mui/material/Checkbox";

export default function SearchIn() {
  const [state, setState] = React.useState({
    title: false,
    description: false,
    content: false,
  });

  const handleChange = (event) => {
    setState({
      ...state,
      [event.target.name]: event.target.checked,
    });
  };

  const { title, description, content } = state;
  const error = [title, description, content].filter((v) => v).length !== 2;

  return (
    <Box sx={{ display: "flex" }}>
      <FormControl sx={{ m: 3 }} component="fieldset" variant="standard">
        <FormLabel component="legend" sx={{ textAlign: "left" }}>
          Search In:
        </FormLabel>
        <FormGroup>
          <FormControlLabel
            control={
              <Checkbox checked={title} onChange={handleChange} name="title" />
            }
            label="Title"
          />
          <FormControlLabel
            control={
              <Checkbox
                checked={description}
                onChange={handleChange}
                name="description"
              />
            }
            label="Description"
          />
          <FormControlLabel
            control={
              <Checkbox
                checked={content}
                onChange={handleChange}
                name="content"
              />
            }
            label="Content"
          />
        </FormGroup>
      </FormControl>
    </Box>
  );
}
