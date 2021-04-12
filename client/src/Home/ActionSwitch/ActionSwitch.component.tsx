import React from "react";
import { Button } from "@material-ui/core";
import { APIEndPoint } from "../APIEndpoint";

interface IActionSwitchProps {
  setAPIUrl: (url: string) => void;
}

export default function ActionSwitch({ setAPIUrl }: IActionSwitchProps) {
  return (
    <div>
      {APIEndPoint.map(({ url, buttonName }, index) => {
        return (
          <Button
            key={index}
            variant="contained"
            color="primary"
            onClick={() => setAPIUrl(url)}
            style={{margin: '0 0.5rem'}}
          >
            {buttonName}
          </Button>
        );
      })}
    </div>
  );
}
