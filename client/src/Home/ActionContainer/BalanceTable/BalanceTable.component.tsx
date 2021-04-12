import React from "react";
import {
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
} from "@material-ui/core";
import { createStyles, makeStyles, Theme } from "@material-ui/core/styles";
import { useFetchBalance } from "./useFetchBalance";

const useStyles = makeStyles((theme: Theme) =>
  createStyles({
    root: {
      marginTop: theme.spacing(5),
    },
  })
);

export default function BalanceTable() {
  const classes = useStyles();

  const {
    models: { results, loading },
  } = useFetchBalance();

  const hasResults = results.length > 0;

  return (
    <>
      {hasResults && !loading && (
        <TableContainer component={Paper} className={classes.root}>
          <Table aria-label="simple table">
            <TableHead>
              <TableRow>
                <TableCell align="center">Payer</TableCell>
                <TableCell align="center">Points</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {results.map(({ payer, points }, index) => (
                <TableRow key={index}>
                  <TableCell component="th" scope="row" align="center">
                    {payer}
                  </TableCell>
                  <TableCell align="center">{points}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      )}
      {!hasResults && !loading && (
        <p>There are no balances. Please create new transactions!</p>
      )}
      {loading && <p>Loading...</p>}
    </>
  );
}
