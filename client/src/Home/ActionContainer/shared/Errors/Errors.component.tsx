import Alert from "@material-ui/lab/Alert";
import React from "react";
import { createStyles, makeStyles, Theme } from "@material-ui/core/styles";

interface IErrorsPayload {
  errors: string[];
}

const useStyles = makeStyles((theme: Theme) =>
  createStyles({
    alert: {
      marginTop: theme.spacing(1),
    },
  })
);

export function Errors(payload: IErrorsPayload) {
  const classes = useStyles();

  const { errors }: IErrorsPayload = payload;

  return (
    <>
      {errors.length > 0 &&
        errors.map((error, index) => {
          return (
            <Alert key={index} severity="error" className={classes.alert}>
              {error}
            </Alert>
          );
        })}
    </>
  );
}
