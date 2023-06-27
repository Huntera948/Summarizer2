import * as React from "react";
import Box from "@mui/material/Box";
import TextField from "@mui/material/TextField";
import Autocomplete from "@mui/material/Autocomplete";

export default function CountrySelect() {
  return (
    <Box sx={{ display: "flex", justifyContent: "center" }}>
      <Autocomplete
        id="country-select-demo"
        sx={{ width: 300 }}
        options={countries}
        autoHighlight
        getOptionLabel={(option) => option.label}
        renderOption={(props, option) => (
          <Box
            component="li"
            sx={{ "& > img": { mr: 2, flexShrink: 0 } }}
            {...props}
          >
            <img
              loading="lazy"
              width="20"
              src={`https://flagcdn.com/w20/${option.code.toLowerCase()}.png`}
              srcSet={`https://flagcdn.com/w40/${option.code.toLowerCase()}.png 2x`}
              alt=""
            />
            {option.label} ({option.code})
          </Box>
        )}
        renderInput={(params) => (
          <TextField
            {...params}
            label="Choose a country"
            inputProps={{
              ...params.inputProps,
              autoComplete: "new-password", // disable autocomplete and autofill
            }}
          />
        )}
      />
    </Box>
  );
}

// From https://bitbucket.org/atlassian/atlaskit-mk-2/raw/4ad0e56649c3e6c973e226b7efaeb28cb240ccb0/packages/core/select/src/data/countries.js
const countries = [
  {
    code: "ar",
    label: "Argentina",
  },
  {
    code: "au",
    label: "Australia",
  },
  {
    code: "at",
    label: "Austria",
  },
  {
    code: "be",
    label: "Belgium",
  },
  {
    code: "br",
    label: "Brazil",
  },
  {
    code: "bg",
    label: "Bulgaria",
  },
  {
    code: "ca",
    label: "Canada",
  },
  {
    code: "cn",
    label: "China",
  },
  {
    code: "co",
    label: "Colombia",
  },
  {
    code: "cu",
    label: "Cuba",
  },
  {
    code: "cz",
    label: "Czech Republic",
  },
  {
    code: "eg",
    label: "Egypt",
  },
  {
    code: "fr",
    label: "France",
  },
  {
    code: "de",
    label: "Germany",
  },
  {
    code: "gr",
    label: "Greece",
  },
  {
    code: "hk",
    label: "Hong Kong",
  },
  {
    code: "hu",
    label: "Hungary",
  },
  {
    code: "in",
    label: "India",
  },
  {
    code: "id",
    label: "Indonesia",
  },
  {
    code: "ie",
    label: "Ireland",
  },
  {
    code: "il",
    label: "Israel",
  },
  {
    code: "it",
    label: "Italy",
  },
  {
    code: "jp",
    label: "Japan",
  },
  {
    code: "lv",
    label: "Latvia",
  },
  {
    code: "lt",
    label: "Lithuania",
  },
  {
    code: "my",
    label: "Malaysia",
  },
  {
    code: "mx",
    label: "Mexico",
  },
  {
    code: "ma",
    label: "Morocco",
  },
  {
    code: "nl",
    label: "Netherlands",
  },
  {
    code: "nz",
    label: "New Zealand",
  },
  {
    code: "ng",
    label: "Nigeria",
  },
  {
    code: "no",
    label: "Norway",
  },
  {
    code: "ph",
    label: "Philippines",
  },
  {
    code: "pl",
    label: "Poland",
  },
  {
    code: "pt",
    label: "Portugal",
  },
  {
    code: "ro",
    label: "Romania",
  },
  {
    code: "ru",
    label: "Russia",
  },
  {
    code: "sa",
    label: "Saudi Arabia",
  },
  {
    code: "rs",
    label: "Serbia",
  },
  {
    code: "sg",
    label: "Singapore",
  },
  {
    code: "sk",
    label: "Slovakia",
  },
  {
    code: "si",
    label: "Slovenia",
  },
  {
    code: "za",
    label: "South Africa",
  },
  {
    code: "kr",
    label: "South Korea",
  },
  {
    code: "se",
    label: "Sweden",
  },
  {
    code: "ch",
    label: "Switzerland",
  },
  {
    code: "tw",
    label: "Taiwan",
  },
  {
    code: "th",
    label: "Thailand",
  },
  {
    code: "tr",
    label: "Turkey",
  },
  {
    code: "ae",
    label: "UAE",
  },
  {
    code: "ua",
    label: "Ukraine",
  },
  {
    code: "gb",
    label: "United Kingdom",
  },
  {
    code: "us",
    label: "United States",
    suggested: true,
  },
  {
    code: "ve",
    label: "Venezuela",
  },
];
