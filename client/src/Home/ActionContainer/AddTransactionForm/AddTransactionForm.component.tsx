import React from "react";
import { createStyles, makeStyles, Theme } from "@material-ui/core/styles";
import { Controller, useForm } from "react-hook-form";
import { Input, TextField } from "@material-ui/core";
import CheckIcon from "@material-ui/icons/Check";
import { Errors } from "../shared/Errors/Errors.component";
import { Inputs, useAddTransaction } from "./useAddTransaction";

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
    submitInput: {
      alignSelf: "center",
    },
    alert: {
      marginTop: theme.spacing(1),
    },
  })
);

export default function AddTransactionForm() {
  const classes = useStyles();

  const { control, handleSubmit } = useForm<Inputs>();
  const {
    operations: { onSubmit },
    models: { addedTransaction, errors },
  } = useAddTransaction();

  return (
    <>
      <form className={classes.root} onSubmit={handleSubmit(onSubmit)}>
        <Controller
          name="payer"
          defaultValue=""
          as={<TextField id="payer" label="Payer" color="secondary" required />}
          control={control}
        />
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
      {addedTransaction && <CheckIcon />}
    </>
  );
}
