import { useState } from "react";
import Select from "react-select";
import { AddressAutofill } from "@mapbox/search-js-react";
import { FaEye, FaEyeSlash } from "react-icons/fa";
import "../css/field.css";

export function Field({
  label,
  type = "text",
  name,
  placeholder,
  value,
  onChange = () => {},
  halfWidth = false,
  optional = false,
  disabled = false,
  autoComplete = "off",
  addressAutofill = false,
  onRetrieve = () => {},
}) {
  const accessToken = process.env.REACT_APP_MAPBOX_TOKEN;
  const inputField = (
    <input
      className={disabled ? "disabled" : ""}
      type={type}
      name={name}
      placeholder={placeholder}
      value={value}
      onChange={onChange}
      autoComplete={autoComplete}
      disabled={disabled}
    />
  );

  return (
    <div className={`formGroup ${halfWidth ? "half" : ""}`}>
      <label htmlFor={name}>
        {label}
        {optional && <span>{"(optional)"}</span>}
      </label>
      {addressAutofill ? (
        <AddressAutofill
          accessToken={accessToken}
          onChange={(value) => {
            onChange({ target: { name, value } });
          }}
          onRetrieve={onRetrieve}
        >
          {inputField}
        </AddressAutofill>
      ) : (
        inputField
      )}
    </div>
  );
}

export function Password({
  label,
  name,
  placeholder,
  value,
  onChange = () => {},
}) {
  const [showPassword, setShowPassword] = useState(false);
  return (
    <div className="formGroup">
      <label htmlFor={name}>{label}</label>
      <div className="passwordField">
        <input
          type={showPassword ? "text" : "password"}
          name={name}
          placeholder={placeholder}
          value={value}
          onChange={onChange}
        />
        {showPassword ? (
          <FaEyeSlash onClick={() => setShowPassword(false)} />
        ) : (
          <FaEye onClick={() => setShowPassword(true)} />
        )}
      </div>
    </div>
  );
}

export function Textarea({
  label,
  rows = "4",
  name,
  placeholder,
  value,
  onChange = () => {},
}) {
  return (
    <div className="formGroup">
      <label htmlFor={name}>{label}</label>
      <textarea
        name={name}
        placeholder={placeholder}
        rows={rows}
        value={value}
        onChange={onChange}
      ></textarea>
    </div>
  );
}

export function Dropdown({
  label,
  name,
  value = "",
  options,
  onChange = () => {},
  halfWidth = false,
  optional = false,
}) {
  const selectStyles = {
    control: (styles) => ({
      ...styles,
      fontSize: "0.9rem",
      fontWeight: "400",
      lineHeight: "1.25rem",
      paddingLeft: "0.375rem",
      border: "1px solid #e0e0e0",
      borderRadius: "0.25rem",
      transition: "border-color 0.3s ease-in-out",
      outline: "none",
      boxShadow: "none",
      "&:hover": {
        borderColor: "#4990e2",
      },
    }),
    option: (styles, { isFocused, isSelected }) => {
      return {
        ...styles,
        fontSize: "0.9rem",
        fontWeight: "400",
        lineHeight: "1.5rem",
        backgroundColor: isSelected
          ? "#4990e2"
          : isFocused
          ? "#e5f1ff"
          : "transparent",
        cursor: "pointer",
      };
    },
  };
  return (
    <div className={`formGroup ${halfWidth ? "half" : ""}`}>
      <label htmlFor={name}>
        {label}
        {optional && <span>{"(optional)"}</span>}
      </label>
      <Select
        options={options}
        styles={selectStyles}
        name={name}
        value={value}
        onChange={onChange}
      />
    </div>
  );
}
