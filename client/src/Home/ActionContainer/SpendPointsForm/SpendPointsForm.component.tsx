import React from "react";
import { Controller, useForm } from "react-hook-form";
import {
  Input,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TextField,
} from "@material-ui/core";
import { createStyles, makeStyles, Theme } from "@material-ui/core/styles";
import { Errors } from "../shared/Errors/Errors.component";
import { Inputs, useSpendPoints } from "./useSpendPoints";

const useStyles = makeStyles((theme: Theme) =>
  createStyles({
    root: {
      "& > *": {
        margin: theme.spacing(1),
        width: "25ch",
      },
      marginTop: theme.spacing(3),
      display: "flex",
      flexDirection: "column",
    },
    tableContainer: {
      marginTop: theme.spacing(2),
    },
    table: {
      minWidth: 350,
    },
    submitInput: {
      alignSelf: "center",
    },
    alert: {
      marginTop: theme.spacing(1),
    },
  })
);

export default function SpendPointsForm() {
  const classes = useStyles();

  const { control, handleSubmit } = useForm<Inputs>();
  const {
    operations: { onSubmit },
    models: { results, errors },
  } = useSpendPoints();

  return (
    <>
      <form className={classes.root} onSubmit={handleSubmit(onSubmit)}>
        <Controller
          name="points"
          defaultValue=""
          as={
            <TextField id="points" label="Points" color="secondary" required />
          }
          control={control}
        />
        <Input type="submit" className={classes.submitInput} />
      </form>
      <Errors errors={errors} />
      {results.length > 0 && (
        <TableContainer component={Paper} className={classes.tableContainer}>
          <Table className={classes.table} aria-label="simple table">
            <TableHead>
              <TableRow>
                <TableCell>Payer</TableCell>
                <TableCell>Points</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {results.map((row, index) => (
                <TableRow key={index}>
                  <TableCell component="th" scope="row">
                    {row.payer}
                  </TableCell>
                  <TableCell>{row.points}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      )}
    </>
  );
}
